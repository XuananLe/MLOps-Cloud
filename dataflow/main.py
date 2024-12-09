import os
from pathlib import Path
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.pubsub import ReadFromPubSub as BeamPubSub
from apache_beam.io.gcp.bigquery import WriteToBigQuery as BeamBigQuery
from apache_beam.transforms.window import FixedWindows
from google.cloud import pubsub_v1
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(Path(__file__).parent.parent / 'mlops-gcs.json')
PROJECT_ID = 'k8ss-441616'
REGION = 'us-central1'
BIGQUERY_TABLE = 'k8ss-441616.mlops_project.data'
SUBSCRIPTION_IDS = ['mlops-sub-1', 'mlops-sub-2', 'mlops-sub-3', 'mlops-sub-4', 'mlops-sub-5']
TMP_BUCKET = 'gs://dataflow-apache-quickstart_k8ss-441616/temp/'
subscriber = pubsub_v1.SubscriberClient()

class NormalizeAndRound(beam.DoFn):
    def process(self, element):
        if isinstance(element, beam.io.gcp.pubsub.PubsubMessage):
            try:
                element = json.loads(element.data.decode('utf-8'))
            except json.JSONDecodeError:
                return

        element.pop('timestamp', None)

        normalized_y = (element['y'] - 0) / (10 - 0)
        normalized_x = (element['x'] - 0) / (10 - 0)
        
        element['x'] = round(element['x'], 2)
        element['y'] = round(element['y'], 2)
        element['normalized_x'] = round(normalized_x, 2)
        element['normalized_y'] = round(normalized_y, 2)
        print(element)
        yield element

def run_pipeline():
    beam_options = PipelineOptions([
        '--runner=DataflowRunner',
        f'--region={REGION}',
        f'--project={PROJECT_ID}',
        f'--temp_location={TMP_BUCKET}',
        '--streaming'
    ])

    with beam.Pipeline(options=beam_options) as pipeline:
        messages = (
            pipeline
            | 'Read from PubSub' >> BeamPubSub(
                subscription=subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_IDS[-1]),
                with_attributes=True
            )
            | 'Window into Fixed Intervals' >> beam.WindowInto(FixedWindows(60))
        )

        processed_data = (
            messages
            | 'Normalize and Round Data' >> beam.ParDo(NormalizeAndRound())
        )

        processed_data | 'Write to BigQuery' >> BeamBigQuery(
            table=BIGQUERY_TABLE,
            schema='x:FLOAT,y:FLOAT',
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        )

if __name__ == '__main__':
    run_pipeline()