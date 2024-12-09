import time
import numpy as np
from flask import Flask, Response

app = Flask(__name__)


def generate_data():
    while True:
        x = np.random.uniform(0, 10)
        noise = np.random.normal(0, 1)
        y = 2 * x + noise
        timestamp = time.time()

        yield f"data: {{'x': {x}, 'y': {y}, 'timestamp': {timestamp}}}\n\n"
        
        time.sleep(1)

@app.route('/data')
def sse_stream():
    return Response(generate_data(), content_type='text/event-stream')
@app.route('/')
def index():
    return "Data generator server is running..., go to /data to get data."

if __name__ == '__main__':
    print("Starting data generator server...")
    app.run(host = "localhost" ,port = 5003, threaded=True)
