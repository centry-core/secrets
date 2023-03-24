from typing import Tuple

from flask import request

from tools import api_tools, VaultClient


class ProjectAPI(api_tools.APIModeHandler):
    def post(self, project_id: int) -> Tuple[dict, int]:
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        vault_client = VaultClient.from_project(project)
        data = request.json
        secrets = vault_client.get_project_secrets()
        for secret in data.get('secrets', []):
            try:
                del secrets[secret]
            except KeyError:
                ...
        vault_client.set_project_secrets(secrets)
        return {"message": "deleted"}, 204


class AdminAPI(api_tools.APIModeHandler):
    def post(self, project_id: int) -> Tuple[dict, int]:
        data = request.json
        vault_client = VaultClient()
        secrets = vault_client.get_project_secrets()
        for secret in data.get('secrets', []):
            try:
                del secrets[secret]
            except KeyError:
                ...
        vault_client.set_project_secrets(secrets)
        return {"message": "deleted"}, 204


class API(api_tools.APIBase):
    url_params = [
        '<string:mode>/<int:project_id>'
    ]

    mode_handlers = {
        'default': ProjectAPI,
        'administration': AdminAPI,
    }
