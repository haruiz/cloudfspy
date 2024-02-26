# Getting started with cloudfspy

`cloudFspy` provides an api based on `pathlib.Path` to access files on cloud storage services. It is a wrapper, similar to `fsspec`, around the `fsspec` library, which provides a common interface to many different file systems. `cloudFspy` is designed to be easy to use and to provide a consistent interface to access files on cloud storage services.This tutorial will show you how to use `cloudFspy` to access files on cloud storage services.

### Downloading and Uploading Files

We start by importing the `GenericPath` class from the `cloudFspy` library. We can then use the `GenericPath` class to access files on cloud storage services.


```python
import cloudfspy
from cloudfspy import GenericPath as Path
```

The `set_cache_folder` and `clear_cache_folder` methods enable the configuration and purging of the cache directory. This directory serves as a temporary storage area for files fetched from the cloud, facilitating efficient access to large files without the need for repeated downloads. Future enhancements will introduce various caching tactics. Presently, our caching approach involves transferring the file to the cache directory for subsequent access. If a file in the cache is more than two days old, it will be re-downloaded. We aim to make this behavior adjustable in upcoming updates.


```python
# set the cache folder
cloudfspy.set_cache_folder("cache")
cloudfspy.clear_cache_folder()
```

**Downloading files**



```python
from_path = Path("gs://gpr-studio-data/Archive.zip")
to_path = Path("/Users/haruiz/Desktop/Archive.zip")

from_path.download_to(to_path)
with open(to_path, "rb") as f:
    data = f.read()
```

    Downloading file: 100%|██████████| 22.5M/22.5M [00:00<00:00, 30.5MiB/s]


**Uploading Files**


```python
from_path = Path("/Users/haruiz/Desktop/Archive.zip")
to_path = Path("gs://gpr-studio-data/Archive.zip")

from_path.upload_to(to_path)
with open(to_path, "rb") as f:
    data = f.read()
```

    Uploading file:  93%|█████████▎| 21.0M/22.5M [00:10<00:00, 2.07MB/s]
    Downloading file: 100%|██████████| 22.5M/22.5M [00:00<00:00, 30.8MiB/s]



```python
cloudfspy.list_cache_folder(max_levels=5)
```

    cache
        - gpr-studio-data
            - Archive.zip


## creating and deleting folders

The `mkdir` and `rmdir` methods are used to create and delete folders, respectively. The `mkdir` method creates a folder at the specified path, while the `rmdir` method deletes the folder at the specified path. 


```python
path = Path("gs://gpr-studio-data/test_folder/")
path.mkdir(exist_ok=True, parents=True)
path.exists()
```




    True




```python
path.rmdir()
path.exists()
```




    False


