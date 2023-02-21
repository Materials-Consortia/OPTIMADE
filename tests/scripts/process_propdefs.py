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


def dict_get_one(d):
    if len(d) != 1:
        raise Exception("Expected only one field in dictionary: "+str(d))
    key = list(d.keys())[0]
    return key, d[key]


def data_to_str(data):

    field, data = dict_get_one(data)
    title = data['title']
    description, sep, reqs = data['description'].partition('\n\n')

    #TODO: need to iterate through dicts, lists to get the full type
    optimade_type = data['x-optimade-type']

    reqs = reqs.replace("Requirements/Conventions:\n","")

    s = field+"\n"
    s += "~"*len(field)+"\n"
    s += "\n"
    s += "**Name**: "+str(title)+"\n"
    s += "**Description**: "+str(description)+"\n"
    s += "**Type**: "+str(optimade_type)+"\n"
    s += "**Requirements/Conventions**:\n"
    s += "\n"
    s += "  - **Support**:\n"
    s += "  - **Query**:\n"
    s += "  - **Response**:\n"
    s += "  "+str(reqs).replace("\n","\n  ")+"\n"
    s += "\n"
    s += "**Examples**:"
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
    elif output_format == "rst":
        return data_to_str(data)
    else:
        raise Exception("Unknown output format"+str(output_format))


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
        if refs_mode == "rewrite":
            base, ext = os.path.splitext(ref)
            return { "$ref": base + '.' + input_format }
        elif refs_mode == "insert":
            if os.path.isabs(ref):
                # Re-process root path to a sane file path
                absref = urllib.parse.urljoin(id_base, ref)
                prefix = os.path.commonprefix([id_base, absref])
                relref = os.path.relpath(absref[len(prefix):],'/')
                ref = os.path.join(basedir,relref)
                base, ext = os.path.splitext(ref)
                if ext == '' and not os.path.exists(ref):
                    ref += "."+input_format
            else:
                input_format = 'auto'
            data = read_file(ref, input_format)[0]
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


def process(source, refs_mode="rewrite", input_format="auto", output_format="json", basedir="./"):
    """
    Processes the input file according to the specified parameters.

    Parameters
    ----------
    source : str
        The filename or URL of the input file to be processed.
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
    data, input_format = read_file(source)

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

    return output_str(data, output_format)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process property definition source files into other formats", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('source', help='The property definition file to process (path or URL).')
    parser.add_argument('--refs-mode', help='How to handle $ref references', choices=["insert", "rewrite", "retain"], default="insert")
    parser.add_argument('--input-format', help='The input format to read', default="auto", choices=["auto","yaml"])
    parser.add_argument('--output-format', help='The output format to generate', default="json", choices=["json","yaml","rst"])
    parser.add_argument('--basedir', help='Reference top-level directory to use to resolve $ref reference paths')
    parser.add_argument('--output', help='Write the output to a file')
    args = parser.parse_args()

    output_str = process(args.source, args.refs_mode, args.input_format, args.output_format, args.basedir)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_str)
    else:
        print(output_str)
