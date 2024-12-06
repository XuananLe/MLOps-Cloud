import time
import threading
import numpy as np
from flask import Flask, jsonify, Response

app = Flask(__name__)


def generate_data():
    x = 0
    while True:
        noise = np.random.normal(0, 1)
        y = 2 * x + noise
        timestamp = time.time()

        yield f"data: {{'x': {x}, 'y': {y}, 'timestamp': {timestamp}}}\n\n"
        
        x += 1
        time.sleep(1)

@app.route('/data')
def sse_stream():
    return Response(generate_data(), content_type='text/event-stream')

if __name__ == '__main__':
    print("Starting data generator server...")
    app.run(host = "localhost" ,port = 5003, threaded=True)
