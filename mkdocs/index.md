# Cloudfspy

Cloudfspy is a Python package that provides a `pathlib.Path` kind of interface, for working with cloud storage services.
It is designed to be easy to use and to provide a consistent interface for working with different cloud storage
services. Currently `Cloudfspy` supports the following cloud storage services:

- Google Cloud Storage (supported)
- Amazon S3 (coming soon)
- Azure Blob Storage (coming soon)
- Google Drive (coming soon)

## Installation

The package is available on PyPI and can be installed using pip:

```bash
pip install cloudfspy
```

## Prerequisites

- [Python 3.10+](https://www.python.org/downloads/)

## Build the documentation

To build the documentation you need to install the dev dependencies:

```bash
poetry install --with dev
mkdocs build
mkdocs serve -a localhost:8000
```

## Usage

To use the library you need to import it:

```python
import cloudfspy
from cloudfspy import GenericPath as Path

# set the cache folder
cloudfspy.set_cache_folder("cache")
cloudfspy.clear_cache_folder()

from_path = Path("/Users/haruiz/Desktop/Archive.zip")
to_path = Path("gs://gpr-studio-data/Archive.zip")

from_path.upload_to(to_path)
with open(to_path, "rb") as f:
    data = f.read()
```

## Contributing

If you would like to contribute to the project, please contact the maintainers to discuss the changes you would like to
make. We welcome contributions from everyone, and are grateful for even the smallest contributions.