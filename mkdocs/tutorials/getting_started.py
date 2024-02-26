#!/usr/bin/env python
# coding: utf-8

# # Getting started with cloudfspy
# 
# `cloudFspy` provides an api based on `pathlib.Path` to access files on cloud storage services. It is a wrapper, similar to `fsspec`, around the `fsspec` library, which provides a common interface to many different file systems. `cloudFspy` is designed to be easy to use and to provide a consistent interface to access files on cloud storage services.This tutorial will show you how to use `cloudFspy` to access files on cloud storage services.
# 
# ### Downloading and Uploading Files
# 
# We start by importing the `GenericPath` class from the `cloudFspy` library. We can then use the `GenericPath` class to access files on cloud storage services.

# In[1]:


import cloudfspy
from cloudfspy import GenericPath as Path


# The `set_cache_folder` and `clear_cache_folder` methods enable the configuration and purging of the cache directory. This directory serves as a temporary storage area for files fetched from the cloud, facilitating efficient access to large files without the need for repeated downloads. Future enhancements will introduce various caching tactics. Presently, our caching approach involves transferring the file to the cache directory for subsequent access. If a file in the cache is more than two days old, it will be re-downloaded. We aim to make this behavior adjustable in upcoming updates.

# In[2]:


# set the cache folder
cloudfspy.set_cache_folder("cache")
cloudfspy.clear_cache_folder()


# **Downloading files**
# 

# In[3]:


from_path = Path("gs://gpr-studio-data/Archive.zip")
to_path = Path("/Users/haruiz/Desktop/Archive.zip")

from_path.download_to(to_path)
with open(to_path, "rb") as f:
    data = f.read()


# **Uploading Files**

# In[4]:


from_path = Path("/Users/haruiz/Desktop/Archive.zip")
to_path = Path("gs://gpr-studio-data/Archive.zip")

from_path.upload_to(to_path)
with open(to_path, "rb") as f:
    data = f.read()


# In[5]:


cloudfspy.list_cache_folder(max_levels=5)

