# purl-license-checker

Retrieve missing licenses for `purl` documented dependencies.


[![CodeQL](https://github.com/Malwarebytes/purl-license-checker/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/Malwarebytes/purl-license-checker/actions/workflows/codeql.yml)
[![CI](https://github.com/Malwarebytes/purl-license-checker/actions/workflows/ruff.yml/badge.svg)](https://github.com/Malwarebytes/purl-license-checker/actions/workflows/ruff.yml)
[![Downloads](https://static.pepy.tech/personalized-badge/purl-license-checker?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/purl-license-checker)
[![Supported Versions](https://img.shields.io/pypi/pyversions/purl-license-checker.svg)](https://pypi.org/project/purl-license-checker)
[![Contributors](https://img.shields.io/github/contributors/malwarebytes/purl-license-checker.svg)](https://github.com/malwarebytes/purl-license-checker/graphs/contributors)


This cli utility takes one or more purl formatted urls from stdin and will try to find the license attached to each of them, by querying various package managers databases.

This is particularly useful to fill GitHub's Dependabot gap of missing 90% of licenses when working at scale with [ghas-cli](https://github.com/Malwarebytes/ghas-cli
) for instance.

## Supported package managers:

- Github Actions ✔️
- Composer✔️
- Go✔️
- Maven✔️
- NPM: 🟠 [wip - see issue](https://github.com/Malwarebytes/purl-license-checker/issues/10)
- Nuget✔️
- Pip: 🟠[wip - see issue](https://github.com/Malwarebytes/purl-license-checker/issues/7)
- Rubygems✔️
- Rust: 🟠 [wip - see issue](https://github.com/Malwarebytes/purl-license-checker/issues/12)
- Swift: 🟠 wip

## Installation

Builds are available in the [`Releases`](https://github.com/Malwarebytes/purl-license-checker/releases) tab and on [Pypi](https://pypi.org/project/purl-license-checker/)

* Pypi:

```bash
pip install purl-license-checker
```

* Manually:

```bash
python -m pip install /full/path/to/purl-license-checker-xxx.whl

# e.g: python3 -m pip install Downloads/purl-license-checker-0.5.0-none-any.whl
```

## Usage

To show the help message for each command, run `purl-license-checker -h`:

```
Usage: purl-license-checker [OPTIONS] COMMAND [ARGS]...

  Retrieve licenses for purl documented dependencies.

  Get help: `@jboursier-mwb` on GitHub

Options:
  --help  Show this message and exit.

Commands:
  get_license
  load_file
  merge_csv
```

### Get a license

```
get_license PURL GITHUB_TOKEN
```

e.g:

```
get_license pip:ghas-cli gh-123456789qwerty
```

### Find licenses for a csv-list of purl dependencies

```
load_file PATH GITHUB_TOKEN
```

e.g:

With a `PATH` csv file formatted as follow:

```csv
repo_name, purl, version, license
```

Where missing licenses are set to `Unknown`, for instance:

```csv
ghas-cli, ghas-cli, com.github.Malwarebytes/ghas-cli,, MIT
ghas-cli, pip:charset-normalizer,3.3.2, MIT
ghas-cli, pip:colorama,0.4.6, BSD-2-Clause AND BSD-3-Clause
ghas-cli, pip:click,8.1.7, BSD-2-Clause AND BSD-3-Clause
ghas-cli, pip:python-magic,0.4.27, MIT
ghas-cli, pip:urllib3,2.2.3, MIT
ghas-cli, pip:requests,2.32.3, Apache-2.0
ghas-cli, pip:configparser,7.1.0, MIT
ghas-cli, pip:certifi,2024.8.30, MPL-2.0
ghas-cli, pip:idna,3.10, BSD-2-Clause AND BSD-3-Clause
ghas-cli, actions:actions/checkout,4.*.*, Unknown
ghas-cli, actions:github/codeql-action/analyze,3.*.*, Unknown
ghas-cli, actions:github/codeql-action/init,3.*.*, Unknown
ghas-cli, actions:actions/dependency-review-action,4.*.*, Unknown
```

`load_file` will do its best to find the licenses for all `Unknown` license fields and will output its results in `output.csv`.

The output format is as follow:

```csv
purl, license
```

For instance:

```csv
npm:unicode-match-property-ecmascript, MIT
npm:unicode-match-property-value-ecmascript, MIT
npm:unicode-property-aliases-ecmascript, MIT
npm:universalify, MIT
npm:unpipe, MIT
npm:use-sync-external-store, MIT
npm:util-deprecate, MIT
npm:utils-merge, MIT
```

### Fill an existing partial csv list of purl licenses
```
merge_csv LICENSES_INPUT_PATH DEPENDENCIES_OUTPUT_PATH GITHUB_TOKEN
```

Allows to fill the unknown dependencies in `DEPENDENCIES_OUTPUT_PATH` formatted as `repo_name, purl, version, license` from `LICENSES_INPUT_PATH` containing only `purl, license`.
Particularly useful with a workflow based on [ghas-cli](https://github.com/Malwarebytes/ghas-cli).

## Development

### Build

[Install uv](https://docs.astral.sh/uv/getting-started/installation/) first, then:

```bash
make dev
```

### Bump the version number

* Bump the version number: `uv version --minor`
* Update the `__version__` field in `src/cli.py` accordingly.

### Publish a new version

**Requires `syft` to be installed to generate the sbom.**

1. Bump the version number as described above
2. `make release` to build the packages
3. `git commit -a -S Bump to version 1.1.2` and `git tag -s v1.1.2 -m "1.1.2"`
4. Upload `dist/*`, `checksums.sha512` and `checksums.sha512.asc` to a new release in GitHub.




# Miscellaneous

This repository is provided as-is and isn't bound to Malwarebytes' SLA.
