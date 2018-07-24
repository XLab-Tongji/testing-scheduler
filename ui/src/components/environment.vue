<template>
<div class="wrapper wrapper-content">
	<div class="row">
        <div class="col-lg-offset-2 col-lg-8">
            <div class="ibox">
                <div class="ibox-content">
                    <h1>SUT</h1>
                    <form method="get" class="form-horizontal">
                        <div class="form-group">
                            <label class="col-lg-3 control-label">Cluster</label>
                            <div class="col-lg-5">
                                <input type="text" class="form-control" placeholder="192.168.1.1">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-lg-3 control-label"></label>
                            <div class="col-lg-5">
                                <input type="text" class="form-control" placeholder="192.168.1.2">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-lg-3 control-label"></label>
                            <div class="col-lg-5">
                                <input type="text" class="form-control" placeholder="192.168.1.3">
                            </div>
                        </div>

                        <div class="form-group">
                            <label class="col-lg-3 control-label">Config file</label>
                            <div class="col-lg-5">
                                <input type="text" class="form-control" placeholder="/openrc">
                            </div>
                            <div class="col-lg-2"><button class="btn btn-w-m btn-info">upload</button></div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="col-lg-offset-2 col-lg-8">
            <div class="ibox">
                <div class="ibox-content">
                    <h1>Service</h1>
                    <div class="service-table">
                        <table id="serviceList" class="table table-bordered table-hover text-center">
                            <thead>
                                <tr>
                                    <th class="text-center">No</th>
                                    <th class="text-center">Service</th>
                                    <th class="text-center">Time</th>
                                    <th class="text-center">Operation</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="service in serviceList" v-on:click="editService(service.name)" style="cursor: pointer;">
                                    <td style="vertical-align: middle;">{{ service.id }}</td>
                                    <td style="vertical-align: middle;">{{ service.name }}</td>
                                    <td style="vertical-align: middle;">{{ service.time }}</td>
                                    <td style="vertical-align: middle;"><button type="button" class="btn btn-white" v-on:click.stop="deleteService(service.name)"><i class="fa fa-trash"></i></button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <div>
                            <button class="btn btn-lg btn-success" style="float:right;" v-on:click="addNewService()">  Add  </button>
                        </div>
                    </div>

                    <!-- modal of one service -->
                    <div class="row">
                        <service-modal v-bind:type="type" v-on:service-creation="plusAService" v-on:service-edition="editAServiceName" v-on:creation-fail="creationFailHandler"></service-modal>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import Vue from 'vue'
import service_modal from "./env_component/service_modal.vue"
import showMessage from './message/showMessage.js'

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
    	'service-modal': service_modal
    },
    created: function() {
        var self = this;
        var msgTitle = "GET -- SERVICE LIST";
        var errorInfo = 'Unable to get the service list';
        $.ajax({
            url: this.global.SERVER_ADDR + "env/getAllServices",
            method: "get",
            success: function(data) {
                if(data['code'] == 200) {
                    self.serviceList = data['result'];
                } else {
                    showMessage(data['code'], msgTitle, errorInfo, data['error']);
                }
            },
            error: function(obj, status, msg) {
                showMessage("error", msgTitle, errorInfo, msg);
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
            item['time'] = this.getFormatDate(new Date());
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
            var msgTitle = "GET -- SERVICE";
            var errorInfo = "Unable to get the service: <strong>" + self.type.service + "</strong>";
            $.ajax({
                url: this.global.SERVER_ADDR + "env/getService",
                method: "GET",
                data: {
                    "serviceName": serviceName
                },
                success: function(data) {
                    if(data['code'] == 200) {
                        self.type.tag = "hhh";
                        self.type.content = data['result'];
                        self.type.originName = self.type.service;
                    } else {
                        showMessage(data['code'], msgTitle, errorInfo, data['error']);
                    }
                    
                },
                error: function(obj, status, msg) {
                    showMessage("error", msgTitle, errorInfo, msg);
                }
            });
            $("#myModal").modal("show");
        },
        deleteService: function(serviceName){
            var msgTitle = "DELETE -- SERVICE";
            $.ajax({
                url: this.global.SERVER_ADDR + "env/deleteService",
                method: "POST",
                data: {
                    "serviceName": serviceName
                },
                success: function(data) {
                    if(data['code'] == 200) {
                        showMessage(data['code'], msgTitle, "Delete <strong>" + serviceName + "</strong> successfully.");
                    } else {
                        showMessage(data['code'], msgTitle,  "Failed to delete <strong>" + serviceName + "</strong>", data['error']);
                    }
                },
                error: function(obj, status, msg) {
                    showMessage("error", msgTitle, "Failed to delete <strong>" + serviceName + "</strong>", msg);
                }
            });
            for(var i = 0;i < this.serviceList.length; i++) {
                if(serviceName == this.serviceList[i]['name']) {
                    this.serviceList.splice(i, 1);
                }
            }
        },
        creationFailHandler: function(serviceName) {
            for(var i = 0; i < this.serviceList.length; i++) {
                if(serviceName == this.serviceList[i].name) {
                    this.serviceList.splice(i, 1);
                }
            }
        },
        getFormatDate: function(date) {
            var year = date.getFullYear();
            var month = date.getMonth() + 1;
            var strDate = date.getDate();
            var seperator = "-";
            if(month >= 1 && month <= 9) {
                month = "0" + month;
            }
            if(strDate >= 1 && strDate <= 9) {
                strDate = "0" + strDate;
            }
            var formatDate = year + seperator + month + seperator + strDate;
            return formatDate;
        }
    }
}
</script>