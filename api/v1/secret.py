from typing import Tuple

from flask import make_response, request
from flask_restful import Resource

from tools import secrets_tools


class API(Resource):  # pylint: disable=C0111
    url_params = [
        '<int:project_id>/<string:secret>',
    ]

    def __init__(self, module):
        self.module = module

    def get(self, project_id: int, secret: str) -> Tuple[dict, int]:  # pylint: disable=R0201,C0111
        # Check project_id for validity
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        # Get secret
        secrets = secrets_tools.get_project_secrets(project.id)
        _secret = secrets.get(secret) if secrets.get(secret) else secrets_tools.get_project_hidden_secrets(project.id).get(secret)
        return make_response({"secret": _secret}, 200)

    def post(self, project_id: int, secret: str) -> Tuple[dict, int]:  # pylint: disable=C0111
        data = request.json
        # Check project_id for validity
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        # Set secret
        secrets = secrets_tools.get_project_secrets(project.id)
        secrets[secret] = data["secret"]
        secrets_tools.set_project_secrets(project.id, secrets)
        return make_response({"message": f"Project secret was saved"}, 200)

    def put(self, project_id: int, secret: str) -> Tuple[dict, int]:  # pylint: disable=C0111
        # Check project_id for validity
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        # Set secret
        secrets = secrets_tools.get_project_secrets(project.id)
        hidden_secrets = secrets_tools.get_project_hidden_secrets(project.id)
        hidden_secrets[secret] = secrets[secret]
        secrets.pop(secret, None)
        secrets_tools.set_project_secrets(project.id, secrets)
        secrets_tools.set_project_hidden_secrets(project.id, hidden_secrets)
        return make_response({"message": f"Project secret was moved to hidden secrets"}, 200)

    def delete(self, project_id: int, secret: str) -> Tuple[dict, int]:  # pylint: disable=C0111
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        secrets = secrets_tools.get_project_secrets(project.id)
        if secret in secrets:
            del secrets[secret]
        secrets_tools.set_project_secrets(project.id, secrets)
        return make_response({"message": "deleted"}, 204)
