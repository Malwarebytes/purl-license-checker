# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import logging
import time

import requests
from bs4 import BeautifulSoup
from packageurl import PackageURL


def get_license(purl: str, token: str):
    try:
        purlfmt = PackageURL.from_string(purl)
    except ValueError:
        # Invalid purl, try to reformat it.
        try:
            purlfmt = PackageURL.from_string(f"pkg:{purl.replace(':', '/', 1)}")
        except ValueError:
            try:
                purlfmt = PackageURL.from_string(f"pkg:{purl.replace(':', '/', 2)}")  # Maven fixes
            except ValueError:
                return False

    match purlfmt.type:
        case "actions":
            return get_gha_license(purlfmt, token)
        case "go":
            return get_go_license(purlfmt)
        case "composer":
            return get_php_license(purlfmt)
        case "maven":
            return get_maven_license(purlfmt, token)
        case "npm":
            return get_npm_license(purlfmt)
        case "nuget":
            return get_nuget_license(purlfmt)
        case "pypi":
            return get_pip_license(purlfmt)
        case "cargo":
            return get_rust_license(purlfmt)
        case "rubygems":
            return get_ruby_license(purlfmt)
        case "swift":
            return get_swift_license(purlfmt, token)
        case _:
            return False


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

    return _get_github_repo_license(purl_path, token)


def _get_github_repo_license(repo_path: str, token: str):
    """
    Resolve the SPDX license id for a `owner/repo` GitHub repository.
    """
    headers = {
        "accept": "application/vnd.github+json",
        "User-Agent": "malwarebytes/purl-license-checker",
        "X-GitHub-Api-Version": "2022-11-28",  # https://docs.github.com/en/rest/overview/api-versions#supported-api-versions
    }
    if token:
        headers["authorization"] = f"Bearer {token}"

    repo = requests.get(
        url=f"https://api.github.com/repos/{repo_path}",
        headers=headers,
    )

    if repo.status_code != 200:
        logging.warning("GitHub API returned %s for %s", repo.status_code, repo_path)
        return False

    try:
        license = repo.json()["license"]["spdx_id"]
    except (KeyError, TypeError, ValueError):
        return False

    return license

def get_go_license(purlfmt: PackageURL):
    """
    Fetch pkg.go.dev to discover a license

    Ex: https://pkg.go.dev/github.com/juju/errors?tab=licenses
    """
    purl_path = f"{purlfmt.namespace}/{purlfmt.name}"

    headers = {
        "User-Agent": "malwarebytes/purl-license-checker",
    }
    pkg = requests.get(
        url=f"https://pkg.go.dev/{purl_path}?tab=licenses",
        headers=headers,
    )

    if pkg.status_code != 200:
        logging.warning("pkg.go.dev returned %s for %s", pkg.status_code, purl_path)
        return False
    
    try:
        page = BeautifulSoup(pkg.text, "html.parser")
        element = page.select_one("#lic-0")
        if element is None:
            return False
        license = element.get_text(strip=True)
    except Exception as e:
        logging.warning("Failed to parse Go license for %s: %s", purl_path, e)
        return False
    
    return license

def get_maven_license(purlfmt: PackageURL, token: str):
    """
    Fetch maven to discover a license

    Ex: https://central.sonatype.com/artifact/io.github.pen-drive/jet-ads
    """
    purl_path = f"{purlfmt.namespace}/{purlfmt.name}"

    headers = {
        "User-Agent": "malwarebytes/purl-license-checker",
    }
    pkg = requests.get(
        url=f"https://central.sonatype.com/artifact/{purl_path}",
        headers=headers,
    )

    if pkg.status_code != 200:
        logging.warning("central.sonatype.com returned %s for %s", pkg.status_code, purl_path)
        return False
    
    try:
        page = BeautifulSoup(pkg.text, "html.parser")
        element = page.find(attrs={"data-test": "license"})
        if element is None:
            return False
        license = element.get_text(strip=True)
    except Exception as e:
        logging.warning("Failed to parse Maven license for %s: %s", purl_path, e)
        return False
    
    time.sleep(0.5)

    return license


def get_nuget_license(purlfmt: PackageURL):
    """
    Fetch nuget.org to discover a license

    Ex: https://www.nuget.org/packages/Microsoft.CodeDom.Providers.DotNetCompilerPlatform/
    """
    purl_path = f"{purlfmt.name}"

    headers = {
        "User-Agent": "malwarebytes/purl-license-checker",
    }
    pkg = requests.get(
        url=f"https://azuresearch-ussc.nuget.org/query?q={purl_path}",
        headers=headers,
    )

    if pkg.status_code != 200:
        logging.warning("nuget query returned %s for %s", pkg.status_code, purl_path)
        return False
    
    try:
        license = pkg.json()["data"][0]["licenseUrl"]
    except (KeyError, IndexError, TypeError, ValueError) as e:
        logging.warning("Failed to parse Nuget license for %s: %s", purl_path, e)
        return False

    return license

