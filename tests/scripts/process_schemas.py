#!/usr/bin/env python3
"""
This is a preprocessor and format conversion tool for OPTIMADE schema files.
It can process individual files or entire directories and supports various
input and output formats. In particular, it adds a few preprocessor directives:

- $$inherit: reference another schema or a list of schemas to inline into the
  schema being processed, with further dictionary members being deep merged
  into the inherited schema. Non-dictionary members are replaced.

- $$keep: used alongside $$inherit to specify a list of keys to import.
  If specified, only the members specified are merged and all others discarded.
  $keep is always evaluated before $exclude, i.e., $exclude can be used to
  exclude keys inside those members that are kept.

- $$exclude: a list of keys to use alongside $$inherit to not import some members
  via inheritance. It is in particular useful when one wants to replace a
  dictionary member instead of deep merge members into it. If "/" is in the
  value, it is used as a pointer specification to descend into members.

- $$schema: is replaced by $shema with an extension added for the output format.

Usage:

  process_schemas.py source [options]

Examples:

  # Process a single file and write the output to stdout:
  process_schemas.py file.json

  # Process all files in a directory and write the output to a file:
  process_schemas.py dir -o output.json

Dependencies:

  - apt: `apt install python3-yaml python3-jsonschema python3-markdown python3-mdx-math python3-pygments`
  - pip: `pip install PyYAML jsonschema python-markdown python-markdown-math pygments`
  - conda: `conda install python=3 pyyaml jsonschema markdown python-markdown-math pygments

"""

import argparse, io, codecs, os, sys, logging, traceback, pprint, posixpath
from collections import OrderedDict
import urllib.parse
import urllib.request

supported_input_formats = ['json', 'yaml']
supported_output_formats = ["json", "yaml", "md", "html"]

