class MicroSmellerError(Exception):
    """
    A base class from which all other exceptions inherit.
    If you want to catch all errors that the MicroSmeller might raise,
    catch this base exception.
    """


class ImporterError(MicroSmellerError):
    """Exception raised for errors in the Importer module.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class ExporterError(MicroSmellerError):
    pass
    
class MicroToscaError(MicroSmellerError):
    """Exception raised for errors in the Importer module.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

