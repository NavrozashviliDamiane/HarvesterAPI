import gevent.monkey
gevent.monkey.patch_all()

from flask import Flask
from flask_socketio import SocketIO, emit
import subprocess
import os

# Initialize Flask and Flask-SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def run_scan(domain, tool):
    """Execute theHarvester and emit the results."""
    try:
        result = subprocess.check_output(
            ['python', '/opt/theHarvester/theHarvester.py', '-d', domain, '-b', tool],
            text=True
        )
        # Emit the scan result to the WebSocket client
        socketio.emit('scan_result', {"status": "completed", "domain": domain, "output": result})
    except Exception as e:
        # Emit the error to the WebSocket client
        socketio.emit('scan_result', {"status": "failed", "domain": domain, "error": str(e)})

@socketio.on('start_scan')
def handle_start_scan(data):
    """Handle incoming scan requests from the WebSocket client."""
    domain = data.get("domain")
    tool = data.get("tool", "all")

    # Emit a processing status immediately
    emit("scan_status", {"status": "processing", "domain": domain})

    # Start the scan in a separate greenlet
    gevent.spawn(run_scan, domain, tool)

# The entry point for Gunicorn
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