arguments = [
    {
        'names': ['source'],
        'help': 'The property definition file, directory or URL to process.',
        'type': str,
    },
    {
        'names': ['--refs-mode'],
        #'help': 'How to handle $ref references. Can also be set by a x-propdefs-ref-mode key alongside $ref. Also, the x-propdefs-inherit-ref key does a deep merge on the referenced definition.',
        'help': argparse.SUPPRESS,
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
        'help': 'Base directory relative to which $$inherit referencs are resolved',
    },
    {
        'names': ['--baseid'],
        'help': 'Base id to relative to which $$inherit references are resolved',
    },
    {
        'names': ['--resolve-path'],
        'help': 'Add the given path to the list of paths when trying to resolve $$inherit',
        'action': 'append', 'default': []
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
        'names': ['--index'],
        'help': 'Create an index over files',
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
    {
        'names': ['-c', '--clean-inner-schemas'],
        'help': 'Clean out inner $schema occurences',
        'action': 'store_true',
        'default': False
    },
    {
        'names': ['--schema'],
        'help': 'Add a schema to use for validation if its $id is referenced by $schema in the instance (can be given multiple times)',
        'action': 'append', 'nargs': 1
    },
    {
        'names': ['--force-schema'],
        'help': 'Force validation against the given schema regardless of precense of $schema or not in instance',
        'nargs': 1
    },
    {
        'names': ['--html-header'],
        'help': 'Add the given string to the header of generated html output, e.g., to insert a link for css',
        'action': 'append', 'default': []
    },
    {
        'names': ['--html-top'],
        'help': 'Add the given string to the beginning of the body part of generated html output',
        'action': 'append', 'default': []
    },
    {
        'names': ['--html-bottom'],
        'help': 'Add the given string to the bottom of the body part of generated html output',
        'action': 'append', 'default': []
    },

]

general_support_descs = {
    None: "Not specified.",
    "must": "MUST be implemented.",
    "should": "SHOULD be implemented.",
    "may": "OPTIONAL."
}
support_descs = {
    None: "Not specified.",
    "must": "MUST be supported by all implementations, MUST NOT be `null`.",
    "should": "SHOULD be supported by all implementations, i.e., SHOULD NOT be `null`.",
    "may": "OPTIONAL support in implementations, i.e., MAY be `null`."
}
general_response_descs = {
    None: "Not specified.",
    "always": "MUST always be included in the response.",
    "must": "MUST be included by default in the response.",
    "should": "SHOULD be included by default in the response.",
    "may": "MAY be included by default in the response.",
    "should not": "SHOULD NOT be included by default in the response.",
    "must not": "MUST NOT be included by default in the response."
}
response_descs = {
    None: "Not specified.",
    "always": "Is always be included in the response.",
    "yes": "Is included by default in the response.",
    "no": "Is not included by default in the response."
}
query_support_descs = {
    None: "Not specified.",
    "all mandatory" : "MUST be a queryable property with support for all mandatory filter features.",
    "equality only" : "MUST be queryable using the OPTIMADE filter language equality and inequality operators. Other filter language features do not need to be available.",
    "partial" : "MUST be a queryable property.",
    "none": "Support for queries on this property is OPTIONAL."
}

codehilite_css = """
pre { line-height: 125%; }
td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
.codehilite .hll { background-color: #ffffcc }
.codehilite { background: #f8f8f8; }
.codehilite .c { color: #3D7B7B; font-style: italic } /* Comment */
.codehilite .err { border: 1px solid #FF0000 } /* Error */
.codehilite .k { color: #008000; font-weight: bold } /* Keyword */
.codehilite .o { color: #666666 } /* Operator */
.codehilite .ch { color: #3D7B7B; font-style: italic } /* Comment.Hashbang */
.codehilite .cm { color: #3D7B7B; font-style: italic } /* Comment.Multiline */
.codehilite .cp { color: #9C6500 } /* Comment.Preproc */
.codehilite .cpf { color: #3D7B7B; font-style: italic } /* Comment.PreprocFile */
.codehilite .c1 { color: #3D7B7B; font-style: italic } /* Comment.Single */
.codehilite .cs { color: #3D7B7B; font-style: italic } /* Comment.Special */
.codehilite .gd { color: #A00000 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .gr { color: #E40000 } /* Generic.Error */
.codehilite .gh { color: #000080; font-weight: bold } /* Generic.Heading */
.codehilite .gi { color: #008400 } /* Generic.Inserted */
.codehilite .go { color: #717171 } /* Generic.Output */
.codehilite .gp { color: #000080; font-weight: bold } /* Generic.Prompt */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #800080; font-weight: bold } /* Generic.Subheading */
.codehilite .gt { color: #0044DD } /* Generic.Traceback */
.codehilite .kc { color: #008000; font-weight: bold } /* Keyword.Constant */
.codehilite .kd { color: #008000; font-weight: bold } /* Keyword.Declaration */
.codehilite .kn { color: #008000; font-weight: bold } /* Keyword.Namespace */
.codehilite .kp { color: #008000 } /* Keyword.Pseudo */
.codehilite .kr { color: #008000; font-weight: bold } /* Keyword.Reserved */
.codehilite .kt { color: #B00040 } /* Keyword.Type */
.codehilite .m { color: #666666 } /* Literal.Number */
.codehilite .s { color: #BA2121 } /* Literal.String */
.codehilite .na { color: #687822 } /* Name.Attribute */
.codehilite .nb { color: #008000 } /* Name.Builtin */
.codehilite .nc { color: #0000FF; font-weight: bold } /* Name.Class */
.codehilite .no { color: #880000 } /* Name.Constant */
.codehilite .nd { color: #AA22FF } /* Name.Decorator */
.codehilite .ni { color: #717171; font-weight: bold } /* Name.Entity */
.codehilite .ne { color: #CB3F38; font-weight: bold } /* Name.Exception */
.codehilite .nf { color: #0000FF } /* Name.Function */
.codehilite .nl { color: #767600 } /* Name.Label */
.codehilite .nn { color: #0000FF; font-weight: bold } /* Name.Namespace */
.codehilite .nt { color: #008000; font-weight: bold } /* Name.Tag */
.codehilite .nv { color: #19177C } /* Name.Variable */
.codehilite .ow { color: #AA22FF; font-weight: bold } /* Operator.Word */
.codehilite .w { color: #bbbbbb } /* Text.Whitespace */
.codehilite .mb { color: #666666 } /* Literal.Number.Bin */
.codehilite .mf { color: #666666 } /* Literal.Number.Float */
.codehilite .mh { color: #666666 } /* Literal.Number.Hex */
.codehilite .mi { color: #666666 } /* Literal.Number.Integer */
.codehilite .mo { color: #666666 } /* Literal.Number.Oct */
.codehilite .sa { color: #BA2121 } /* Literal.String.Affix */
.codehilite .sb { color: #BA2121 } /* Literal.String.Backtick */
.codehilite .sc { color: #BA2121 } /* Literal.String.Char */
.codehilite .dl { color: #BA2121 } /* Literal.String.Delimiter */
.codehilite .sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.codehilite .s2 { color: #BA2121 } /* Literal.String.Double */
.codehilite .se { color: #AA5D1F; font-weight: bold } /* Literal.String.Escape */
.codehilite .sh { color: #BA2121 } /* Literal.String.Heredoc */
.codehilite .si { color: #A45A77; font-weight: bold } /* Literal.String.Interpol */
.codehilite .sx { color: #008000 } /* Literal.String.Other */
.codehilite .sr { color: #A45A77 } /* Literal.String.Regex */
.codehilite .s1 { color: #BA2121 } /* Literal.String.Single */
.codehilite .ss { color: #19177C } /* Literal.String.Symbol */
.codehilite .bp { color: #008000 } /* Name.Builtin.Pseudo */
.codehilite .fm { color: #0000FF } /* Name.Function.Magic */
.codehilite .vc { color: #19177C } /* Name.Variable.Class */
.codehilite .vg { color: #19177C } /* Name.Variable.Global */
.codehilite .vi { color: #19177C } /* Name.Variable.Instance */
.codehilite .vm { color: #19177C } /* Name.Variable.Magic */
.codehilite .il { color: #666666 } /* Literal.Number.Integer.Long */

.codehilite code, .codehilite pre{
overflow: auto;
overflow-wrap: break-word;
}
"""


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
        cause = e
        tb = cause.__traceback__
        tbdump = traceback.extract_tb(tb)
        if len(tbdump) > 1:
            if tbdump[0].filename == tbdump[-1].filename:
                edata = " ("+str(tbdump[0].filename)+" line:"+str(tbdump[0].lineno)+" triggered at line: "+str(tbdump[-1].lineno)+")."
            else:
                edata = " ("+str(tbdump[0].filename)+" line "+str(tbdump[0].lineno)+" triggered in: "+str(tbdump[-1].filename)+" at line "+str(tbdump[-1].lineno)+")."
        else:
            edata = " ("+str(tbdump[0].filename)+" line "+str(tbdump[0].lineno)+")."
        if isinstance(e, ExceptionWrapper):
            self.messages = [msg + edata] + e.messages
        elif type(e) == Exception:
            self.messages = [msg, str(cause) + edata]
        else:
            self.messages = [msg, type(cause).__name__+": "+str(cause) + edata]
        full_message = msg +". Error details:\n- "+("\n- ".join(self.messages[1:]))+"\n"
        if not self.debug:
            full_message += "\nAdd command line argument -d for a full traceback or one or more -v for higher verbosity."
        super().__init__(full_message)

def validate(instance, args, bases=None, source=None, schemas={}, schema=None, use_schema_field=False, sanity_check=True):
    import jsonschema
    from jsonschema import RefResolver

    # Block attempts to resolve schemas over the Internet, we only want to use Schemas present in the repository
    class LocalOnlyRefResolver(RefResolver):
        def resolve_remote(self, uri):
            raise Exception("Validation: attempt to fetch remove schema over the internet blocked: "+str(uri))

    if '$schema' in instance:
        schema_id = instance['$schema']
    else:
        schema_id = None

    if '$id' in instance:
        iid = instance['$id']
    else:
        iid = None

    if schema is None:
        if schema_id is not None:
            if schema_id in schemas:
                schema = schemas[schema_id]
            else:
                base_schema_id, ext = os.path.splitext(schema_id)
                if base_schema_id in schemas:
                    schema = schemas[base_schema_id]
                else:
                    raise Exception("Validation: reference to unknown schema id: "+str(schema_id))
        else:
            raise Exception("Validation: validation requested but instance does not contain $schema, nor was an explicit schema given")

    if sanity_check:
        # Check that the id and file path makes sense
        if (source is not None) and (iid is not None) and (bases is not None) and ('dir' in bases) and ('id' in bases):

            # if the top $id is inherited from another file, do the sanity check against that file path
            if 'id_inherited_from' in bases:
                idsource = inherit_to_source(bases['id_inherited_from'], bases['self'], args.resolve_path, supported_input_formats)
            else:
                idsource = source

            dirprefix = os.path.commonprefix([bases['dir'], idsource])
            dirpath = os.path.realpath(idsource)
            _dummy, dirext = os.path.splitext(idsource)

            idprefix = os.path.commonprefix([bases['id'], iid])
            idpath = os.path.realpath(os.path.join(dirprefix,iid[len(idprefix):]+dirext))

            if(dirpath!=idpath):
                raise Exception("Validation: sanity check failed, $id ("+iid+") does not match source file path ("+idsource+")\n"+
                                "The fully resolved file path is: "+dirpath+" and the expected path based on the id is: "+idpath)

        # Check that the definition name and filename are the same
        if 'x-optimade-definition' in instance and source is not None:
            if 'name' in instance['x-optimade-definition']:
                defname = instance['x-optimade-definition']['name']
                basename = os.path.basename(source)
                base, ext = os.path.splitext(basename)
                if defname != base:
                    raise Exception("Validation: sanity check failed, x-optimade-definition -> name ("+defname+") does not match source file name ("+basename+")")

    try:
        logging.debug("\n\n** Validating:**\n\n"+pprint.pformat(instance)+"\n\n** Using schema:**\n\n"+pprint.pformat(schema)+"\n\n")

        resolver = LocalOnlyRefResolver.from_schema(schema=schema, store=schemas)

        if use_schema_field:
            if schema_id is not None:
                validator = jsonschema.validators.validator_for(schema, default=_UNSET)
            else:
                raise Exception("Validation: asked to use $schema field to decide validator, but no such field present.")
        else:
            try:
                validator = jsonschema.Draft202012Validator(schema=schema, format_checker=jsonschema.FormatChecker(), resolver=resolver)
            except AttributeError:
                logging.warning("JSON Schema Python library is not aware of the Draft202012 standard. It is probably too old. Will validate using default validator.")
                validator = None

        if validator is not None:
            validator.validate(instance)
        else:
            jsonschema.validate(instance=instance, schema=schema, format_checker=jsonschema.FormatChecker(), resolver=resolver)

    except jsonschema.ValidationError as e:
        logging.debug("Schema validation failed, full output:\n"+str(e))
        logging.debug("Data being validated:\n"+str(instance))
        raise Exception("Schema validation failed:\n"+
                        "  - Instance id: "+str(iid)+"\n"+
                        "  - Schema: "+str(schema_id)+"\n"+
                        "  - Instance path: "+("/".join([str(x) for x in e.absolute_path]))+"\n"+
                        "  - Schema path: "+("/".join([str(x) for x in e.absolute_schema_path]))+"\n"+
                        "  - Error: "+str(e.message)+"\n")

    except jsonschema.SchemaError as e:
        logging.debug("Invalid schema: "+str(e))
        raise Exception("Invalid schema: "+e.message)

def read_data(source, input_format='auto', preserve_order=True, origin=None):
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
            if preserve_order:
                class YamlOrderedSafeLoader(yaml.SafeLoader):
                    def __init__(self, stream, object_pairs_hook=OrderedDict):
                        super().__init__(stream)
                        def mapper(loader, node):
                            loader.flatten_mapping(node)
                            return object_pairs_hook(loader.construct_pairs(node))
                        self.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapper)
                return yaml.load(reader, YamlOrderedSafeLoader), "yaml"
            else:
                return yaml.safe_load(reader), "yaml"

        if input_format == "json":
            import json
            if preserve_order:
                return json.load(reader, object_pairs_hook=OrderedDict), "json"
            else:
                return json.load(reader), "json"
        else:
            raise Exception("Unknown input format or unable to automatically detect for: "+source+", input_format: "+str(input_format))
    except Exception as e:
        if origin is None:
            raise ExceptionWrapper("Couldn't load data from: "+str(source),e)
        else:
            raise ExceptionWrapper("When processing source: " +str(origin)+ " couldn't load data from: "+str(source),e)

    finally:
        if reader is not None:
            reader.close()


