from flask import Flask
from app.controllers.image_controller import image_blueprint
from app.controllers.deployment_controller import deployment_blueprint
from app.controllers.pipeline_controller import pipeline_blueprint

app = Flask(__name__)

app.register_blueprint(image_blueprint, url_prefix='/api/images')
app.register_blueprint(deployment_blueprint, url_prefix='/api/deployments')
app.register_blueprint(pipeline_blueprint, url_prefix='/api/pipelines')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)