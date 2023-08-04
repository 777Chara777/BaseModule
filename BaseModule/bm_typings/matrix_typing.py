class BaseMatrixError(Exception):
    """Base class for matrix-related errors."""

class InvalidMatrixSizeError(BaseMatrixError):
    """An error is raised when an invalid matrix size is encountered."""

class InvalidMatrixOperationError(BaseMatrixError):
    """An error that occurs when performing operations on matrices that cannot be implemented due to size mismatches or other restrictions."""

class InvalidMatrixElementError(BaseMatrixError):
    """The error used when selecting or using a matrix element at invalid indices, or when choosing the preferred value of a matrix element."""

class MatrixDimensionError(BaseMatrixError):
    """An error that occurs when performing operations with matrices when their sizes do not meet the requirements of the operation, for example, when trying to multiply matrices, where the number of columns of the first matrix is not equal to the number of rows of the second matrix."""