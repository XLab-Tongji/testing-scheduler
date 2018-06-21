<template>
<div class="col-md-offset-1" >
    <!-- step -->
    <h1>STEP</h1>
    <br>
    <div class="row">
        <div class="col-lg-6">
            <div class="ibox float-e-margins">
                <div class="ibox-title">
                    <h5>Step</h5>
                     
                    <div class="ibox-tools">
                        <button class="btn btn-success " type="button" id="new-step">&nbsp;&nbsp;<span class="bold">New Step</span></button>
                            <a class="collapse-link">
                                <i class="fa fa-chevron-up"></i>
                            </a>
                            <a class="close-link">
                                <i class="fa fa-times"></i>
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
                            <select class="select2_demo_3 form-control" id="service">
                                <option></option> 
                                <option v-for='service in dataService' v-bind:value='service'>{{service}}</option>                               
                            </select>
                        </div>
                    </div>
                    <div class="row">
                            <label class="headmsg control-label">Action:</label>
                            <div class="col-md-4">                               
                                <select class="select2_demo_3 form-control" id="action">
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
       
        <div class="col-lg-6">
            <div class="ibox float-e-margins">
                <div class="ibox-title">
                    <h5>StepList</h5>
                    <div class="ibox-tools">
                            <a class="collapse-link">
                                <i class="fa fa-chevron-up"></i>
                            </a>
                            <a class="close-link">
                                <i class="fa fa-times"></i>
                            </a>
                    </div>
                </div>
                <div class="ibox-content" id="step-list">
                    
                </div>
            </div>

        </div>
        <!-- <div class="ibox float-e-margins">
               
        </div> -->
    </div>


    <!-- FLOW PART -->
    <h1>FLOW</h1>
    <br>
    <div class="row">
        <button class="btn btn-success" type="button" id="new-flow">&nbsp;&nbsp;<span class="bold">ADD FLOW</span></button>
        <div class="col-md-2">
           <span class="select-box" >
            <select id="flowSelect" class="select form-control" v-on:change="test" >
                <option value="1">Normal</option>
                <option value="2">Switch</option>
                <option value="3">Parallel</option>
            </select>
            </span>
        </div>
        <br>
        <div id="x1" style="display:block;">
            <!-- Normal -->
            <div class="col-lg-6" id="normalform">
                <br>
                <div>
                    <div class="ibox">
                        <div class="ibox-title">
                            <h5>Normal</h5>
                            <div class="ibox-tools">
                                <a class="collapse-link">
                                    <i class="fa fa-chevron-up"></i>
                                </a>
                                <a class="close-link">
                                    <i class="fa fa-times"></i>
                                </a>
                            </div>
                        </div>
                        <div class="ibox-content">
                           <!-- <div class="form-group">                              
                              <div class="col-lg-6 row"><label>name</label><input id="NName" type="name" placeholder="name" class="form-control"></div>
                           </div> -->
                           <div class="form-group">
                             <div class="col-sm-6">
                                <label>Step</label>
                                <select class="chooseStep select2_demo_3 form-control" id="NStep">
                                        <option></option>
                                </select>
                             </div>
                           </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Switch -->
        <div id="x2" style="display:none;">
            <br>
            <div class="row">
                <div class="col-lg-6">
                    <div class="ibox float-e-margins">
                        <div class="ibox-title">
                            <h5>Switch</h5>
                                
                            <div class="ibox-tools">
                                <button class="btn btn-success " type="button" id="new-case">&nbsp;&nbsp;<span class="bold">New Case</span></button>
                                <a class="collapse-link">
                                    <i class="fa fa-chevron-up"></i>
                                </a>
                                <a class="close-link">
                                    <i class="fa fa-times"></i>
                                </a>
                            </div>
                        </div>
                        <div id="switchcase">
                            <div class="ibox-content">
                                <div class="row">
                                    <div class="form-group">  
                                        <label class="headmsg control-label">CaseValue:</label>  
                                        <div class="col-md-5"><input type="text" class="case form-control"></div>
                                    </div>
                                </div>
                                <div class="row">
                                        <label class="headmsg control-label">Case:</label>
                                        <div class="col-md-4">                               
                                            <select class="chooseStep select2_demo_3 form-control">
                                                <option></option>
                                            </select>
                                        </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Parallel -->
        <div id="x3" style="display:none;">
            <br>
            <div class="row">
                <div class="col-lg-6">
                    <div class="ibox float-e-margins">
                        <div class="ibox-title">
                            <h5>Parallel</h5>
                            <div class="ibox-tools">
                                <button class="btn btn-success " type="button" id="para-step">&nbsp;&nbsp;<span class="bold">New Step</span></button>
                                <a class="collapse-link">
                                    <i class="fa fa-chevron-up"></i>
                                </a>
                                <a class="close-link">
                                    <i class="fa fa-times"></i>
                                </a>
                            </div>
                        </div>
                        <div id="parallel">
                            <div class="ibox-content">
                                <div class="row">
                                    <label class="headmsg control-label">Step:</label>
                                    <div class="col-md-4">                               
                                        <select class="chooseStep select2_demo_3 form-control">
                                            <option></option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-lg-6">
            <div class="ibox float-e-margins">
                <div class="ibox-title">
                    <h5>FlowList</h5>
                    <div class="ibox-tools">
                            <a class="collapse-link">
                                <i class="fa fa-chevron-up"></i>
                            </a>
                            <a class="close-link">
                                <i class="fa fa-times"></i>
                            </a>
                    </div>
                </div>
                <div class="ibox-content" id="flow-list">
                    
                </div>
            </div>

        </div>
    </div>


