import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import requests
import json

class FetchDataFromAPI(beam.DoFn):
    def process(self, element):
        url = 'http://127.0.0.1:5003/data'
        response = requests.get(url, stream=True)
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data:'):
                    json_str = decoded_line[5:]
                    json_str = json_str.replace("'", '"')
                    try:
                        data = json.loads(json_str)
                        yield data
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        continue

class NormalizeAndRound(beam.DoFn):
    def process(self, element):
        element.pop('timestamp', None)
        normalized_y = (element['y'] - 0) / (10 - 0)
        normalized_x = (element['x'] - 0) / (10 - 0)
        element['x'] = round(element['x'], 2)
        element['y'] = round(element['y'], 2)
        element['normalized_x'] = round(normalized_x, 2)
        element['normalized_y'] = round(normalized_y, 2)
        yield element

def run_pipeline():
    options = PipelineOptions(
        flags=None,
        runner='DataflowRunner',
        project='k8ss-441616',
        region='us-central1',
        temp_location='gs://cloud-computing-job123/temp/',
        staging_location='gs://cloud-computing-job123/staging/'
    )
    
    with beam.Pipeline(options=options) as pipeline:
        (
            pipeline
            | 'Start Streaming Data' >> beam.Create([None])
            | 'Fetch Data from API' >> beam.ParDo(FetchDataFromAPI())
            | 'Normalize and Round Data' >> beam.ParDo(NormalizeAndRound())
            | 'Print Results' >> beam.Map(print)
        )

if __name__ == '__main__':
    run_pipeline()
