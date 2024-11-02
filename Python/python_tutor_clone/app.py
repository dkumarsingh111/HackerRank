from flask import Flask, render_template, request, jsonify
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    code = request.json.get('code')
    try:
        # This is where you would use a Python execution environment
        # For safety, you should never use eval on untrusted input
        exec_globals = {}
        exec(code, exec_globals)
        return jsonify(success=True, output="Code executed successfully.")
    except Exception as e:
        return jsonify(success=False, error=str(e), traceback=traceback.format_exc())

if __name__ == '__main__':
    app.run(debug=True)
