import os
from pathlib import Path
import time
import numpy as np
from flask import Flask, Response
from google.cloud import pubsub_v1
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(Path(__file__).parent.parent / 'mlops-gcs.json')
PROJECT_ID = 'k8ss-441616'
TOPIC_ID = 'mlops'
app = Flask(__name__)

def generate_data():
    while True:
        x = np.random.uniform(0, 10)
        noise = np.random.normal(0, 1)
        y = 2 * x + noise
        timestamp = time.time()
        data = f"data: {{'x': {x}, 'y': {y}, 'timestamp': {timestamp}}}\n\n" 
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
        data = data.encode('utf-8')
        future = publisher.publish(topic_path, data)
        print(future.result())
        yield data
        time.sleep(1)

@app.route('/data')
def sse_stream():
    return Response(generate_data(), content_type='text/event-stream')

@app.route('/')
def index():
    return "Data generator server is running..., go to /data to get data."

if __name__ == '__main__':
    app.run(host='localhost', port=5003, threaded=True)