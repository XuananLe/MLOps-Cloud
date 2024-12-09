import os
from pathlib import Path
from google.cloud import pubsub_v1

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(Path(__file__).parent.parent / 'mlops-gcs.json')

PROJECT_ID = 'k8ss-441616'
TOPIC_ID = 'mlops'
SUBSCRIPTION_ID = 'mlops-sub-5'
MESSAGE_COUNT = 100

def main():
    subscriber = pubsub_v1.SubscriberClient()
    
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    
    message_counter = 0
    
    def callback(message):
        nonlocal message_counter
        
        print(f"Message {message_counter + 1}: {message.data.decode()}")
        
        message.ack()
        
        message_counter += 1
        
        if message_counter >= MESSAGE_COUNT:
            subscriber.close()
    
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    
    print(f"Listening for {MESSAGE_COUNT} messages on {subscription_path}...")
    
    try:
        streaming_pull_future.result(timeout=60)
    except Exception as e:
        print(f"An error occurred: {e}")
        streaming_pull_future.cancel()

if __name__ == '__main__':
    main()