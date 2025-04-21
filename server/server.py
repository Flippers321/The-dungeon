import flask
import json
import math

app = flask.Flask(__name__)

@app.route("/SERVER", methods=["GET"])
def get():
    #defines a route for th GET request to /SERVER
    d = open('leaderboard.json') #opens the leaderboard JSON file
    data = json.load(d)
    #creating a single 2d array from the JSON file, which includes arrays for both the users and scores within the dictionary
    top_ten = merge_sort(list(zip(data["names"], data["scores"])), key = lambda x:x[1])
    return top_ten[:10] #returns only the top ten

def merge_sort(array, key):
    #sorting leaderboard into the top ten via a merge sort
    if len(array) > 1: #spliting array into left and right half
        left_array = array[:len(array)//2]
        right_array = array[len(array)//2:]
        
        #recursively sort the left and right halves, until in arrays of 2
        merge_sort(left_array, key)
        merge_sort(right_array, key)
        
        #merge
        i = 0 # left index
        j = 0 # right index
        k = 0 # merged index
        while i < len(left_array) and j < len(right_array):
            #adding the smaller elements into the merged array
            if key(left_array[i]) < key(right_array[j]):
                array[k] = left_array[i] 
                i += 1
            else:
                array[k] = right_array[j]
                j += 1
            k += 1
            
        #adding remaining elements into the left/right array
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
    #defining a route for the POST request to /leaderboard
    d = open('leaderboard.json')
    data = json.load(d)
    #appending new scores to the array
    data["scores"].append(json.loads(flask.request.json)["data"][1])
    data["names"].append(json.loads(flask.request.json)["data"][0])
    with open("leaderboard.json", "w") as outfile:
        json.dump(data, outfile) #saving the updated leaderboard
    return data["scores"]

app.run()
    
