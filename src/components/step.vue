<template>
<!-- step -->
<div class="row">
    <div class="col-lg-12">
        <div class="ibox float-e-margins">
            <div class="ibox-title">
                <h5>Step</h5>
                 
                <div class="ibox-tools" style="height: 25px;">
                    <button class="btn btn-success " type="button" id="new-step">&nbsp;&nbsp;<span class="bold">New Step</span></button>
                        <a class="collapse-link" >
                            <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                        </a>
                </div>
            </div>
            <div class="ibox-content">
                <div class="row">
                    <div class="form-group">  
                        <label class="headmsg control-label">Name:</label>  
                        <div class="col-md-5"><input type="text" class="form-control" id="name"></div>
                    </div>
                </div>
                
                <div class="row">
                    <label class="headmsg control-label">Service:</label>
                    <div class="col-md-4">
                        <select class="form-control" id="service">
                            <option></option> 
                            <option v-for='service in dataService' v-bind:value='service'>{{service}}</option>                               
                        </select>
                    </div>
                </div>
                <div class="row">
                        <label class="headmsg control-label">Action:</label>
                        <div class="col-md-4">                               
                            <select class="form-control" id="action">
                                <option></option>
                                <option v-for='action in dataAction' v-bind:value='action.name'>{{action.name}}</option>  
                            </select>
                        </div>
                </div>
                <div class="row" id="parameter">
                    <div class="form-group" v-for='(param, index) in dataParam'>
                        <label class="headmsg control-label" v-bind:title="param.description">{{ param.name }}
                        </label>
                        <div class="col-md-5">
                            <input type="text" class="form-control"  v-bind:placeholder="param.description" v-bind:id="'par'+index">
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
   
    <div class="col-lg-12">
        <div class="ibox float-e-margins">
            <div class="ibox-title">
                <h5>StepList</h5>
                <div class="ibox-tools">
                        <a class="collapse-link">
                            <i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                        </a>
                </div>
            </div>
            <div class="ibox-content" id="step-list">
            	<div v-for='(step, index) in stepList' class='ibox'>
                	<div class="ibox-title step">
                		<h5>Step{{index + 1}} &nbsp;&nbsp; {{step.name}} </h5>
                		<div class="ibox-tools">
                			<a class="collapse-link">
                            	<i class="fa fa-chevron-up" v-on:click.stop='collapseBox'></i>
                        	</a>
                			<a class="close-link" v-on:click='removeStep(index)'>
                				<i class="fa fa-times"></i>
                			</a>
                		</div>
                	</div>
                	<div class="ibox-content">
                		<div class="row">
                			<label class="control-label">Service: {{ step.service }}</label>
                        </div>
                    	<div class="row">
                          <label class="control-label">Action: {{ step.action }}</label>
                        </div>
                   		<div class="param row">
                          <label class="control-label">Parameter: {{step.params.join('&nbsp;&nbsp;')}}</label>
                        </div>

                   	</div>
                </div>
            </div>
        </div>

    </div>
</div>
</template>
<script>

export default {
	name: 'step',
	data: function() {
		return {
			dataService: [],
            dataAction: [],
            dataParam: [],
            stepList: []
		}
	},
	mounted: function() {
        this.getServiceList();
        var self = this;
        $("#service").change(function(){
            self.selectService();
        });
        $("#action").change(function(){
            self.selectAction();
        });
        $('#new-step').click(function(){
            self.newStep();
        });
	},
	methods: {
		getServiceList: function(){
            console.log("get serviceList!");
            var self = this;
            $.ajax({
                url: "http://10.60.38.181:5202/service/list",
                method: "GET",
                async:false,
                success: function(data){
                    console.log("ajax success!");
                    if(data['code'] == 200){
                        self.dataService = [];
                        self.dataService = data['result'];
                    }
                }
            });
        },
        getServiceContent: function(name){
            var self = this;
            $.ajax({
                url: "http://10.60.38.181:5202/service/content",
                method: "GET",
                async:false,
                data: {
                    "serviceName": name
                },
                success: function(data){
                    if(data['code'] == 200){
                        self.dataAction = [];
                        self.dataAction = data['result']['actions'];
                    }
                }
            });
        },
        getParams: function(name){
            for(var i in this.dataAction){
                if(this.dataAction[i].name == name){
                    this.dataParam = [];
                    this.dataParam = this.dataAction[i].params;
                    break;
                }
            }
        },
        selectService: function(event){
            var selectedName = $("#service").val();
            this.getServiceContent(selectedName);
        },
        selectAction: function(event){
            var selectedName = $("#action").val();
            if(selectedName=="") {
                this.dataParam = [];
                return;
            }
            this.getParams(selectedName);
            if(this.dataParam==undefined) this.dataParam = [];
            
        },
        newStep: function(){
            var ser = $("#service").val();
            var act = $("#action").val();
            var na = $("#name").val();
            if(ser==""||act==""||na==""){
                alert('Not completed!');
                return;
            } 
            var parCount = this.dataParam.length;
            var par = [];
            for(var i=0; i<parCount; ++i){
                var temp = $('#par'+i).val();
                if(temp==""){
                    alert('Not completed!');
                    return;
                } 
                var name = this.dataParam[i].name;
                par.push(name+': '+temp);
            }
            this.stepList.push({name: na, service: ser, action: act, params: par});
            $("#name").val("");
            $("#service").val("");
            this.dataAction = [];
            this.dataParam = [];
        },
       	
        removeStep: function(index) {
        	this.stepList.splice(index, 1);
        },
        collapseBox: function(event) {
        	console.log("collapse");
        	var ele = event.target;
        	console.log(event);
        	console.log(ele);
        	var ibox = $(ele).closest('div.ibox');
        	var content = ibox.children('.ibox-content');
        	content.slideToggle(200);
            $(ele).toggleClass('fa-chevron-up').toggleClass('fa-chevron-down');
        }
	},
	watch: {
		stepList: function() {
			this.$emit('stepList', this.stepList);
		}
	}
}
</script>