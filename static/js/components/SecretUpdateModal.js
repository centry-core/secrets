const SecretUpdateModal = {
    props: ['selectedSecret'],
    data() {
        return {
            secretData: {
                name: '',
                value: '',
            },
            isLoading: false,
        }
    },
    mounted() {
        const vm = this;
        $("#secretUpdateModal").on("show.bs.modal", function (e) {
            vm.fetchSecret().then((secret) => {
                vm.secretData.name = vm.selectedSecret.name;
                vm.secretData.value = secret.secret;
            })
        });
    },
    methods: {
        async fetchSecret() {
            // TODO rewrite session
            const api_url = this.$root.build_api_url('secrets', 'secret')
            const resp = await fetch(`${api_url}/${getSelectedProjectId()}/${this.selectedSecret.name}`)
            return resp.json();
        },
        saveSecret() {
            this.isLoading = true;
            const api_url = this.$root.build_api_url('secrets', 'secret')
            fetch(`${api_url}/${getSelectedProjectId()}/${this.secretData.name}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json', dataType: 'json'},
                body: JSON.stringify({
                    "secret": {
                        "old_name": this.selectedSecret.name,
                        "value": this.secretData.value,
                    }
                })
            }).then((response) => response.json())
            .then(data => {
                this.isLoading = false;
                this.secretData.name = '';
                this.secretData.value = '';
                $('#secretUpdateModal').modal('hide');
                this.$emit('refresh-table');
                showNotify('SUCCESS', 'Secret updated.');
            }).catch(err => {
                this.isLoading = false;
                showNotify('ERROR', err);
                console.log(err)
            })
        },
    },
    template: `
    <div class="modal modal-small fixed-left fade shadow-sm" tabindex="-1" role="dialog" id="secretUpdateModal">
    <div class="modal-dialog modal-dialog-aside" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <div class="row w-100">
                    <div class="col">
                        <h2>Update secret</h2>
                    </div>
                    <div class="col-xs d-flex">
                        <button type="button" class="btn btn-secondary mr-2" data-dismiss="modal" aria-label="Close">
                            Cancel
                        </button>
                        <button type="button" 
                            class="btn btn-basic d-flex align-items-center"
                            @click="saveSecret"
                        >Save<i v-if="isLoading" class="preview-loader__white ml-2"></i></button>
                    </div>
                </div>
            </div>
            <div class="modal-body">
                <div class="section">
                    <div class="row" id="secretFields">
                        <div class="custom-input mb-3 w-100">
                            <label for="SecretUpdateName" class="font-weight-bold mb-1">Name</label>
                            <input
                                id="SecretUpdateName"
                                type="text"
                                v-model="secretData.name"
                                placeholder="Secret name">
                        </div>
                        <div class="custom-input mb-3 w-100">
                            <label for="SecretUpdateValue" class="font-weight-bold mb-1">Value</label>
                            <input
                                id="SecretUpdateValue"
                                type="password"
                                v-model="secretData.value"
                                placeholder="Secret value">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
    `
}
