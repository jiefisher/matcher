import matcher
rules = matcher.build()
query= "today weather is ok"
results = matcher.match(query,rules)
print(results)