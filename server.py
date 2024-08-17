from flask import Flask, send_from_directory, jsonify
import subprocess
import os

app = Flask(__name__)

# Define the directory to serve
BASE_DIR = os.path.dirname(__file__)
DIST_DIR = os.path.join(BASE_DIR, 'dist')

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    # Execute the Python script
    try:
        result = subprocess.run(
            ['python', os.path.join(DIST_DIR, 'error_message.py')],
            capture_output=True, text=True, check=True
        )
        return jsonify({"status": "success", "output": result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": str(e), "output": e.output})

if __name__ == '__main__':
    app.run(port=8000, debug=True)
