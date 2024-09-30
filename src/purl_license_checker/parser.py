# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from packageurl import PackageURL
import requests

def get_license(purl: str, token: str):
    try:
        purlfmt = PackageURL.from_string(purl)
    except:
        #print("Invalid purl, trying to reformat...")
        try:
            purlfmt = PackageURL.from_string(f"pkg:{purl.replace(':', '/', 1)}")
        except:
            return False

    match purlfmt.type:
        case "actions":
          return get_gha_license(purlfmt, token)
        case "composer":
            return get_php_license(purlfmt)
        case _:
            return False

    return None

def get_pip_license():
    """
    Fetch pypi to discover a license
    """
    return None


def get_gha_license(purlfmt: PackageURL, token: str):
    """
    Fetch GitHub for a license
    """
    # Format purl
    ## Some actions purl are like `cloudposse/actions/github/slash-command-dispatch`, we need to trim it down.
    purl_path = f"{purlfmt.namespace}/{purlfmt.name}"
    if purlfmt.namespace.count('/') == 1:
        purl_path = purlfmt.namespace
    if purlfmt.namespace.count('/') >1:
        purl_path = purlfmt.namespace.split('/')[0] + "/" + purlfmt.namespace.split('/')[1]

    # Fetch license
    headers = {
        "accept": "application/vnd.github+json",
        "authorization": f"Bearer {token}",
        "User-Agent": "malwarebytes/purl-license-checker",
        "X-GitHub-Api-Version": "2022-11-28",  # https://docs.github.com/en/rest/overview/api-versions#supported-api-versions
    }

    repo = requests.get(
        url=f"https://api.github.com/repos/{purl_path}",
        headers=headers,
    )

    if repo.status_code != 200:
        print(repo.status_code)
        return False

    try:
        license = repo.json()["license"]["spdx_id"]
    except Exception as e:
        return False

    return license

def get_php_license(purlfmt: PackageURL):
    """
    Fetch packagists.org to discover a license

    Ex: https://repo.packagist.org/p2/symfony/event-dispatcher-contracts.json
    """
    purl_path = f"{purlfmt.namespace}/{purlfmt.name}"

    headers = {
        "User-Agent": "malwarebytes/purl-license-checker",
    }
    pkg = requests.get(
        url=f"https://repo.packagist.org/p2/{purl_path}.json",
        headers=headers,
    )

    if pkg.status_code != 200:
        print(pkg.status_code)
        return False

    try:
        license = pkg.json()["packages"][purl_path][0]["license"][0]
    except Exception as e:
        return False

    return license

def get_swift_license():
    """
    Fetch GitHub to discover a license
    """
    return None

def get_go_license():
    """
    Fetch golang.org to discover a license
    """
    return None