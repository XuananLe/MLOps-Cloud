import subprocess
from app.config import KUBECONFIG_PATH

def run_kubectl_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr}"

def get_running_pods(namespace=None):
    cmd = ["kubectl", "get", "pods", "--all-namespaces"] if not namespace else ["kubectl", "get", "pods", "-n", namespace]
    return run_kubectl_command(cmd)

def apply_yaml(file_path):
    cmd = ["kubectl", "--kubeconfig", KUBECONFIG_PATH, "apply", "-f", file_path]
    return run_kubectl_command(cmd)