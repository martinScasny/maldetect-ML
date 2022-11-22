from capstone import *
import binascii

# INFO not certain if I need to store whole ins or stripped ins
# TODO modify to store from jmp to jmp
def getCallsDump(code):
	call_dump = []
	cur_call = []
	for ins in code:
		ins_s = ins[0]
		cur_call = []
		if ins_s == 'jmp' or ins_s == 'jz':
			call_dump.append(cur_call)
		else:
			cur_call.append(ins_s)
	return call_dump

      
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
			print("Could not find '",ins[0],"' instruction")

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
        
    return selectDistinctNgram(result)

				
print(len(getNgram('sample31',4)))


# CODE = b"\x55\x48\x8b\x05\xb8\x13\x00\x00"
# result = []
# md = Cs(CS_ARCH_X86, CS_MODE_64)
# for i in md.disasm(CODE, 0x1000):
#     result.append([i.mnemonic,i.bytes])

# print(result)