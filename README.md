
# cloudfspy


`cloudfspy` is a Python library that offers a `pathlib`-style interface for interacting with various cloud storage services, including Amazon S3, Azure Blob Storage, and Google Cloud Storage. It provides a simple and consistent API, modeled after the `Path` class from the `pathlib` module, enabling seamless access and manipulation of files and folder in cloud storage. Currently, `cloudfspy` supports the following cloud storage services:

- [x] Google Cloud Storage (GCS)
- [ ] Amazon S3
- [ ] Azure Blob Storage
- [ ] Dropbox
- [ ] OneDrive
- [ ] FTP/SFTP

## Installation

```bash
pip install cloudfspy
```

## Usage

cloudfspy uses a `GenericPath` class that is a subclass of `pathlib.Path`. This class provides a consistent interface for accessing files on cloud storage services.

### Downloading and Uploading Files

```python
from cloudfspy import GenericPath as Path

# Download a file from GCS to a local file
from_path = Path("gs://my-bucket/my-file.txt")
to_path = Path("/path/to/my-file.txt")
from_path.download_to(to_path)

# Upload a local file to GCS
from_path = Path("/path/to/my-file.txt")
to_path = Path("gs://my-bucket/my-file.txt")
from_path.upload_to(to_path)
```

### Working with Directories

```python
from cloudfspy import GenericPath as Path

# Create a directory on GCS
cloud_dir = Path("gs://my-bucket/my-directory")
cloud_dir.mkdir(exist_ok=True, parents=True)

# Iterate over the files in a directory
for file in cloud_dir.iterdir():
    print(file)

# Remove a directory
cloud_dir.rmdir()
```

### Metadata

```python
from cloudfspy import GenericPath as Path

# Get the metadata of a file
cloud_file = Path("gs://my-bucket/my-file.txt")
metadata = cloud_file.metadata

# Set the metadata of a file
cloud_file.metadata = {"description": "My file"}
