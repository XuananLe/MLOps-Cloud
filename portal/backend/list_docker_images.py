from google.cloud import artifactregistry_v1


def list_docker_images(client, project_id, repository_name, location):
    parent = f"projects/{project_id}/locations/{location}/repositories/{repository_name}"

    request = artifactregistry_v1.ListDockerImagesRequest(
        parent=parent,
    )

    page_result = client.list_docker_images(
        request=request,
    )

    result = []

    for response in page_result:
        # Extract the file name and generate a formatted URL
        file_name = response.name.split("/")[-1].split("@")[0]  # Extract the last part as the model name
        formatted_link = f"{repository_name}/{project_id}/{file_name}"
        result.append((file_name, formatted_link))
        # print(f"{file_name} {formatted_link}")
        # print(response)

    return result