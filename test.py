import matcher
rules = matcher.build()
query= "hakb"
results = matcher.match(query,rules)
print(results)