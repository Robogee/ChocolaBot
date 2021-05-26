import json

teststring = "Hello world -u"

task = {}
params = teststring.split('-')

task["task"] = params[0]
if len(params) > 1:
    task["urgent"] = True
else:
    task['urgent'] = False

new = json.dumps(task)
print(new)
