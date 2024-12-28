import os
from app.adapters.k8s_adapter import apply_yaml

def deploy_application(deployment_name, image_url, port):
    yaml_template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'template2.yaml')
    temp_yaml_path = os.path.join(os.path.dirname(__file__), '..', 'temp', f'{deployment_name}_deployment.yaml')

    with open(yaml_template_path, 'r') as file:
        yaml_content = file.read()

    yaml_content = yaml_content.replace('{{deployment_name}}', deployment_name)
    yaml_content = yaml_content.replace('{{image_url}}', image_url)
    yaml_content = yaml_content.replace('{{port}}', str(port))

    os.makedirs(os.path.dirname(temp_yaml_path), exist_ok=True)
    with open(temp_yaml_path, 'w') as file:
        file.write(yaml_content)

    return apply_yaml(temp_yaml_path)