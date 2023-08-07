class BaseVectorError(Exception):
    """Base class for vector-related errors."""

class NoAnnotationsError(BaseVectorError):
    """Error raised when there are no annotations to define class fields.

    This exception is raised when attempting to create a vector class with no annotations
    to define its fields. In Python, annotations are used to specify the data types of
    class attributes, and they are necessary for proper vector initialization. If a vector
    class does not have any annotations, it may lead to unexpected behavior or errors in
    vector operations.

    This class is a subclass of BaseVectorError, which serves as a base class for all
    vector-related errors in this application. By raising NoAnnotationsError or its
    subclasses, the application can handle specific vector-related issues separately,
    allowing for more precise error handling.

    Attributes:
        message (str): A descriptive error message indicating the reason for the exception.
    """

class NameAnnotationsError(BaseVectorError):
    """Error raised when attempting to override essential annotations.

    This exception is raised when someone attempts to override essential annotations
    in a vector class. In Python, certain attributes like '__module__', '__doc__', and
    '__annotations__' are essential for class definition and behavior. Attempting to
    modify or redefine these annotations can lead to unexpected consequences and
    incorrect behavior of the vector class.

    It is essential to preserve these attributes for proper functioning of the class,
    and this error serves as a safeguard against unintended modifications.

    The 'NameAnnotationsError' class is a subclass of 'BaseVectorError', which serves as
    a base class for all vector-related errors in this application. By raising
    'NameAnnotationsError' or its subclasses, the application can handle specific vector-
    related issues separately, allowing for more precise error handling.

    Attributes:
        message (str): A descriptive error message indicating the reason for the exception.
    """
