from google.cloud import aiplatform
from google.cloud import bigquery
import pandas as pd
import functions_framework
import base64

@functions_framework.cloud_event
def train_model(cloud_event):
    message_data = cloud_event.data.get("message", {}).get("data", "")
    if message_data:
        decoded_message = base64.b64decode(message_data).decode("utf-8")
        print(f"Received Pub/Sub message: {decoded_message}")

    project_id = "k8ss-441616"
    location = "us-central1"
    dataset_id = "mlops_project"
    table_id = "data"
    model_display_name = "vertex-bq-auto-model2"

    bq_client = bigquery.Client(project=project_id)
    query = f"SELECT x, y FROM `{project_id}.{dataset_id}.{table_id}`"
    print("Fetching data from BigQuery...")
    df = bq_client.query(query).to_dataframe()
    print(f"Fetched {len(df)} rows from BigQuery")

    aiplatform.init(project=project_id, location=location)
    print("Training model using Vertex AI...")

    training_job = aiplatform.AutoMLTabularTrainingJob(
        display_name="auto-training-job2",
        optimization_prediction_type="regression"
    )

    model = training_job.run(
        dataset=aiplatform.TabularDataset.create_from_dataframe(
            display_name="bq_dataset",
            dataframe=df
        ),
        target_column="y",
        model_display_name=model_display_name,
        sync=True
    )

    print(f"Model {model.display_name} is trained and registered!")
    return {"message": f"Model {model.display_name} registered successfully."}
