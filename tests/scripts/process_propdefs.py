#!/usr/bin/env python3
"""
This script processes property definition source files into other formats. It can process individual
files or entire directories and supports various input and output formats. The script also includes
options for handling $ref references and specifying base directories or IDs for resolving references.

Usage:
  propdefs.py source [options]

Examples:
  # Process a single file and write the output to stdout:
  propdefs.py file.json

  # Process all files in a directory and write the output to a file:
  propdefs.py dir -o output.json

"""

import argparse, io, codecs, os, sys, logging
import urllib.parse
import urllib.request

supported_input_formats = ['json', 'yaml']
supported_output_formats = ["json", "yaml", "md"]

arguments = [
    {
        'names': ['source'],
        'help': 'The property definition file, directory or URL to process.',
        'type': str,
    },
    {
        'names': ['--refs-mode'],
        'help': 'How to handle $ref references. Can also be set by a x-propdefs-ref-mode key alongside $ref. Also, the x-propdefs-inherit-ref key does a deep merge on the referenced definition.',
        'choices': ["insert", "rewrite", "retain"],
        'default': "retain",
    },
    {
        'names': ['-i', '--input-format'],
        'help': 'The input format to read',
        'choices': ["auto"] + supported_input_formats,
        'default': "auto",
    },
    {
        'names': ['-f', '--output-format'],
        'help': 'The output format to generate',
        'choices': ["auto"] + supported_output_formats,
        'default': "auto",
    },
    {
        'names': ['--basedir'],
        'help': 'Base directory relative to which $ref referencs are resolved',
    },
    {
        'names': ['--baseid'],
        'help': 'Base id to relative to which $ref references are resolved',
    },
    {
        'names': ['-s', '--sub'],
        'help': 'Define a subsitution: all occurences in strings of key will be replaced by val',
        'nargs': 2, 'metavar': ('key', 'value'), 'action': 'append',
        'default': []
    },
    {
        'names': ['-o', '--output'],
        'help': 'Write the output to a file',
    },
    {
        'names': ['--remove-null'],
        'help': 'Remove keys if the value is null',
        'action': 'store_true',
        'default': False
    },
    {
        'names': ['-d', '--debug'],
        'help': 'Produce full tracebacks on error',
        'action': 'store_true',
        'default': False
    },
    {
        'names': ['-v', '--verbose'],
        'help': 'Increase verbosity of output',
        'dest': 'verbosity', 'action': 'append_const', 'const': 1,
    },
    {
        'names': ['-q', '--quiet'],
        'help': 'Decrease verbosity of output',
        'dest': 'verbosity', 'action': 'append_const', 'const': -1,
    },
]

class ExceptionWrapper(Exception):
    """
    A class used to wrap exceptions with additional information.

    Attributes
    ----------
    debug : bool
        A flag indicating whether debug mode is enabled. (If not, a helpful message
        about how to enable a full traceback and/or more verbosity in the error
        reporting. Default is False.
    """
    debug = False
    def __init__(self,msg,e):
        """
        Initialize the ExceptionWrapper instance.

        Parameters
        ----------
        msg : str
            The message to include in the error.
        e : Exception
            The exception to wrap.
        """
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
            import json
            return json.load(reader), "json"
        else:
            raise Exception("Unknown input format or unable to automatically detect for: "+source+", input_format: "+str(input_format))
    except Exception as e:
        raise ExceptionWrapper("Couldn't load data from: "+str(source),e)

    finally:
        if reader is not None:
            reader.close()


def data_to_md(data):
    """
    Convert data representing OPTIMADE Property Definitions into a markdown string.

    Parameters
    ----------
    data : dict
        A dictionary containing the OPTIMADE Property Definition data.

    Returns
    -------
    str
        A string representation of the input data.
    """

    if not "x-optimade-property" in data:
        s = ""
        for item in sorted(data.keys()):
            s += item + "\n"
            s += '-'*len(item)+"\n\n"

            try:
                if isinstance(data[item], dict):
                    s += data_to_md(data[item])
                else:
                    raise Exception("Internal error, unexpected data for data_to_md: "+str(data))
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
    Serializes key-value data into a string using the specified output format.

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
        return yaml.dump(data)
    elif output_format == "md":
        return data_to_md(data)
    else:
        raise Exception("Unknown output format: "+str(output_format))


def ref_to_source(ref, bases):
    """
    Convert a JSON Schema $ref reference to a source path.

    Parameters
    ----------
    ref : str
        A JSON reference to be converted to a source path.
    bases : dict
        A dictionary containing information about the base paths to use when
        converting the reference to a source path. Must contain the keys "id"
        and "dir".

    Returns
    -------
    str
        The source path corresponding to the input reference.

    """
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


