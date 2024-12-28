import os

KUBECONFIG_PATH = os.path.join(os.path.dirname(__file__), '.kubeconfig3')
GCP_CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')