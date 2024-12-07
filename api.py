from flask import Flask, request, jsonify
import subprocess
import threading

app = Flask(__name__)

# Dictionary to store scan results by a unique ID
results = {}

def run_scan(scan_id, domain, tool):
    try:
        result = subprocess.check_output(
            ['python', '/opt/theHarvester/theHarvester.py', '-d', domain, '-b', tool],
            text=True
        )
        results[scan_id] = {"status": "success", "output": result}
    except Exception as e:
        results[scan_id] = {"status": "error", "message": str(e)}

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    domain = data.get('domain')
    tool = data.get('tool', 'all')

    # Create a unique scan ID
    scan_id = f"scan-{len(results) + 1}"

    # Run the scan in a background thread
    threading.Thread(target=run_scan, args=(scan_id, domain, tool)).start()

    return jsonify({"status": "processing", "scan_id": scan_id})

@app.route('/scan/<scan_id>', methods=['GET'])
def get_scan(scan_id):
    # Retrieve scan result
    result = results.get(scan_id)
    if result:
        return jsonify(result)
    else:
        return jsonify({"status": "error", "message": "Scan not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
