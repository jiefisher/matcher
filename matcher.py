import copy
class Expr:
	def __init__(self,name,tp,value,domain=""):
		self.name=name
		self.type=tp
		self.value=value
		self.domain=domain
def recurrent(s,sentences):
	stack=[]
	b_flag=0
	x=""
	index=0
	new_str=""
	for i in range(len(s)):
		if s[i-2] == "$" and s[i-1] =="{":
			x+=s[i]
			b_flag=1
		elif s[i]=='}':
			stack.append(copy.deepcopy(x))
			x=""
			b_flag=0
		elif b_flag==1 and s[i] not in "${":
			x+=s[i]
	for name in stack:
		for sentence in sentences:
			if sentence.name == name:
				s=s.replace("${"+name+"}",sentence.value)
	print(s)
	return s
def build():
	sentences=[]
	f=open("code.txt","r")
	lines=f.readlines()
	for line in lines:
		c=Expr
		li= line.split("=")
		lhs=li[0].strip()
		rhs=li[1].strip()
		p=lhs.split()
		c.name=p[1]
		c.type=p[0]
		c.value=rhs
		if c.type=='export':
			c.value=rhs
			c.domain=li[2].strip().replace(">","")
			sentences.append(copy.deepcopy(Expr(c.name,c.type,c.value,c.domain)))
		else:
			sentences.append(copy.deepcopy(Expr(c.name,c.type,c.value)))



	for i in range(len(sentences)):
		sentences[i].value=recurrent(sentences[i].value,sentences)

	return sentences
		# ##print(sentences[i].value)

def pos(s):
	position=[0 for i in range(len(s))]
	op_stack=[]
	index=1
	for i in range(len(s)):
		if s[i]=='(':
			op_stack.append('(')
		elif s[i]==')':
			op_stack.pop()
		position[i]=index
		if len(op_stack)==0:
			index+=1
	##print(s)
	##print(position)
	return position


def match(query,sentences):
	import regex
	res=[]

	nfa={}
	for i in range(len(sentences)):
		if sentences[i].type=='export':
			if sentences[i].domain in nfa:
				##print(sentences[i].value)
				position=pos(sentences[i].value)
				# ##print(sentences[i].value,sentences[i].domain)
				nfa[sentences[i].domain]+=regex.compile(sentences[i].value),
			else:
				# ##print(sentences[i].value,sentences[i].domain)
				##print(sentences[i].value)
				position = pos(sentences[i].value)
				nfa[sentences[i].domain]=[regex.compile(sentences[i].value)]
	

	for key in nfa:
		for i in range(len(nfa[key])):
			if nfa[key][i].match(query):
				res.append(key)
	return res
