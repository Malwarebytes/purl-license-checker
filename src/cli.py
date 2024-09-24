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

