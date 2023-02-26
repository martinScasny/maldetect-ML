from capstone import *
import pe_parser
import hashlib


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

# def testGetCallsDump(code):
# 	jump_ins = ['jmp','jz','jnz','je','jne','jg','jge','jl','jle','ja','jae','jb','jbe','jcxz','jecxz','jrcxz']
# 	call_dump = []
# 	call = ""
# 	counter = 0
# 	for ins in code:
# 		if ins in jump_ins or counter > 49:
# 			call_dump.append(call)
# 			call = ""
# 			counter = 0
# 		else:
# 			call += ins
# 			counter += 1
	  
# 	return selectDistinctNgram(call_dump)

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
    currGram = b''
    file = open(filename,"rb")
    bvalue = b''
    try:
        bvalue = file.read(n)
    except:
        print("no value")
        return result
    result.append(int(bvalue.hex(),16))
    currGram = bvalue
    while True:
        bvalue = file.read(1)
        if not bvalue:
            break

        currGram = bytes.fromhex("".join(currGram.hex())[2:]) + bvalue
        if currGram:
            result.append(int(currGram.hex(),16))
            
    file.close()
    return selectDistinctNgram(result)

				
# CODE = b"\x55\x48\x8b\x05\xb8\x13\x00\x00"
# result = []
# md = Cs(CS_ARCH_X86, CS_MODE_64)
# for i in md.disasm(CODE, 0x1000):
#     result.append([i.mnemonic,i.bytes])

# print(result)
# peelement = pe_parser.createObject('Anti-malware-tool\\adware_lazy')
# code = peelement.getCode()
# print(getCallsDump(code))

