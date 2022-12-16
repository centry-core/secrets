from typing import Tuple

from flask import request
from flask_restful import Resource

from tools import secrets_tools


class API(Resource):  # pylint: disable=C0111
    url_params = [
        '<int:project_id>',
    ]

    def __init__(self, module):
        self.module = module
        
    def get(self, project_id: int) -> Tuple[list, int]:  # pylint: disable=R0201,C0111
        # Check project_id for validity
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        # Get secrets
        secrets_dict = secrets_tools.get_project_secrets(project.id)
        resp = []
        for key in secrets_dict.keys():
            resp.append({"name": key, "secret": "******"})
        return resp, 200

    def post(self, project_id: int) -> Tuple[dict, int]:  # pylint: disable=C0111
        # Check project_id for validity
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        data = request.json
        # Set secrets
        secrets_tools.set_project_secrets(project.id, data["secrets"])
        return {"message": f"Project secrets were saved"}, 200
