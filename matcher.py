import copy
class token:
	def __init__(self,name,tp,value,domain=""):
		self.name=name
		self.type=tp
		self.value=value
		self.domain=domain
def recurrent(s,sentences):
	stack=[]
	x=""
	index=0
	new_str=""
	for i in range(len(s)):
		if s[i] == "$" and s[i+1] =="{":
			new_str += "".join(list(s)[index:i])
			index = i
			for j in range(i+2,len(s)):
				if s[j]!="}":
					x+=s[j]
				else:
					index = j+1
					for k in range(len(sentences)):
						if sentences[k].name ==x:
							p = recurrent(sentences[k].value,sentences)
							# print(p)
							new_str+=p
	new_str+="".join(list(s)[index:len(s)])
	# print(new_str)
	return new_str
def build():
	sentences=[]
	f=open("code.txt","r")
	lines=f.readlines()
	for line in lines:
		c=token
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
			sentences.append(copy.deepcopy(token(c.name,c.type,c.value,c.domain)))
		else:
			sentences.append(copy.deepcopy(token(c.name,c.type,c.value)))



	# print(recurrent("${b}(e|f)"))
	for i in range(len(sentences)):
		sentences[i].value=recurrent(sentences[i].value,sentences)
	return sentences
		# print(sentences[i].value)

def match(query,sentences):
	import regex
	res=[]

	nfa={}
	for i in range(len(sentences)):
		if sentences[i].type=='export':
			if sentences[i].domain in nfa:
				# print(sentences[i].value,sentences[i].domain)
				nfa[sentences[i].domain]+=regex.compile(sentences[i].value),
			else:
				# print(sentences[i].value,sentences[i].domain)
				nfa[sentences[i].domain]=[regex.compile(sentences[i].value)]
	

	for key in nfa:
		for i in range(len(nfa[key])):
			if nfa[key][i].match(query):
				res.append(key)
	return res
