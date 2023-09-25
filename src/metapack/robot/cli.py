# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE

"""

"""
from .descriptions import column_description
import argparse
from metapack.cli.core import MetapackCliMemo as _MetapackCliMemo
from metapack import Downloader

downloader = Downloader.get_instance()


class ArgumentError(Exception): pass


class MetapackCliMemo(_MetapackCliMemo):

    def __init__(self, args, downloader):
        super().__init__(args, downloader)


def robot(subparsers):
    """
    Robot Overlord!
    """

    parser = subparsers.add_parser('robot',
                                   help='Summon robot overlords',
                                   description=robot.__doc__,
                                   formatter_class=argparse.RawDescriptionHelpFormatter,
                                   )

    parser.set_defaults(run_command=run_robot)

    # parser.add_argument('-j', '--json', default=False, action='store_true',
    #                    help='Display configuration and diagnostic information ad JSON')

    subparsers = parser.add_subparsers()

    ##
    ## Data Dictionaries

    dd = subparsers.add_parser('dd', help='Processing Data Dictionaries')
    dd_subparsers = dd.add_subparsers()
    dd.set_defaults(sub_command=run_dd_cmd)
    # load.add_argument('-C', '--clean', default=False, action='store_true',
    #                  help='Delete everything from the database first')
    # load.add_argument('urls', nargs='*', help="Database or Datapackage URLS")

    # create JSONL subparser

    jsonl_p = dd_subparsers.add_parser('jsonl', help='Processing JSONL files')
    jsonl_p.set_defaults(sub_command=run_jsonl_cmd)

    jsonl_p.add_argument('metatabfile_js', nargs='?', help="Path to a notebook file or a Metapack package")
    ##
    ## Metadata

    info = subparsers.add_parser('md', help='Updating metadata')
    info.set_defaults(sub_command=run_md_cmd)

    # info.add_argument('url', help="Database or Datapackage URL")

    parser.add_argument('metatabfile', nargs='?', help="Path to a notebook file or a Metapack package")


def run_robot(args):

    if args.metatabfile_js:
        args.metatabfile = args.metatabfile_js

    m = MetapackCliMemo(args, downloader)


    args.sub_command(m)


def run_dd_cmd(m):
    print("DD")


def run_md_cmd(m):
    print("MD")


def run_jsonl_cmd(m):
    import json


    if m.resource is None:
        resources = m.resources()
    else:
        resources = [m.doc.resource(m.resource)]

    name = m.doc.name

    for r in resources:
        st = r.schema_term
        cols = r.columns()

        for c in cols:
            d = {
                'id': name + ":" + c['header'],
                'text': column_description(c),
                'source_id': m.doc.name
            }

            print(json.dumps(d))
