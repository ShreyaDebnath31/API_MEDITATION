from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("AIzaSyAr5Y0PkiBcud22VdAns_MliATO-zPv9Mc"))

# Load Gemini Pro model and start chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Define route for chatbot endpoint
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get question from request JSON
    question = request.json.get('question')
    
    # Check if question is provided
    if not question:
        return jsonify({'error': 'Question not provided'}), 400
    
    # Send question to Gemini Pro model and get response
    try:
        response = chat.send_message(question, stream=True)
    except genai.types.generation_types.BlockedPromptException as e:
        # Handle blocked prompt exception
        return jsonify({'response': 'Sorry, I cannot respond to that question. Please ask another question.'})
    
    # Extract response text from chunks
    response_text = ""
    for chunk in response:
        response_text += chunk.text + " "
    
    # Return response
    return jsonify({'response': response_text.strip()})

if __name__ == '__main__':
    app.run(debug=True)