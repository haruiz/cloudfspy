import typing

from .any_path import AnyPath

if typing.TYPE_CHECKING:
    from .cloud_path import CloudPath
    from .generic_path import GenericPath


class LocalPath(AnyPath):
    def __init__(self, *args, **kwargs):
        """
        Constructor
        :param args: Arguments
        :param kwargs: Keyword arguments
        """
        super().__init__()

    def exists(self, *args, **kwargs):
        """
        Check if the path exists
        :return:
        """
        return super().exists()

    def upload_to(
        self,
        destination: typing.Union[str, "GenericPath", "CloudPath"],
        *args,
        **kwargs,
    ) -> "CloudPath":
        """
        Upload a file to a destination.
        :param destination: Destination path (CloudPath)
        """
        from .cloud_path import CloudPath

        assert isinstance(
            destination, (str, CloudPath)
        ), "Invalid destination parameter"
        if isinstance(destination, str):
            destination = CloudPath(destination)

        with open(self, "rb") as f:
            # read bytes from local and write to cloud
            destination.write_bytes(f.read())

        metadata = kwargs.get("metadata")
        if metadata is not None and isinstance(metadata, dict):
            destination.metadata = metadata

        return destination
