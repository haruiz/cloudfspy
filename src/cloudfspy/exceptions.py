class CloudFsPyException(Exception):
    """
    Base class for CloudFs
    """


class NotSchemeSupported(CloudFsPyException):
    """
    Exception raised when a cloud provider is not supported.
    """


class InvalidCloudPath(CloudFsPyException):
    """
    Exception raised when a cloud path is invalid.
    """
