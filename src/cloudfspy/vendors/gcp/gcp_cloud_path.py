import logging
import mimetypes
from datetime import timedelta
from io import BytesIO
from pathlib import Path

import requests
from tqdm import tqdm

from cloudfspy import CloudPath, CloudPathFactory
from cloudfspy.decorators import gcp_exception

log = logging.getLogger("rich")

try:
    from google.cloud import storage
    from google.cloud.storage import Bucket
    import google.cloud.storage.constants as StorageApiConstants
except ImportError:
    raise ImportError(
        "Please install google-cloud-storage using pip install google-cloud-storage"
    )


@CloudPathFactory.register("gs")
class GCPCloudPath(CloudPath):
    """
    This class creates a GCP CloudFile object from a path.
    """

    def __init__(self, cloud_path: str) -> None:
        """
        Constructor
        :param cloud_path: Cloud path
        """
        super().__init__(cloud_path)

        self._client = storage.Client()

    @property
    def bucket(self):
        """
        Get the bucket name
        :return: Bucket name
        """
        bucket_name = self.uri_parts.netloc
        return self._client.bucket(bucket_name)

    @property
    def blob(self):
        """
        Get the blob name
        :return: Blob name
        """
        bucket = self.bucket
        blob_name = self.uri_parts.path.lstrip("/")
        return bucket.blob(blob_name)

    @property
    def metadata(self):
        """
        Get metadata
        :return: Metadata
        """
        return self.blob.metadata

    @metadata.setter
    def metadata(self, metadata: dict):
        """
        Set metadata
        :param metadata: Metadata
        """
        blob = self.blob
        blob.metadata = metadata
        blob.patch()

    @gcp_exception
    def get_tags(self):
        """
        Get tags
        :return: Tags
        """
        blob = self.blob
        return {
            "etag": blob.etag,
            "size": blob.size,
            "updated": blob.updated,
            "content_type": blob.content_type,
        }

    def _create_bucket(
        self,
        bucket_class=StorageApiConstants.STANDARD_STORAGE_CLASS,
        location="us",
    ):
        """
        this function creates a new bucket in the google cloud storage
        :param bucket_class:
        :return:
        """
        bucket: Bucket = self.bucket
        if bucket.exists():
            return bucket
        bucket.storage_class = bucket_class
        bucket.location = location
        new_bucket = bucket.create()
        return new_bucket

    def _delete_bucket(self):
        """
        this function deletes a bucket from the google cloud storage
        :return:
        """
        bucket: Bucket = self.bucket
        print(bucket.exists())
        if not bucket.exists():
            return
        # List all objects in the bucket and delete each one
        blobs = bucket.list_blobs()
        for blob in blobs:
            blob.delete()
        bucket.delete()

    @gcp_exception
    def exists(self) -> bool:
        """
        Check if the file exists
        :return: True if the file exists, False otherwise
        """

        return self.blob.exists()

    @gcp_exception
    def is_dir(self):
        """
        Check if the path is a directory
        :return: True if the path is a directory, False otherwise
        """
        blob_path = self.uri_parts.path.lstrip("/")
        return blob_path.endswith("/") and self.blob.exists()

    @gcp_exception
    def is_file(self):
        """
        Check if the path is a file
        :return: True if the path is a file, False otherwise
        """
        blob_path = self.uri_parts.path.lstrip("/")
        return not blob_path.endswith("/") and self.blob.exists()

    @gcp_exception
    def mkdir(self, exist_ok: bool = False, parents: bool = False) -> None:
        """
        Create a directory
        :param exist_ok: If True, do not raise an exception if the directory
        already exists
        :param parents: If True, also create any missing parent directories
        :return: None
        """
        bucket = self.bucket
        blob_path = self.uri_parts.path.lstrip("/")
        if not bucket.exists():
            self._create_bucket()
        if blob_path == "":
            return

        assert blob_path.endswith(
            "/"
        ), "you are attempting to create a directory, make sure the path ends with a /"

        blob = self.blob
        # check if the folder has already been created
        if blob.exists():
            if not exist_ok:
                raise FileExistsError(f"Directory exists: {self}")
            return

        blob.upload_from_string(
            "", content_type="application/x-www-form-urlencoded;charset=UTF-8"
        )

    @gcp_exception
    def rmdir(self):
        """
        Remove the directory
        :return: None
        """
        blob_path = self.uri_parts.path.lstrip("/")
        if not self.is_dir():
            raise NotADirectoryError(f"Not a directory: {self}")

        blobs = self.bucket.list_blobs(prefix=blob_path)
        for blob in blobs:
            blob.delete()

    @gcp_exception
    def read_bytes(self) -> bytes:
        """
        Read the file as bytes
        :return: File as bytes
        """
        if self.is_dir():
            raise IsADirectoryError(f"Is a directory: {self}")

        signed_url = self.blob.generate_signed_url(
            version="v4", expiration=timedelta(minutes=15), method="GET"
        )
        response = requests.get(signed_url, stream=True)
        file_size = int(response.headers.get("content-length", 0))
        file_chunk_size = 1024 * 1024 * 10  # 10 MB
        progress_bar = tqdm(
            total=file_size, unit="iB", unit_scale=True, desc="Downloading file"
        )
        with BytesIO() as data_stream:
            for data in response.iter_content(file_chunk_size):
                progress_bar.update(len(data))
                data_stream.write(data)
            progress_bar.close()
            if file_size != 0 and progress_bar.n != file_size:
                raise ValueError("Error in downloading file from GCP")
            return data_stream.getvalue()

    @gcp_exception
    def write_bytes(self, data: bytes):
        """
        Write bytes to a file
        :param data: Data to write
        already exists
        :return: None
        """
        if self.is_dir():
            raise IsADirectoryError(f"Is a directory: {self}")
        blob_content_type = mimetypes.guess_type(str(self))[0]
        signed_url = self.blob.create_resumable_upload_session(
            content_type=blob_content_type, client=self._client
        )
        data_length = len(data)
        file_chunk_size = 1024 * 1024 * 10

        with tqdm(
            total=data_length, unit="B", unit_scale=True, desc="Uploading file"
        ) as progress_bar:

            for i in range(0, data_length, file_chunk_size):
                chunk = data[i : i + file_chunk_size]
                start_byte_index = i
                end_byte_index = i + len(chunk)
                response = requests.put(
                    signed_url,
                    data=chunk,
                    headers={
                        "Content-Type": "application/octet-stream",
                        "Content-Range": f"bytes {start_byte_index}-{end_byte_index - 1}/{data_length}",
                    },
                )
                if response.status_code == 308:
                    progress_bar.update(len(chunk))
                elif response.status_code == 200:
                    # log.info("File uploaded successfully")
                    break

    @gcp_exception
    def iterdir(self):
        """
        Iterate over the directory
        :return: Iterator
        """
        blob_path = self.uri_parts.path.lstrip("/")
        if blob_path == "":
            for blob in self.bucket.list_blobs():
                yield GCPCloudPath(f"gs://{self.uri_parts.netloc}/{blob.name}")

        if not self.is_dir():
            raise NotADirectoryError(f"Not a directory: {self}")

        blob_path = self.uri_parts.path.lstrip("/")
        bucket_name = self.uri_parts.netloc
        for child_blob in self.bucket.list_blobs(prefix=blob_path):
            yield GCPCloudPath(f"gs://{bucket_name}/{child_blob.name}")

    def __fspath__(self):
        """
        Get the file system path
        :return: File system path
        """

        if self.is_dir():
            raise IsADirectoryError(f"Is a directory: {self}")
        self.__check_for_file_in_cache()
        return super().__fspath__()

    def __download_file_to_cache(self):
        """
        Download the file to the cache
        :return:
        """
        # transform the cloud path to a local path
        cloud_file_local_path = Path(self)
        # create the parent directory where the file will be downloaded if it does not exist
        cloud_file_local_path.parent.mkdir(parents=True, exist_ok=True)
        # download the file from the cloud and load it into memory
        cloud_file_bytes = self.read_bytes()
        # write the file to the local path
        with open(cloud_file_local_path, "wb") as file_obj:
            file_obj.write(cloud_file_bytes)

    def __check_for_file_in_cache(self):
        """
        Get or update the cached file, the file is updated if it is older than 1 day
        :return:
        """
        cloud_file_local_path = Path(self)
        cloud_file_is_cached = cloud_file_local_path.exists()
        if cloud_file_is_cached:
            cloud_file_last_modified = cloud_file_local_path.stat().st_mtime
            cloud_file_age = timedelta(seconds=cloud_file_last_modified)
            cloud_file_age_threshold = timedelta(days=1)
            cloud_file_is_outdated = cloud_file_age < cloud_file_age_threshold
            if cloud_file_is_outdated:
                self.__download_file_to_cache()
        else:
            self.__download_file_to_cache()
