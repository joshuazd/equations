import ctypes
import pathlib

class RESULT(ctypes.Structure):
    _fields_ = [("ret", ctypes.c_int),
                ("val", ctypes.c_longdouble),
                ("msg", ctypes.c_char_p)]
libname = pathlib.Path().absolute() / 'eval.so'
clib = ctypes.CDLL(libname)
clib.parse.restype = RESULT
StringArray = ctypes.c_char_p * 2
clib.unique.argtypes = [
        ctypes.c_char_p,
        StringArray,
        ctypes.c_int]
clib.unique.restype = ctypes.c_bool
print(clib.unique(b'1+2',StringArray(b'4+1',b'3+1'),1))
try:
    res = (clib.parse("8^9v5".encode('utf-8')))
    # res = (clib.parse(b'1+2^3'))
    print(res.ret, res.val)
    if res.ret != 0:
        raise Exception(res.msg.decode())
except Exception as e:
    print("Exception occured: ", e)
