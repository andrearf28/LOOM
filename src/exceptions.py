def GenerateExceptionMessage(code, issuer, reason=''):
    """
    Generate a standardized exception message.

    Parameters
    ----------
    code : int
        Numeric identifier for the exception.
    issuer : str
        The function or module where the exception originated.
    reason : str
        Detailed explanation of what caused the exception.

    Returns
    -------
    str
        Full exception message.
    """
    message = f"{issuer} raised exception #{code}"
    if reason != '':
        message += f": {reason}"
    return message


def handle_missing_data(func):
    """
    Decorator that catches missing parameter errors (KeyError)
    when instantiating analysis classes.

    It re-raises the error with a clearer message to help the user
    understand which required parameter is missing.
    
    Intended for decorating __init__ methods of analysis-related classes:
    
    Example:
        @handle_missing_data
        def __init__(self, ...):
            ...
    """
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyError as e:
            raise KeyError(GenerateExceptionMessage(
                1,
                'handle_missing_data()',
                "Missing required input parameter when instantiating an analysis class. "
                f"Missing key: {str(e)[1:-1]}"
            ))
    return wrapper


# === Base Exception for the LOOM framework ===
class LoomBaseException(Exception):
    """
    Base class for all custom exceptions raised by the LOOM framework.
    All LOOM-specific exceptions should inherit from this.
    """
    pass


# === Specific Exceptions ===
class NoDataInFile(LoomBaseException):
    """
    Raised when the input file is empty, or it contains no valid data 
    (e.g., no optical measurements or improperly formatted lines).
    """
    pass

class IllFormedAnalysisFolder(LoomBaseException):
    """
    Raised when the analysis folder does not contain the required structure,
    such as missing files or directories (e.g., steering.yml, analysis script).
    """
    pass

class IllFormedSteeringFile(LoomBaseException):
    """
    Raised when the steering YAML file does not follow the required format
    or is missing essential fields.
    """
    pass

class IllFormedParametersFile(LoomBaseException):
    """
    Raised when the parameters file is malformed or does not contain valid keys
    required for the analysis.
    """
    pass

class IllFormedAnalysisClass(LoomBaseException):
    """
    Raised when the analysis class does not follow the expected interface or
    is missing required methods such as `execute()` or `get_input_params_model()`.
    """
    pass

class IncompatibleInput(LoomBaseException):
    """
    Raised when provided input parameters are logically incompatible,
    such as mutually exclusive flags being set at the same time.
    """
    pass

class NonExistentDirectory(LoomBaseException):
    """
    Raised when a specified path or folder does not exist on disk.
    """
    pass
