<template>
<div class="col-md-offset-1" >
    <!-- step -->
    <h1 style='padding-left:30px;'>STEP</h1>
    <br>
    <div class="row">
        <div class='col-md-10'>
            <step v-on:stepList="getStepList"></step>
        </div>
    </div>

    <!-- FLOW PART -->
    <h1 style='padding-left:30px;'>FLOW</h1>
    <br>
    <div class="row">
        <div class='row'>
            <button style='margin-left:20px;' class="btn btn-success" type="button" id="new-flow" v-on:click='addSubflow'>&nbsp;&nbsp;<span class="bold">ADD FLOW</span></button>
        </div>
        <div class='col-md-10'>
            <flow v-model='mainflowName' v-bind:stepsRefs='stepNameList' v-bind:flowsRefs='subflowNameList' v-on:orderList='updateOrderList($event, mainflowName)'></flow>
            <div v-for='subflow in subflowList'>
                <flow v-model='subflow.name' v-bind:stepsRefs='stepNameList' v-bind:flowsRefs='subflowNameList' v-on:orderList='updateOrderList($event, subflow.name)'></flow>
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
import step from './step.vue'
import flow from './flow.vue'

export default {
    name: 'editor',
    data: function(){
        return {
            runList: [],
            stepList: [],
            subflowList: [],
            mainOrdersList: [],
            mainflowName: 'main'
        }
    },
    components: {
        step,
        flow
    },
    methods: {
        getStepList: function(stepList) {
            this.stepList = stepList;
        },
        addSubflow: function() {
            this.subflowList.push({'name': '', 'orderList': ''});
        },
        updateOrderList: function(orderList, flowName) {
            console.log("updateOrderList");
            console.log(orderList);
            console.log(flowName);
            console.log("updateOrderList end");
            if(flowName == 'main') {
                this.mainOrdersList = orderList;
            } else {
                for(var i = 0; i < this.subflowList; ++i) {
                    if(this.subflowList[i].name = flowName) {
                        this.subflowList[i].orderList = orderList;
                    }
                }
            }
        }
    },
    computed: {
        stepNameList: function() {
            var stepNameArr = [];
            for(var i = 0; i < this.stepList.length; i++) {
                stepNameArr.push(this.stepList[i].name);
            }
            return stepNameArr;
        },
        subflowNameList: function() {
            var subflowNameArr = [];
            for(var i = 0; i < this.subflowList.length; i++) {
                subflowNameArr.push(this.subflowList[i].name);
            }
            return subflowNameArr;
        }
    }
}
</script>