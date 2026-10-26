# -*- coding: utf-8 -*-
#!/usr/bin/env python3

__author__ = "jboursier"
__copyright__ = "Copyright 2025, Malwarebytes"
__version__ = "0.2.0"
__maintainer__ = "jboursier"
__email__ = "jboursier@malwarebytes.com"
__status__ = "Development"


try:
    import csv
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
    with open(path, "r", newline="") as f:
        for row in csv.reader(f):
            if len(row) < 4:
                continue
            purl = row[1].strip()
            license = row[3].strip()

            # Keep the first non-empty license we see for a given purl.
            if licenses.get(purl):
                continue

            licenses[purl] = "" if license == "Unknown" else license

        # Fetch the license for each empty license
        for l in licenses.keys():
            if licenses[l] == "":
                license_res = parser.get_license(purl=l, token=token)
                if license_res:
                    licenses[l] = license_res


    # Store the output
    with open("output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for k in licenses.keys():
            writer.writerow([k, licenses[k]])

@cli.command("get_license")
@click.argument("purl")
@click.argument("token")
def get_purl_license(purl: str, token: str) -> None:
    click.echo(parser.get_license(purl=purl, token=token))


@cli.command("merge_csv")
@click.argument("input_licenses_file")
@click.argument("output_license_file")
# Merge CSV, add licenses.csv into deps_list_output.csv
def merge_csvs(input_licenses_file: str, output_license_file: str) -> None:
    licenses_input: Dict[str, str] = {}
    with open(input_licenses_file, "r", newline="") as finput:
        for row in csv.reader(finput):
            if len(row) < 2:
                continue
            purl, license = row[0], row[1]
            licenses_input[purl.strip()] = license.strip()

    with open("deps_output.csv", "w", newline="") as fexport:
        writer = csv.writer(fexport)
        with open(output_license_file, "r", newline="") as foutput:
            for row in csv.reader(foutput):
                if len(row) < 4:
                    continue
                repo_output, purl_output, version_output = (
                    row[0].strip(),
                    row[1].strip(),
                    row[2].strip(),
                )
                license = licenses_input.get(purl_output) or "Unknown"
                writer.writerow([repo_output, purl_output, version_output, license])


if __name__ == "__main__":
    cli()
    #get_license()
    #load_csv()
    #merge_csvs()