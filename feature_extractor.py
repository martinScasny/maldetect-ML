import pe_parser

# INFO not certain if I need to store whole ins or stripped ins
def getCallsDump(code):
	in_call = 0
	in_end = 0
	call_dump = []
	cur_call = []
	for ins in code:
		print("ins je",ins)
		ins_s = ins.split(' ')[0]
		print("ins_s je",ins)
		if ins_s == 'call':
			in_call = 1
			cur_call = []
			continue
		if ins_s == 'ret':
			in_end = 1
			in_call = 0
		if in_call:
			cur_call.append(ins)
		elif in_end:
			call_dump.append(cur_call)
			in_end = 0
	return call_dump

      
      

def getInstRatio(code):
  pass
  # disassembled code
  #POPAD, PUSHAD, JE, JC, LOOP, INT, JAE, CWD, LODSB, and JNE
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
      	sig_ins[ins.split(' ')[0]] += 1
      except:
      	print("Could not find '",ins,"' instruction")

  a = [x/ins_count for x in list(sig_ins.values())]
  b = list(sig_ins.keys())
  sig_ins = dict(map(lambda i,j : (i,j) , b,a))

return sig_ins