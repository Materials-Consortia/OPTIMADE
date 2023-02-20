#!/usr/bin/env python3

import argparse, io, codecs, os, sys
import urllib.parse
import urllib.request

def read_file(source, input_format='auto'):
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
                os.chdir(os.path.dirname(base))
            except FileNotFoundError:
                reader = open(base, 'r')
            if input_format == 'auto':
                input_format = ext.lstrip('.')

        if input_format == "yaml":
            import yaml
            return yaml.safe_load(reader), "yaml"
        else:
            raise Exception("Unknown input format or unable to automatically detect for: "+source+", input_format: "+str(input_format))
    except FileNotFoundError:
        raise Exception("File not found: "+str(source)+" relative to:"+os.getcwd())

    finally:
        if reader is not None:
            reader.close()




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
    else:
        raise Exception("Unknown output format"+str(output_format))


def handle_refs(data, id_uri=None, refs_mode="rewrite", input_format=None):
    """
    Recursively handles all '$ref' references in the input data.

    Parameters
    ----------
    data : dict
        The input data to be processed for '$ref' references.
    id_uri : str, optional
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

    def handle_single_ref(ref, id_uri, refs_mode, input_format):
        if refs_mode == "rewrite":
            base, ext = os.path.splitext(ref)
            return { "$ref": base + '.' + input_format }
        elif refs_mode == "insert":
            if os.path.isabs(ref) and id_uri is not None:
                absref = urllib.parse.urljoin(id_uri, ref)
                prefix = os.path.commonprefix([id_uri, absref])
                ref = absref[len(prefix):]
                ref = os.path.join("../"*(len(ref.split(os.sep))-1),ref)
                base, ext = os.path.splitext(ref)
                if ext == '' and not os.path.exists(ref):
                    ref += "."+input_format
                return read_file(ref,input_format)
                #print("IM HERE",input_format,file=sys.stderr)
            return read_file(ref)
        else:
            raise Exception("Internal error: unexpected refs_mode: "+str(refs_mode))

    if '$ref' in data:
        if len(data) > 1:
            raise Exception("Unexpected fields present alongside $ref in:"+str(data))
        return handle_single_ref(data['$ref'], id_uri, refs_mode, input_format)

    for k, v in data.items():
        if isinstance(v, dict):
            data[k] = handle_refs(v, id_uri, refs_mode, input_format)

    return data


def process(f, refs_mode="rewrite", input_format="auto", output_format="json"):
    """
    Processes the input file according to the specified parameters.

    Parameters
    ----------
    f : str
        The name of the input file to be processed.
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

    data, input_format = read_file(f)

    if len(data) != 1:
        raise Exception("Unexpected format of property definition.")

    name = list(data.keys())[0]

    if refs_mode != "retain":
        if "$id" in data[name]:
            id_uri = data[name]["$id"]
        else:
            id_uri = None
        data = handle_refs(data, id_uri, refs_mode, input_format)

    return output_str(data)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process property definition source files into other formats", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file', help='The property definition file to process (path or URL).')
    parser.add_argument('--refs-mode', help='How to handle $ref references', choices=["insert", "rewrite", "retain"], default="insert")
    parser.add_argument('--input-format', help='The input format to read', default="auto", choices=["auto","yaml"])
    parser.add_argument('--output-format', help='The output format to generate', default="json", choices=["json"])
    args = parser.parse_args()

    output_str = process(args.file, args.refs_mode, args.input_format, args.output_format)

    print(output_str)
