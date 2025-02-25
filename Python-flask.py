from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask (__name__)

Mongo_URI = "mongodb+srv://rhiza:qwertyuiop@cluster0.q5acz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Database_Iot"
COLLECTION = "Collection_IoT"

client = MongoClient(Mongo_URI)
db = client[DB_NAME]
collection = db[COLLECTION]

@app.route("/save", methods=["POST"])
def save_data():
    data = request.get_json()
    temperature = data.get("temperature")
    humidity = data.get("humidity")
    ldr_value = data.get("light")
    motion = data.get("motion")

    data = {
        "temperature": {"value": temperature},
        "humidity": {"value": humidity},
        "light": {"value": ldr_value},
        "motion": {"value": motion}
    }

    collection.insert_one(data)
    print("success")
    return jsonify({"message" : "Success"})

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