def recursive_replace(d, subs):
    """
    Recursively replace substrings in values of nested dictionaries that are strings.

    Parameters
    ----------
    d : dict
        The dictionary of strings to perform the replacements on.
    subs : list of tuple
        The list of key-value pairs to use for replacement. Each tuple contains
        two elements: the substring to replace and the string to replace it with.

    Returns
    -------
    dict
        A dictionary with the specified replacements.
    """
    logging.debug("Substuting strings: %s", subs)

    for key, val in d.items():
        if isinstance(val,str):
            for lhs,rhs in subs.items():
                val = val.replace(lhs,rhs)
            d[key] = val
        if isinstance(val,dict):
            recursive_replace(val, subs)
    return d


def handle_one(ref, refs_mode, input_format, bases, subs):
    """
    Handle a single JSON reference.

    Parameters
    ----------
    ref : str
        The JSON reference to be handled.
    refs_mode : str
        The mode to use when handling the reference. Must be one of "retain",
        "rewrite", or "insert".
    input_format : str
        The format of the input data, if known. If not provided, the format
        will be inferred from the file extension.
    bases : dict
        A dictionary containing information about the base paths to use when
        converting the reference to a source path. Must contain the keys "id",
        "self", and "dir".
    subs: dict
        dictionary of substitutions to make in strings.

    Returns
    -------
    dict or str
        If the reference mode is "retain" or "rewrite", the function returns a
        dictionary containing the reference. If the reference mode is "insert",
        the function returns the data from the referenced file, as a dictionary
        or string.
    """

    logging.info("Handle single $ref: %s",ref)
    if refs_mode == "retain":
        return { "$ref": ref }
    elif refs_mode == "rewrite":
        base, ext = os.path.splitext(ref)
        return { "$ref": base + '.' + input_format }
    elif refs_mode == "insert":
        source = ref_to_source(ref, bases)
        data = read_data(source, input_format)[0]
        if subs is not None:
            return recursive_replace(data, subs)
        else:
            return data
    else:
        raise Exception("Internal error: unexpected refs_mode: "+str(refs_mode))


def merge_deep(d, other, replace=True):
    """
    Make a deep merge of the other dictionary into the first (modifying the first)

    Parameters
    ----------
    d : dict
        The dictionary to be merged into.
    other : dict
        The dictionary to merge from.
    replace : bool
        Replace items already in d
    """
    for other_key, other_val in other.items():
        val = d.get(other_key)
        if isinstance(val, dict) and isinstance(other_val, dict):
            merge_deep(val, other_val)
        elif replace or (other_key not in d):
            d[other_key] = other_val


def handle_all(data, refs_mode, input_format, bases, subs, remove_null):
    """
    Recursively handles all '$ref' references and perform substitutions in the input data.

    Parameters
    ----------
    data : dict
        The input data to be processed for '$ref' references.
    refs_mode : str
        The mode to use when handling the references. Must be one of "retain",
        "rewrite", or "insert". Default is "rewrite".
    input_format : str
        The format of the input data, if known. If not provided, the format
        will be inferred from the file extension.
    bases : dict
        A dictionary containing information about the base paths to use when
        converting the reference to a source path. Must contain the keys "id",
        "self", and "dir". If not provided, the current working directory will
        be used as the base path.
    subs: dict
        dictionary of substitutions to make in strings.
    remove_null: bool
        remove keys if the value is null.

    Returns
    -------
    dict
        The input data with '$ref' references handled according to the specified mode.
    """

    logging.debug("Handling: %s",data)

    if isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], dict) or isinstance(data[i], list):
                data[i] = handle_all(data[i], refs_mode, input_format, bases, subs, remove_null)
        return data

    elif isinstance(data, dict):

        if 'x-propdefs-inherit-ref' in data:

            ref = data['x-propdefs-inherit-ref']
            logging.debug("Handling x-propdefs-inherit-ref %s",ref)

            output = handle_one(ref, "insert", input_format, bases, subs)
            if isinstance(output, dict):
                # Handle $ref:s recursively
                newbases = bases.copy()
                source = ref_to_source(ref, bases)
                newbases['self'] = os.path.dirname(source)
                output = handle_all(output, refs_mode, input_format, newbases, subs, remove_null)
            merge_deep(data, output, replace=False)
            del data['x-propdefs-inherit-ref']

        if '$ref' in data:

            logging.debug("Handling $ref %s",data['$ref'])

            if 'x-propdefs-ref-mode' in data:
                this_refs_mode = data['x-propdefs-ref-mode']
                del data['x-propdefs-ref-mode']
            else:
                this_refs_mode = refs_mode

            if this_refs_mode == 'retain' or len(data['$ref']) <= 0 or data['$ref'][0] == '#':
                return data

            if not set(data.keys()).issubset({'$id', '$comment', '$ref', 'x-propdefs-ref-mode'}):
                raise Exception("Unexpected fields present alongside $ref in:"+str(data)+"::"+str(len(data)))

            output = handle_one(data['$ref'], this_refs_mode, input_format, bases, subs)
            if isinstance(output, dict):
                # Handle $ref:s recursively
                newbases = bases.copy()
                source = ref_to_source(data['$ref'], bases)
                newbases['self'] = os.path.dirname(source)
                output = handle_all(output, refs_mode, input_format, newbases, subs, remove_null)
            if '$id' in data:
                output['$id'] = data['$id']
            return output

        for k, v in list(data.items()):
            if isinstance(v, dict) or isinstance(v, list):
                data[k] = handle_all(v, refs_mode, input_format, bases, subs, remove_null)
            if remove_null and v is None:
                del data[k]

        return data

    else:
        raise Exception("handle: unknown data type, not dict or list: %s",type(data))