def md_header(s, level, style="display"):
    """
    Format string as markdown header
    """
    md_display_headers=["-", "="]
    md_headers=["#", "##", "###", "####", "#####", "######", "#######", "########"]
    if level <= 1 and style=="display":
        out = s + "\n"
        out += md_display_headers[level]*len(s)+"\n\n"
    elif style=="list":
        out = "    "*level + "* "+s+"\n"
    else:
        out = md_headers[level] + " " + s + "\n\n"
    return out

def md_format_lines(s, level, style="display"):
    """
    Format markdown lines
    """
    if style != "list":
        return s

    prefix = "    "*level

    return "\n".join([prefix + line for line in s.splitlines()]) + "\n"

def data_get_basics(data, default_title="*[untitled]*", default_kind="*[unknown]*", default_Kind="*[Unknown]*"):
    basics = {'title':default_title, 'description_short':"", 'description_details':"", 'examples':"", 'kind':default_kind, 'Kind':default_Kind}
    if 'x-optimade-definition' in data and 'kind' in data['x-optimade-definition']:
        basics['kind'] = data['x-optimade-definition']['kind']
        basics['name'] = data['x-optimade-definition']['name']
    elif '$schema' in data and data['$schema'] == 'https://json-schema.org/draft/2020-12/schema':
        basics['kind'] = 'schema'
    elif '@context' in data:
        basics['kind'] = 'json-ld'
    if 'title' in data:
        basics['title'] = str(data['title'])
    if 'description' in data:
        basics['description_short'], sep, basics['description_details'] = [x.strip() for x in data['description'].partition('\n\n')]
    if 'examples' in data:
        basics['examples'] = "- " + "\n- ".join(["`"+str(x)+"`" for x in data['examples']])
    return basics

