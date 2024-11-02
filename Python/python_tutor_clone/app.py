from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_code():
    code = request.json.get('code')
    try:
        # Create a temporary Python file
        with open('temp.py', 'w') as f:
            f.write(code)

        # Execute the code
        result = subprocess.run(['python3', 'temp.py'], capture_output=True, text=True)
        output = result.stdout + result.stderr
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
