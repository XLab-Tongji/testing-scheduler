<template>
<div class="wrapper wrapper-content">
	<div class="row">
        <div class="row">
            <p class="subTitle" style="margin-left: 70px; margin-bottom: 20px;">SUT</p>
        </div>
        <div class="row">
            <form method="get" class="form-horizontal">
                <div class="form-group">
                    <label class="col-sm-2 control-label">Cluster</label>
                    <div class="col-sm-5"><input type="text" class="form-control" placeholder="192.168.1.1"></div>
                </div>
                <div class="form-group">
                    <label class="col-sm-2 control-label"></label>
                    <div class="col-sm-5"><input type="text" class="form-control" placeholder="192.168.1.2"></div>
                </div>
                <div class="form-group">
                    <label class="col-sm-2 control-label"></label>
                    <div class="col-sm-5"><input type="text" class="form-control" placeholder="192.168.1.3"></div>
                </div>

                <div class="form-group">
                    <label class="col-sm-2 control-label">Config file</label>
                    <div class="col-sm-5"><input type="text" class="form-control" placeholder="/openrc"></div>
                    <div class="col-sm-2"><button class="btn btn-w-m btn-info">upload</button></div>
                </div>
            </form>
        </div>
        <div class="hr-line-dashed"></div>
    </div>
    <div class="hr-line-dashed"></div>
    <div class="row">
        <div class="row">
            <span class="serviceTitle" style="font-size: 30px; margin-right: 30px;">Services</span>
        </div>
        <br/>
        <div class="row">
            <div class="service-table col-sm-offset-1 col-sm-7">
                <table id="serviceList" class="table table-bordered table-hover" style="text-align: center;">
                    <thead>
                        <tr>
                            <td>No</td>
                            <td>Service</td>
                            <td>Time</td>
                            <td>Operation</td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="service in serviceList" v-on:click="editService(service.name)">
                            <td>{{ service.id }}</td>
                            <td>{{ service.name }}</td>
                            <td>{{ service.time }}</td>
                            <td><button type="button" class="btn btn-danger" v-on:click.stop="deleteService(service.name)">delete</button></td>
                        </tr>
                    </tbody>
                </table>
                <div>
                    <button class="btn btn-lg btn-success" style="float:right;" v-on:click="addNewService()">  Add  </button>
                </div>
            </div>
        </div>

        <!-- modal of one service -->
        <div class="row">
            <service-modal v-bind:type="type" v-on:service-creation="plusAService" v-on:service-edition="editAServiceName"></service-modal>
        </div>
    </div>
</div>
</template>

