from cloudfspy import CloudPathFactory, CloudPath


@CloudPathFactory.register("az")
class AzCloudPath(CloudPath):
    """
    This class creates a Azure CloudFile object from a path.
    """

    def exists(self) -> bool:
        """
        Check if the file exists
        :return: True if the file exists, False otherwise
        """
        pass