def get_php_license(purlfmt: PackageURL):
    """
    Fetch packagist.org to discover a license

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
        logging.warning("packagist returned %s for %s", pkg.status_code, purl_path)
        return False

    try:
        license = pkg.json()["packages"][purl_path][0]["license"][0]
    except (KeyError, IndexError, TypeError, ValueError) as e:
        logging.warning("Failed to parse PHP license for %s: %s", purl_path, e)
        return False

    return license

def get_ruby_license(purlfmt: PackageURL)-> str:
    """
    Fetch rubygems.org to discover a license

    Ex: https://rubygems.org/api/v1/gems/xcinvoke.json
    """
    purl_path = f"{purlfmt.name}"

    headers = {
        "User-Agent": "malwarebytes/purl-license-checker",
    }
    pkg = requests.get(
        url=f"https://rubygems.org/api/v1/gems/{purl_path}.json",
        headers=headers,
    )

    if pkg.status_code != 200:
        logging.warning("rubygems returned %s for %s", pkg.status_code, purl_path)
        return False

    try:
        license = pkg.json()["licenses"][0]
    except (KeyError, IndexError, TypeError, ValueError) as e:
        logging.warning("Failed to parse Ruby license for %s: %s", purl_path, e)
        return False

    return license

def get_swift_license(purlfmt: PackageURL, token: str):
    """
    Resolve a Swift package license via its GitHub repository.

    Swift purls carry the VCS host in the namespace, e.g.
    `pkg:swift/github.com/Alamofire/Alamofire@5.6.4`, where namespace is
    `github.com/Alamofire` and name is `Alamofire`.
    """
    namespace = purlfmt.namespace or ""
    parts = [p for p in namespace.split("/") if p]

    # Only GitHub-hosted packages can be resolved through the GitHub API.
    if not parts or parts[0] not in ("github.com", "www.github.com"):
        logging.warning("Unsupported Swift host for %s", namespace)
        return False

    owner = parts[1] if len(parts) > 1 else ""
    if not owner or not purlfmt.name:
        return False

    return _get_github_repo_license(f"{owner}/{purlfmt.name}", token)


def get_pip_license(purlfmt: PackageURL):
    """
    Fetch pypi.org to discover a license

    Ex: https://pypi.org/pypi/requests/json
    """
    purl_path = f"{purlfmt.name}"

    headers = {
        "User-Agent": "malwarebytes/purl-license-checker",
    }
    url = f"https://pypi.org/pypi/{purl_path}/json"
    if purlfmt.version:
        url = f"https://pypi.org/pypi/{purl_path}/{purlfmt.version}/json"

    pkg = requests.get(url=url, headers=headers)

    if pkg.status_code != 200:
        logging.warning("pypi returned %s for %s", pkg.status_code, purl_path)
        return False

    try:
        info = pkg.json()["info"]
    except (KeyError, TypeError, ValueError) as e:
        logging.warning("Failed to parse PyPI response for %s: %s", purl_path, e)
        return False

    # Prefer the SPDX expression, then the free-form license field, then
    # fall back to the classifier trove.
    license = info.get("license_expression")
    if license:
        return license

    license = info.get("license")
    # Some packages dump the full license text into this field; keep only
    # short, identifier-like values.
    if license and len(license) <= 64 and "\n" not in license:
        return license

    for classifier in info.get("classifiers", []):
        if classifier.startswith("License :: "):
            return classifier.split(" :: ")[-1].strip()

    return False


def get_npm_license(purlfmt: PackageURL):
    """
    Fetch the npm registry to discover a license

    Ex: https://registry.npmjs.org/express/latest
    """
    # Scoped packages (@scope/name) keep the scope in the purl namespace.
    if purlfmt.namespace:
        purl_path = f"{purlfmt.namespace}/{purlfmt.name}"
    else:
        purl_path = f"{purlfmt.name}"

    version = purlfmt.version or "latest"

    headers = {
        "User-Agent": "malwarebytes/purl-license-checker",
    }
    pkg = requests.get(
        url=f"https://registry.npmjs.org/{purl_path}/{version}",
        headers=headers,
    )

    if pkg.status_code != 200:
        logging.warning("npm registry returned %s for %s", pkg.status_code, purl_path)
        return False

    try:
        data = pkg.json()
    except ValueError as e:
        logging.warning("Failed to parse npm response for %s: %s", purl_path, e)
        return False

    license = data.get("license")

    # Legacy packages use an object or a list of objects:
    # {"license": {"type": "MIT"}} or {"licenses": [{"type": "MIT"}]}.
    if isinstance(license, dict):
        return license.get("type") or False
    if isinstance(license, str) and license:
        return license

    licenses = data.get("licenses")
    if isinstance(licenses, list) and licenses:
        first = licenses[0]
        if isinstance(first, dict):
            return first.get("type") or False

    return False


def get_rust_license(purlfmt: PackageURL):
    """
    Fetch crates.io to discover a license

    Ex: https://crates.io/api/v1/crates/serde/1.0.229
    """
    purl_path = f"{purlfmt.name}"

    headers = {
        "User-Agent": "malwarebytes/purl-license-checker",
    }
    url = f"https://crates.io/api/v1/crates/{purl_path}"
    if purlfmt.version:
        url = f"https://crates.io/api/v1/crates/{purl_path}/{purlfmt.version}"

    pkg = requests.get(url=url, headers=headers)

    if pkg.status_code != 200:
        logging.warning("crates.io returned %s for %s", pkg.status_code, purl_path)
        return False

    try:
        data = pkg.json()
    except ValueError as e:
        logging.warning("Failed to parse crates.io response for %s: %s", purl_path, e)
        return False

    # The versioned endpoint returns {"version": {...}}; the crate endpoint
    # exposes the newest version through {"versions": [{...}]}.
    try:
        if "version" in data:
            return data["version"].get("license") or False
        if data.get("versions"):
            return data["versions"][0].get("license") or False
    except (KeyError, IndexError, TypeError):
        return False

    return False