from capstone import *
from ctypes import CDLL, POINTER, c_char_p, c_int, c_uint32, pointer
import hashlib
import os
import platform

def getCallsDump(code):
	jump_ins = ['jmp','jz','jnz','je','jne','jg','jge','jl','jle','ja','jae','jb','jbe','jcxz','jecxz','jrcxz']
	call_dump = []
	md5 = hashlib.md5()
	counter = 0
	if code == None:
		return None
	for ins in code:
		ins_s = ins[0]
		if ins_s in jump_ins or counter > 49:
			call_dump.append(md5.hexdigest())
			md5 = hashlib.md5()
			counter = 0
		else:
			md5.update(ins_s.encode('utf-8'))
			counter += 1
	call_dump.append(md5.hexdigest())
	if len(call_dump) == 0:
		return None
	return selectDistinctNgram(call_dump)

# POPAD, PUSHAD, JE, JC, LOOP, INT, JAE, CWD, LODSB,
# JNE, IRET, PUSHA, JNC, POPA, STI, CLI, LEAVE, STD, CMC, BTR, BT, SETO,
# CLC, MOVSB, FNINIT, FBSTP, BTS, FNSTCW, FLDCW, CLD, ADC, STOSD, INSD,
# LDS, REPNE, AAD, FFREE, IN, XCHG, WAIT, JNS, FCLEX, OUTSD, OUT, SAHF,
# AAA, FRNDINT, SETNLE, DAA, SETNBE
      
def getInstRatio(code):
	sig_ins = {
    'popad':0,
    'pushad':0,
    'je':0,
    'jc':0,
    'loop':0,
    'int':0,
    'jae':0,
    'cwd':0,
    'lodsb':0,
    'jne':0,
    'iret':0,
    'pusha':0,
    'jnc':0,
    'popa':0,
    'sti':0,
    'cli':0,
    'leave':0,
    'std':0,
    'cmc':0,
    'btr':0,
    'bt':0,
    'seto':0,
    'clc':0,
    'movsb':0,
    'fninit':0,
    'fbstp':0,
    'bts':0,
    'fnstcw':0,
    'fldcw':0,
    'cld':0,
    'adc':0,
    'stosd':0,
    'insd':0,
    'lds':0,
    'repne':0,
    'aad':0,
    'ffree':0,
    'in':0,
    'xchg':0,
    'wait':0,
    'jns':0,
    'fclex':0,
    'outsd':0,
    'out':0,
    'sahf':0,
    'aaa':0,
    'frndint':0,
    'setnle':0,
    'daa':0,
    'setnbe':0,
	}
	ins_count = 0
	for ins in code:
		ins_count += 1
		try:
			sig_ins[ins[0]] += 1
		except:
			pass
	if ins_count == 0:
		return [value for value in list(sig_ins.values())]

	a = [x/ins_count for x in list(sig_ins.values())]
	b = list(sig_ins.keys())
	sig_ins = dict(map(lambda i,j : (i,j) , b,a))
	
	return [value for value in list(sig_ins.values())]

def selectDistinctNgram(arr):
    result = set()
    result.update(arr)
    
    return list(result)

def getNgram(filename,n):
    result = []
    file = open(filename,"rb")
    bvalue = b''
    b = 0
    e = n
    try:
        bvalue = file.read()
    except:
        print("no value")
        return result
    length = len(bvalue)
    while True:
        if e == length:
            break
        result.append(int(bvalue[b:e].hex(),16))
        b += 1
        e += 1
            
    file.close()
    return selectDistinctNgram(result)

def getNgramC(filename, n):
    # Determine the current operating system
    system = platform.system()
    # Set the filename of the shared library based on the operating system
    if system == 'Windows':
        lib_name = 'ngram_ext.dll'
    elif system == 'Linux':
        lib_name = 'ngram_ext.so'
    else:
        raise RuntimeError('Unsupported operating system: {}'.format(system))

    # Get the absolute path to the shared library
    script_dir = os.path.dirname(os.path.realpath(__file__))
    so_path = os.path.join(script_dir, "c_modules", lib_name)

    # Load the library using the absolute path
    libObject = CDLL(so_path)
    getNgram = libObject.get_ngram
    getNgram.argtypes = [c_char_p, c_int, POINTER(c_int)]
    getNgram.restype = POINTER(c_uint32)
    num_ngrams = c_int(0)
    num_ngramsPtr = pointer(num_ngrams)
    arrPtr = getNgram(filename.encode('utf-8'), c_int(n), num_ngramsPtr)
    result = [arrPtr[x] for x in range(num_ngramsPtr.contents.value)]
    return selectDistinctNgram(result)

