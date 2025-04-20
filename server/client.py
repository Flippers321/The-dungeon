import requests
import json

print("hello")
while True:
    input_ = input("g/p: ")
    print('client here')
    if input[0] == "g" or input_[0] == "get":
        response = requests.get("http://127.0.0.1:5000/TEST") #setup for local host, but can change the ip to anything
        print(response.json())
    elif input_[0] == "p" or input_[0] == "push":
        input_ = input_.split(" ")
        response = requests.post("http://127.0.0.1:5000/TEST",json = json.dumps({"data": [input_[1], input_[2]]}))
    else:
        break