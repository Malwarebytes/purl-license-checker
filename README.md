# purl-license-checker

Retrieve licenses for purl documented dependencies.


This cli utility takes one or more purl formatted urls from stdin and will try to find the license attached to each of them, by querying various package managers databases.

This is particularly useful to fill GitHub's Dependabot gap of missing 90% of licenses.



## Installation

Builds are available in the [`Releases`](https://github.com/Malwarebytes/purl-license-checker/releases) tab.

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

`purl-license-checker -h` or see the [wiki](https://github.com/Malwarebytes/purl-license-checker/wiki).

## Development

### Build

[Install Poetry](https://python-poetry.org/docs/#installation) first, then:

```bash
make dev
```

### Bump the version number

* Bump the version number: `poetry version x.x.x`
* Update the `__version__` field in `src/cli.py` accordingly.

### Publish a new version

**Requires `syft` to be installed to generate the sbom.**

1. Bump the version number as described above
2. `make deps` to update the dependencies
3. `make release` to build the packages
4. `git commit -a -S Bump to version 1.1.2` and `git tag -s v1.1.2 -m "1.1.2"`
5. Upload `dist/*`, `checksums.sha512` and `checksums.sha512.asc` to a new release in GitHub.




# Miscellaneous

This repository is provided as-is and isn't bound to Malwarebytes' SLA.