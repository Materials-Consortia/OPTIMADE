#!/usr/bin/env python3

import argparse, io, codecs, os, sys, logging
import urllib.parse
import urllib.request

supported_input_formats = ['json', 'yaml']

class ExceptionWrapper(Exception):
    debug = False
    def __init__(self,msg,e):
        if isinstance(e, ExceptionWrapper):
            self.messages = [msg] + e.messages
        elif type(e) == Exception:
            self.messages = [msg, str(e)+"."]
        else:
            self.messages = [msg, type(e).__name__+": "+str(e)+"."]
        full_message = msg +". Error details:\n- "+("\n- ".join(self.messages[1:]))+"\n"
        if not self.debug:
            full_message += "\nAdd command line argument -d for a full traceback or one or more -v for higher verbosity."
        super().__init__(full_message)

def read_data(source, input_format='auto'):
    """
    Reads data from a file or a URL and returns the parsed content.

    Parameters
    ----------
    source : str
        A string specifying the file name or the URL to fetch.
    input_format : str, optional
        The format of the input file. If set to 'auto' (default), the format will be detected automatically.

    Returns
    -------
    tuple
        A tuple containing the parsed content and its format.
    """

    logging.debug("Read data from: %s",source)

    reader = None
    try:
        parsed_url = urllib.parse.urlparse(source)
        if parsed_url.scheme in ['http', 'https', 'ftp']:
            resource = urllib.request.urlopen(source)
            charset = resource.headers.get_content_charset()
            reader = codecs.getreader(charset)(resource)
            if input_format == 'auto':
                if resource.headers.get_content_maintype() in ['application', 'text']:
                    input_format = resource.headers.get_content_subtype()
                    if input_format.startswith('x-'):
                       input_format = input_format[2:]
        else:
            base, orig_ext = os.path.splitext(parsed_url.path)
            if os.path.isabs(base):
                base = os.path.join('.',os.path.relpath(base,'/'))
            for ext in [orig_ext] + ["."+x for x in supported_input_formats]:
                logging.debug("Checking for file: %s",base+ext)
                if os.path.isfile(base+ext):
                    reader = open(base+ext, 'r')
                    if input_format == 'auto':
                        input_format = ext.lstrip(".")
                    break
            else:
                # meant to raise a proper FileNotFoundError
                reader = open(base+orig_ext, 'r')

        if input_format == "yaml":
            import yaml
            return yaml.safe_load(reader), "yaml"
        if input_format == "json":
            import yaml
            return json.load(reader), "json"
        else:
            raise Exception("Unknown input format or unable to automatically detect for: "+source+", input_format: "+str(input_format))
    except Exception as e:
        raise ExceptionWrapper("Couldn't load data from: "+str(source),e)

    finally:
        if reader is not None:
            reader.close()


def dict_get_one(d):
    if len(d) != 1:
        raise Exception("Expected only one field in dictionary, but found: "+str(d.keys()))
    key = list(d.keys())[0]
    return key, d[key]


def data_to_str(data):

    if not "x-optimade-property" in data:
        s = ""
        for item in sorted(data.keys()):
            s += item + "\n"
            s += '-'*len(item)+"\n\n"

            try:
                if isinstance(data[item], dict):
                    s += data_to_str(data[item])
                else:
                    raise Exception("Internal error, unexpected data for data_to_str: "+str(data))
                    exit(0)
            except Exception as e:
                raise ExceptionWrapper("Could not process item: "+item,e)
            s += "\n"
        return s

    support_descs = {
        "must": "MUST be supported by all implementations, MUST NOT be :val:`null`.",
        "should": "SHOULD be supported by all implementations, i.e., SHOULD NOT be :val:`null`.",
        "may": "OPTIONAL support in implementations, i.e., MAY be :val:`null`."
    }
    query_support_descs = {
        "all mandatory" : "MUST be a queryable property with support for all mandatory filter features.",
        "equality only" : "MUST be queryable using the OPTIMADE filter language equality and inequality operators. Other filter language features do not need to be available.",
        "partial" : "MUST be a queryable property.",
        "none": "Support for queries on this property is OPTIONAL."
    }

    #field, data = dict_get_one(data)
    title = data['title']
    description_short, sep, description_details = [x.strip() for x in data['description'].partition('**Requirements/Conventions**:')]
    examples = "- " + "\n- ".join(["`"+str(x)+"`" for x in data['examples']])

    req_support_level, req_sort, req_query = ["Not specified"]*3
    req_partial_info = ""
    if 'x-optimade-requirements' in data:
        if 'support' in data['x-optimade-requirements']:
            req_support = data['x-optimade-requirements']['support']
        if 'sortable' in data['x-optimade-requirements']:
            req_sort = data['x-optimade-requirements']['sortable']
        if 'query-support' in data['x-optimade-requirements']:
            req_query = data['x-optimade-requirements']['query-support']
            if req_query == "partial":
                req_partial_info = "The following filter language features MUST be supported: "+", ".join(data['x-optimade-requirements']['query-support-operators'])

    #TODO: need to iterate through dicts, lists to get the full type
    optimade_type = data['x-optimade-type']

    #s = field+"\n"
    #s += "~"*len(field)+"\n"
    #s += "\n"
    s = "**Name**: "+str(title)+"\n"
    s += "**Description**: "+str(description_short)+"\n"
    s += "**Type**: "+str(optimade_type)+"\n"
    s += "**Requirements/Conventions**:\n"
    s += "- **Support**: "+support_descs[req_support]+"\n"
    s += "- **Query**: "+query_support_descs[req_query]+"\n"
    s += "- **Response**:\n"
    s += description_details+"\n"
    s += "\n"
    s += "**Examples**:\n\n"+examples
    s += "\n"

    return s

