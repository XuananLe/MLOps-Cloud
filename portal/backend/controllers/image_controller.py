from flask import Blueprint, request, jsonify
from app.services.image_service import get_images

image_blueprint = Blueprint('images', __name__)

@image_blueprint.route('/', methods=['GET'])
def list_images():
    project_id = request.args.get('project_id')
    repository_name = request.args.get('repository_name')
    location = request.args.get('location')
    images = get_images(project_id, repository_name, location)
    return jsonify(images)