def set_definition_to_md_inner(prop, inner, indent, linksuffix=""):
    inner_basics = data_get_basics(inner)
    kind = inner_basics['kind']

    s = ""
    if '$id' in inner:
        url = inner['$id']
        title = inner['title'] if 'title' in inner else prop
        if title.lower() != prop.lower():
            title = title + " ("+prop+")"
        if '$id' in data:
            base=urllib.parse.urlparse(data['$id'])
            target=urllib.parse.urlparse(inner['$id'])
            if base.netloc == target.netloc:
                base_dir='.'+posixpath.dirname(base.path)
                target='.'+target.path
                url = posixpath.relpath(target,start=base_dir)
        s += indent + "* **["+title+"]("+url+linksuffix+")** ("+kind+") - [`"+inner['$id']+"`]("+inner['$id']+linksuffix+")  \n"
        s += indent + "  "+inner_basics['description_short']
        if 'x-optimade-requirements' in inner:
            req_support, req_sort, req_query, req_response = [None]*4
            req_partial_info = ""
            reqs = inner['x-optimade-requirements']
            req_support = reqs['support'] if 'support' in reqs else None
            req_sort = reqs['sortable'] if 'sortable' in reqs else None
            req_query = reqs['query-support'] if 'query-support' in reqs else None
            req_response = reqs['response-level'] if 'response-level' in reqs else None
            if req_query == "partial":
                req_partial_info = "The following filter language features MUST be supported: "+", ".join(inner['x-optimade-requirements']['query-support-operators'])
            s += "\n\n"
            s += indent + "    **Requirements/Conventions:**  \n\n"
            if inner_basics['kind'] == 'property':
                s += indent + "    - **Support:** "+support_descs[req_support]+"\n"
                s += indent + "    - **Query:** "+query_support_descs[req_query]+"\n"

                if req_response is not None:
                    s += indent + "    - **Response:** "+str(general_response_descs[req_response])+"\n"

                if inner_basics['description_details'] != "":
                    desc = inner_basics['description_details'].split('\n')
                    if "Requirements/Conventions" in desc[0]:
                        del desc[0]
                        while len(desc)>0 and desc[0].strip() == "":
                            del desc[0]
                    s += indent + "    "+("\n    ".join(desc))+"\n\n"

            else:
                s += indent + "    - **Support:** "+general_support_descs[req_support]+"  \n\n"

    s += "\n"
    return s

def set_definition_to_md(data, args, level=0, linksuffix=""):
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
    basics = data_get_basics(data)

    s = ""
    title = (basics['title'] + " ("+basics['kind']+")") if basics['kind'] != "" else basics['title']
    s += md_header(title, level, style="normal")

    s += "This page documents an [OPTIMADE](https://www.optimade.org/) ["+(basics['kind'].capitalize())+" Definition](https://schemas.optimade.org/#definitions). "
    s += "See [https://schemas.optimade.org/](https://schemas.optimade.org/) for more information.\n\n"

    if '$id' in data:
        s += "**ID: [`"+str(data['$id'])+"`]("+data['$id']+linksuffix+")**  \n"
    if 'name' in basics:
        s += "**Definition name:** `"+basics['name']+"`\n"
    s += "\n"

    s += "**"+(basics['kind'].capitalize())+" name:** "+basics['title']+"  \n"

    if basics['description_short'] != "":
        s += "**Description:** "+str(basics['description_short'])
    if basics['description_details'] != "":
        s += "\n\n" + basics['description_details']+"\n"
    else:
        s += "  \n"

    if '$id' in data:
        basename = os.path.basename(data['$id'])
        s += "\n**Formats:** [[JSON]("+basename+".json)] [[MD]("+basename+".md)]\n"

    for itemtype in ['units', 'prefixes', 'constants', 'entrytypes', 'properties']:
        if itemtype in data and isinstance(data[itemtype],dict):
            s += "\n"
            s += "This "+basics['kind'] + " defines the following "+itemtype+":\n\n"
            for prop in data[itemtype].keys():
                inner = data[itemtype][prop]
                s += set_definition_to_md_inner(prop, inner, indent="", linksuffix=linksuffix)

    s += "\n"
    s += "**JSON definition:**\n"
    s += general_to_md(data, args, linksuffix=linksuffix)

    return s

