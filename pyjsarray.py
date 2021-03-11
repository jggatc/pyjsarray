#PyjsArray - Python-to-JavaScript TypedArray Module
#Copyright (c) 2013 James Garnon

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

#PyjsArray version 0.53
#Project Site: http://gatc.ca/

from math import ceil as _ceil
try:
    from __pyjamas__ import JS
except ImportError:
    pass
import sys
if sys.version_info < (3,):
    range = xrange


class PyTypedArray(object):

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
                if pyjs_mode.optimized:
                    self.__data = JS("""new @{{typedarray}}(@{{data}})""")
                else:
                    self.__data = JS("""new @{{typedarray}}(@{{data}}['valueOf']())""")
            elif isinstance(data, (list,tuple)):
                if pyjs_mode.optimized:
                    self.__data = JS("""new @{{typedarray}}(@{{data}}['getArray']())""")
                else:
                    data = [dat.valueOf() for dat in data]
                    self.__data = JS("""new @{{typedarray}}(@{{data}}['getArray']())""")
            elif isinstance(data, PyTypedArray):
                self.__data = JS("""new @{{typedarray}}(@{{data}}['__data'])""")
            else:   #TypedArray or ArrayBuffer
                if offset is None and length is None:
                    self.__data = JS("""new @{{typedarray}}(@{{data}})""")
                else:
                    if offset is None:
                        offset = 0
                    if length is None:
                        self.__data = JS("""new @{{typedarray}}(@{{data}}, @{{offset}})""")
                    else:
                        self.__data = JS("""new @{{typedarray}}(@{{data}}, @{{offset}}, @{{length}})""")
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
        if pyjs_mode.optimized:
            JS("""@{{self}}['__data'][@{{index}}]=@{{value}};""")
        else:
            value = value.valueOf()
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
            if pyjs_mode.optimized:
                self.__data.set(data.getArray(), offset)
            else:
                data = [dat.valueOf() for dat in data]
                self.__data.set(data.getArray(), offset)
        elif isinstance(data, PyTypedArray):
            self.__data.set(data.__data, offset)

    def subarray(self, begin=0, end=None):
        """
        Retrieve a subarray of the array. The subarray is a is a view of the derived array. Optional arguments begin and end (default to begin/end of the array) are the index spanning the subarray.
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
            typedarray = Uint8ClampedArray
            PyTypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):     #-O/-S:TypeError/AttributeError
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
            typedarray = Uint8Array
            PyTypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
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
            typedarray = Uint16Array
            PyTypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
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
            typedarray = Uint32Array
            PyTypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
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
            typedarray = Int8Array
            PyTypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
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
            typedarray = Int16Array
            PyTypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
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
            typedarray = Int32Array
            PyTypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
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
            typedarray = Float32Array
            PyTypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
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
            typedarray = Float64Array
            PyTypedArray.__init__(self, data, offset, length, typedarray)
        except (TypeError, AttributeError):
            if isUndefined(typedarray):
                raise NotImplementedError("TypedArray data type not implemented")
            else:
                raise

    def __getitem__(self, index):
        """
        Get TypedArray element by index.
        """
        return JS("""@{{self}}['__data'][@{{index}}];""")


class PyCanvasPixelArray(PyTypedArray):
    """
    Create a PyTypedArray interface to CanvasPixelArray.
    """

    def __init__(self, data=None, offset=None, length=None):
        PyTypedArray.__init__(self, data, offset, length)
        self._superArray = None
        self._superIndex = (0,0)

    def __iter__(self):
        """
        Iterate over PyTypedArray object.
        """
        if not self._superArray:
            PyTypedArray.__iter__(self)
        else:
            index = self._superIndex[0]
            while index < self._superIndex[1]:
                yield self._superArray[index]
                index += 1

    def __getitem__(self, index):
        """
        Get TypedArray element by index.
        """
        if not self._superArray:
            return PyTypedArray.__getitem__(self, index)
        else:
            return self._superArray.__getitem__(index+self._superIndex[0])

    def __setitem__(self, index, value):
        """
        Set TypedArray element by index.
        """
        if not self._superArray:
            PyTypedArray.__setitem__(self, index, value)
        else:
            self._superArray.__setitem__(index+self._superIndex[0], value)
        return None

    def set(self, data, offset=0):
        """
        Set data to the array. Arguments: data is a list of either the TypedArray or Python type, offset is the start index where data will be set (defaults to 0).
        """
        if not self._superArray:
            for index in range(len(data)):
                self[index+offset] = data[index]
        else:
            self._superArray.set(data, offset+self._superIndex[0])

    def subarray(self, begin=0, end=None):
        """
        Retrieve a subarray of the array. The subarray is a is a view of the derived array. Optional arguments begin and end (default to begin/end of the array) are the index spanning the subarray.
        """
        if end is None:
            end = self.__data.length
        array = self.__class__()
        array.__data = self.__data
        array._superArray = self
        array._superIndex = (begin,end)
        return array


class Ndarray(object):

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
        typedarray = self._typedarray(dtype)
        if isinstance(dim, tuple):
            size = 1
            for i in dim:
                size *= i
            self.__data = typedarray(size)
            self._shape = dim
            indices = []
            for i in self._shape:
                size /= i
                indices.append(size)
            self._indices = tuple(indices)
        elif isinstance(dim, int):
            self.__data = typedarray(dim)
            self._shape = (dim,)
            self._indices = (self._shape[0],)
        elif isinstance(dim, list):
            if not (len(dim)>0 and isinstance(dim[0], list)):
                self.__data = typedarray(dim)
                self._shape = (len(dim),)
                self._indices = (self._shape[0],)
            else:
                _dat = self._lflatten(dim)
                _dim = self._lshape(dim)
                self.__data = typedarray(list(_dat))
                self._shape = (len(self.__data),)
                self.setshape(tuple(_dim))
        else:
            self.__data = dim
            self._shape = (len(dim),)
            self._indices = (self._shape[0],)

    @staticmethod
    def _typedarray(dtype):
        typedarray = {0: PyUint8ClampedArray,
                      1: PyUint8Array,
                      2: PyUint16Array,
                      3: PyUint32Array,
                      4: PyInt8Array,
                      5: PyInt16Array,
                      6: PyInt32Array,
                      7: PyFloat32Array,
                      8: PyFloat64Array}
        return typedarray[dtype]

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

    def _lflatten(self, l):
        for el in l:
            if isinstance(el, list):
                for _l in self._lflatten(el):
                    yield _l
            else:
                yield el

    def _lshape(self, l):
        _l = l
        while isinstance(_l, list):
            yield len(_l)
            _l = _l[0]

    def __getitem__(self, index):
        if hasattr(index, '__len__'):
            indexLn, shapeLn = index.__len__(), len(self._shape)
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
        else:
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
        if hasattr(index, '__len__'):
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
        else:
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

    def __getslice__(self, lower, upper):
        subarray = self.__data.subarray(lower, upper)
        return Ndarray(subarray, self._dtype)

    def __setslice__(self, lower, upper, data):
        subarray = self.__data.subarray(lower, upper)
        subarray.set(data)
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

    def _array_dim(self):
        if self._dtype < 7:
            vmax = len(str(max(self.__data)))
            vmin = len(str(min(self.__data)))
            vlen = {True:vmax, False:vmin}[vmax>vmin]
            vfmt = '%*d'
        else:
            vlen = max([len('%0.4f'%v) for v in self.__data])
            vfmt = '%*.4f'
        return vlen, vfmt

    def _array_str(self, array, vlen, vfmt, vstr):
        if len(array._shape) == 1:
            s = [vfmt % (vlen,val) for val in array]
            vstr.append('[%s]' % ' '.join(s))
        else:
            for i, a in enumerate(array):
                if i == 0:
                    vstr.append('[')
                else:
                    vstr.append(' '*(len(self._shape)-len(a._shape)))
                self._array_str(a, vlen, vfmt, vstr)
                if i < len(array)-1:
                    vstr.append('\n')
                else:
                    if vstr[-1] == ']\n':
                        vstr[-1] = ']'
                    if array._shape != self._shape:
                        vstr.append(']\n')
                    else:
                        vstr.append(']')
        return vstr

    def __str__(self):
        vlen, vfmt = self._array_dim()
        vstr = self._array_str(self, vlen, vfmt, [])
        return ''.join(vstr)

    def __repr__(self):
        s = str(self.tolist())
        sl = len(self._shape)
        for d in range(1, sl):
            s = s.replace(' '+'['*d, '\n'+' '*(sl+8-d)+'['*d)
        return 'Ndarray(%s, dtype=%d)' % (s, self._dtype)

    def __len__(self):
        return self._shape[0]

    def __lt__(self, other):
        ndarray = Ndarray(len(self.__data), 1)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] < other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] < other_data[i]
        return ndarray

    def __le__(self, other):
        ndarray = Ndarray(self._shape, 1)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] <= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] <= other_data[i]
        return ndarray
    
    def __eq__(self, other):
        ndarray = Ndarray(self._shape, 1)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] == other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] == other_data[i]
        return ndarray
    
    def __ne__(self, other):
        ndarray = Ndarray(self._shape, 1)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] != other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] != other_data[i]
        return ndarray
    
    def __gt__(self, other):
        ndarray = Ndarray(self._shape, 1)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] > other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] > other_data[i]
        return ndarray

    def __ge__(self, other):
        ndarray = Ndarray(self._shape, 1)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] >= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] >= other_data[i]
        return ndarray

    def __add__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] + other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] + other_data[i]
        return ndarray

    def __sub__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] - other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] - other_data[i]
        return ndarray

    def __mul__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] * other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] * other_data[i]
        return ndarray

    def __div__(self, other):
        return self.__truediv__(other)

    def __truediv__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] / other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] / other_data[i]
        return ndarray

    def __floordiv__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] // other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] // other_data[i]
        return ndarray

    def __divmod__(self, other):
        return self.__floordiv__(other), self.__mod__(other)

    def __mod__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] % other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] % other_data[i]
        return ndarray

    def __pow__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] ** other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] ** other_data[i]
        return ndarray

    def __neg__(self):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        for i in range(len(data)):
            ndarray_data[i] = -data[i]
        return ndarray

    def __pos__(self):
        ndarray = self.copy()
        return ndarray

    def __abs__(self):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        for i in range(len(data)):
            if data[i] < 0:
                ndarray_data[i] = -data[i]
        return ndarray

    def __matmul__(self, other):
        _other = self._get_array(other)
        x_dim = len(self._shape)
        y_dim = len(_other._shape)
        if x_dim != y_dim:
            raise ValueError('incompatible array shapes for matmul')
        if x_dim == 1:
            if self._shape[0] == _other._shape[0]:
                data = self.__data
                other_data = _other.__data
                result = 0
                for i in range(len(data)):
                    result += (data[i] * other_data[i])
                return result
            else:
                raise ValueError('incompatible array shapes for matmul')
        xshape = self._shape[-2:]
        yshape = _other._shape[-2:]
        if xshape[1] == yshape[0]:
            m = xshape[1]
            n = xshape[0]
            p = yshape[1]
            d = self._shape[:-2]
            d_len = 1
            for v in d:
                d_len*=v
        else:
            raise ValueError('incompatible array shapes for matmul')
        _data = self.__data.__class__(d_len*n*p)
        array = Ndarray(_data, self._dtype)
        array.setshape(d+(n,p))
        if x_dim == 2:
            arrays = [(self, _other, array)]
        elif x_dim == 3:
            arrays = [(self[i], _other[i], array[i])
              for i in range(d[0])]
        elif x_dim == 4:
            arrays = [(self[i,j], _other[i,j], array[i,j])
              for i,j in [(i,j) for i in range(d[0]) for j in range(d[1])]]
        elif x_dim == 5:
            arrays = [(self[i,j,k], _other[i,j,k], array[i,j,k])
              for i,j,k in [(i,j,k) for i in range(d[0]) for j in range(d[1]) for k in range(d[2])]]
        else:
            raise ValueError('incompatible array shapes for matmul')
        for _x, _y, _array in arrays:
            _x_data = _x.__data
            _y_data = _y.__data
            _array_data = _array.__data
            for i in range(n):
                for j in range(p):
                    result = 0
                    for k in range(m):
                        result += (_x_data[i*m+k] * _y_data[k*p+j])
                    _array_data[i*p+j] = result
        return array

    def __iadd__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] += other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] += other_data[i]
        return self

    def __isub__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] -= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] -= other_data[i]
        return self

    def __imul__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] *= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] *= other_data[i]
        return self

    def __idiv__(self, other):
        return self.__itruediv__(other)

    def __itruediv__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] /= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] /= other_data[i]
        return self

    def __ifloordiv__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] //= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] //= other_data[i]
        return self

    def __imod__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] %= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] %= other_data[i]
        return self

    def __ipow__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] **= other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] **= other_data[i]
        return self

    def __lshift__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] << other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] << other_data[i]
        return ndarray

    def __rshift__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] >> other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] >> other_data[i]
        return ndarray

    def __and__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] & other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] & other_data[i]
        return ndarray

    def __or__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] | other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] | other_data[i]
        return ndarray

    def __xor__(self, other):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                ndarray_data[i] = data[i] ^ other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                ndarray_data[i] = data[i] ^ other_data[i]
        return ndarray

    def __ilshift__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] << other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] << other_data[i]
        return self

    def __irshift__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] >> other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] >> other_data[i]
        return self

    def __iand__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] & other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] & other_data[i]
        return self

    def __ior__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] | other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] | other_data[i]
        return self

    def __ixor__(self, other):
        data = self.__data
        if not hasattr(other, '__iter__'):
            for i in range(len(data)):
                data[i] = data[i] ^ other
        else:
            other_data = self._get_data(other)
            for i in range(len(data)):
                data[i] = data[i] ^ other_data[i]
        return self

    def __invert__(self):
        ndarray = self.empty()
        ndarray_data = ndarray.__data
        data = self.__data
        for i in range(len(data)):
            ndarray_data[i] = ~data[i]
        return ndarray

    def _get_data(self, other):
        if not isinstance(other, Ndarray):
            if isinstance(other, list):
                other = Ndarray(other, self._dtype)
            else:
                other = Ndarray(list(other), self._dtype)
        if self._shape != other._shape:
            raise TypeError("array shapes are not compatible")
        return other.__data

    def _get_array(self, other):
        if not isinstance(other, Ndarray):
            if isinstance(other, list):
                other = Ndarray(other, self._dtype)
            else:
                other = Ndarray(list(other), self._dtype)
        return other

    def cmp(self, operator, other):
        """
        Comparison operation across array elements.
        Arguments include operator ('=='...) and int/array.
        Return comparison array.
        """
        ops = {'<':  lambda s,o:s.__lt__(o), '<=': lambda s,o:s.__le__(o),
               '==': lambda s,o:s.__eq__(o), '!=': lambda s,o:s.__ne__(o),
               '>':  lambda s,o:s.__gt__(o), '>=': lambda s,o:s.__ge__(o)}
        return ops[operator](self, other)

    def matmul(self, other):
        """
        Matrix multiplication.
        Argument is an int or array.
        Return matrix multiplied array.
        """
        return self.__matmul__(other)

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

    def set(self, data):
        """
        Set array elements.
        Data argument can be a 1d/2d array or number used to set Ndarray elements, data used repetitively if consists of fewer elements than Ndarray.
        """
        if isinstance(data, (list,tuple)):
            if pyjs_mode.optimized:
                if isinstance(data[0], (list,tuple,PyTypedArray)):
                    data = [value for dat in data for value in dat]
            else:
                if not isinstance(data[0], (list,tuple,PyTypedArray)):
                    data = [dat.valueOf() for dat in data]
                else:
                    data = [value.valueOf() for dat in data for value in dat]
            dataLn = len(data)
            data = data.getArray()
        elif isinstance(data, (Ndarray,PyTypedArray)):
            data = data.getArray()
            dataLn = data.length
        else:
            if pyjs_mode.optimized:
                for index in range(self.__data.__data.length):
                    JS("""@{{self}}['__data']['__data'][@{{index}}]=@{{data}};""")
            else:
                data = data.valueOf()
                for index in range(self.__data.__data.length):
                    JS("""@{{self}}['__data']['__data'][@{{index}}]=@{{data}};""")
            return None
        if dataLn == self.__data.__data.length:
            for index in range(self.__data.__data.length):
                JS("""@{{self}}['__data']['__data'][@{{index}}]=@{{data}}[@{{index}}];""")
        else:
            for index in range(self.__data.__data.length):
                JS("""@{{self}}['__data']['__data'][@{{index}}]=@{{data}}[@{{index}}%@{{dataLn}}];""")
        return None

    def fill(self, value):
        """
        Set array elements to value argument.
        """
        if pyjs_mode.optimized:
            for index in range(self.__data.__data.length):
                JS("""@{{self}}['__data']['__data'][@{{index}}]=@{{value}};""")
        else:
            value = value.valueOf()
            for index in range(self.__data.__data.length):
                JS("""@{{self}}['__data']['__data'][@{{index}}]=@{{value}};""")
        return None

    def copy(self):
        """
        Return copy of array.
        """
        array = self.__data.__class__(self.__data)
        ndarray = Ndarray(array, self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        return ndarray

    def empty(self):
        """
        Return empty copy of array.
        """
        ndarray = Ndarray(len(self.__data), self._dtype)
        ndarray._shape = self._shape
        ndarray._indices = self._indices
        return ndarray

    def astype(self, dtype):
        """
        Return copy of array.
        Argument dtype is TypedArray data type.
        """
        typedarray = self._typedarray(dtype)
        array = typedarray(self.__data)
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
        array = Ndarray(self.__data, self._dtype)
        shape = list(self._shape)
        shape[axis1], shape[axis2] = shape[axis2], shape[axis1]
        array._shape = tuple(shape)
        indices = list(self._indices)
        indices[axis1], indices[axis2] = indices[axis2], indices[axis1]
        array._indices = tuple(indices)
        return array

    def tolist(self):
        """
        Return array as a list.
        """
        def to_list(array, l):
            if hasattr(array[0], '__iter__'):
                if len(l) == 0:
                    _l = l
                else:
                    l = [l]
                    _l = l[0]
                for i, a in enumerate(array):
                    _l.append([])
                    to_list(a, _l[i])
            else:
                l.extend([v for v in array])
            return l
        return to_list(self, [])

    def getArray(self):
        """
        Return JavaScript TypedArray.
        """
        return self.__data.getArray()


class NP(object):

    def zeros(self, size, dtype):
        if dtype == 'i':
            dtype = 3
        return Ndarray(size, dtype)

    def swapaxes(self, array, axis1, axis2):
        return array.swapaxes(axis1, axis2)

    def append(self, array, values):
        if isinstance(values[0], (list,tuple,PyTypedArray)):
            values = [value for dat in values for value in dat]
        newarray = Ndarray(len(array)+len(values), array._dtype)
        newarray.__data.set(array.__data)
        newarray.__data.set(values, len(array))
        return newarray

np = NP()


class PyImageData(object):

    def __init__(self, imagedata):
        """
        Provides an interface to canvas ImageData.
        The argument required is the ImageData instance to be accessed.
        """
        self.__imagedata = imagedata
        if not isUndefined(Uint8ClampedArray):
            self.data = PyUint8ClampedArray()
        else:
            self.data = PyCanvasPixelArray()
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
        if isinstance(self.__imagedata.data, PyUint8ClampedArray):
            Ndarray.__init__(self, self.__imagedata.data, 0)
        else:     #ie10 supports typedarray, not uint8clampedarray
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


class BitSet(object):

    """
    BitSet provides a bitset object to use in a Python-to-JavaScript application. It uses the PyUint8Array implementation of the JavaScript Uint8Array 8-bit typedarray. BitSet16 and BitSet32 stores data in PyUint16Array (16-bit) and PyUint32Array (32-bit) that implement the Uint16Array and Uint32Array typedarray. The BitSet will dynamically expand to hold the bits required, an optional width argument define number of bits the BitSet instance will initially hold.
    """

    __bit = 8
    __bitmask = None
    __typedarray = PyUint8Array

    def __init__(self, width=None):
        if not self.__class__.__bitmask:
            self.__class__.__bitmask = dict([(self.__class__.__bit-i-1,1<<i) for i in range(self.__class__.__bit-1,-1,-1)])
            self.__class__.__bitmask[self.__class__.__bit-1] = int(self.__class__.__bitmask[self.__class__.__bit-1])      #pyjs [1<<0] = 1L
        if width:
            self.__width = abs(width)
        else:
            self.__width = self.__bit
        self.__data = self.__typedarray( _ceil(self.__width/(self.__bit*1.0)) )

    def __str__(self):
        """
        Return string representation of BitSet object.
        """
        return "%s" % self.__class__

    def __repr__(self):
        """
        Return string of the indexes of the set bits.
        """
        setBit = []
        for index in range(self.__width):
            if self.get(index):
                setBit.append(str(index))
        return "{" + ", ".join(setBit) + "}"

    def __getitem__(self, index):
        """
        Get bit by index.
        """
        return self.get(index)

    def __setitem__(self, index, value):
        """
        Set bit by index.
        """
        self.set(index, value)

    def __len__(self):
        """
        Get bit length.
        """
        for index in range(self.__width-1, -1, -1):
            if self.get(index):
                break
        return index+1

    def __iter__(self):
        """
        Iterate over bits.
        """
        index = 0
        while index < self.__width:
            yield self.get(index)
            index += 1

    def get(self, index, toIndex=None):
        """
        Get bit by index.
        Arguments include index of bit, and optional toIndex that return a slice as a BitSet.
        """
        if index > self.__width-1:
            if not toIndex:
                return False
            else:
                size = toIndex-index
                if size > 0:
                    return self.__class__(size)
                else:
                    return None
        if toIndex is None:
            return bool( self.__data[ int(index/self.__bit) ] & self.__bitmask[ index%self.__bit ] )
        else:
            size = toIndex-index
            if size > 0:
                bitset = self.__class__(size)
                ix = 0
                if toIndex > self.__width:
                    toIndex = self.__width
                for i in range(index, toIndex):
                    bitset.set(ix, bool( self.__data[ int(i/self.__bit) ] & self.__bitmask[ i%self.__bit ] ))
                    ix += 1
                return bitset
            else:
                return None

    def set(self, index, value=1):
        """
        Set bit by index.
        Optional argument value is the bit state of 1(True) or 0(False). Default:1
        """
        if index > self.__width-1:
            if value:
                self.resize(index+1)
            else:
                return
        if value:
            self.__data[ int(index/self.__bit) ] = self.__data[ int(index/self.__bit) ] | self.__bitmask[ index%self.__bit ]
#            self.__data[ int(index/self.__bit) ] |= self.__bitmask[ index%self.__bit ]    #pyjs -O: |= not processed
        else:
            self.__data[ int(index/self.__bit) ] = self.__data[ int(index/self.__bit) ] & ~(self.__bitmask[ index%self.__bit ])
#            self.__data[ int(index/self.__bit) ] &= ~(self.__bitmask[ index%self.__bit ])     #pyjs -O: &= not processed
        return None

    def fill(self, index=None, toIndex=None):
        """
        Set the bit. If no argument provided, all bits are set.
        Optional argument index is bit index to set, and toIndex to set a range of bits.
        """
        if index is None and toIndex is None:
            for i in range(0, self.__width):
                self.set(i, 1)
        else:
            if toIndex is None:
                self.set(index, 1)
            else:
                for i in range(index, toIndex):
                    self.set(i, 1)

    def clear(self, index=None, toIndex=None):
        """
        Clear the bit. If no argument provided, all bits are cleared.
        Optional argument index is bit index to clear, and toIndex to clear a range of bits.
        """
        if index is None:
            for i in range(len(self.__data)):
                self.__data[i] = 0
        else:
            if toIndex is None:
                self.set(index, 0)
            else:
                if index == 0 and toIndex == self.__width:
                    for dat in range(len(self.__data)):
                        self.__data[dat] = 0
                else:
                    for i in range(index, toIndex):
                        self.set(i, 0)

    def flip(self, index, toIndex=None):
        """
        Flip the state of the bit.
        Argument index is the bit index to flip, and toIndex to flip a range of bits.
        """
        if toIndex is None:
            self.set(index, not self.get(index))
        else:
            if toIndex > self.__width:
                self.resize(toIndex)
                toIndex = self.__width
            if index == 0 and toIndex == self.__width:
                for dat in range(len(self.__data)):
                    self.__data[dat] = ~self.__data[dat]
            else:
                for i in range(index, toIndex):
                    self.set(i, not self.get(i))

    def cardinality(self):
        """
        Return the count of bit set.
        """
        count = 0
        for bit in range(self.__width):
            if self.get(bit):
                count += 1
        return count

    def intersects(self, bitset):
        """
        Check if set bits in this BitSet are also set in the bitset argument.
        Return True if bitsets intersect, otherwise return False.
        """
        for dat in range(len(bitset.__data)):
            if bitset.__data[dat] & self.__data[dat]:
                return True
        return False

    def andSet(self, bitset):
        """
        BitSet and BitSet.
        """
        data = min(len(self.__data), len(bitset.__data))
        for dat in range(data):
            self.__data[dat] = self.__data[dat] & bitset.__data[dat]
#            self.__data[dat] &= bitset.__data[dat]     #pyjs -O: &= not processed
#        pyjs -S: &= calls __and__ instead of __iand__, -O: no call to operator methods

    def orSet(self, bitset):
        """
        BitSet or BitSet.
        """
        data = min(len(self.__data), len(bitset.__data))
        for dat in range(data):
            self.__data[dat] = self.__data[dat] | bitset.__data[dat]
#            self.__data[dat] |= bitset.__data[dat]    #pyjs -O: |= not processed

    def xorSet(self, bitset):
        """
        BitSet xor BitSet.
        """
        data = min(len(self.__data), len(bitset.__data))
        for dat in range(data):
            self.__data[dat] = self.__data[dat] ^ bitset.__data[dat]
#            self.__data[dat] ^= bitset.__data[dat]    #pyjs -O: |= not processed

    def resize(self, width):
        """
        Resize the BitSet to width argument.
        """
        if width > self.__width:
            self.__width = width
            if self.__width > len(self.__data) * self.__bit:
                array = self.__typedarray( _ceil(self.__width/(self.__bit*1.0)) )
                array.set(self.__data)
                self.__data = array
        elif width < self.__width:
            if width < len(self):
                width = len(self)
            self.__width = width
            if self.__width <= len(self.__data) * self.__bit - self.__bit:
                array = self.__typedarray( _ceil(self.__width/(self.__bit*1.0)) )
                array.set(self.__data.subarray(0,_ceil(self.__width/(self.__bit*1.0))))
                self.__data = array

    def size(self):
        """
        Return bits used by BitSet storage array.
        """
        return len(self.__data) * self.__bit

    def isEmpty(self):
        """
        Check whether any bit is set.
        Return True if none set, otherwise return False.
        """
        for data in self.__data:
            if data:
                return False
        return True

    def clone(self):
        """
        Return a copy of the BitSet.
        """
        new_bitset = self.__class__(1)
        data = self.__typedarray(self.__data)
        new_bitset.__data = data
        new_bitset.__width = self.__width
        return new_bitset


class BitSet16(BitSet):
    """
    BitSet using PyUint16Array.
    """
    __bit = 16
    __bitmask = None
    __typedarray = PyUint16Array

    def __init__(self, width=None):
        BitSet.__init__(self, width)


class BitSet32(BitSet):
    """
    BitSet using PyUint32Array.
    """
    __bit = 32
    __bitmask = None
    __typedarray = PyUint32Array

    def __init__(self, width=None):
        BitSet.__init__(self, width)


class Pyjs_Mode(object):

    def __init__(self):
        self.strict, self.optimized = self._setmode()

    def __getattr__(self, attr):
        if attr == '__strict_mode':
            return True

    def _setmode(self):
        if self.__strict_mode == True:
            return True, False
        else:
            return False, True

pyjs_mode = Pyjs_Mode()
