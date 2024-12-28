from flask import Blueprint, request, jsonify
from app.services.deployment_service import deploy_application

deployment_blueprint = Blueprint('deployments', __name__)

@deployment_blueprint.route('/', methods=['POST'])
def create_deployment():
    data = request.json
    deployment_name = data.get('deployment_name')
    image_url = data.get('image_url')
    port = data.get('port')
    result = deploy_application(deployment_name, image_url, port)
    return jsonify({"message": result})