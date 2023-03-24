const SecretCreateModal = {
    data() {
        return {
            secretData: {
                name: '',
                value: '',
            },
            isLoading: false,
        }
    },
    methods: {
        saveSecret() {
            this.isLoading = true;
            const api_url = this.$root.build_api_url('secrets', 'secret')
            fetch(`${api_url}/${getSelectedProjectId()}/${this.secretData.name}`,{
                method: 'POST',
                headers: {'Content-Type': 'application/json', dataType: 'json'},
                body: JSON.stringify({
                    "secret": this.secretData.value,
                })
            }).then(data => {
                this.isLoading = false;
                this.secretData.name = '';
                this.secretData.value = '';
                $('#secretCreateModal').modal('hide');
                this.$emit('refresh-table');
                showNotify('SUCCESS', 'Secret created.');
            }).catch(err => {
                this.isLoading = false;
                showNotify('ERROR', err);
            })
        },
    },
    template: `
        <div class="modal modal-small fixed-left fade shadow-sm" tabindex="-1" role="dialog" id="secretCreateModal">
            <div class="modal-dialog modal-dialog-aside" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="row w-100">
                            <div class="col">
                                <h2>Create secret</h2>
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
                                    <label for="SecretName" class="font-weight-bold mb-1">Name</label>
                                    <input
                                        id="SecretName"
                                        type="text"
                                        v-model="secretData.name"
                                        placeholder="Secret name">
                                </div>
                                <div class="custom-input mb-3 w-100">
                                    <label for="SecretValue" class="font-weight-bold mb-1">Value</label>
                                    <input
                                        id="SecretValue"
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
