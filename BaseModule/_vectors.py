import numpy
import math


__version__ = 2.5
def check_instance(func):
    def wrapper(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError( "'%s' not supported please use '%s'" % (type(other).__name__, type(self).__name__) )
        return func(self, other)
    return wrapper


def check_instance_v2(*args):
    def function(func):
        def wrapper(self, other):
            if not isinstance(other, (self.__class__, *args)):
                raise TypeError( "'%s' not supported please use '%s' or %s" % (type(other).__name__, type(self).__name__, ", ".join([arg.__name__ for arg in args])) )
            return func(self, other, isinstance(other, self.__class__))
        return wrapper
    return function


Vector = typing.NewType("Vector", Exception)

class ObjectVector:
    """
    A base class representing an object vector with dynamic attributes.

    The `ObjectVector` class allows you to create and manipulate vector objects with dynamic attributes.
    Each attribute represents a component of the vector. The class provides various operations and
    functionalities for working with vectors, such as equality comparison, arithmetic operations, and more.

    Attributes:
    - __dict__ (dict): Dictionary containing the attribute-value pairs of the vector.

    Methods:
    - __init__(self, **kwargs): Initializes the vector object with the specified attribute-value pairs.
    - __str__(self): Returns a string representation of the vector.
    - __repr__(self): Returns a string representation of the vector including its attributes and hash value.
    - __eq__(self, other): Checks if the vector is equal to another vector.
    - __hash__(self): Returns the hash value of the vector.
    - __lt__(self, other): Checks if the vector is less than another vector.
    - __gt__(self, other): Checks if the vector is greater than another vector.
    - __add__(self, other): Performs vector addition with another vector or scalar.
    - __iadd__(self, other): Performs in-place vector addition with another vector or scalar.
    - __sub__(self, other): Performs vector subtraction with another vector or scalar.
    - __isub__(self, other): Performs in-place vector subtraction with another vector or scalar.
    - __mul__(self, other): Performs element-wise multiplication with another vector or scalar.
    - __imul__(self, other): Performs in-place element-wise multiplication with another vector or scalar.
    - __pow__(self, other): Performs element-wise exponentiation with another vector or scalar.
    - __ipow__(self, other): Performs in-place element-wise exponentiation with another vector or scalar.
    - __mod__(self, other): Performs element-wise modulo operation with another vector or scalar.
    - __imod__(self, other): Performs in-place element-wise modulo operation with another vector or scalar.
    - __floordiv__(self, other): Performs element-wise floor division with another vector or scalar.
    - __ifloordiv__(self, other): Performs in-place element-wise floor division with another vector or scalar.
    - __truediv__(self, other): Performs element-wise true division with another vector or scalar.
    - __itruediv__(self, other): Performs in-place element-wise true division with another vector or scalar.
    - __iter__(self): Returns an iterator for the vector.
    - __pos__(self): Returns a new vector with each component's sign unchanged.
    - __neg__(self): Returns a new vector with each component's sign reversed.
    - __abs__(self): Returns a new vector with the absolute values of each component.
    - __round__(self, number): Returns a new vector with each component rounded to the specified number of decimals.
    - __floor__(self): Returns a new vector with each component rounded down to the nearest integer.
    - __ceil__(self): Returns a new vector with each component rounded up to the nearest integer.
    - __trunc__(self): Returns a new vector with each component truncated to the nearest integer.
    - __getattr__(self, tag): Retrieves the values of attributes based on the specified tag(s).
    - totuple(self): Converts the vector to a tuple.
    - tonumpy(self, dtype=numpy.float64): Converts the vector to a NumPy array.
    - copy(self): Creates a copy of the vector.
    - sum(self): Returns the sum of all components in the vector.

    Example usage:
    >>> class Vec3(ObjectVector):
    ...     x: float = 0.0
    ...     y: float = 0.0   
    ...     z: float = 0.0

    >>> vec = Vec3(x=1, y=2, z=3)
    >>> vec
    <module '__main__:Vec3' {'x': 1, 'y': 2, 'z': 3}, hesh=529344867495597451, hex=0x5589c5a36c0558b, combined_hash=783914749563017248>
    >>> vec.sum()
    6
    >>> vec.copy()
    <module '__main__:Vec3' {'x': 1, 'y': 2, 'z': 3}, hesh=529344867495597451, hex=0x5589c5a36c0558b, combined_hash=783914749563017584>
    >>> vec.totuple()
    (1, 2, 3)
    >>> vec.tonumpy()
    array([1., 2., 3.])
    """

    def __new__(cls, *args, **kwargs):
        if len(cls.__annotations__) == 0:
            raise ValueError(f"No annotations to define class fields")

        for key, _type in cls.__annotations__.items():

            if _type not in (float, int):
                raise TypeError(f"Invalid type for field {key}. Only float or int types are allowed.")

        for key in cls.__annotations__:
            if cls.__dict__.get(key, True):
                raise ValueError(f"Please specify a value for the field {key}")
        return super().__new__(cls)
    
    def __init__(self, *args, **kwargs):

        for number, value in enumerate(args):
            setattr(self, list(self.__annotations__.keys())[number], value)

        for key, value in kwargs.items():
            if key not in self.__annotations__:
                raise ValueError(f"Invalid field name: {key}")
            setattr(self, key, value)

    @property
    def __get_array(self) -> dict:
        return {key: getattr(self, key) for key in self.__annotations__}

    def __str__(self) -> str:
        return "<%s %s>" % (
            f"{self.__class__.__module__}:{self.__class__.__name__}",
            self.__get_array
        )
    
    def __repr__(self) -> str:
        return "<module '%s' %s, hesh=%i, hex=%s, combined_hash=%i>" % (
            f"{self.__class__.__module__}:{self.__class__.__name__}", 
            self.__get_array, 
            self.__hash__(), 
            hex( self.__hash__() ), 
            self.combined_hash()
            )
    
    def __len__(self) -> int:
        return len( self.__annotations__ )

    @check_instance
    def __eq__(self, other: Vector) -> bool:
        return all( getattr(self, key) == getattr(other, key) for key in other.__annotations__ )

    def __hash__(self) -> int:
        return hash( self.totuple() )
    
    @check_instance
    def __lt__(self, other: Vector) -> bool:
        return all( getattr(self, key) < getattr(other, key) for key in other.__annotations__ )

    @check_instance
    def __gt__(self, other: Vector) -> bool:
        return all( getattr(self, key) > getattr(other, key) for key in other.__annotations__ )

    @check_instance_v2(int, float)
    def __add__(self, other: "Vector | int | float", is_main_class):
        if is_main_class:
            response = { key: getattr(self, key) + getattr(other, key) for key in other.__annotations__ }
        else:
            response = { key: getattr(self, key) + other for key in self.__annotations__ }
        return self.__class__(**response)
                        
    def __iadd__(self, other: "Vector | int | float"):
        # TODO: Rewriting the code without using that workaround is considered more efficient.
        return self.__add__(other)

    @check_instance_v2(int, float)
    def __sub__(self, other: "Vector | int | float", is_main_class):
        if is_main_class:
            response = { key: getattr(self, key) - getattr(other, key) for key in other.__annotations__ }
        else:
            response = { key: getattr(self, key) - other for key in self.__annotations__ }
        return self.__class__(**response)
    
    def __isub__(self, other: "Vector | int | float"):
        # TODO: Rewriting the code without using that workaround is considered more efficient.
        return self.__sub__(other)
    
    @check_instance_v2(int, float)
    def __mul__(self, other: "Vector | int | float", is_main_class):
        if is_main_class:
            response = { key: getattr(self, key) * getattr(other, key) for key in other.__annotations__ }
        else:
            response = { key: getattr(self, key) * other for key in self.__annotations__ }
        return self.__class__(**response)
    
    def __imul__(self, other: "Vector | int | float"):
        # TODO: Rewriting the code without using that workaround is considered more efficient.
        return self.__mul__(other)

    @check_instance_v2(int, float)
    def __pow__(self, other: "Vector | int | float", is_main_class):
        if is_main_class:
            response = { key: getattr(self, key) ** getattr(other, key) for key in other.__annotations__ }
        else:
            response = { key: getattr(self, key) ** other for key in self.__annotations__ }
        return self.__class__(**response)
    
    def __ipow__(self, other: "Vector | int | float"):
        # TODO: Rewriting the code without using that workaround is considered more efficient.
        return self.__pow__(other)

    @check_instance_v2(int, float)
    def __mod__(self, other: "Vector | int | float", is_main_class):
        if is_main_class:
            response = { key: getattr(self, key) % getattr(other, key) for key in other.__annotations__ }
        else:
            response = { key: getattr(self, key) % other for key in self.__annotations__ }
        return self.__class__(**response)
                        
    def __imod__(self, other: "Vector | int | float"):
        # TODO: Rewriting the code without using that workaround is considered more efficient.
        return self.__mod__(other)

    @check_instance_v2(int, float)
    def __floordiv__(self, other: "Vector | int | float", is_main_class):
        if is_main_class:
            response = { key: getattr(self, key) // getattr(other, key) for key in other.__annotations__ }
        else:
            response = { key: getattr(self, key) // other for key in self.__annotations__ }
        return self.__class__(**response)
    
    def __ifloordiv__(self, other: "Vector | int | float"):
        # TODO: Rewriting the code without using that workaround is considered more efficient.
        return self.__floordiv__(other)

    @check_instance_v2(int, float)
    def __truediv__(self, other: "Vector | int | float", is_main_class):
        if is_main_class:
            response = { key: getattr(self, key) / getattr(other, key) for key in other.__annotations__ }
        else:
            response = { key: getattr(self, key) / other for key in self.__annotations__ }
        return self.__class__(**response)

    def __itruediv__(self, other: "Vector | int | float"):
        # TODO: Rewriting the code without using that workaround is considered more efficient.
        return self.__truediv__(other)
    
    def __iter__(self):
        return iter( self.__get_array.items() )

    def __pos__(self):
        return self.__class__( **{ key: +getattr(self, key) for key in self.__annotations__ } )
    
    def __neg__(self):
        return self.__class__( **{ key: -getattr(self, key) for key in self.__annotations__ } )
    
    def __abs__(self):
        return self.__class__( **{ key: numpy.abs(getattr(self, key)) for key in self.__annotations__ } )
    
    def __round__(self, number: int):
        return self.__class__( **{ key: numpy.round(getattr(self, key), number) for key in self.__annotations__ } )

    def __floor__(self):
        return self.__class__( **{ key: numpy.floor(getattr(self, key)) for key in self.__annotations__ } )

    def __ceil__(self):
        return self.__class__( **{ key: numpy.ceil(getattr(self, key)) for key in self.__annotations__ } )

    def __trunc__(self):
        return self.__class__( **{ key: numpy.trunc(getattr(self, key)) for key in self.__annotations__ } )

    def __getattr__(self, tag) -> tuple | float | int:
        """
        Handle access to non-existent attributes.

        This method is called when an attempt is made to access a non-existent attribute of an object.
        It allows custom logic to be defined for handling such cases.

        Args:
            tag (str): The name of the requested attribute.

        Returns:
            tuple: A tuple containing the values of the attributes corresponding to the characters in `tag`.
            int or float: If `tag` contains only one character.

        Raises:
            ValueError: If any character in `tag` does not exist as an attribute of the object.

        Example:
            >>> vec = vector3d(x=0, y=2, z=1) 
            >>> vec.xz
            (0, 1)
            >>> vec.x
            0
        """

        response: tuple = ()
        for symble in tag:
            if symble not in self.__dict__:
                raise ValueError("Attribute '%s' not found in '%s'." % (
                        symble, self.__class__.__name__
                ))
            response += ( self.__dict__[symble], )
        return response 


    def totuple(self) -> tuple:
        """
        Convert the vector object to a tuple.

        Returns:
            tuple: A tuple representation of the vector.

        Example:
            >>> vec = Vector2D(3, 5)
            >>> vec.totuple()
            (3, 5)
        """
        return tuple( self.__get_array.values() )
    
    def tonumpy(self, dtype = numpy.float64) -> None:
        """
        Convert the vector object to a NumPy array.

        Returns:
            numpy.ndarray: A NumPy array representation of the vector.

        Example:
            >>> vec = Vector2D(3, 5)
            >>> vec.tonumpy()
            array([3, 5])
        """
        return numpy.array(self.totuple(), dtype=dtype)
    
    def copy(self) -> Vector:
        """
        Create a shallow copy of the vector object.

        Returns:
            Vector: A new vector object with the same attribute values.

        Example:
            >>> vec1 = Vector2D(3, 5)
            >>> vec2 = vec1.copy()
            >>> vec2.x
            3
            >>> vec2.y
            5
        """
        return self.__class__(**self.__get_array)
    
    def sum(self) -> float | int:
        """
        Compute the sum of all values in the vector.

        Returns:
            float or int: The sum of all values in the vector.

        Example:
            >>> vec = Vector2D(3, 5)
            >>> vec.sum()
            8
        """
        return sum( self.totuple() )

    def combined_hash(self) -> int:
        """
        Computes a combined hash value for the object using XOR operation.

        Args:
            self: The object for which to compute the combined hash.

        Returns:
            The combined hash value.

        Example:
            >>> vec = Vector(...)
            >>> hash_value = combined_hash(vec)
        """
        return self.__hash__() ^ hash(id(self))



class Vector2D( ObjectVector ):
    x: float = 0.0
    y: float = 0.0

class Vector3D( ObjectVector ):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

class Vector4D( ObjectVector ):
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    w: int   = 1

def resize_vectors(a: Vector, b: Vector) -> tuple[Vector, Vector]:
    """
    Resizes the given vectors to have the same length by adjusting their sizes.
    
    Args:
        a (Vector): The first vector.
        b (Vector): The second vector.
        
    Returns:
        tuple[Vector, Vector]: A tuple containing the resized vectors, where the first element 
        is the vector with adjusted size and the second element is the vector with the original size.
    """
    max_vector, min_vector = (a,b) if len(a) >= len(b) else (b,a)
    return (max_vector.__class__(*min_vector.totuple()), max_vector)

def vec_sum(a: "Vector") -> float | int:
    """
    Compute the sum of all values in the vector.

    Returns:
        float or int: The sum of all values in the vector.
    
    Raises:
        ValueError: If the input `a` is not a Vector or its subclass.

    Example:
        >>> vec = Vector2D(3, 5)
        >>> vec.vec_sum()
        8
    """
    if not issubclass(a.__class__, ObjectVector):
        raise ValueError("a is not a Vector or its subclass")
    
    return sum(a)

def mul(a: "Vector", value: int) -> "Vector":
    """
    Multiply a vector by a scalar value.

    Args:
        a (Vector): The vector to be multiplied.
        value (int): The scalar value to multiply the vector by.

    Returns:
        Vector: The result of multiplying the vector by the scalar value.
    
        Raises:
        ValueError: If the input `a` is not a Vector or its subclass.

    Example:
        >>> vec = Vector(3, 15)
        >>> mul(vec, 5)
        Vector(15, 75)
    """
    if not issubclass(a.__class__, ObjectVector):
        raise ValueError("a is not a Vector or its subclass")

    return a.__class__(**{key: a.__dict__[key]*value for key in a.__dict__})

def sub(a: "Vector", value: int) -> "Vector":
    """
    Divide a vector by a scalar value.

    Args:
        a (Vector): The vector to be divided.
        value (int): The scalar value to divide the vector by.

    Returns:
        Vector: The result of dividing the vector by the scalar value.

    Raises:
        ValueError: If the input `a` is not a Vector or its subclass.

    Example:
        >>> vec = Vector(3, 15)
        >>> sub(vec, 5)
        Vector(0.6, 3.0)
    """
    if not issubclass(a.__class__, ObjectVector):
        raise ValueError("a is not a Vector or its subclass")

    return a.__class__(**{key: a.__dict__[key]/value for key in a.__dict__} )

def dot(a: "Vector", b: "Vector") -> float:
    """
    Compute the dot product of two vectors.

    Args:
        a (Vector): The first vector.
        b (Vector): The second vector.

    Returns:
        float: The dot product of the two vectors.

    Raises:
        ValueError: If the input `a` or `b` is not a Vector or its subclass.

    Example:
        >>> vec1 = Vector(3, 5)
        >>> vec2 = Vector(2, 4)
        >>> dot(vec1, vec2)
        26
    """
    if not all(issubclass(clas.__class__, ObjectVector) for clas in (a, b)):
        raise ValueError("a or b is not a Vector or its subclass")

    a,b = resize_vectors(a, b)
    return sum( a.__dict__[key]*b.__dict__[key] for key in a.__dict__ )



def length(a: "Vector"):
    """
    Compute the length of a vector.

    Args:
        a (Vector): The vector.

    Returns:
        float: The length of the vector.

    Raises:
        ValueError: If the input `a` is not a Vector or its subclass.

    Example:
        >>> vec = Vector(3, 15)
        >>> length(vec)
        15.297058540778355
    """
    if not issubclass(a.__class__, ObjectVector) :
        raise ValueError("a is not a Vector or its subclass")

    return math.sqrt( sum([a.__dict__[key]**2 for key in a.__dict__]) )


def distance(a: "Vector", b: "Vector"):
    """
    Compute the distance between two vectors.

    Args:
        a (Vector): The first vector.
        b (Vector): The second vector.

    Returns:
        float: The distance between the two vectors.
    
    Raises:
        ValueError: If the input `a` or `b` is not a Vector or its subclass.

    Example:
        >>> vec1 = Vector(3, 15)
        >>> vec2 = Vector(0, 0)
        >>> distance(vec1, vec2)
        15.297058540778355
    """

    if not all(issubclass(clas.__class__, ObjectVector) for clas in (a, b)):
        raise ValueError("a or b is not a Vector or its subclass")

    return length(b - a)

def normalize(a: "Vector") -> "Vector":
    """
    Normalize a vector to a length of 1 while maintaining its direction.

    Args:
        a (Vector): The vector to be normalized.

    Returns:
        Vector: The normalized vector.
    
    Raises:
        ValueError: If the input `a` is not a Vector or its subclass.
        ZeroDivisionError: If length `a` is get zero

    Example:
        >>> vec = Vector(10, 0, 6)
        >>> normalize(vec)
        Vector(0.8574929257125441, 0.0, 0.5144957554275265)
    """
    value = length(a)

    if value == 0.0:
        raise ZeroDivisionError(f"division by zero, value length get `{value}` with vector `{a}`")

    return sub(a, value)

def reflect(rd: "Vector", n: "Vector") -> "Vector":
    """
    Compute the reflection of a vector off a surface with a given normal vector.

    Args:
        rd (Vector): The incident vector.
        n (Vector): The surface normal vector.

    Returns:
        Vector: The reflected vector.

    Raises:
        ValueError: If the input `rd` or `n` is not a Vector or its subclass.

    Example:
        >>> incident = Vector(1, 1, 1)
        >>> normal = Vector(0, 1, 0)
        >>> reflect(incident, normal)
        Vector(1, -1, 1)
    """
    if not all(issubclass(clas.__class__, ObjectVector) for clas in (rd, n)):
        raise ValueError("a or b is not a Vector or its subclass")

    return rd - n * (2 * dot(n, rd))

def angle(a: "Vector", b: "Vector") -> float:
    """
        Args:
        a (Vector): The first vector.
        b (Vector): The second vector.

    Returns:
        float: The angle between the two vectors in radians.

    Raises:
        ValueError: If the input `a` or `b` is not a Vector or its subclass.

    Example:
        >>> vec1 = Vector(0, 3)
        >>> vec2 = Vector(4, 6)
        >>> angle(vec1, vec2)
        0.8320502943378437
    """
    if not all(issubclass(clas.__class__, ObjectVector) for clas in (a, b)):
        raise ValueError("a or b is not a Vector or its subclass")
    
    return dot(a, b) / (length(a)*length(b))

def cos(a: "Vector") -> "Vector":
    """
    Compute the cosine of each component of a Vector.

    This function takes a Vector object or its subclass as input and computes the cosine of each component
    of the vector. The resulting vector has the same type as the input vector.

    Args:
        a (Vector): The input vector.

    Returns:
        Vector: A new vector with the cosine of each component.

    Raises:
        ValueError: If the input `a` is not a Vector or its subclass.

    Example:
        >>> v = Vector2D(0.5, 1)
        >>> cos(v)
        Vector2D(x=0.8775825618903728, y=0.5403023058681398)
    """
    if not issubclass(a.__class__, ObjectVector):
        raise ValueError("a is not a Vector or its subclass")
    
    return a.__class__( **{ key: math.cos(a.__dict__[key]) for key in a.__dict__ } )
def sin(a: "Vector") -> "Vector":
    """
    Compute the sine of each component of a Vector.

    This function takes a Vector object or its subclass as input and computes the sine of each component
    of the vector. The resulting vector has the same type as the input vector.

    Args:
        a (Vector): The input vector.

    Returns:
        Vector: A new vector with the sine of each component.

    Raises:
        ValueError: If the input `a` is not a Vector or its subclass.

    Example:
        >>> v = Vector2D(y=1)
        >>> sin(v)
        Vector2D(x=0.479425538604203, y=0.8414709848078965)
    """
    if not issubclass(a.__class__, ObjectVector):
        raise ValueError("a is not a Vector or its subclass")
    
    return a.__class__( **{ key: math.sin(a.__dict__[key]) for key in a.__dict__ } )

def sign_3(a):
    return (0 < a) - (a < 0)
def step_3(edge, x):
    return x > edge

def clamp(value: float, min_: float, max_: float) -> float:
    return max(min(value,max_), min_)

abs3 = lambda a : Vector3D(math.fabs(a.x), math.fabs(a.y), math.fabs(a.z))

sign = lambda a : Vector3D(sign_3(a.x), sign_3(a.y), sign_3(a.z))
step = lambda edge, a : Vector3D(step_3(edge.x, a.x), step_3(edge.y, a.y), step_3(edge.z, a.z))

radians = lambda degrees : (float(degrees) * math.pi) / 180

def radians_in_degrees(radians: float) -> float:
    """
    radians -> degrees
    radians: math.acos
    """
    return ( radians * 180 ) / math.pi

def ListToVector(data: list) -> "None | Vector2D | Vector3D":
    if isinstance(data, list) or isinstance(data, tuple):
        if len(data) == 2:
            return Vector2D(*data)
        elif len(data) == 3:
            return Vector3D(*data)
    return None

# def VectorAngle(angle:float) -> Vector2D:
#     return Vector2D( (WIDTH * math.cos(angle)), 
#                      (WIDTH * math.sin(angle)) )

def cross(a: "Vector3D", b: "Vector3D") -> "Vector3D": 
    return Vector3D(a.y * b.z - a.z * b.y, 
                    a.z * b.x - a.x * b.z, 
                    a.x * b.y - a.y * b.x )


def GetTriangleNormal(a: Vector3D, b: Vector3D, c: Vector3D) -> Vector3D:
    edge1: Vector3D= b - a
    edge2: Vector3D= c - a
    return cross(edge1, edge2)

def sphIntersect(ro: Vector3D, rd: Vector3D, r: int) -> Vector2D:
    b = dot(ro, rd)
    c = dot(ro, ro) - r ** 2
    h = b * b - c
    
    if h < 0.0: return Vector2D(-1)
    
    h = math.sqrt(h)
    return Vector2D(-b - h, -b + h)


# def triIntersect(ro: Vector3D, rd: Vector3D, trangle: Triangle3D):
#     v0, v1, v2 = trangle

#     v1v0 = v1 - v0
#     v2v0 = v2 - v0
#     rov0 = ro - v0
#     n = cross( v1v0, v2v0 )
#     q = cross( rov0, rd )
    
#     rdn = dot( rd, n )
#     d = (1.0 / rdn) if rdn != 0 else 0
#     u = d * dot( -q, v2v0 )
#     v = d * dot(  q, v1v0 )
#     t = d * dot( -n, rov0 )

#     if ( u < 0.0 ) or ( v < 0.0 ) or ( u+v > 1.0 ) : t = -1.0

#     return Vector3D( t, u, v )


def coutVector(a: "Vector", b: "Vector", num: int) -> "True | False":
    return distance(a, b) <= num