def output_str(data, output_format='json'):
    """
    Returns a string representation of the input data in the specified output format.

    Parameters
    ----------
    data : dict
        The data to be represented as a string in the specified output format.
    output_format : str, optional
        The format of the output string. Default is 'json'.

    Returns
    -------
    str
        A string representation of the input data in the specified output format.

    """

    if output_format == "json":
        import json
        return json.dumps(data, indent=4)
    elif output_format == "yaml":
        import yaml
        return yaml.dumps(data)
    elif output_format == "md":
        return data_to_str(data)
    else:
        raise Exception("Unknown output format: "+str(output_format))


def handle_refs(data, refs_mode="rewrite", input_format=None, bases=None):
    """
    Recursively handles all '$ref' references in the input data.

    Parameters
    ----------
    data : dict
        The input data to be processed for '$ref' references.
    refs_mode : str, optional
        The mode for handling '$ref' references: 'rewrite' to rewrite the '$ref' field, 'insert'
        to insert the referenced data. Default is 'rewrite'.
    input_format : str, optional
        The input_format, used to look for apropriate file extensions when resolving the '$ref'
        to a file.

    Returns
    -------
    dict
        A new dictionary with all '$ref' references handled according to the specified mode.

    """

    def ref_to_source(ref, bases):
        parsed_ref = urllib.parse.urlparse(ref)
        if parsed_ref.scheme in ['file', '']:
            ref = parsed_ref.path
            if os.path.isabs(ref):
                # Re-process absolute path to file path
                absref = urllib.parse.urljoin(bases['id'], ref)
                relref = absref[len(bases['id']):]
                return os.path.join(bases['dir'],relref)
            else:
                return os.path.join(bases['self'],ref)
        return ref

    def handle_single_ref(ref, refs_mode, input_format, bases):
        logging.info("Handle single $ref: %s",ref)
        if refs_mode == "retain":
            return { "$ref": ref }
        elif refs_mode == "rewrite":
            base, ext = os.path.splitext(ref)
            return { "$ref": base + '.' + input_format }
        elif refs_mode == "insert":
            source = ref_to_source(ref, bases)
            return read_data(source, input_format)[0]
        else:
            raise Exception("Internal error: unexpected refs_mode: "+str(refs_mode))

    logging.debug("Handling refs in: %s",data)

    if '$ref' in data:
        if not set(data.keys()).issubset({'$id', '$comment', '$ref', 'x-propdefs-ref-mode'}):
            raise Exception("Unexpected fields present alongside $ref in:"+str(data)+"::"+str(len(data)))

        if 'x-propdefs-ref-mode' in data:
            this_refs_mode = data['x-propdefs-ref-mode']
            del data['x-propdefs-ref-mode']
        else:
            this_refs_mode = refs_mode

        if this_refs_mode == 'retain':
            return data

        output = handle_single_ref(data['$ref'], this_refs_mode, input_format, bases)
        if isinstance(output, dict):
            # Handle $ref:s recursively
            newbases = bases.copy()
            source = ref_to_source(data['$ref'], bases)
            newbases['self'] = os.path.dirname(source)
            output = handle_refs(output, refs_mode, input_format, newbases)
        if '$id' in data:
            output['$id'] = data['$id']
        return output

    for k, v in data.items():
        if isinstance(v, dict):
            data[k] = handle_refs(v, refs_mode, input_format, bases)

    return data


