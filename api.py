from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    domain = data.get('domain')
    tool = data.get('tool', 'all')

    try:
        result = subprocess.check_output(
            ['python', '/opt/theHarvester/theHarvester.py', '-d', domain, '-b', tool],
            text=True
        )
        return jsonify({"status": "success", "output": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
