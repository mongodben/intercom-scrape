import json
with open("output-2.json") as f:
    json_obj = json.loads(f.read())
    for item in json_obj[20:21]:
        print(item['url'])
        print(item['markdown'])
        print()
