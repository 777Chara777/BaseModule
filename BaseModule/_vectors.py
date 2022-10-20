version = 1.0

import math

def is_eq_class(func):
    def wrepper(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError( "'%s' not supported please use '%s'" % (type(other).__name__, type(self).__name__) )
        
        return func(self, other)
    return wrepper

# def for_data(func, other, if_ = (lambda a : True)) -> list:
#     return [ func(key) for key in other if if_(key) ]

class _ObjectVector:
    def __init__(self, **kargs) -> None:
        self.__dict__ = kargs

    def __str__(self) -> str:
        FormMessage = [ f"{key}={self.__dict__[key]}" for key in self.__dict__ ]
        return "<%s {%s}>" % (type(self).__name__, ", ".join(FormMessage))

    def __repr__(self) -> str:
        return "<module '%s' %s>" % (type(self).__name__, self.__dict__)
    
    @is_eq_class
    def __eq__(self, __o: "_ObjectVector") -> bool:
        for key in __o.__dict__:
            if key in self.__dict__ and str(__o.__dict__[key]) != str(self.__dict__[key]):
                return False
        return True

    def __hesh__(self):
        return hash(self.__dict__)

    @is_eq_class
    def __lt__(self, other: "_ObjectVector"):
        type_and = [ self.__dict__[key] < other.__dict__[key] for key in other.__dict__ if key in self.__dict__ ]
        if True in type_and:
            return True
        return False

    @is_eq_class
    def __gt__(self, other: "_ObjectVector"):
        type_and = [ self.__dict__[key] > other.__dict__[key] for key in other.__dict__ if key in self.__dict__ ]
        if True in type_and:
            return True
        return False

    @is_eq_class
    def __add__(self, other: "_ObjectVector"):
        response = { key: self.__dict__[key] + other.__dict__[key] for key in other.__dict__ if key in self.__dict__ }
        return self.__class__(**response)
                        
    def __iadd__(self, other: "_ObjectVector"):
        return self.__add__(other)

    @is_eq_class
    def __sub__(self, other: "_ObjectVector"):
        response = { key: self.__dict__[key] - other.__dict__[key] for key in other.__dict__ if key in self.__dict__ }
        return self.__class__(**response)
    
    def __isub__(self, other: "_ObjectVector"):
        return self.__sub__(other)
    
    @is_eq_class
    def __mul__(self, other: "_ObjectVector"):
        response = { key: self.__dict__[key] * other.__dict__[key] for key in other.__dict__ if key in self.__dict__ }
        return self.__class__(**response)
    
    def __imul__(self, other: "_ObjectVector"):
        return self.__mul__(other)

    @is_eq_class
    def __mod__(self, other: "_ObjectVector"):
        response = { key: self.__dict__[key] % other.__dict__[key] for key in other.__dict__ if key in self.__dict__ }
        return self.__class__(**response)
                        
    def __imod__(self, other: "_ObjectVector"):
        return self.__mod__(other)

    @is_eq_class
    def __floordiv__(self, other: "_ObjectVector"):
        response = { key: self.__dict__[key] // other.__dict__[key] for key in other.__dict__ if key in self.__dict__ }
        return self.__class__(**response)
    
    def __ifloordiv__(self, other: "_ObjectVector"):
        return self.__floordiv__(other)

    @is_eq_class
    def __truediv__(self, other: "_ObjectVector"):
        response = { key: self.__dict__[key] / other.__dict__[key] for key in other.__dict__ if key in self.__dict__ }
        return self.__class__(**response)

    def __itruediv__(self, other: "_ObjectVector"):
        return self.__truediv__(other)

    def copy(self):
        "copy vector"
        return self.__class__(**self.__dict__)

    def muls(self, value: int) -> None:
        "mul vector on value"
        for key in self.__dict__: self.__dict__[key] *= value

    def subs(self, value: int) -> None:
        "sub vector on value"
        for key in self.__dict__: self.__dict__[key] /= value


class Vector2D(_ObjectVector):
    def __init__(self, x=0.0, y=0.0) -> None:
        super().__init__(x=x, y=y)

class Vector3D(_ObjectVector):
    def __init__(self, x=0.0, y=0.0, z=0.0) -> None:
        super().__init__(x=x, y=y, z=z)

class Vector4D(_ObjectVector):
    def __init__(self, x=0.0, y=0.0, z=0.0, w=1) -> None:
        super().__init__(x=x, y=y, z=z, w=w)


summ = lambda a: int(a.x+a.y)

def mulS(a: "Vector3D | Vector2D", value: int) -> "Vector3D | Vector2D":
    if isinstance(a, Vector2D): return Vector2D(a.x*value, a.y*value)
    elif isinstance(a, Vector3D): return Vector3D(a.x*value, a.y*value, a.z*value)

def mulS_sub(a: "Vector3D | Vector2D", value: int) -> "Vector3D | Vector2D":
    if isinstance(a, Vector2D): return Vector2D(a.x/value, a.y/value)
    elif isinstance(a, Vector3D): return Vector3D(a.x/value, a.y/value, a.z/value)

def dot(a: "Vector3D | Vector2D", b: "Vector3D | Vector2D") -> int:
    if isinstance(a, Vector2D) and isinstance(b, Vector2D): return a.x*b.x + a.y*b.y
    elif isinstance(a, Vector3D) and isinstance(b, Vector3D): return a.x*b.x + a.y*b.y + a.z*b.z

def length(a: "Vector3D | Vector2D"):
    if isinstance(a, Vector2D): return math.sqrt(a.x**2 + a.y**2)
    elif isinstance(a, Vector3D): return math.sqrt(a.x**2 + a.y**2 + a.z**2)

def normalize(a: "Vector3D | Vector2D") -> "Vector2D | Vector3D":
    return mulS(a, 1 / length(a))

def reflect(rd: "Vector3D | Vector2D", n: "Vector3D | Vector2D") -> "Vector3D | Vector2D":
    return rd - mulS(n, 2 * dot(n, rd))


def sign_3(a):
    return (0 < a) - (a < 0)
def step_3(edge, x):
    return x > edge


abs3 = lambda a : Vector3D(math.fabs(a.x), math.fabs(a.y), math.fabs(a.z))

sign = lambda a : Vector3D(sign_3(a.x), sign_3(a.y), sign_3(a.z))
step = lambda edge, a : Vector3D(step_3(edge.x, a.x), step_3(edge.y, a.y), step_3(edge.z, a.z))

radians = lambda degrees : (float(degrees) * math.pi) / 180

def ListToVector(data: list) -> "None | Vector2D | Vector3D":
    if isinstance(data, list) or isinstance(data, tuple):
        if len(data) == 2:
            x, y    = (x for x in data)
            return Vector2D(x,y)
        elif len(data) == 3:
            x, y, z = (x for x in data)
            return Vector3D(x,y,z)
    
    return None

# def VectorAngle(angle:float) -> Vector2D:
#     return Vector2D( (WIDTH * math.cos(angle)), 
#                      (WIDTH * math.sin(angle)) )

def cross(a: Vector3D, b: Vector3D) -> Vector3D: 
    return Vector3D( a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x )

def GetTriangleNormal(a: Vector3D, b: Vector3D, c: Vector3D) -> Vector3D:
    edge1: Vector3D= b - a
    edge2: Vector3D= c - a
    return cross(edge1, edge2)

# def sphInersect(ro, rd, ra) -> list:
#     b = dot3(ro,rd)
#     c = dot3(ro,ro) - ra * ra
#     h = b * b - c
#     if h < 0.0:
#         return Vector2D(-1.0,-1.0)
#     h = math.sqrt(h)
#     return Vector2D(-b - h, -b + h)


def coutVector(a:Vector2D,b:Vector2D, num:int) -> "True | False":
    d = math.sqrt( (a.x-b.x)**2 + (a.y-b.y)**2 )

    return True if d <= num else False

def coutVector(a: "Vector3D | Vector2D", b: "Vector3D | Vector2D"):
    if isinstance(a, Vector2D) and isinstance(b, Vector2D): return math.sqrt( (a.x-b.x)**2 + (a.y-b.y)**2 )
    elif isinstance(a, Vector3D) and isinstance(b, Vector3D): return math.sqrt( (a.x-b.x)**2 + (a.y-b.y)**2, + (a.z-b.z)**2 )