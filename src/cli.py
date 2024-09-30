# -*- coding: utf-8 -*-
#!/usr/bin/env python3

__author__ = "jboursier"
__copyright__ = "Copyright 2024, Malwarebytes"
__version__ = "0.0.1"
__maintainer__ = "jboursier"
__email__ = "jboursier@malwarebytes.com"
__status__ = "Development"


try:
    import click
    import json
    from typing import Dict, Any, List
    from datetime import datetime
    import logging

    logging.getLogger().setLevel(level=logging.INFO)
except ImportError:
    import sys

    logging.error("Missing dependencies. Please reach @jboursier-mwb if needed.")
    sys.exit(255)

from purl_license_checker import parser


def main() -> None:
    try:
        cli()
    except Exception as e:
        click.echo(e)


@click.group()
def cli() -> None:
    """Retrieve licenses for purl documented dependencies.

    Get help: `@jboursier-mwb` on GitHub
    """

#@click.command()
#@click.argument("purl")
#def get_license(purl: str) -> None:
#    return parser.get_license(purl=purl)

@click.command()
@click.argument("path")
@click.argument("token")
def load_csv(path: str, token: str) -> None:

    merge_csvs()
    return
    # Dict formed by {purl: license} entries
    licenses = {}

    # Parse the csv input
    # repo_name, purl, version, license
    input_csv = {}
    with open(path, "r") as f:
        for l in f.readlines():
            line = l.split(",")
            input_csv
            try:
                if licenses[line[1].strip()] != "":
                    continue
            except:
                pass
            if line[3].strip() != "Unknown":
                licenses[line[1].strip()] = line[3].strip()
            else:
                licenses[line[1].strip()] = ""

        # Fetch the license for each empty license
        for l in licenses.keys():
            if licenses[l] == "":
                license_res = parser.get_license(purl=l, token=token)
                if license_res:
                    licenses[l] = license_res


    # Store the output
    with open("output.csv", "w") as f:
        for k in licenses.keys():
            f.write(f"{k}, {licenses[k]}\n")

    #print(licenses)

# Merge CSV, add licenses.csv into deps_list_output.csv
def merge_csvs() -> None:
    str_output = ""
    with open("licenses.csv", "r") as finput:
        with open("deps_list_output.csv", 'r') as foutput:
            finput_lines = finput.readlines()
            for line in foutput.readlines():
                repo_output, purl_output, version_output, license_output = line.split(',')[:4]
                purl_output = purl_output.strip()
                license_output = license_output.strip()
                for l in finput_lines:
                    purl, license = l.split(',')
                    purl = purl.strip()
                    license = license.strip()
                    if purl_output == purl:
                        str_output += f"{repo_output.strip()}, {purl_output.strip()}, {version_output.strip()}, {license}"
                        str_output += "\n"

    with open("deps_output.csv", "w") as fexport:
        fexport.write(str_output)


if __name__ == "__main__":
    #get_license()
    load_csv()
    #merge_csvs()