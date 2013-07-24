#PyjsArray - Copyright (C) 2013 James Garnon

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#PyjsArray version 0.5
#Project Site: http://gatc.ca

from __pyjamas__ import JS


class PyTypedArray:

    """
    PyTypedArray is the base class that wraps the JavaScript TypedArray objects.
    The derived objects provides an interface to the JavaScript array objects:
        PyUint8ClampedArray     [Uint8ClampedArray]
        PyUint8Array            [Uint8Array]
        PyUint16Array           [Uint16Array]
        PyUint32Array           [Uint32Array]
        PyInt8Array             [Int8Array]
        PyInt16Array            [Int16Array]
        PyInt32Array            [Int32Array]
        PyFloat32Array          [Float32Array]
        PyFloat64Array          [Float64Array]
     The PyTypedArray interface include index syntax, iteration, and math operations.
     The module contains an Ndarray class to instantiate N-dimensional arrays, and PyImageData and PyImageMatrix classes that provide an interface to canvas ImageData.
    """

    def __init__(self, data=None, offset=None, length=None, typedarray=None):
        """
        The PyTypedArray is instantiated with either the array size, an array of the TypedArray or Python type, or an existing ArrayBuffer to view, which creates a new TypedArray of size and included data as the specified type. Optional arguments include offset index at which ArrayBuffer data is inserted and length of an ArrayBuffer.
        """
        if data:
            if isinstance(data, int):
                self.__data = typedarray(float(data))
            elif isinstance(data, (list,tuple)):
                data = [float(dat) for dat in data]
                self.__data = typedarray(data.getArray())
            elif isinstance(data, PyTypedArray):
                self.__data = typedarray(data.__data)
            else:   #TypedArray or ArrayBuffer
                if offset is None and length is None:
                    self.__data = typedarray(data)
                else:
                    if offset is None:
                        offset = 0
                    if length is None:
                        self.__data = typedarray(data, offset)
                    else:
                        self.__data = typedarray(data, offset, length)
        else:
            self.__data = None

    def __str__(self):
        """
        Return string representation of PyTypedArray object.
        """
        return self.__data.toString()

    def __iter__(self):
        """
        Iterate over PyTypedArray object.
        """
        index = 0
        while index < self.__data.length:
            yield self[index]
            index += 1

    def __getitem__(self, index):
        """
        Get TypedArray element by index.
        """
        return JS("""@{{int}}(@{{self}}['__data'][@{{index}}]);""")

    def __setitem__(self, index, value):
        """
        Set TypedArray element by index.
        """
        value = float(value)
        JS("""@{{self}}['__data'][@{{index}}]=@{{value}};""")
        return None

    def __len__(self):
        """
        Get TypedArray array length.
        """
        return self.__data.length

    def set(self, data, offset=0):
        """
        Set data to the array. Arguments: data is a list of either the TypedArray or Python type, offset is the start index where data will be set (defaults to 0).
        """
        if isinstance(data, (list,tuple)):
            data = [float(dat) for dat in data]
            data = data.getArray()
            self.__data.set(data, offset)
        elif isinstance(data, PyTypedArray):
            self.__data.set(data.__data, offset)

    def subarray(self, begin, end=None):
        """
        Retrieve a subarray of the array. The subarray is a TypedArray and is a view of the derived array. Arguments begin and optional end (defaults to array end) are the index spanning the subarray.
        """
        if end is None:
            end = self.__data.length
        array = self.__data.subarray(begin, end)
        pytypedarray = self.__class__()
        pytypedarray.__data = array
        return pytypedarray

    def getLength(self):
        """
        Return array.length attribute.
        """
        return self.__data.length

    def getByteLength(self):
        """
        Return array.byteLength attribute.
        """
        return self.__data.byteLength

    def getBuffer(self):
        """
        Return array.buffer attribute.
        """
        return self.__data.buffer

    def getByteOffset(self):
        """
        Return array.byteOffset attribute.
        """
        return self.__data.byteOffset

    def getBytesPerElement(self):
        """
        Return array.BYTES_PER_ELEMENT attribute.
        """
        return self.__data.BYTES_PER_ELEMENT

    def getArray(self):
        """
        Return JavaScript TypedArray.
        """
        return self.__data

    def setArray(self, array):
        """
        Set JavaScript TypedArray.
        """
        self.__data = array
        return None


class PyUint8ClampedArray(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint8ClampedArray.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Uint8ClampedArray)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class PyUint8Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint8Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Uint8Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class PyUint16Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint16Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Uint16Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class PyUint32Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Uint32Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Uint32Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class PyInt8Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Int8Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Int8Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class PyInt16Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Int16Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Int16Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class PyInt32Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Int32Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Int32Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise


