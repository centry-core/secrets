from typing import Tuple

from flask import request
from flask_restful import Resource

from tools import api_tools, VaultClient


class ProjectAPI(api_tools.APIModeHandler):  # pylint: disable=C0111

    def get(self, project_id: int) -> Tuple[list, int]:  # pylint: disable=R0201,C0111
        # Check project_id for validity
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        vault_client = VaultClient.from_project(project)
        # Get secrets
        secrets_dict = vault_client.get_project_secrets()
        # hs = vault_client.get_project_hidden_secrets() # todo: remove
        resp = []
        for key in secrets_dict.keys():
            resp.append({"name": key, "secret": "******"})
        # for key in hs.keys(): # todo: remove
        #     resp.append({"name": f'!_HIDDEN_{key}', "secret": "******"}) # todo: remove
        return resp, 200

    def post(self, project_id: int) -> Tuple[dict, int]:  # pylint: disable=C0111
        # Check project_id for validity
        project = self.module.context.rpc_manager.call.project_get_or_404(project_id)
        vault_client = VaultClient.from_project(project)
        # Set secrets
        vault_client.set_project_secrets(request.json["secrets"])
        return {"message": f"Project secrets were saved"}, 200


class AdminAPI(api_tools.APIModeHandler):  # pylint: disable=C0111
    def patch(self, project_id: int) -> Tuple[list, int]:  # pylint: disable=R0201,C0111
        # Get secrets
        vault_client = VaultClient()
        secrets_dict = vault_client.get_project_secrets()
        resp = []
        for key in secrets_dict.keys():
            resp.append({"name": key, "secret": "******"})
        vc2 = VaultClient.from_project(project_id)
        return {
            'v': {
                'vault_name': vault_client.vault_name,
                'auth': vault_client.auth
            },
            'v2': {
                'vault_name': vc2.vault_name,
                'auth': vc2.auth.dict()
            },
            'v_secrets': vault_client.get_project_secrets(),
            'v_h_secrets': vault_client.get_project_hidden_secrets(),
            'v_all_secrets': vault_client.get_all_secrets(),
            'resp': resp,
            'pv_secrets': vc2.get_project_secrets(),
            'pv_h_secrets': vc2.get_project_hidden_secrets(),
            'pv_all_secrets': vc2.get_all_secrets(),
        }, 200
    def get(self, project_id: int) -> Tuple[list, int]:  # pylint: disable=R0201,C0111
        # Get secrets
        vault_client = VaultClient()
        secrets_dict = vault_client.get_project_secrets()
        resp = []
        for key in secrets_dict.keys():
            resp.append({"name": key, "secret": "******"})
        return resp, 200

    def post(self, project_id: int) -> Tuple[dict, int]:  # pylint: disable=C0111
        # Set secrets
        vault_client = VaultClient()
        vault_client.set_project_secrets(request.json["secrets"])
        return {"message": f"Project secrets were saved"}, 200


class API(api_tools.APIBase):
    url_params = [
        '<string:mode>/<int:project_id>'
    ]

    mode_handlers = {
        'default': ProjectAPI,
        'administration': AdminAPI,
    }