def process(source, refs_mode="rewrite", input_format="auto", bases=None):
    """
    Processes the input file according to the specified parameters.

    Parameters
    ----------
    source : str
        The path to a file or a URL to the input to be processed.
    refs_mode : str, optional
        The mode for handling '$ref' references: 'rewrite' to rewrite the '$ref' field, 'insert'
        to insert the referenced data, or 'retain' to leave the '$ref' field as is. Default is
        'rewrite'.
    input_format : str, optional
        The format of the input file, or 'auto' to automatically determine the format based on
        the file extension. Default is 'auto'.
    output_format : str, optional
        The format of the output file. Default is 'json'.

    Returns
    -------
    str
        A string representation of the processed output data in the specified output format.

    """
    data, input_format = read_data(source)
    parsed_source = urllib.parse.urlparse(source)
    bases['self'] = os.path.dirname(parsed_source.path)

    if "$id" in data:
        id_uri = data["$id"]

        if bases['id'] is None:
            prefix = os.path.commonprefix([bases['dir'], source])
            rel_source = source[len(prefix):]
            if not id_uri.endswith(rel_source):
                rel_source, ext = os.path.splitext(rel_source)
                if not id_uri.endswith(rel_source):
                    raise Exception("The $id field needs to end with: "+str(rel_source)+" but it does not: "+str(id_uri))
            bases = {'id': id_uri[:-len(rel_source)], 'dir': bases['dir'] }

    if refs_mode != "retain":
        data = handle_refs(data, refs_mode, input_format, bases)

    return data


def process_dir(source_dir, refs_mode="rewrite", input_format="auto", bases=None):

    alldata = {}

    for filename in os.listdir(source_dir):
        f = os.path.join(source_dir,filename)
        if os.path.isdir(f):
            logging.info("Process dir reads directory: %s",f)
            dirdata = process_dir(f, refs_mode, input_format, bases)
            alldata[os.path.basename(f)] = dirdata
        elif os.path.isfile(f):
            base, ext = os.path.splitext(f)
            if ext[1:] in supported_input_formats:
                logging.info("Process dir reads file: %s",f)
                data = process(f, refs_mode, input_format, bases)
                alldata.update(data)

    return alldata


if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(description="Process property definition source files into other formats", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('source', help='The property definition file, directory or URL to process.')
        parser.add_argument('--refs-mode', help='How to handle $ref references. Can also be set by a x-propdefs-ref-mode key alongside $ref.', choices=["insert", "rewrite", "retain"], default="insert")
        parser.add_argument('-i','--input-format', help='The input format to read', default="auto", choices=["auto", "json", "yaml"])
        parser.add_argument('-f','--output-format', help='The output format to generate', default="json", choices=["json", "yaml", "md"])
        parser.add_argument('--basedir', help='Base directory relative to which $ref referencs are resolved')
        parser.add_argument('--baseid', help='Base id to relative to which $ref references are resolved')
        parser.add_argument('-o', '--output', help='Write the output to a file')
        parser.add_argument('-d', '--debug', help='Produce full tracebacks on error', default=False, action='store_true')
        parser.add_argument('-v', '--verbose', dest="verbosity", action="append_const", const=1)
        parser.add_argument('-q', '--quiet', dest="verbosity", action="append_const", const=-1)
        parser.set_defaults(verbosity=[2])
        args = parser.parse_args()

        bases = {'id':args.baseid, 'dir':args.basedir }

        # Make sure verbosity is in the allowed range
        log_levels = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
        verbosity = min(len(log_levels) - 1, max(sum(args.verbosity), 0))
        logging.basicConfig(format='%(levelname)s: %(message)s',level=log_levels[verbosity])
        # Turn on tracebacks, etc., if verbosity is max *or* the debug flag is given
        debug = args.debug or verbosity == len(log_levels)-1
        ExceptionWrapper.debug = debug

    except Exception as e:
        print("Internal error when parsing command line arguments: " +type(e).__name__+": "+str(e)+'.', file=sys.stderr)
        exit(1)

    try:
        try:
            if os.path.isdir(args.source):
                logging.info("Processing directory: %s", args.source)
                data = process_dir(args.source, args.refs_mode, args.input_format, bases)
            else:
                logging.info("Processing file: %s", args.source)
                data = process(args.source, args.refs_mode, args.input_format, bases)

        except Exception as e:
            raise ExceptionWrapper("Processing of input failed", e) from e

        try:
            logging.info("Serializing data into format: %s", args.output_format)
            outstr = output_str(data, args.output_format)
        except Exception as e:
            raise ExceptionWrapper("Serialization of data failed", e) from e

        try:
            if args.output:
                logging.info("Writing serialized output to file: %s", args.output)
                with open(args.output, "w") as f:
                    f.write(outstr)
            else:
                logging.info("Writing serialized output to stdout")
                print(outstr)

        except Exeption as e:
            raise ExceptionWrapper("Writing output data failed", e) from e

    except Exception as e:
        if debug:
            raise
        else:
            print(e)
            exit(1)
