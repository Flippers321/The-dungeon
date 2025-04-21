import flask
import json

app = flask.Flask(__name__)

@app.route("/SERVER", methods=["GET"])
def get():
    d = open('leaderboard.json')
    data = json.load(d)
    top_ten = merge_sort(list(zip(data["names"], data["scores"])), key = lambda x:x[1])
    return top_ten[:10]

def merge_sort(array, key):
    if len(array) > 1:
        left_array = array[:len(array)//2]
        right_array = array[len(array)//2:]
        
        #recursion
        merge_sort(left_array, key)
        merge_sort(right_array, key)
        
        #merge
        i = 0 # left index
        j = 0 # right index
        k = 0 # merged index
        while i < len(left_array) and j < len(right_array):
            if key(left_array[i]) < key(right_array[j]):
                array[k] = left_array[i]
                i += 1
            else:
                array[k] = right_array[j]
                j += 1
            k += 1
            
        while i < len(left_array):
            array[k] = left_array[i]
            i += 1
            k += 1
            
        while j < len(right_array):
            array[k] = right_array[j]
            j += 1
            k += 1
            
    return array #scores should be lowest first so don't reverse the order again
    

@app.route("/leaderboard", methods=["POST"])
def send():
    d = open('leaderboard.json')
    data = json.load(d)
    data["scores"].append(json.loads(flask.request.json)["data"][1])
    data["names"].append(json.loads(flask.request.json)["data"][0])
    with open("leaderboard.json", "w") as outfile:
        json.dump(data, outfile)
    return data["scores"]

app.run()
    
