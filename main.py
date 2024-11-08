from flask import Flask,request,jsonify,render_template
from pymongo import MongoClient
import requests

app=Flask("IntrovBOT")

client=MongoClient("mongodb://localhost:27017/")
cursor=client["BOTvert"]
user_det=cursor["Users"]
chat_collection=cursor["Chats"]

HUGGING_FACE_API_URL="https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers={"Authorization":f"Bearer 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"}

def get_response_from_API(message):
    response = requests.post(HUGGING_FACE_API_URL, headers=headers, json={"inputs": message})
    print("Hugging Face API response:", response.json())  # Debugging print statement
    if response.status_code == 200:
        return response.json()[0].get('generated_text', "I'm Listening. Please Continue !!")
    else:
        return "Sorry, I'm having trouble processing your request."


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    if data is None:
        return jsonify({"error": "Request must be in JSON format"}), 400  # Error if no JSON

    user_message = data.get("message")
    if user_message:
        bot_response = get_response_from_API(user_message)
        
        # Save the conversation in MongoDB
        chat_collection.insert_one({"user": user_message, "bot": bot_response})
        
        return jsonify({"response": bot_response})
    return jsonify({"error": "No message received"}), 400  # Error if no message received

@app.route("/")
def home():
    return render_template("frontend.html")

if __name__ == "__main__":
    app.run(debug=True)