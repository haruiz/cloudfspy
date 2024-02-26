import typing
from pathlib import Path
from typing import Dict, Callable
from urllib.parse import urlparse

from .any_path import AnyPath
from .exceptions import NotSchemeSupported
from .settings import get_cache_folder

if typing.TYPE_CHECKING:
    from .local_path import LocalPath


class CloudPathFactory:
    """
    This class creates a CloudFile object from a path.
    """

    registry: Dict[str, AnyPath] = {}

    @classmethod
    def register(cls, key: str) -> Callable:
        """
        Register a file handler class.
        :param key: Key for the file handler class
        :return: File handler class
        """

        def wrapper(wrapped_class: AnyPath) -> AnyPath:
            """
            Register a file handler class
            :param wrapped_class:  File handler class
            :return:
            """
            cls.registry[key] = wrapped_class
            return wrapped_class

        return wrapper

    @classmethod
    def build(cls, key: str) -> AnyPath:
        """
        Build a file handler instance for the given key.
        :param key: Key for the file handler class
        :param kwargs: The keyword arguments to pass to the file
        handler constructor.
        :return: File handler instance
        """
        if key not in cls.registry:
            raise NotSchemeSupported(f"scheme {key} not supported")
        file_handler_class = cls.registry[key]
        return file_handler_class


class CloudPath(AnyPath):
    """
    CloudPath class is a subclass of GenericPath
    """

    def __new__(cls, cloud_path: str, *args, **kwargs):
        """
        Create a CloudPath object from a path.
        :param args: Arguments
        :param kwargs: Keyword arguments
        """
        cloud_path_parts = urlparse(cloud_path)
        path_scheme = cloud_path_parts.scheme
        path_netloc = cloud_path_parts.netloc

        if path_scheme == "":
            raise ValueError("Invalid cloud path")

        cloud_path_cls = CloudPathFactory.build(path_scheme)

        # solve cache path
        # the local path is the cache folder + the netloc + the path

        cache_folder = get_cache_folder()
        local_path = cache_folder.joinpath(
            path_netloc, cloud_path_parts.path.lstrip("/")
        )

        return super().__new__(cloud_path_cls, local_path, *args)

    def __init__(self, cloud_path: str, *args, **kwargs):
        """
        Constructor
        :param args: Arguments
        :param kwargs: Keyword arguments
        """
        super().__init__()

        self.uri = cloud_path
        self.uri_parts = urlparse(cloud_path)

    @property
    def parent(self):
        """
        Get the parent path
        :return: Parent path
        """
        parent_path = Path(self.uri_parts.path).parent
        parent_uri = self.drive + self.uri_parts.netloc + str(parent_path)
        if parent_path == Path("/"):
            raise ValueError("Parent path not found")
        cls = self.__class__
        return cls(parent_uri)

    def joinpath(self, *other):
        """
        Join the path
        :param other: Other path
        :return: New path
        """
        cloud_paths_objects = [self] + [CloudPath(p) for p in other]
        all_same_netloc = all(
            [p.uri_parts.netloc == self.uri_parts.netloc for p in cloud_paths_objects]
        )
        if not all_same_netloc:
            raise ValueError("All paths must have the same netloc")
        local_paths = [Path(p.uri_parts.path) for p in cloud_paths_objects]
        new_path = Path.joinpath(*local_paths)
        new_uri = self.drive + self.uri_parts.netloc + str(new_path)
        cls = self.__class__
        return cls(new_uri)

    @property
    def drive(self):
        """
        Get the GCP drive
        :return: GCP drive
        """
        return self.uri_parts.scheme + "://"

    def download_to(
        self, destination: typing.Union[str, "LocalPath"], *args, **kwargs
    ) -> "LocalPath":
        """
        Download a file to a destination.
        :param destination: Destination path (LocalPath)
        """
        from .local_path import LocalPath

        assert isinstance(
            destination, (str, LocalPath)
        ), "Invalid destination parameter"
        if isinstance(destination, str):
            destination = LocalPath(destination)
        with open(destination, "wb+") as f:
            # read bytes from cloud and write to local
            f.write(self.read_bytes())

        return destination
