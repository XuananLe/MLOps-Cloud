from google.cloud import aiplatform
from google.cloud import bigquery
import pandas as pd
import functions_framework

@functions_framework.http
def train_model(request):
    project_id = "k8ss-441616"  
    location = "us-central1"   
    dataset_id = "mlops_project"
    table_id = "data"
    model_display_name = "vertex-bq-auto-model"

    bq_client = bigquery.Client(project=project_id)
    query = f"SELECT x, y FROM `{project_id}.{dataset_id}.{table_id}`"
    print("Fetching data from BigQuery...")
    df = bq_client.query(query).to_dataframe()
    print(f"Fetched {len(df)} rows from BigQuery")

    aiplatform.init(project=project_id, location=location)

    print("Training model using Vertex AI...")
    training_job = aiplatform.AutoMLTabularTrainingJob(
        display_name="auto-training-job",
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