def process(source, refs_mode, input_format, bases, subs, remove_null):
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
    bases : dict, optional
        A dictionary containing information about the base paths to use when converting references
        to source paths. Must contain the keys "id" and "dir". If not provided, the current working
        directory will be used as the base path.
    subs: dict
        dictionary of substitutions to make in strings.
    remove_null: bool
        remove keys if the value is null.

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

    data = handle_all(data, refs_mode, input_format, bases, subs, remove_null)

    return data


def process_dir(source_dir, refs_mode, input_format, bases, subs, remove_null):
    """
    Processes all files in a directory and its subdirectories according to the specified parameters.

    Parameters
    ----------
    source_dir : str
        The path to the directory containing the files to be processed.
    refs_mode : str
        The mode for handling '$ref' references: 'rewrite' to rewrite the '$ref' field, 'insert'
        to insert the referenced data, or 'retain' to leave the '$ref' field as is. Default is
        'rewrite'.
    input_format : str
        The format of the input files, or 'auto' to automatically determine the format based on
        the file extension. Default is 'auto'.
    bases : dict
        A dictionary containing information about the base paths to use when converting references
        to source paths. Must contain the keys "id" and "dir". If not provided, the current working
        directory will be used as the base path.
    subs: dict
        dictionary of substitutions to make in strings.
    remove_null: bool
        remove keys if the value is null.

    Returns
    -------
    dict
        A dictionary containing the processed data from all files in the directory and its
        subdirectories, where the keys are the file names and the values are the processed data.
    """

    alldata = {}

    for filename in os.listdir(source_dir):
        f = os.path.join(source_dir,filename)
        if os.path.isdir(f):
            logging.info("Process dir reads directory: %s",f)
            dirdata = process_dir(f, refs_mode, input_format, bases, subs)
            alldata[os.path.basename(f)] = dirdata
        elif os.path.isfile(f):
            base, ext = os.path.splitext(f)
            if ext[1:] in supported_input_formats:
                logging.info("Process dir reads file: %s",f)
                data = process(f, refs_mode, input_format, bases, subs)
                alldata.update(data)

    return alldata


if __name__ == "__main__":

    try:

        parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
        for arg in arguments:
            names = arg.pop('names')
            parser.add_argument(*names, **arg)

        parser.set_defaults(verbosity=[2])

        args = parser.parse_args()
        bases = {'id':args.baseid, 'dir':args.basedir }
        subs = dict(args.sub) if len(args.sub) > 0 else None

        # Make sure verbosity is in the allowed range
        log_levels = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
        verbosity = min(len(log_levels) - 1, max(sum(args.verbosity), 0))
        logging.basicConfig(format='%(levelname)s: %(message)s',level=log_levels[verbosity])
        # Turn on tracebacks, etc., if verbosity is max *or* the debug flag is given
        debug = args.debug or verbosity == len(log_levels)-1
        ExceptionWrapper.debug = debug

    except Exception as e:
        print("Internal error when parsing command line arguments: " +type(e).__name__+": "+str(e)+'.', file=sys.stderr)
        if "-d" in sys.argv:
            raise
        exit(1)

    try:
        try:
            if os.path.isdir(args.source):
                logging.info("Processing directory: %s", args.source)
                data = process_dir(args.source, args.refs_mode, args.input_format, bases, subs, args.remove_null)
            else:
                logging.info("Processing file: %s", args.source)
                data = process(args.source, args.refs_mode, args.input_format, bases, subs, args.remove_null)

        except Exception as e:
            raise ExceptionWrapper("Processing of input failed", e) from e

        try:
            # Figure out output format
            if args.output_format == "auto":
                if args.output:
                    base, ext = os.path.splitext(args.output)
                    if ext in ["."+x for x in supported_input_formats]:
                        output_format = ext[1:]
                    else:
                        raise Exception("Output format cannot be determined, use -f. Output file extension: "+str(ext))
                else:
                    output_format = "json"
            else:
                output_format = args.output_format

            logging.info("Serializing data into format: %s", output_format)
            outstr = output_str(data, output_format)
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
