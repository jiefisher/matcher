import matcher
rules,li = matcher.build()
query= "给我买一张明天十点去北京的机票"
results = matcher.match(query,rules,li)
print(results)