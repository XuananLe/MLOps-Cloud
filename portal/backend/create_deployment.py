import subprocess
import os

kubeconfig_path_global = os.yaml_template_path = os.path.join(os.path.dirname(__file__), '.kubeconfig3')


def get_running_pods(namespace=None):
    try:
        cmd = ["kubectl", "get", "pods", "--all-namespaces"]
        if namespace:
            cmd = ["kubectl", "get", "pods", "-n", namespace]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Error output: {e.stderr}")



def apply_yaml(deployment_name, image_url, port):
    global kubeconfig_path
    yaml_template_path = os.path.join(os.path.dirname(__file__),'yaml', 'template2.yaml')

    with open(yaml_template_path, 'r') as file:
        yaml_content = file.read()

    yaml_content = yaml_content.replace('{{deployment_name}}', deployment_name)
    yaml_content = yaml_content.replace('{{image_url}}', image_url)
    # yaml_content = yaml_content.replace('{{model_url}}', model_url)
    yaml_content = yaml_content.replace('{{port}}', str(port))

    temp_yaml_path = os.path.join(os.path.dirname(__file__), 'yaml', f'{deployment_name}_deployment.yaml')
    os.makedirs(os.path.dirname(temp_yaml_path), exist_ok=True)
    with open(temp_yaml_path, 'w') as file:
        file.write(yaml_content)
    print(f"Generated deployment file: {temp_yaml_path}")

    # Sử dụng kubectl apply để triển khai file YAML
    apply_command = f"kubectl --kubeconfig {kubeconfig_path_global}  apply -f {temp_yaml_path} > kubectl_apply.log 2>&1"
    #
    try:
        subprocess.run(apply_command, shell=True, check=True)
        print(f"Deployment {deployment_name} applied successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error applying deployment: {e}")


def create_deployment(deployment_name, image_url, model_url, port):
    apply_yaml(deployment_name, image_url, model_url, port)




if __name__ == "__main__":
    # Ví dụ sử dụng
    apply_yaml(
        deployment_name="flask-ml-model",
        image_url="quy23/flask-ml-model:latest",
        port=8080
    )
