import matcher
rules,li = matcher.build()
query= "eattkb"
results = matcher.match(query,rules,li)
print(results)