def single_definition_to_md(data, args, level=0, linksuffix=""):
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
    basics = data_get_basics(data)

    s = ""
    title = (basics['title'] + ", " + data['display-symbol'] + " ("+basics['kind']+")") if basics['kind'] != "" else basics['title']
    s += md_header(title, level, style="normal")

    s += "This page documents an [OPTIMADE](https://www.optimade.org/) ["+(basics['kind'].capitalize())+" Definition](https://schemas.optimade.org/#definitions). "
    s += "See [https://schemas.optimade.org/](https://schemas.optimade.org/) for more information.\n\n"

    if '$id' in data:
        s += "**ID: [`"+str(data['$id'])+"`]("+data['$id']+linksuffix+")**  \n"
    if 'name' in basics:
        s += "**Definition name:** `"+basics['name']+"`\n"
    s += "\n"

    s += "**"+(basics['kind'].capitalize())+" name:** "+basics['title']+"  \n"
    s += "**Latin symbol:** "+data['symbol']+"  \n"
    s += "**Display symbol:** "+data['display-symbol']+"  \n"
    if 'alternate-symbol' in data:
        s += "**Alternate:**"+(", ".join(data["alternate-symbols"]))+"  \n"
    else:
        s += "  \n"

    s += "**Description:** "+str(basics['description_short'])
    s += "\n\n" + basics['description_details']+"\n\n"
    if basics['examples'] != '':
        s += "**Examples:**\n\n"+basics['examples']+"\n\n"

    if 'resources' in data:
        s += "**Resources:**\n\n"
        for resource in data['resources']:
            s += "- ["+resource["relation"]+"]("+resource["resource-id"]+")\n"
        s += "\n\n"

    if '$id' in data:
        basename = os.path.basename(data['$id'])
        s += "**Formats:** [[JSON]("+basename+".json)] [[MD]("+basename+".md)]\n\n"
    s += "**JSON definition:**\n"
    s += general_to_md(data, args, linksuffix=linksuffix)

    return s

def general_to_md(data, args, level=0, linksuffix=""):
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
    import json

    s = "\n``` json\n"
    s += json.dumps(data, indent=4)
    s += "\n```"
    return s

def schema_to_md(data, args, level=0, linksuffix=""):
    """
    Convert data representing a JSON schema into a markdown string.

    Parameters
    ----------
    data : dict
        A dictionary containing the OPTIMADE Property Definition data.

    Returns
    -------
    str
        A string representation of the input data.
    """
    import json
    s = ""

    titlestr = (data['title'] + " (schema)") if 'title' in data else "Schema"
    s += md_header(titlestr, level, style="display")

    s += "This page documents a JSON Schema definition.\n\n"

    s += "**JSON definition:**\n"
    s += general_to_md(data, args, linksuffix=linksuffix)

    return s


def property_definition_to_md(data, args, level=0, linksuffix=""):
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
    s = ""

    basics = data_get_basics(data)

    req_support, req_sort, req_query, req_response = [None]*4
    req_partial_info = ""
    if 'x-optimade-requirements' in data:
        reqs = data['x-optimade-requirements']
        req_support = reqs['support'] if 'support' in reqs else None
        req_sort = reqs['sortable'] if 'sortable' in reqs else None
        req_query = reqs['query-support'] if 'query-support' in reqs else None
        req_response = reqs['response-level'] if 'response-level' in reqs else None
        if req_query == "partial":
            req_partial_info = "The following filter language features MUST be supported: "+", ".join(data['x-optimade-requirements']['query-support-operators'])

    #TODO: need to iterate through dicts, lists to get the full type
    optimade_type = data['x-optimade-type']

    s = ""

    title = (basics['title'] + " ("+basics['kind']+")") if basics['kind'] != "" else basics['title']
    s += md_header(title, level, style="normal")

    s += "This page documents an [OPTIMADE](https://www.optimade.org/) [Property Definition](https://schemas.optimade.org/#definitions). "
    s += "See [https://schemas.optimade.org/](https://schemas.optimade.org/) for more information.\n\n"

    if '$id' in data:
        s += "**ID: [`"+str(data['$id'])+"`]("+data['$id']+linksuffix+")**  \n"
    if 'name' in basics:
        s += "**Definition name:** `"+basics['name']+"`\n"
    s += "\n"

    s += "**Property name:** "+basics['title']+"  \n"
    s += "**Description:** "+basics['description_short']+"  \n"
    s += "**Type:** "+str(optimade_type)+"  \n"
    if 'x-optimade-requirements' in data:
        s += "**Implementation requirements:**  \n"
        s += "- **Support:** "+support_descs[req_support]+"  \n\n"
        s += "- **Query:** "+query_support_descs[req_query]+"  \n"
        if req_response is not None:
            s += "- **Response:**  \n"
    s += "\n"
    s += basics['description_details']+"\n\n"
    s += "**Examples:**\n\n"
    s += basics['examples']+"\n\n"

    if 'resources' in data:
        s += "**Resources:**\n\n"
        for resource in data['resources']:
            s += "- ["+resource["relation"]+"]("+resource["resource-id"]+")\n"
        s += "\n\n"

    if '$id' in data:
        basename = os.path.basename(data['$id'])
        s += "**Formats:** [[JSON]("+basename+".json)] [[MD]("+basename+".md)]\n\n"
    s += "**JSON definition:**\n"
    s += general_to_md(data, args, linksuffix=linksuffix)

    return s

