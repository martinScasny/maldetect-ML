from capstone import *
import pe_parser
import hashlib

# INFO not certain if I need to store whole ins or stripped ins
# TODO modify to store from jmp to jmp
def getCallsDump(code):
	jump_ins = ['jmp','jz','jnz','je','jne','jg','jge','jl','jle','ja','jae','jb','jbe','jcxz','jecxz','jrcxz']
	call_dump = []
	md5 = hashlib.md5()
	for ins in code:
		ins_s = ins[0]
		if ins_s in jump_ins:
			call_dump.append(md5.hexdigest())
			md5 = hashlib.md5()
		else:
			md5.update(ins_s.encode('utf-8'))
	  
	return selectDistinctNgram(call_dump)

      
def getInstRatio(code):
	sig_ins = {
				'popad':0,
				'pushad':0,
				'je':0,
				'jc':0,
				'int':0,
				'jae':0,
				'cwd':0,
				'lodsb':0,
				'jne':0
				}
	ins_count = 0
	for ins in code:
		ins_count += 1
		try:
			sig_ins[ins[0]] += 1
		except:
			pass

	a = [x/ins_count for x in list(sig_ins.values())]
	b = list(sig_ins.keys())
	sig_ins = dict(map(lambda i,j : (i,j) , b,a))
	
	return sig_ins

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

				
# print(len(getNgram('sample31',4)))


# CODE = b"\x55\x48\x8b\x05\xb8\x13\x00\x00"
# result = []
# md = Cs(CS_ARCH_X86, CS_MODE_64)
# for i in md.disasm(CODE, 0x1000):
#     result.append([i.mnemonic,i.bytes])

# print(result)
# peelement = pe_parser.createObject('Anti-malware-tool\\adware_lazy')
# code = peelement.getCode()
# print(getCallsDump(code))

