from flask import Flask, jsonify, request, render_template
import os
import json
import uuid

app = Flask(__name__,template_folder='../templates')

# Directory to store chat histories
CHAT_HISTORY_DIR = "./chat_histories"
os.makedirs(CHAT_HISTORY_DIR, exist_ok=True)  # Ensure the directory exists

class ModelManager:
    def __init__(self):
        self.models = {}

    def add_model(self, name, model):
        self.models[name] = model

    def get_model(self, name):
        return self.models.get(name, None)

    def list_models(self):
        return list(self.models.keys())

# Example models
from models import model1, model2

class Model1:
    def predict(self, input_text):
        m1 = model1.Model1()
        m1_res = m1.predict(input_text=input_text)
        return m1_res

class Model2:
    def predict(self, input_text):
        m2 = model2.Model2()
        m2_res = m2.predict(input_text=input_text)
        return m2_res

model_manager = ModelManager()
model_manager.add_model("model1", Model1())
model_manager.add_model("model2", Model2())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

def save_chat_history(session_id, chat_data):
    """Save chat history to a JSON file."""
    filepath = os.path.join(CHAT_HISTORY_DIR, f"{session_id}.json")
    with open(filepath, 'w') as file:
        json.dump(chat_data, file)

def load_chat_histories():
    """Load all chat histories from the directory."""
    histories = {}
    for filename in os.listdir(CHAT_HISTORY_DIR):
        if filename.endswith('.json'):
            session_id = filename.split('.')[0]
            filepath = os.path.join(CHAT_HISTORY_DIR, filename)
            with open(filepath, 'r') as file:
                histories[session_id] = json.load(file)
    return histories

def clear_chat_history(session_id=None):
    """Delete specific or all chat histories."""
    if session_id:
        filepath = os.path.join(CHAT_HISTORY_DIR, f"{session_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    else:
        for filename in os.listdir(CHAT_HISTORY_DIR):
            filepath = os.path.join(CHAT_HISTORY_DIR, filename)
            os.remove(filepath)
        return True

@app.route('/get_all_sessions', methods=['GET'])
def get_all_sessions():
    """Fetch all stored chat histories."""
    return jsonify({"status": "success", "sessions": load_chat_histories()})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear chat history for a specific session or all."""
    data = request.json
    session_id = data.get('session_id')

    if session_id:
        if clear_chat_history(session_id):
            return jsonify({"status": "success", "message": f"Session {session_id} cleared."})
        else:
            return jsonify({"status": "error", "message": "Session not found."})
    else:
        clear_chat_history()
        return jsonify({"status": "success", "message": "All sessions cleared."})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    model_name = data.get('model_name')
    input_text = data.get('input')
    session_id = data.get('session_id', str(uuid.uuid4()))
    model = model_manager.get_model(model_name)

    if not model:
        return jsonify({"status": "error", "message": "Model not found."})

    try:
        result = model.predict(input_text)

        # Save chat history
        chat_history = load_chat_histories().get(session_id, [])
        chat_history.append({"user": input_text, "model": result})
        save_chat_history(session_id, chat_history)

        return jsonify({"status": "success", "result": result, "session_id": session_id})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