def data_to_md(data, args, level=0, linksuffix=""):
    """
    Convert data representing OPTIMADE Definitions of different kinds into a markdown string.

    Parameters
    ----------
    data : dict
        A dictionary containing the OPTIMADE Property Definition data.

    Returns
    -------
    str
        A string representation of the input data.
    """
    if args.index:
        return data_to_md_index(data, args, level=level, linksuffix=linksuffix)

    s = ""
    if not "x-optimade-definition" in data:
        if '$schema' in data and data['$schema'] == 'https://json-schema.org/draft/2020-12/schema':
            s += schema_to_md(data, args, linksuffix=linksuffix)
            return s
        if 'title' in data:
            basics = data_get_basics(data)
            s += md_header(basics['title'], level, style="display")
            s += general_to_md(data, args, linksuffix=linksuffix)
            return s
        for item in sorted(data.keys()):
            try:
                if isinstance(data[item], dict):
                    s += md_header(item, level, style="display")
                    s += data_to_md(data[item], args, level=level+1, linksuffix=linksuffix)
                #elif item == "$id":
                #    continue
                #else:
                #    raise Exception("Internal error, unexpected data for data_to_md: "+str(data))
                #    exit(0)
            except Exception as e:
                raise ExceptionWrapper("Could not process item: "+item,e)
            s += "\n"
        return s

    if not "kind" in data['x-optimade-definition']:
        raise Exception("x-optimade-definition encountered without a 'kind' field.")
    kind = data['x-optimade-definition']['kind']

    if kind == 'property':
        s += property_definition_to_md(data, args, level, linksuffix=linksuffix)
    elif kind in ['unit', 'constant', 'prefix']:
        s += single_definition_to_md(data, args, level, linksuffix=linksuffix)
    elif kind in ['standard', 'entrytype', 'unitsystem']:
        s += set_definition_to_md(data, args, level, linksuffix=linksuffix)
    else:
        raise Exception("Unknown kind in x-optimade-definition: "+str(data['x-optimade-definition']['kind']))

    return s

def data_to_md_index(data, args, path=[], level=0, linksuffix=""):
    s = ""
    # The heuristic of looking for a 'title' field that is a string
    # to determine how to print things is not foolproof,
    # but seems to work for now. This may need revisiting later.
    if ('title' in data and isinstance(data['title'],str)) or '@context' in data:
        basics = data_get_basics(data, default_title=path[-1])
        title = basics['title']
        kind = basics['kind']
        if '$id' in data:
            s += md_header("**["+title+"]("+("/".join(path))+linksuffix+")** ("+kind+") - [`"+data['$id']+"`]("+data['$id']+linksuffix+")",level=level,style="list")
            s += md_format_lines("\n"+basics['description_short'],level=level+1,style="list")
        else:
            s += md_header("**["+title+"]("+("/".join(path))+linksuffix+")** ("+kind+")",level=level,style="list")
            s += md_format_lines("\n"+basics['description_short'],level=level+1, style="list")
        s += "\n"
    else:
        if len(path) > 0:
            s += md_header("**"+path[-1]+"**", level, style="list")
            next_level = level + 1
        else:
            s += md_header("Index", level, style="header")
            next_level = 0
        for item in sorted(data.keys()):
            try:
                if isinstance(data[item], dict) and ('title' in data[item] and isinstance(data[item]['title'],str)):
                    s += data_to_md_index(data[item], args, path=path+[str(item)], level=next_level, linksuffix=linksuffix)
            except Exception as e:
                raise ExceptionWrapper("Could not process item: "+item,e)
        for item in sorted(data.keys()):
            try:
                if isinstance(data[item], dict) and not ('title' in data[item] and isinstance(data[item]['title'],str)):
                    s += data_to_md_index(data[item], args, path=path+[str(item)], level=next_level, linksuffix=linksuffix)
            except Exception as e:
                raise ExceptionWrapper("Could not process item: "+item,e)

    return s


def data_to_html(data, args, header=""):

    import markdown

    # Couldn't get the standard MathJaxv2 config to work
    #<script type="text/javascript" src="https://cdn.jsdelivr.net/npm/mathjax@2/MathJax.js">
    #</script>
    #<script type="text/x-mathjax-config">
    #MathJax.Hub.Config({
    #  config: ["MMLorHTML.js"],
    #  jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
    #  extensions: ["MathMenu.js", "MathZoom.js"]
    #});
    #</script>

    htmldoc = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.css" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/katex/dist/katex.min.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex/dist/contrib/mathtex-script-type.min.js" defer></script>
    <title>%(title)s</title>
    <style>%(style)s</style>
%(header)s
  </head>
