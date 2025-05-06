# -*- coding: utf-8 -*-
#!/usr/bin/env python3

__author__ = "jboursier"
__copyright__ = "Copyright 2025, Malwarebytes"
__version__ = "0.2.0"
__maintainer__ = "jboursier"
__email__ = "jboursier@malwarebytes.com"
__status__ = "Development"


try:
    import json
    import logging
    from datetime import datetime
    from typing import Any, Dict, List

    import click

    logging.getLogger().setLevel(level=logging.INFO)
except ImportError:
    import sys

    logging.error("Missing dependencies. Please reach @jboursier-mwb if needed.")
    sys.exit(255)

from . import parser


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


@cli.command("load_file")
@click.argument("path")
@click.argument("token")
def load_csv(path: str, token: str) -> None:

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

@cli.command("get_license")
@click.argument("purl")
@click.argument("token")
def get_purl_license(purl: str, token: str) -> None:
    click.echo(parser.get_license(purl=purl, token=str))


@cli.command("merge_csv")
@click.argument("input_licenses_file")
@click.argument("output_license_file")
# Merge CSV, add licenses.csv into deps_list_output.csv
def merge_csvs(input_licenses_file: str, output_license_file: str) -> None:
    str_output = ""
    licenses_input = {}
    with open(input_licenses_file, "r") as finput:
        finput_lines = finput.readlines()
        for l in finput_lines:
            try:
                purl, license = l.split(',', maxsplit=1)
            except Exception as e:
                print(l + str(e))
            licenses_input[purl.strip()] = license.strip()

    with open(output_license_file, 'r') as foutput:
        for line in foutput.readlines():
            repo_output, purl_output, version_output, license_output = line.split(',')[:4]
            purl_output = purl_output.strip()
            license_output = license_output.strip()
            if licenses_input[purl_output]:
                str_output += f"{repo_output.strip()}, {purl_output.strip()}, {version_output.strip()}, {licenses_input[purl_output]}"
                str_output += "\n"
            else:
                str_output += f"{repo_output.strip()}, {purl_output.strip()}, {version_output.strip()}, Unknown"
                str_output += "\n"

    with open("deps_output.csv", "w") as fexport:
        fexport.write(str_output)


if __name__ == "__main__":
    cli()
    #get_license()
    #load_csv()
    #merge_csvs()