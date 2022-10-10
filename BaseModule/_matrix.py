from ._vectors import is_eq_class

version = 1.0

class Matrix:
    def __init__(self, m: int=3, n: int=3, **kargs):

        def check() -> tuple:
            array = kargs["array"]

            list_len_numbers = [ len(number) for number in array]

            visited = set()
            dup = [x for x in list_len_numbers if x in visited or (visited.add(x) or False)]

            for num, x in enumerate(list_len_numbers):
                for y in dup:
                    if x != y:
                        return (False, f"{num+1}", f"{y - x}")

            return (True,)

        if "array" in kargs:

            type_bool, *arg = check()

            if type_bool:
                self.__matrix_array = kargs["array"]
            else:
                raise Exception("Matrix is missing {0[0]} character in {0[1]} columns".format(arg))

        else:
            self.__matrix_array = [ [0 for _ in range(m)] for _ in range(n) ]

    def _eq_size(self, other: "Matrix") -> bool:
        main_array  = self.__matrix_array
        other_array =other.__matrix_array
        
        main_len_numbers = sum([ len(number) for number in main_array  ])
        other_len_numbers= sum([ len(number) for number in other_array ])

        if main_len_numbers == other_len_numbers:
            return True
        raise Exception("To add two matrices, they must be the same size.")

    # магические элементы

    @is_eq_class
    def __mul__(self, other: "Matrix"):
        m = len(self.__matrix_array)  # a: m × n
        n = len(other.__matrix_array) # b: n × k
        k = len(other.__matrix_array[0])

        c = Matrix(k,m)

        for i in range(m):
            for j in range(k):       
                c[i][j] = sum(self.__matrix_array[i][kk] * other.__matrix_array[kk][j] for kk in range(n))
        
        return c
    
    def __imul__(self, other: "Matrix"):
        return self.__mul__(other)

    @is_eq_class
    def __truediv__(self, other: "Matrix"):
        m = len(self.__matrix_array)  # a: m / n
        n = len(other.__matrix_array) # b: n / k
        k = len(other.__matrix_array[0])

        c = Matrix(k,m)

        for i in range(m):
            for j in range(k):       
                c[i][j] = sum(self.__matrix_array[i][kk] / other.__matrix_array[kk][j] for kk in range(n))
        
        return c
    
    def __itruediv__(self, other: "Matrix"):
        return self.__truediv__(other)

    @is_eq_class
    def __floordiv__(self, other: "Matrix"):
        m = len(self.__matrix_array)  # a: m / n
        n = len(other.__matrix_array) # b: n / k
        k = len(other.__matrix_array[0])

        c = Matrix(k,m)

        for i in range(m):
            for j in range(k):       
                c[i][j] = sum(self.__matrix_array[i][kk] // other.__matrix_array[kk][j] for kk in range(n))
        
        return c
    
    def __ifloordiv__(self, other):
        return self.__floordiv__(other)

    @is_eq_class
    def __mod__(self, other: "Matrix"):
        m = len(self.__matrix_array)  # a: m / n
        n = len(other.__matrix_array) # b: n / k
        k = len(other.__matrix_array[0])

        c = Matrix(k,m)

        for i in range(m):
            for j in range(k):       
                c[i][j] = sum(self.__matrix_array[i][kk] % other.__matrix_array[kk][j] for kk in range(n))
        
        return c

    def __imod__(self, other: "Matrix"):
        return self.__mod__(other)

    @is_eq_class
    def __add__(self, other: "Matrix"):
        self._eq_size(other)
        m = len(self.__matrix_array    ) # a: m + n
        k = len(other.__matrix_array[0])
        c = Matrix(k,m)
        for i in range(k):
            for x in range(m):
                c[x][i] = self.__matrix_array[x][i] + other.__matrix_array[x][i]        
        return c

    def __iadd__(self, other: "Matrix"):
        return self.__add__(other)

    @is_eq_class
    def __sub__(self, other: "Matrix"):
        self._eq_size(other)
        m = len(self.__matrix_array    ) # a: m + n
        k = len(other.__matrix_array[0])
        c = Matrix(k,m)
        for i in range(k):
            for x in range(m):
                c[x][i] = self.__matrix_array[x][i] - other.__matrix_array[x][i]        
        return c

    def __isub__(self, other: "Matrix"):
        return self.__sub__(other)

    def __repr__(self) -> str:
        return "<Matrix size=%s, array=%s>" % ( f"{len(self.__matrix_array)}x{len(self.__matrix_array[0])}", self.__matrix_array)

    def __str__(self) -> str:
        def fun() -> str:
            message = ""

            len_size_array = len(self.__matrix_array[0])
            len_array = len(self.__matrix_array)

            for number in range(len_size_array):
                for num_stalb in range(len_array):
                    message += f'{self.__matrix_array[num_stalb][number]} '
                message += '\n'

            return message

        return "<Matrix size=%s, array={\n%s}>" % ( f"{len(self.__matrix_array)}x{len(self.__matrix_array[0])}", fun())

    def __getitem__(self, __value):
        return self.__matrix_array[__value]

    # функцыи

    def copy(self) -> "Matrix":
        "copy matrix"
        return Matrix(array=self.__matrix_array)