<body>
%(body)s
</body>
</html>
"""
    if args.index:
        title = "Index"
    else:
        title = str(data['title']) if 'title' in data else "?"
    s = data_to_md(data, args)
    md = markdown.Markdown(output_format="html5",
                           extensions = ['mdx_math', 'codehilite', 'fenced_code'],
                           extension_configs={'mdx_math': {"enable_dollar_delimiter": False}})
    body = md.convert(s)
    return htmldoc % { 'title':title, 'body':"".join(args.html_top)+body+"".join(args.html_bottom), 'style': codehilite_css, 'header': "".join(args.html_header)}

def output_str(data, output_format, args):
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
        return data_to_md(data, args, linksuffix=".md")
    elif output_format == "html":
        return data_to_html(data, args)
    else:
        raise Exception("Unknown output format: "+str(output_format))


def inherit_to_source(ref, reldir, absdirs, formats):
    """
    Convert a JSON Schema $$inherit reference to a source path.

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
    if parsed_ref.scheme not in ['file', '']:
        return ref
    ref = parsed_ref.path

    if os.path.isabs(ref):
        # Re-process absolute path to file path
        #absref = urllib.parse.urljoin(bases['id'], ref)
        #ref = absref[len(bases['id']):]
        ref = os.path.relpath(ref,'/')
        checkdirs = absdirs
    else:
        # Relative paths are always resolved relative to the file itself
        checkdirs = [ reldir ]

    _dummy, ext = os.path.splitext(ref)
    if ext is not None and ext != "":
        try_exts = ['']
    else:
        try_exts = ['.'+s for s in formats]

    for d in checkdirs:
        for ext in try_exts:
            candidate = os.path.join(d,ref)+ext
            if os.path.exists(candidate):
              return candidate

    raise Exception("File not found when dereferencing $$inherit: "+str(ref)+" looked in: "+str(checkdirs))


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


def handle_inherit(ref, mode, bases, subs, args, origin=None):
    """
    Handle a single inheritance.

    Parameters
    ----------
    ref : str
        The JSON reference to be handled.
    mode : str
        The mode to use when handling the reference. Must be one of "retain",
        "rewrite", or "insert".
    bases : dict
        A dictionary containing information about the base paths to use when
        converting the reference to a source path. Must contain the keys "id",
        "self", and "dir".
    subs: dict
        dictionary of substitutions to make in strings.

    Returns
    -------
    dict or str
        If mode is "retain" or "rewrite", the function returns a
        dictionary containing the reference. If the reference mode is "insert",
        the function returns the data from the referenced file, as a dictionary
        or string.
    """

    logging.info("Handle single $$inherit: %s",ref)
    if mode == "retain":
        return { "$ref": ref }
    elif mode == "rewrite":
        base, ext = os.path.splitext(ref)
        return { "$ref": base + '.' + args.input_format }
    elif mode == "insert":
        source = inherit_to_source(ref, bases['self'], args.resolve_path, supported_input_formats)
        data = read_data(source, args.input_format, origin=origin)[0]
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
            merge_deep(val, other_val, replace)
        elif replace or (other_key not in d):
            d[other_key] = other_val


def handle_all(data, bases, subs, args, level, origin=None):
    """
    Recursively handles all '$$inherit' references and perform substitutions in the input data.

    Parameters
    ----------
    data : dict
        The input data to be processed for '$$inherit' references.
    bases : dict
        A dictionary containing information about the base paths to use when
        converting the reference to a source path. Must contain the keys "id",
        "self", and "dir". If not provided, the current working directory will
        be used as the base path.
    subs: dict
        dictionary of substitutions to make in strings.
    args: dict or dict-like (e.g., argument parse object)
        additional settings affecting processing
    level: int, optional
        count recursion level. Default is 0.

    Returns
    -------
    dict
        The input data with '$$inherit' references handled according to the specified mode.
    """

    logging.debug("Handling: %s",data)

    if isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], dict) or isinstance(data[i], list):
                data[i] = handle_all(data[i], bases, subs, args, level=level+1, origin=origin)
        return data

    elif isinstance(data, dict):

        if '$$inherit' in data:

            if not isinstance(data['$$inherit'], list):
                inherits = [data['$$inherit']]
            else:
                inherits = data['$$inherit']

            for inherit in inherits:

                logging.debug("Handling $$inherit preprocessor directive: %s",inherit)

                output = handle_inherit(inherit, "insert", bases, subs, args, origin=origin)
                if isinstance(output, dict):
                    # Handle the inherit recursively
                    newbases = bases.copy()
                    source = inherit_to_source(inherit, bases['self'], args.resolve_path, supported_input_formats)
                    newbases['self'] = os.path.dirname(source)
                    output = handle_all(output, newbases, subs, args, level=level+1, origin=source)

            if '$$keep' in data:
                logging.debug("Handling $$keep preprocessor directive: %s",data['$$keep'])
                for key in list(output.keys()):
                    if key not in data['$$keep']:
                        del output[key]
                del data['$$keep']

            if '$$exclude' in data:
                logging.debug("Handling $$exclude preprocessor directive: %s",data['$$exclude'])
                for item in data['$$exclude']:
                    pointer = re.split(r'(?<!\\)/', item)
                    loc = output
                    while len(pointer) > 1:
                        key = pointer.pop(0)
                        if key in loc:
                            loc = loc[key]
                        else:
                            raise Exception("$$exclude path pointer invalid:",item)
                    del loc[pointer[0]]
                del data['$$exclude']

            merge_deep(data, output, replace=False)
            del data['$$inherit']

        if '$$schema' in data:
            data['$schema'] = data['$$schema']+"."+args.output_format
            del data['$$schema']

        if '$schema' in data and level > 0 and args.clean_inner_schemas:
            del data['$schema']

        for k, v in list(data.items()):
            if isinstance(v, dict) or isinstance(v, list):
                data[k] = handle_all(v, bases, subs, args, level=level+1, origin=origin)
            if args.remove_null and v is None:
                del data[k]

        # Always place $schema and $id at the top of the output for ordered output
        if isinstance(data,OrderedDict):
            if '$id' in data:
                data.move_to_end('$id',last=False)
            if '$schema' in data:
                data.move_to_end('$schema',last=False)

        return data

    else:
        raise Exception("handle: unknown data type, not dict or list: %s",type(data))


