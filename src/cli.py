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
    # Dict formed by {purl: license} entries
    licenses = {}

    # Parse the csv input
    # repo_name, purl, version, license
    with open(path, "r") as f:
        for l in f.readlines():
            line = l.split(",")
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


if __name__ == "__main__":
    #get_license()
    load_csv()