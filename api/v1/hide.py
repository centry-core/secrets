from typing import Tuple

from flask import make_response
from flask_restful import Resource

from tools import secrets_tools


class API(Resource):
    url_params = [
        '<int:project_id>/<string:secret>',
    ]

    def __init__(self, module):
        self.module = module

    def post(self, project_id: int, secret: str) -> Tuple[dict, int]:
        # Check project_id for validity
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        # Set secret
        secrets = secrets_tools.get_project_secrets(project.id)
        hidden_secrets = secrets_tools.get_project_hidden_secrets(project.id)
        try:
            hidden_secrets[secret] = secrets[secret]
        except KeyError:
            return make_response({"message": "Project secret was not found"}, 404)
        secrets.pop(secret, None)
        secrets_tools.set_project_secrets(project.id, secrets)
        secrets_tools.set_project_hidden_secrets(project.id, hidden_secrets)
        return make_response({"message": "Project secret was moved to hidden secrets"}, 200)