class PyFloat32Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Float32Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Float32Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise

    def __getitem__(self, index):
        """
        Get TypedArray element by index.
        """
        return JS("""@{{self}}['__data'][@{{index}}];""")


class PyFloat64Array(PyTypedArray):
    """
    Create a PyTypedArray interface to Float64Array.
    """

    def __init__(self, data=None, offset=None, length=None):
        try:
            PyTypedArray.__init__(self, data, offset, length, typedarray=Float64Array)
        except AttributeError:
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise

    def __getitem__(self, index):
        """
        Get TypedArray element by index.
        """
        return JS("""@{{self}}['__data'][@{{index}}];""")


class Ndarray:

    __typedarray = {0: PyUint8ClampedArray,
                    1: PyUint8Array,
                    2: PyUint16Array,
                    3: PyUint32Array,
                    4: PyInt8Array,
                    5: PyInt16Array,
                    6: PyInt32Array,
                    7: PyFloat32Array,
                    8: PyFloat64Array}

    def __init__(self, dim, dtype=8):
        """
        Generate an N-dimensional array of TypedArray data.
        Argument can be size (int or tuple) or data (list or TypedArray).
        Optional argument dtype (default:8) specifies TypedArray data type:
            0: Uint8ClampedArray
            1: Uint8Array
            2: Uint16Array
            3: Uint32Array
            4: Int8Array
            5: Int16Array
            6: Int32Array
            7: Float32Array
            8: Float64Array
        """
        self._dtype = dtype
        if isinstance(dim, tuple):
            size = 1
            for i in dim:
                size *= i
            self.__data = Ndarray.__typedarray[dtype](size)
            self._shape = dim
            indices = []
            for i in self._shape:
                size /= i
                indices.append(size)
            self._indices = tuple(indices)
        elif isinstance(dim, int):
            self.__data = Ndarray.__typedarray[dtype](dim)
            self._shape = (dim,)
            self._indices = (self._shape[0],)
        elif isinstance(dim, list):
            self.__data = Ndarray.__typedarray[dtype](dim)
            self._shape = (len(dim),)
            self._indices = (self._shape[0],)
        else:
            self.__data = dim
            self._shape = (len(dim),)
            self._indices = (self._shape[0],)

    @property
    def shape(self):        #not implemented in pyjs -O
        """
        Return array shape.
        Ndarray.shape accessible with compilation in --strict mode.
        """
        return self._shape

    @shape.setter
    def shape(self, dim):    #not implemented in pyjs -O
        """
        Set shape of array.
        Argument is new shape.
        Raises TypeError if shape is not appropriate.
        Ndarray.shape accessible with compilation in --strict mode.
        """
        self.setshape(dim)
        return None

    def __getitem__(self, index):
        try:
            indexLn, shapeLn = index.__len__(), len(self._shape)    #len(0) no exception
            if indexLn == shapeLn:
                return self.__data[sum([index[i]*self._indices[i] for i in range(indexLn)])]
            else:
                begin = sum([index[i]*self._indices[i] for i in range(indexLn)])
                end = begin + self._indices[indexLn-1]
                subarray = self.__data.subarray(begin, end)
                array = Ndarray(subarray, self._dtype)
                array._shape = self._shape[indexLn:]
                array._indices = self._indices[indexLn:]
                return array
        except (TypeError,AttributeError):  #index[i] if index is int raises both AttributeError -S and TypeError -O. No exception for len(index) if index is int.
            if len(self._shape) == 1:
                return self.__data[index]
            else:
                begin = index * self._indices[0]
                end = begin + self._indices[0]
                subarray = self.__data.subarray(begin, end)
                array = Ndarray(subarray, self._dtype)
                array._shape = self._shape[1:]
                array._indices = self._indices[1:]
                return array

    def __setitem__(self, index, value):
        def unpack(obj, lst=None):
            if lst is None:
                lst = []
            for element in obj:
                if isinstance(element, (list,tuple)):
                    unpack(element, lst)
                else:
                    lst.append(element)
            return lst
        try:
            indexLn, shapeLn = index.__len__(), len(self._shape)
            if indexLn == shapeLn:
                self.__data[sum([index[i]*self._indices[i] for i in range(indexLn)])] = value
            else:
                begin = sum([index[i]*self._indices[i] for i in range(indexLn)])
                end = begin + self._indices[indexLn-1]
                subarray = self.__data.subarray(begin, end)
                if isinstance(value, Ndarray):
                    value = value.__data
                else:
                    if isinstance(value[0], (list,tuple)):
                        value = unpack(value)
                subarray.set(value)
        except (TypeError,AttributeError):
            if len(self._shape) == 1:
                self.__data[index] = value
            else:
                begin = index * self._indices[0]
                end = begin + self._indices[0]
                subarray = self.__data.subarray(begin, end)
                if isinstance(value, Ndarray):
                    value = value.__data
                else:
                    if isinstance(value[0], (list,tuple)):
                        value = unpack(value)
                subarray.set(value)
        return None

    def __iter__(self):
        if len(self._shape) > 1:
            index = 0
            while index < self._shape[0]:
                begin = index * self._indices[0]
                end = begin + self._indices[0]
                subarray = self.__data.subarray(begin, end)
                array = Ndarray(subarray, self._dtype)
                array._shape = self._shape[1:]
                array._indices = self._indices[1:]
                yield array
                index += 1
        else:
            index = 0
            while index < self._shape[0]:
                yield self.__data[index]
                index += 1

    def __str__(self):
        def array_str(array, width, strval):
            alst = []
            if len(array._shape) == 1:
                alst.append('[')
                alst.extend([strval % (width,val) for val in array])
