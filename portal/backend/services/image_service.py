from app.adapters.gcp_adapter import list_docker_images

def get_images(project_id, repository_name, location):
    return list_docker_images(project_id, repository_name, location)
