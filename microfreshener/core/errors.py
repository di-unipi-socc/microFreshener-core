class MicroFreshenerError(Exception):
    """
    A base class from which all other exceptions inherit.
    If you want to catch all errors that the MicroFreshener might raise,
    catch this base exception.
    """


class ImporterError(MicroFreshenerError):
    """Exception raised for errors in the Importer module.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class YMLImporterError(ImporterError):

    def __init__(self, message):
        super(YMLImporterError, self).__init__(message)


class ExporterError(MicroFreshenerError):
    """Exception raised for errors in the Exporter module.

    Attributes:
        message -- explanation of the error
    """
    pass


class MicroToscaModelError(MicroFreshenerError):
    """Exception raised for errors in the MicroToscaModel module.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class RelationshipNotFoundError(MicroToscaModelError):
    """Exception raised for sel loop rlationship

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super(RelationshipNotFoundError, self).__init__(message)


class SelfLoopMicroToscaModelError(MicroToscaModelError):
    """Exception raised for sel loop rlationship

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super(SelfLoopMicroToscaModelError, self).__init__(message)


class GroupNotFoundError(MicroToscaModelError):
    """Exception raised for sel loop rlationship

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super(GroupNotFoundError, self).__init__(message)


class MultipleEdgeGroupsError(MicroToscaModelError):
    """Exception raised for multiple edge nodes defined in themodel

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        super(MultipleEdgeGroupsError, self).__init__(message)