</div>

</template>
<script>
import '../css/editor.css'
import '../css/iCheck/custom.css'
import '../css/chosen/bootstrap-chosen.css'
import '../css/awesome-bootstrap-checkbox/awesome-bootstrap-checkbox.css'

import '../scri/select2.full.min.js'

export default {
    name: 'editor',
    data: function(){
        return {
            dataService: [],
            dataAction: [],
            dataParam: [],
            data: [],
            runList: []
        }
    },
    mounted: function(){
        $(".select2_demo_3").select2({
            placeholder: "Select a state",
            allowClear: true
        });
        $('.scroll_content').slimscroll({
            height: '200px'
        }); 

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
        $('#new-flow').click(function(){
            self.newFlow();
        });
        $("#new-case").click(function(){
            self.addSwitch();
        });
        $("#para-step").click(function(){
            self.addPara();
        })
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
        update: function(){
            $(".select2_demo_3").select2({
            placeholder: "Select a state",
            allowClear: true
            });
            $('.scroll_content').slimscroll({
                height: '200px'
            }); 

            var stepList = document.getElementById("step-list");
            stepList.innerHTML="";
            var guid = 0;

            $(".chooseStep").select2("val", ""); 
            $('.chooseStep').empty();
            
            var self = this;
            this.data.forEach(function(itemData, index){
                var step = document.createElement('div');
                var id = 'step' + guid++;
                step.setAttribute('id', id);
                step.classList.add("ibox");
                step.classList.add("float-e-margins");
                
                
                $('.chooseStep').append("<option></option>");
                $(".chooseStep").append("<option value='"+(guid-1)+"'>step"+guid+"</option>");

                var parShow = itemData.parameter.join("&nbsp;&nbsp;");
                if(parShow=="") parShow = "None";
                step.innerHTML = [
                    '<div class="ibox-title step">',
                    '  <h5>Step'+(index+1)+'&nbsp;&nbsp;'+itemData.name+'</h5>',
                    '  <div class="ibox-tools">',
                    // '    <a class="collapse-link">',
                    // '      <i class="fa fa-chevron-up"></i>',
                    // '    </a>',
                    '    <a class="close-link">',
                    '      <i class="fa fa-times"></i>',
                    '    </a>',
                    '  </div>',
                    '  <div class="ibox-content">',
                    '    <div class="row">',
                    '      <label class="headmsg control-label">Service:&nbsp;&nbsp;'+itemData.service+'</label>',
                    '    </div>',
                    '    <div class="row">',
                    '      <label class="headmsg control-label">Action:&nbsp;&nbsp;'+itemData.action+'</label>',
                    '    </div>',
                    '    <div class="param row">',
                    '      <label class="headmsg control-label">Parameter:&nbsp;&nbsp;'+parShow+'</label>',
                    '    </div>',
                    '  </div>',
                    '</div>'
                ].join('');

                step.querySelector('.close-link').addEventListener('click', function() {
                    self.data.splice(index, 1);
                    self.update();
                }, false);

                stepList.appendChild(step);
            });            
        },

        updateFlow: function(){
            var flowList = document.getElementById("flow-list");
            flowList.innerHTML="";
            var guid = 0;
            var self = this;
            this.runList.forEach(function(itemData, index){
                var flow = document.createElement('div');
                var id = 'flow' + guid++;
                flow.setAttribute('id', id);
                flow.classList.add("ibox");
                flow.classList.add("float-e-margins");

                if(itemData.type==1){
                    var parShow = 'Step'+(itemData.step+1);
                }
                else if(itemData.type==2){
                    var parShow = "";
                    for(i=0,len=itemData.step.length; i<len; ++i){
                        var temp=[
                            'Case:&nbsp;&nbsp;',
                            itemData.step[i].case,
                            '&nbsp;&nbsp;&nbsp;&nbsp;',
                            'Step',
                            itemData.step[i].step+1,
                            '<br>'
                        ].join('');
                        parShow += temp;
                    }
                    
                }
                else{
                    var parShow = "Parallel:&nbsp;&nbsp;";
                    for(i=0,len=itemData.step.length; i<len; ++i){
                        var temp = [
                            'Step',itemData.step[i]+1,'&nbsp;&nbsp;'
                        ].join('');
                        parShow += temp;
                    }
                }

                
                if(parShow=="") parShow = "None";
                flow.innerHTML = [
                    '<div class="ibox-title step">',
                    '  <h5>Flow'+(index+1)+'</h5>',
                    '  <div class="ibox-tools">',
                    '    <a class="close-link">',
                    '      <i class="fa fa-times"></i>',
                    '    </a>',
                    '  </div>',
                    '  <div class="ibox-content">',
                    '    <div class="row">',
                    '      <label class="headmsg control-label">'+parShow+'</label>',
                    '    </div>',
                    '  </div>',
                    '</div>'
                ].join('');

                
                flow.querySelector('.close-link').addEventListener('click', function() {
                    self.runList.splice(index, 1);
                    self.updateFlow();
                }, false);

                flowList.appendChild(flow);
            });
        },
        
        addSwitch: function(){
            var sw = document.getElementById('switchcase');
            var temp = document.createElement('div');
            temp.classList.add('ibox-content');
            temp.innerHTML=[
                '<div class="row">',
                '    <div class="form-group">',
                '        <label class="headmsg control-label">CaseValue:</label>',
                '        <div class="col-md-5"><input type="text" class="case form-control"></div>',
                '    </div>',
                '</div>',
                '<div class="row">',
                '    <div class="form-group">',
                '        <label class="headmsg control-label">Case:</label>',
                '        <div class="col-md-4">',
                '            <select class="chooseStep select2_demo_3 form-control">',
                '                <option></option>',
                '            </select>',
                '        </div>',
                '    </div>',
                '</div>',
            ].join('');
            sw.appendChild(temp);
            this.update();
        },
        addPara: function(){
            var pa = document.getElementById('parallel');
            var temp = document.createElement('div');
            temp.classList.add('ibox-content');
            temp.innerHTML=[
                '<div class="row">',
                '    <div class="form-group">',
                '        <label class="headmsg control-label">Step:</label>',
                '        <div class="col-md-4">',
                '            <select class="chooseStep select2_demo_3 form-control">',
                '                <option></option>',
                '            </select>',
                '        </div>',
                '    </div>',
                '</div>',
            ].join('');
            pa.appendChild(temp);
            this.update();
        },
        test: function(){
            var Names = $("#flowSelect").val();
            for (var i=1;i<4;i++){
                var tempname=""+i;
                var NewsHot="x"+i;
                if (Names==tempname){
                    var Nnews=document.getElementById(NewsHot);
                    Nnews.style.display='';
                }else{
                    var Nnews=document.getElementById(NewsHot);
                    Nnews.style.display='none'; 
                }
            }
        },
        selectService: function(event){
            var selectedName = $("#service").val();
            this.getServiceContent(selectedName);

            $("#action").select2("val", ""); 
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
                par.push(name+':&nbsp;'+temp);
            }
            this.data.push({name: na, service: ser, action: act, parameter: par});
            this.update();
            $("#service").select2("val", "");
            $("#name").val("");
        },
        newFlow: function(){
            var select = $("#flowSelect").val();
            if(select == 1){
                var stepId = $("#NStep").val();
                var temp = {type:1,step:parseInt(stepId)};
                this.runList.push(temp);
                
                $("#NStep").select2("val", "");
                this.updateFlow();
            }
            if(select == 2){
                var stepId = [];
                // tempCase = [{case:"条件"},{step: id}]
                var switchList = [];
                // switchList.push(tempCase);

                var allStep = $('#switchcase .chooseStep');
                for(var i=0; i<allStep.length; ++i){
                    var chooseStep = allStep[i].value;
                    if(chooseStep==""){
                        alert("Not completed!!!");
                        return;
                    }
                    stepId.push(parseInt(chooseStep));
                }
                var allCase = $('#switchcase .case');
                for(var i=0; i<allCase.length; ++i){
                    var writeCase = allCase[i].value;
                    if(writeCase==""){
                        alert("Not completed!!!");
                        return;
                    }
                    switchList.push({case:writeCase, step:stepId[i]});
                }

                temp = {type:2,step:switchList};
                this.runList.push(temp);

                this.updateFlow();
                $('#switchcase').empty();
                this.addSwitch();
            }
            if(select == 3){
                var tempArr = [];

                var allStep = $('#parallel .chooseStep');
                for(var i=0; i<allStep.length; ++i){
                    var chooseStep = allStep[i].value;
                    if(chooseStep==""){
                        alert("Not completed!!!");
                        return;
                    }
                    tempArr.push(parseInt(chooseStep));
                }

                temp = {type:3,step:tempArr};
                this.runList.push(temp);
                this.updateFlow();
                $('#parallel').empty();
                this.addPara();
            }            
        }
    }
}
</script>