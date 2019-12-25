A regex engine in Python support context free grammar. 


This regex engine can be used in text classification, domain classification:
You can write rule like this:
```
var date =(today |tomorrow )
var b=${date}(weather |temp )
var artist =(tom |tony )
var y=${artist}(song |music )
export weather_rule=${b}(is ok|not ok) => weather
export music_rule=${y}(good|bad) => music
```
Following codes shows how to get the results of query:
```python
import matcher
rules = matcher.build()
query= "today weather is ok"
results = matcher.match(query,rules)
print(results)
```


Currently it supports the following:

* Repetition operators: \* \+ ?
* Parenthesis
* Characters (no character sets)


Run `python3 test.py ` to use.