def process(source, bases, subs, args):
    """
    Processes the input file according to the specified parameters.

    Parameters
    ----------
    source : str
        The path to a file or a URL to the input to be processed.
    bases : dict, optional
        A dictionary containing information about the base paths to use when converting references
        to source paths. Must contain the keys "id" and "dir". If not provided, the current working
        directory will be used as the base path.
    subs: dict
        dictionary of substitutions to make in strings.
    args: dict or dict-like (e.g., argument parse object)
        additional settings affecting processing

    Returns
    -------
    str
        A string representation of the processed output data in the specified output format.

    """
    data, input_format = read_data(source, args.input_format)
    parsed_source = urllib.parse.urlparse(source)
    bases['self'] = os.path.dirname(parsed_source.path)

    # First handle all replacements
    if subs is not None:
        recursive_replace(data, subs)

    # Inheriting the top $id is interpreted as a special case that needs to be
    # remembered to be handled correctly by the sanity check in the validator, since
    # the $id should be named according to the referenced path.
    if ('$$inherit' in data) and ('$id' not in data):
        bases['id_inherited_from'] = data['$$inherit']

    if "$id" in data:
        id_uri = data["$id"]

        if bases['id'] is None:
            if 'dir' in bases and bases['dir'] is not None:
                prefix = os.path.commonprefix([bases['dir'], source])
            else:
                prefix = ""
            rel_source = source[len(prefix):]
            if not id_uri.endswith(rel_source):
                rel_source, ext = os.path.splitext(rel_source)
                if not id_uri.endswith(rel_source):
                    raise Exception("The $id field needs to end with: "+str(rel_source)+" but it does not: "+str(id_uri))
            bases = {'id': id_uri[:-len(rel_source)], 'dir': bases['dir'] }

    data = handle_all(data, bases, subs, args, level=0, origin=source)

    return data


def process_dir(source_dir, bases, subs, args):
    """
    Processes all files in a directory and its subdirectories according to the specified parameters.

    Parameters
    ----------
    source_dir : str
        The path to the directory containing the files to be processed.
    bases : dict
        A dictionary containing information about the base paths to use when converting references
        to source paths. Must contain the keys "id" and "dir". If not provided, the current working
        directory will be used as the base path.
    subs: dict
        dictionary of substitutions to make in strings.
    args: dict or dict-like (e.g., argument parse object)
        additional settings affecting processing

    Returns
    -------
    dict
        A dictionary containing the processed data from all files in the directory and its
        subdirectories, where the keys are the file names and the values are the processed data.
    """

    alldata = OrderedDict()

    for filename in os.listdir(source_dir):
        f = os.path.join(source_dir,filename)
        if os.path.isfile(f):
            base, ext = os.path.splitext(f)
            if ext[1:] in supported_input_formats:
                logging.info("Process dir reads file: %s",f)
                data = process(f, bases, subs, args)
                #alldata.update(data)
                alldata[os.path.basename(base)] = data
    for filename in os.listdir(source_dir):
        f = os.path.join(source_dir,filename)
        if os.path.isdir(f):
            logging.info("Process dir reads directory: %s",f)
            dirdata = process_dir(f, bases, subs, args)
            alldata[os.path.basename(f)] = dirdata

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
        if args.basedir is not None:
            args.resolve_path = [ args.basedir ] + args.resolve_path
        subs = dict(args.sub) if len(args.sub) > 0 else None

        # Make sure verbosity is in the allowed range
        log_levels = [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
        verbosity = min(len(log_levels) - 1, max(sum(args.verbosity), 0))
        logging.basicConfig(format='%(levelname)s: %(message)s',level=log_levels[verbosity])
        # Turn on tracebacks, etc., if verbosity is max *or* the debug flag is given
        debug = args.debug or verbosity == len(log_levels)-1
        ExceptionWrapper.debug = debug

        # Figure out output format
        if args.output_format == "auto":
            if args.output:
                base, ext = os.path.splitext(args.output)
                if ext in ["."+x for x in supported_input_formats]:
                    args.output_format = ext[1:]
                else:
                    raise Exception("Output format cannot be determined, use -f. Output file extension: "+str(ext))
            else:
                args.output_format = "json"

    except Exception as e:
        print("Internal error when parsing command line arguments: " +type(e).__name__+": "+str(e)+'.', file=sys.stderr)
        if "-d" in sys.argv:
            raise
        exit(1)

    try:
        try:
            if os.path.isdir(args.source):
                logging.info("Processing directory: %s", args.source)
                data = process_dir(args.source, bases, subs, args)
            else:
                logging.info("Processing file: %s", args.source)
                data = process(args.source, bases, subs, args)

        except Exception as e:
            raise ExceptionWrapper("Processing of input failed", e) from e

        try:
            if args.force_schema:
                schema_data, ext = read_data(args.force_schema, "json")
                validate(data, args, bases=bases, source=args.source, schema=args.force_schema)

            if args.schema is not None and '$schema' in data:
                schemas = {}
                for schema in args.schema:
                    schema_data, ext = read_data(schema[0], "json")
                    if '$id' in schema_data:
                        schemas[schema_data['$id']] = schema_data
                    else:
                        raise Exception("Schema provided without $id field: "+str(schema_data))
                validate(data, args, bases=bases, source=args.source, schemas=schemas)

        except Exception as e:
            raise ExceptionWrapper("Validation of data failed", e) from e

        try:
            logging.info("Serializing data into format: %s", args.output_format)
            outstr = output_str(data, args.output_format, args)
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
