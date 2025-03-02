from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

all_data = []
alerts = []

def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp / 1e6).strftime('%Y-%m-%d %H:%M:%S')


@app.route('/add_message', methods=['POST'])
def add_message():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
        all_data.append(data)
        print("Received data:", data)
        return jsonify({'message': 'Data received successfully', 'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


'''
def get_completion(prompt):
    return "OK"

@app.route("/", methods=['POST', 'GET']) 
def query_view(): 
    if request.method == 'POST': 
        print('step1') 
        prompt = request.form['prompt'] 
        response = get_completion(prompt) 
        print(response) 
        return jsonify({'response': response}) 
    return render_template('index.html') 
'''
  
@app.route("/", methods=['POST', 'GET']) 
def query_view(): 
    if request.method == 'POST': 
        data = {}
        data['question'] = request.form['prompt']
        
        # Handling chatbot queries
        if "question" in data:
            question = data["question"].lower()

            if "how many cameras" in question:
                unique_devices = list(set(d["DeviceName"] for d in all_data))
                if len(unique_devices) == 0:
                    return jsonify({'response': "No devices yet ! "})
                return jsonify({'response': "We have "+str(len(unique_devices))+" cameras. The camera name is/are : "+str(unique_devices)})

            elif "happening" in question:
                person_detections = [convert_timestamp(d['Timestamp']) for d in all_data if d["BBoxes_xyxy"].get("person")]
                return jsonify({'response': person_detections if person_detections else "No activity detected"})

            elif "list of objects" in question:
                unique_objects = set()
                for d in all_data:
                    unique_objects.update(d["BBoxes_xyxy"].keys())
                return jsonify({'response': list(unique_objects) if len(unique_objects) != 0 else "No objects seen!"})

            elif "set a alert" in question:
                alerts.append("black hoodie")
                return jsonify({'response': "OK"})

            return jsonify({'response': "I don't understand the question."})
            
    return render_template('index.html')  # Serve the frontend for GET requests

if __name__ == '__main__':
    app.run(debug=True)
