from google.cloud import artifactregistry_v1

def list_docker_images(project_id, repository_name, location):
    client = artifactregistry_v1.ArtifactRegistryClient()
    parent = f"projects/{project_id}/locations/{location}/repositories/{repository_name}"
    request = artifactregistry_v1.ListDockerImagesRequest(parent=parent)
    result = []

    for response in client.list_docker_images(request=request):
        file_name = response.name.split("/")[-1].split("@")[0]
        formatted_link = f"{repository_name}/{project_id}/{file_name}"
        result.append({"name": file_name, "url": formatted_link})
    return result