#                    alst.extend(["{0:>{1}} ".format(val,width) for val in array])
                    #pyjs-O {0:>{1}} width > NaN?
                alst[-1] = alst[-1].rstrip()
                alst.append(']')
            else:
                alst.append('[')
                for a in array:
                    alst.extend( array_str(a,width,strval) )
                alst.append(']')
            return alst
        if self._dtype < 7:
            alst = array_str(self, len(str( max([i for i in self.__data]) )), "%*d ")
        else:
            alst = array_str(self, len(str( max([i for i in self.__data]) ))+7, "%*f ")
        tab = len(self._shape)
        i = tab
        while True:
            try:
                i = alst.index('[', i)
            except ValueError:
                break
            count = 0
            while True:
                if alst[i+count] == '[':
                    count += 1
                    continue
                else:
                    if count == 1:      #pyjs-O ' '*n > NaN
                        alst[i] = '\n'+''.join([' ' for x in range(tab-count)])+alst[i]
                    else:
                        alst[i] = '\n\n'+''.join([' ' for x in range(tab-count)])+alst[i]
                    i += count
                    break
        return ''.join(alst)

    def __len__(self):
        return self._shape[0]

    def __add__(self, other):
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] + other
        except (TypeError, ValueError):      #pys -S TypeError, -O ValueError
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] + other.__data[i]
        return ndarray

    def __sub__(self, other):
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] - other
        except (TypeError, ValueError):
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] - other.__data[i]
        return ndarray

    def __mul__(self, other):
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] * other
        except (TypeError, ValueError):
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] * other.__data[i]
        return ndarray

    def __div__(self, other):
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] / other
        except (TypeError, ValueError):
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] / other.__data[i]
        return ndarray

    def add(self, other):
        """
        Add across array elements.
        Argument is a numeral or another array.
        Return new array.
        """
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] + other
        except (TypeError, ValueError):
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] + other.__data[i]
        return ndarray

    def sub(self, other):
        """
        Subtract across array elements.
        Argument is a numeral or another array.
        Return new array.
        """
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] - other
        except (TypeError, ValueError):
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] - other.__data[i]
        return ndarray

    def mul(self, other):
        """
        Multiply across array elements.
        Argument is a numeral or another array.
        Return new array.
        """
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] * other
        except (TypeError, ValueError):
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] * other.__data[i]
        return ndarray

    def div(self, other):
        """
        Divide across array elements.
        Argument is a numeral or another array.
        Return new array.
        """
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] / other
        except (TypeError, ValueError):
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] / other.__data[i]
        return ndarray

    def iadd(self, other):
        """
        Add across array elements in-place.
        Argument is a numeral or another array.
        """
        try:
            for i in xrange(len(self.__data)):
                self.__data[i] = self.__data[i] + other
        except (TypeError, ValueError):
            if self._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(self.__data)):
                    self.__data[i] = self.__data[i] + other.__data[i]
        return None

    def isub(self, other):
        """
        Subtract across array elements in-place.
        Argument is a numeral or another array.
        """
        try:
            for i in xrange(len(self.__data)):
                self.__data[i] = self.__data[i] - other
        except (TypeError, ValueError):
            if self._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(self.__data)):
                    self.__data[i] = self.__data[i] - other.__data[i]
        return None

    def imul(self, other):
        """
        Multiply across array elements in-place.
        Argument is a numeral or another array.
        """
        try:
            for i in xrange(len(self.__data)):
                self.__data[i] = self.__data[i] * other
        except (TypeError, ValueError):
            if self._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(self.__data)):
                    self.__data[i] = self.__data[i] * other.__data[i]
        return None

    def idiv(self, other):
        """
        Divide across array elements in-place.
        Argument is a numeral or another array.
        """
        try:
            for i in xrange(len(self.__data)):
                self.__data[i] = self.__data[i] / other
        except (TypeError, ValueError):
            if self._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(self.__data)):
                    self.__data[i] = self.__data[i] / other.__data[i]
        return None

    def bitwise_and(self, other):
        """
        Bitwise AND across array elements.
        Argument is a numeral or another array.
        Return new array.
        """
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] & other
        except (TypeError, ValueError):
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] & other.__data[i]
        return ndarray

    def bitwise_or(self, other):
        """
        Bitwise OR across array elements.
        Argument is a numeral or another array.
        Return new array.
        """
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] | other
        except (TypeError, ValueError):
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] | other.__data[i]
        return ndarray

    def bitwise_xor(self, other):
        """
        Bitwise XOR across array elements.
        Argument is a numeral or another array.
        Return new array.
        """
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        try:
            for i in xrange(len(ndarray.__data)):
                ndarray.__data[i] = ndarray.__data[i] ^ other
        except (TypeError, ValueError):
            if ndarray._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(ndarray.__data)):
                    ndarray.__data[i] = ndarray.__data[i] ^ other.__data[i]
        return ndarray

    def bitwise_iand(self, other):
        """
        Bitwise AND across array elements in-place.
        Argument is a numeral or another array.
        """
        try:
            for i in xrange(len(self.__data)):
                self.__data[i] = self.__data[i] & other
        except (TypeError, ValueError):
            if self._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(self.__data)):
                    self.__data[i] = self.__data[i] & other.__data[i]
        return None

    def bitwise_ior(self, other):
        """
        Bitwise OR across array elements in-place.
        Argument is a numeral or another array.
        """
        try:
            for i in xrange(len(self.__data)):
                self.__data[i] = self.__data[i] | other
        except (TypeError, ValueError):
            if self._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(self.__data)):
                    self.__data[i] = self.__data[i] | other.__data[i]
        return None

    def bitwise_ixor(self, other):
        """
        Bitwise XOR across array elements in-place.
        Argument is a numeral or another array.
        """
        try:
            for i in xrange(len(self.__data)):
                self.__data[i] = self.__data[i] ^ other
        except (TypeError, ValueError):
            if self._shape != other._shape:
                raise TypeError("array shapes are not compatible")
            else:
                for i in xrange(len(self.__data)):
                    self.__data[i] = self.__data[i] ^ other.__data[i]
        return None

    def bitwise_not(self):
        """
        Bitwise NOT across array elements.
        Return new array.
        """
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        for i in xrange(len(ndarray.__data)):
            ndarray.__data[i] = ~self.__data[i]
        return ndarray

    def setshape(self, *dim):
        """
        Set shape of array.
        Argument is new shape.
        Raises TypeError if shape is not appropriate.
        Ndarray.shape accessible with compilation in --strict mode.
        """
        if isinstance(dim[0], tuple):
            dim = dim[0]
        size = 1
        for i in dim:
            size *= i
        array_size = 1
        for i in self._shape:
            array_size *= i
        if size != array_size:
            raise TypeError("array size cannot change")
        self._shape = dim
        indices = []
        for i in self._shape:
            size /= i
            indices.append(size)
        self._indices = tuple(indices)
        return None

    def getshape(self):
        """
        Return array shape.
        Ndarray.shape accessible with compilation in --strict mode.
        """
        return self._shape

    def reshape(self, dim):
        """
        Return view of array with new shape.
        Argument is new shape.
        Raises TypeError if shape is not appropriate.
        """
        size = 1
        for i in dim:
            size *= i
        array_size = 1
        for i in self._shape:
            array_size *= i
        if size != array_size:
            raise TypeError("array size cannot change")
        subarray = self.__data.subarray(0)
        array = Ndarray(subarray)
        array._shape = dim
        indices = []
        for i in array._shape:
            size /= i
            indices.append(size)
        array._indices = tuple(indices)
        return array

    def fill(self, value):
        """
        Set array elements to value argument.
        """
        value = float(value)
        for index in xrange(len(self.__data)):
            self.__data[index] = value
        return None

    def copy(self):
        """
        Return copy of array.
        """
        array = Ndarray.__typedarray[self._dtype](self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        return ndarray

    def astype(self, dtype):
        """
        Return copy of array.
        Argument dtype is TypedArray data type.
        """
        array = Ndarray.__typedarray[dtype](self.__data)
        ndarray = Ndarray(array, dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        return ndarray

    def view(self):
        """
        Return view of array.
        """
        subarray = self.__data.subarray(0)
        array = Ndarray(subarray)
        array._shape = self._shape
        array._indices = self._indices
        return array

    def swapaxes(self, axis1, axis2):
        """
        Swap axes of array.
        Arguments are the axis to swap.
        Return view of array with axes changed.
        """
        subarray = self.__data.subarray(0)
        array = Ndarray(subarray)
        shape = list(self._shape)
        shape[axis1], shape[axis2] = shape[axis2], shape[axis1]
        array._shape = tuple(shape)
        array_size = 1
        for i in array._shape:
            array_size *= i
        indices = []
        for i in array._shape:
            array_size /= i
            indices.append(array_size)
        array._indices = tuple(indices)
        return array

    def getArray(self):
        """
        Return JavaScript TypedArray.
        """
        return self.__data.getArray()


class PyImageData:

    def __init__(self, imagedata):
        """
        Provides an interface to canvas ImageData.
        The argument required is the ImageData instance to be accessed.
        """
        self.__imagedata = imagedata
        try:
            self.data = PyUint8ClampedArray()
        except NotImplementedError:     #CanvasPixelArray
            self.data = PyTypedArray()
        self.data.__data = imagedata.data
        self.width = imagedata.width
        self.height = imagedata.height

    def getImageData(self):
        """
        Return JavaScript ImageData instance.
        """
        return self.__imagedata


class PyImageMatrix(Ndarray):

    def __init__(self, imagedata):
        """
        Provides an interface to canvas ImageData as an Ndarray array.
        The argument required is the ImageData instance to be accessed.
        """
        self.__imagedata = PyImageData(imagedata)
        try:
            Ndarray.__init__(self, self.__imagedata.data, 0)
        except NotImplementedError:     #ie10 supports typedarray, not uint8clampedarray
            Ndarray.__init__(self, self.__imagedata.data, 1)
        self.setshape(self.__imagedata.height,self.__imagedata.width,4)

    def getWidth(self):
        """
        Return ImageData width.
        """
        return self.__imagedata.width

    def getHeight(self):
        """
        Return ImageData height.
        """
        return self.__imagedata.height

    def getPixel(self, index):
        """
        Get pixel RGBA.
        The index arguement references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return (self.__imagedata.data[i], self.__imagedata.data[i+1], self.__imagedata.data[i+2], self.__imagedata.data[i+3])

    def setPixel(self, index, value):
        """
        Set pixel RGBA.
        The arguements index references the 2D array element and value is pixel RGBA.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self.__imagedata.data[i], self.__imagedata.data[i+1], self.__imagedata.data[i+2], self.__imagedata.data[i+3] = value[0], value[1], value[2], value[3]
        return None

    def getPixelRGB(self, index):
        """
        Get pixel RGB.
        The index arguement references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return (self.__imagedata.data[i], self.__imagedata.data[i+1], self.__imagedata.data[i+2])

    def setPixelRGB(self, index, value):
        """
        Set pixel RGB.
        The arguements index references the 2D array element and value is pixel RGB.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self.__imagedata.data[i], self.__imagedata.data[i+1], self.__imagedata.data[i+2] = value[0], value[1], value[2]
        return None

    def getPixelAlpha(self, index):
        """
        Get pixel alpha.
        The index arguement references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return self.__imagedata.data[i+3]

    def setPixelAlpha(self, index, value):
        """
        Set pixel alpha.
        The arguements index references the 2D array element and value is pixel alpha.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self.__imagedata.data[i+3] = value
        return None

    def getPixelInteger(self, index):
        """
        Get pixel integer color.
        The index arguement references the 2D array element.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        return self.__imagedata.data[i]<<16 | self.__imagedata.data[i+1]<<8 | self.__imagedata.data[i+2] | self.imagedata.data[i+3]<<24

    def setPixelInteger(self, index, value):
        """
        Set pixel integer color.
        The arguements index references the 2D array element and value is pixel color.
        """
        i = (index[0]*self._indices[0]) + (index[1]*4)
        self.__imagedata.data[i], self.__imagedata.data[i+1], self.__imagedata.data[i+2], self.__imagedata.data[i+3] = value>>16 & 0xff, value>>8 & 0xff, value & 0xff, value>>24 & 0xff
        return None

    def getImageData(self):
        """
        Return JavaScript ImageData instance.
        """
        return self.__imagedata.getImageData()

