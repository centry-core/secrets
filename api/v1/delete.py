from typing import Tuple

from flask import request, make_response
from flask_restful import Resource

from tools import secrets_tools


class API(Resource):
    url_params = [
        '<int:project_id>',
    ]

    def __init__(self, module):
        self.module = module

    def post(self, project_id: int) -> Tuple[dict, int]:
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        data = request.json
        secrets = secrets_tools.get_project_secrets(project.id)
        for secret in data.get('secrets', []):
            try:
                del secrets[secret]
            except KeyError:
                ...
        secrets_tools.set_project_secrets(project.id, secrets)
        return make_response({"message": "deleted"}, 200)