<script>
    var baseInput = {
        props: ['name', 'value'],
        data: function() {
            return {
                inputName: this.name,
                inputValue: this.value,
                fake: "abc"
            }
        },
        template: 
        '<div class="form-group"> \
            <label class="col-sm-3 control-label">{{ name }}</label> \
            <div class="col-sm-7"><input type="text" class="form-control" v-bind:value="value" v-on:input="$emit(\'input\', $event.target.value)"></div> \
        </div>'
    };
    var apiParam = {
        props: ["params"],
        watch: {
            params: function(){
                this.$emit("params", this.params);
            }
        },
        methods: {
            addNewParam: function() {
                this.params.push({'name': '', 'description': ''});
            },
            deleteParam: function(name) {
                for(var i = 0;i < this.params.length; i++) {
                    if(name == this.params[i]['name']) {
                        this.params.splice(i, 1);
                    }
                }
            }
        },
        template: 
        '<div> \
             <div class="row"> \
                <label class="col-sm-3 control-label">Params</label> \
                <button type="button" class="btn btn-primary btn-sm" v-on:click="addNewParam()">New</button> \
             </div> \
             <div class="row"> \
                <div class="col-sm-offset-2 col-sm-8"> \
                     <table class="table table-bordered"> \
                        <thead> \
                            <tr> \
                                <td>name</td>\
                                <td>description</td>\
                                <td>operation</td>\
                            </tr> \
                        </thead> \
                        <tbody> \
                            <tr v-for="param in params"> \
                                <td><input type="text" class="form-control" style="border: 0px" v-model="param.name"></td> \
                                <td><input type="text" class="form-control" style="border: 0px" v-model="param.description"></td> \
                                <td><button type="button" class="btn btn-danger" v-on:click="deleteParam(param.name)">delete</button></td> \
                            </tr> \
                        </tbody> \
                     </table> \
                 </div> \
              </div> \
         </div>'
    };
    var serviceApi = {
        props: ['panelParent', 'name', 'method', 'uri', 'params'],
        watch: {
            name: function(val) {
                this.$emit("name", val);
            },
            method: function(val) {
                this.$emit("method", val);
            },
            uri: function(val) {
                this.$emit("uri", val);
            },
            params: function(val) {
                this.$emit("params", val);
            }
        },
        components: {
        	'base-input': baseInput,
        	'api-param': apiParam
        },
        methods: {
            deleteApi: function(apiName) {
                this.$emit("delete", apiName);
            }
        },
        template: 
        '<div class="panel panel-default"> \
            <div class="panel-heading"> \
                <h5 class="panel-title"> \
                    <a data-toggle="collapse" data-parent="panelParent" v-bind:href="\'#\' + name + \'-collapse\'" style="display:block;">{{ name }}</a> \
                    <button type="button" class="btn btn-xs btn-danger" style="float:right;margin-top: -20px;margin-left: 10px;" v-on:click="deleteApi(name)">delete</button> \
                </h5> \
            </div> \
            <div  v-bind:id="name + \'-collapse\'" class="panel-collapse collapse"> \
                <div class="panel-body"> \
                    <base-input name="name" v-model="name"></base-input> \
                    <base-input name="method" v-model="method"></base-input> \
                    <base-input name="uri" v-model="uri"></base-input> \
                    <api-param v-bind:params="params"></api-param> \
                </div> \
            </div> \
        </div>'
    };
    var serviceModal = {
        props: ['type'],
        data: function() {
            return {
                typeTag: this.type.tag,
                ip: "",
                port: "",
                apis: []
            }
        },
        created: function() {
            var self = this;
            $('#myModal').on('show.bs.modal', function () {
                alert("##########modal open!!");
            });
            $('#myModal').on('hidden.bs.modal', function () {
                self.resetModalData();
            });
        },
        watch: {
            type: {
                handler: function(newVal, oldVal) {
                    console.log("###########type is changed!");
                    console.log(oldVal);
                    console.log(newVal);
                    if(newVal.content) {
                       var content = newVal.content;
                       this.ip =  content.ip;
                       this.port = content.port;
                       this.apis = content.apis;
                    } else {
                        this.resetModalData();
                    }
                    console.log("end!");
                },
                deep: true
            }
        },
        methods: {
            addNewApi: function() {
                var newApi = {'name': 'new', 'method': 'GET', 'uri': '', 'params': []};
                this.apis.push(newApi);
            },
            removeApi: function(name) {
                console.log("remove get!");
                console.log(name);
                for(var i = 0; i < this.apis.length; i++) {
                    if(name == this.apis[i]['name']) {
                        this.apis.splice(i, 1);
                    }
                }
            },
            save: function() {
                if(this.type.edit == true) {
                    this.saveEdition();
                } else {
                    this.saveCreation();
                }
                this.resetModalData();
                $("#myModal").modal("hide");
            },
            saveEdition: function() {
                console.log("save edit!!!");
                var self = this;
                $.ajax({
                    url: "http://localhost:8234/editService",
                    method: "post",
                    data: {
                        "oldName": self.type.originName,
                        "newName": self.type.service,
                        "ip": this.ip,
                        "port": this.port,
                        "apis": JSON.stringify(this.apis)
                    },
                    success: function(data) {
                        console.log("#############success edit");
                    }
                });
                var edition = {
                    'oldName': this.type.originName,
                    'newName': this.type.service
                };
                this.$emit("service-edition", edition);
            },
            saveCreation: function() {
                console.log("save creation!!!");
                var self = this;
                $.ajax({
                    url: "http://localhost:8234/createService",
                    method: "post",
                    data: {
                        "name": self.type.service,
                        "ip": this.ip,
                        "port": this.port,
                        "apis": JSON.stringify(this.apis)
                    },
                    success: function(data) {
                        console.log("#############success create");
                    }
                });
                this.$emit("service-creation", this.type.service);
            },
            resetModalData: function() {
                this.ip = "";
                this.port = "";
                this.apis = [];
            },
            getData: function() {
                console.log("apis:");
                for(i in this.apis) {
                    console.log(this.apis[i]);
                }
            }
        },
        components: {
        	'service-api': serviceApi
        },
        template: '<div class="modal inmodal" id="myModal" tabindex="-1" role="dialog" aria-hidden="true"> \
                        <div class="modal-dialog modal-lg"> \
                            <div class="modal-content animated"> \
                                <div class="modal-header"> \
                                    <button type="button" class="close" data-dismiss="modal"> \
                                        <span aria-hidden="true">&times;</span><span class="sr-only">Close</span> \
                                    </button> \
                                    <i class="fa fa-laptop modal-icon"></i> \
                                    <input  type="text" class="form-control modal-title service-title" v-model="type.service" placeholder="please input service name." style="border: 0"> \
                                    <small class="font-bold"></small> \
                                </div> \
                                <div class="modal-body"> \
                                    <div class="row" style=""> \
                                        <form method="get" class="form-horizontal"> \
                                            <div id="service-address"> \
                                                <button class="btn btn-default">Address</button> \
                                                <div class="form-group"> \
                                                    <label class="col-sm-3 control-label">ip</label> \
                                                    <div class="col-sm-7"><input type="text" class="form-control" v-model="ip"></div> \
                                                </div> \
                                                <div class="form-group"> \
                                                    <label class="col-sm-3 control-label">port</label> \
                                                    <div class="col-sm-7"><input type="text" class="form-control" v-model="port"></div> \
                                                </div> \
                                            </div> \
                                            <div class="hr-line-dashed"></div> \
                                            <div id="service-apis"> \
                                                <div id="apis-nav"> \
                                                    <button class="btn btn-default">Apis</button> \
                                                    <button type="button" class="btn btn-primary" v-on:click="addNewApi()">New</button> \
                                                </div> \
                                                <br /> \
                                                <div id="api-panels" class="api col-sm-offset-1 col-sm-10"> \
                                                    <div class="panel-group" id="accordion">  \
                                                        <service-api v-for="api in apis" panel-parent="#accordion" v-bind="api" v-on:name="api.name = $event" v-on:method="api.method = $event" v-on:uri="api.uri = $event" v-on:params="api.params = $event" v-on:delete="removeApi"></service-api> \
                                                    </div> \
                                                </div> \
                                            </div> \
                                        </form> \
                                    </div> \
                                </div> \
                                <div class="modal-footer"> \
                                    <button type="button" class="btn btn-white" v-on:click="getData()">getData</button> \
                                    <button type="button" class="btn btn-white" data-dismiss="modal">Close</button> \
                                    <button type="button" class="btn btn-primary" v-on:click="save()">Save changes</button> \
                                </div> \
                            </div> \
                        </div> \
                    </div>',
    };
    export default {
  		name: 'environment',
        data: function() {
	        return {
	            serviceList: [],
	            type: {
	                edit: true,
	                service: "ansible",
                    tag: "default"
	            }
	        }
        },
        components: {
        	'service-modal': serviceModal
        },
        created: function() {
            var self = this;
            $.ajax({
                url: "http://localhost:8234/getAllService",
                method: "get",
                success: function(data) {
                    if(data['code'] == 200) {
                        self.serviceList = data['result'];
                    }
                }
            });
        },
        methods: {
            addNewService: function(){
                this.type.edit = false;
                this.type.tag = "abc";
                this.type.service = null;
                this.type.originName = null;
                if(this.type.content){
                    this.type.content = null;
                }
                $("#myModal").modal("show");
            },
            plusAService: function(serviceName){
                var item = {'id': '', 'name': '', 'time': ''};
                item['id'] = this.serviceList[this.serviceList.length - 1]['id'] + 1;
                item['name'] = serviceName;
                item['time'] = '2018-01-01';
                this.serviceList.push(item);
            },
            editAServiceName: function(edition) {
                for(var i = 0;i < this.serviceList.length; i++) {
                    if(edition['oldName'] == this.serviceList[i]['name']) {
                        this.serviceList[i]['name'] = edition['newName'];
                    }
                }
            },
            editService: function(serviceName){
                this.type.edit = true;
                this.type.tag = "abc";
                this.type.service = serviceName;
                this.type.originName = serviceName;
                if(this.type.content){
                    this.type.content = null;
                }
                console.log(this.type);
                var self = this;
                $.ajax({
                    url: "http://localhost:8234/getService",
                    method: "get",
                    data: {
                        "serviceName": serviceName
                    },
                    success: function(data) {
                        console.log("#############get service!!!");
                        self.type.tag = "heyheyhey";
                        self.type.content = data['result'];
                        self.type.originName = self.type.service;
                        console.log(self.type.content);
                        console.log("#############end!!!");
                    }
                });
                $("#myModal").modal("show");
            },
            deleteService: function(serviceName){
                $.ajax({
                    url: "http://localhost:8234/deleteService",
                    method: "post",
                    data: {
                        "serviceName": serviceName
                    },
                    success: function(data) {
                        console.log("#############delete service!!!");
                    }
                });
                for(var i = 0;i < this.serviceList.length; i++) {
                    if(serviceName == this.serviceList[i]['name']) {
                        this.serviceList.splice(i, 1);
                    }
                }
            }
        }
    }
</script>