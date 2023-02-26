#!/usr/bin/env python3

import argparse, io, codecs, os, sys, logging
import urllib.parse
import urllib.request

class ExceptionWrapper(Exception):
    debug = False
    def __init__(self,msg,e):
        if isinstance(e, ExceptionWrapper):
            self.messages = [msg] + e.messages
        elif isinstance(e, Exception):
            self.messages = [msg, str(e)+"."]
        else:
            self.messages = [msg, type(e).__name__+": "+str(e)+"."]
        full_message = msg +". Error details:\n- "+("\n- ".join(self.messages[1:]))+"\n"
        if not self.debug:
            full_message += "\nAdd command line argument -d for a full traceback of the error."
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

    logging.debug("Read data from: %s"+str(source))

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
            base, ext = os.path.splitext(parsed_url.path)
            if os.path.isabs(base):
                base = os.path.join('.',os.path.relpath(base,'/'))
            try:
                reader = open(base+ext, 'r')
            except FileNotFoundError:
                reader = open(base, 'r')
            if input_format == 'auto':
                input_format = ext.lstrip('.')

        if input_format == "yaml":
            import yaml
            return yaml.safe_load(reader), "yaml"
        if input_format == "json":
            import yaml
            return json.load(reader), "json"
        else:
            raise Exception("Unknown input format or unable to automatically detect for: "+source+", input_format: "+str(input_format))
    except FileNotFoundError as e:
        raise ExceptionWrapper("File not found: "+str(source)+" relative to:"+os.getcwd(),e)

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
            s += '~'*len(item)+"\n"

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


def handle_refs(data, id_base=None, refs_mode="rewrite", input_format=None, basedir="./"):
    """
    Recursively handles all '$ref' references in the input data.

    Parameters
    ----------
    data : dict
        The input data to be processed for '$ref' references.
    id_base : str, optional
        The contents of the topmost $id field.
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

    def handle_single_ref(ref, id_base, refs_mode, input_format, basedir):
        logging.info("Handle single $ref: %s",ref)
        if refs_mode == "rewrite":
            base, ext = os.path.splitext(ref)
            return { "$ref": base + '.' + input_format }
        elif refs_mode == "insert":
            if os.path.isabs(ref):
                # Re-process root path to a sane file path
                absref = urllib.parse.urljoin(id_base, ref)
                prefix = os.path.commonprefix([id_base, absref])
                relref = absref[len(prefix):]
                ref = os.path.join(basedir,relref)
                base, ext = os.path.splitext(ref)
                if ext == '' and not os.path.exists(ref):
                    ref += "."+input_format
            else:
                input_format = 'auto'
            data = read_data(ref, input_format)[0]
            if len(data) != 1:
                raise Exception("Reference points at multiple top-level items: "+str(data))
            return data[list(data.keys())[0]]
        else:
            raise Exception("Internal error: unexpected refs_mode: "+str(refs_mode))

    if '$ref' in data:
        if ('$id' in data and len(data) > 2) or ('$id' not in data and len(data) > 1):
            raise Exception("Unexpected fields present alongside $ref in:"+str(data)+"::"+str(len(data)))
        output = handle_single_ref(data['$ref'], id_base, refs_mode, input_format, basedir)
        if '$id' in data:
            output['$id'] = data['$id']
        return output

    for k, v in data.items():
        if isinstance(v, dict):
            data[k] = handle_refs(v, id_base, refs_mode, input_format, basedir)

    return data


def process(source, refs_mode="rewrite", input_format="auto", basedir="./"):
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

    if len(data) != 1:
        raise Exception("Unexpected format of property definition.")

    name = list(data.keys())[0]
    if "$id" not in data[name]:
        raise Exception("Missing top-level $id field.")

    id_uri = data[name]["$id"]

    prefix = os.path.commonprefix([basedir, source])
    rel_source = source[len(prefix):]
    if not id_uri.endswith(rel_source):
        rel_source, ext = os.path.splitext(rel_source)
        if not id_uri.endswith(rel_source):
            raise Exception("The $id field needs to end with: "+str(rel_source)+" but it does not: "+str(id_uri))
    id_base = id_uri[:-len(rel_source)]

    if refs_mode != "retain":
        data = handle_refs(data, id_base, refs_mode, input_format, basedir)

    return data


def process_dir(source_dir, refs_mode="rewrite", input_format="auto", basedir="./"):

    alldata = {}

    for filename in os.listdir(source_dir):
        f = os.path.join(source_dir,filename)
        if os.path.isdir(f):
            logging.info("Process dir reads directory: %s",f)
            dirdata = process_dir(f, refs_mode, input_format, basedir)
            alldata[os.path.basename(f)] = dirdata
        elif os.path.isfile(f):
            logging.info("Process dir reads file: %s",f)
            data = process(f, refs_mode, input_format, basedir)
            alldata.update(data)

    return alldata


if __name__ == "__main__":

    try:
        parser = argparse.ArgumentParser(description="Process property definition source files into other formats", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument('source', help='The property definition file, directory or URL to process.')
        parser.add_argument('-r','--refs-mode', help='How to handle $ref references', choices=["insert", "rewrite", "retain"], default="insert")
        parser.add_argument('-i','--input-format', help='The input format to read', default="auto", choices=["auto", "json", "yaml"])
        parser.add_argument('-f','--output-format', help='The output format to generate', default="json", choices=["json", "yaml", "md"])
        parser.add_argument('-b', '--basedir', help='Reference top-level directory to use to resolve $ref reference paths')
        parser.add_argument('-o', '--output', help='Write the output to a file')
        parser.add_argument('-d', '--debug', help='Produce full tracebacks on error', default=False, action='store_true')
        parser.add_argument('-v', '--verbose', dest="verbosity", action="append_const", const=1)
        parser.add_argument('-q', '--quiet', dest="verbosity", action="append_const", const=-1)
        parser.set_defaults(verbosity=[2])
        args = parser.parse_args()

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
                data = process_dir(args.source, args.refs_mode, args.input_format, args.basedir)
            else:
                logging.info("Processing file: %s", args.source)
                data = process(args.source, args.refs_mode, args.input_format, args.basedir)

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
