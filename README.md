A regex engine in Python support context free grammar. 


This regex engine can be used in text classification, domain classification.


You can write rule like this:
```
var date =(今天|明天)
var time =(十点|十一点)
var vehicle =(机票|高铁票)
var weather=(天气|温度)
export weather_rule=(${b})(怎么样|如何) => domain = 气象,气候参数=$1
export music_rule=(给我|替我)(订|买)一张(${date})(${time})的(${vehicle}) => domain = 交通,日期 = $3,时间=$4,票种=$5
```
Following codes shows how to get the results of query:
```python
import matcher
rules,li = matcher.build()
query= "给我买一张明天十点的机票"
results = matcher.match(query,rules,li)
print(results)
```
Following is the domain and slot filling results: 
```json
{
    "query":"给我买一张明天十点的机票",
    "semantic":{
        "domain":"交通",
        "slots":[
            {
                "name":"日期",
                "value":"明天"
            },
            {
                "name":"时间",
                "value":"十点"
            },
            {
                "name":"票种",
                "value":"机票"
            }
        ]
    }
}
```
Currently it supports the following:

* Repetition operators: \* \+ ?
* Parenthesis
* Characters (no character sets)


Run `python3 test.py ` to use.
