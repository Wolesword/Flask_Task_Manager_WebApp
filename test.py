import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes": 1610, "name": "Wole", "views": 100000},
        {"likes": 154, "name": "Jojo on the dance floor", "views": 1000},
        {"likes": 16, "name": "Sami", "views": 10000}]

for i in range(len(data)):
    response = requests.put(BASE + "video/1" + str(i), data[i])
    print(response.json())

response = requests.delete(BASE + "video/0")
print(response)
input()

response = requests.get(BASE + "video/2")
print(response.json())
