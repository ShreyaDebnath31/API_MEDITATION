from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.getenv("AIzaSyAr5Y0PkiBcud22VdAns_MliATO-zPv9Mc"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

@app.route('/chatbot', methods=['POST'])
def chatbot():
    
    question = request.json.get('question')
    
    
    if not question:
        return jsonify({'error': 'Question not provided'}), 400
    

    try:
        response = chat.send_message(question, stream=True)
    except genai.types.generation_types.BlockedPromptException as e:
       
        return jsonify({'response': 'Sorry, I cannot respond to that question. Please ask another question.'})
    
    
    response_text = ""
    for chunk in response:
        response_text += chunk.text + " "
    

    return jsonify({'response': response_text.strip()})

if __name__ == '__main__':
    app.run("0.0.0.0",port = 5003,debug=True,use_reloader=True)