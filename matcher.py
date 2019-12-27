import copy
import regex
import json
class Slot:
	def __init__(self, name='',value=""):
		self.name=name
		self.value=value
	def slot_filling(self,query,pos):
		if self.value[0]=="$":
			self.value=self.value.replace("$","")
			new_value=''
			index=int(self.value)
			for i in range(len(query)):
				if pos[i]==index:
					new_value+=query[i]
		self.value=new_value

class Post:
	def __init__(self, domain,slot=Slot()):
		self.domain=domain
		self.slot=slot
class Expr:
	def __init__(self,ID,name,tp,value,domain="",post=None):
		self.ID = ID
		self.name=name
		self.type=tp
		self.value=value
		self.domain = domain
		self.post=post
def recurrent(s,sentences):
	stack=[]
	b_flag=0
	x=""
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
	return s
def postfunc(line):
	line_li = line.split(',')
	p = Post('', [])
	for element in line_li:
		element_li = element.split('=')
		e_name = element_li[0].strip()
		e_value = element_li[1].strip()
		if e_name == "domain":
			p.domain = e_value
		else:
			slot = Slot(e_name, e_value)
			p.slot.append(slot)
	return p
def build():
	sentence_ID=0
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
			c.value = c.value.replace("(","[")
			c.value = c.value.replace(")", "]")
			post_value=postfunc("=".join(li[2:]).strip().replace(">",""))
			c.domain = post_value.domain
			sentences.append(copy.deepcopy(Expr(sentence_ID,c.name,c.type,c.value,c.domain,post_value)))
			sentence_ID+=1
		else:
			sentences.append(copy.deepcopy(Expr(sentence_ID,c.name,c.type,c.value)))
			sentence_ID+=1
	for i in range(len(sentences)):
		sentences[i].value=recurrent(sentences[i].value,sentences)
	nfa = {}
	for i in range(len(sentences)):
		if sentences[i].type == 'export':
			if sentences[i].ID in nfa:
				position = pos(sentences[i].value)
				nfa[sentences[i].ID] += regex.compile(sentences[i].value,position),
			else:
				position = pos(sentences[i].value)

				nfa[sentences[i].ID] = [regex.compile(sentences[i].value,position)]
	return nfa,sentences


def pos(s):
	position=[0 for i in range(len(s))]
	op_stack=[]
	index=1
	door=0
	for i in range(len(s)):
		if s[i]=='[':
			op_stack.append('[')
			door=1
		elif s[i]==']':
			op_stack.pop()
			if len(op_stack) == 0:
				index += 1
				door = 0
		if door ==1:
			position[i]=index
		if door ==0:
			position[i]=0
	return position

class Object:
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,
							sort_keys=True, indent=4,ensure_ascii=False)


def match(query,nfa,li):
	me = Object()
	me.query=query
	me.semantic= Object()
	for key in nfa:
		for i in range(len(nfa[key])):
			Is_match,pos_li = nfa[key][i].match(query)
			print(query)
			print(pos_li)
			if Is_match:
				for j in range(len(li)):
					if li[j].ID ==key:
						me.semantic.domain = li[j].post.domain
						me.semantic.slots=[]
						for k in li[j].post.slot:
							k.slot_filling(query,pos_li)
							me.semantic.slots.append(k)
	res=str(me.toJSON()).replace('\n','').replace(" ",'')
	return res
