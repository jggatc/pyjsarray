PyjsArray - Python-to-JavaScript TypedArray Module

PyjsArray module provides Python objects that wrap the JavaScript TypedArray objects. It was designed for use in Python-to-JavaScript applications that are translated with the Pyjs compiler (http://pyjs.org). The module provides the following TypedArray objects:

    PyjsArray object        TypedArray object
    ----------------        -----------------
    PyUint8ClampedArray     [Uint8ClampedArray]
    PyUint8Array            [Uint8Array]
    PyUint16Array           [Uint16Array]
    PyUint32Array           [Uint32Array]
    PyInt8Array             [Int8Array]
    PyInt16Array            [Int16Array]
    PyInt32Array            [Int32Array]
    PyFloat32Array          [Float32Array]
    PyFloat64Array          [Float64Array]

The module also includes an Ndarray class to instantiate N-dimensional arrays, PyImageData/PyImageMatrix classes that provide an interface to the canvas ImageData array, and BitSet/BitSet16/BitSet32 classes that store bitarray data in 8/16/32 bit size providing functionality similar to Java BitSet.

PyjsArray is released under the MIT License, see license.txt for further information.

PyjsArray docs: http://gatc.ca/projects/pyjsdl/doc/

