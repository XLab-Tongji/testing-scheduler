<template>
<div class="col-md-offset-1" >
    <!-- step -->
    <h1 style='padding-left:30px;'>STEP</h1>
    <br>
    <div class="row">
        <div class='col-md-10'>
            <step v-bind:stepList="stepList" v-on:stepList="getStepList"></step>
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
            <flow v-model='mainflowName' v-bind:orderList='mainOrdersList' v-bind:stepsRefs='stepNameList' v-bind:flowsRefs='flowNameList' v-on:orderList='updateOrderList($event, mainflowName)'></flow>
            <div v-for='subflow in subflowList'>
                <flow v-model='subflow.name' v-bind:orderList='subflow.orderList' v-bind:stepsRefs='stepNameList' v-bind:flowsRefs='flowNameList' v-on:orderList='updateOrderList($event, subflow.name)'></flow>
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
    props: ['saveSignal', 'stepList', 'mainOrdersList', 'subflowList'],
    model: {
        prop: 'saveSignal',
        event: 'saveResponse'
    },
    data: function(){
        return {
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
            this.subflowList.push({'name': '', 'orderList': []});
        },
        updateOrderList: function(orderList, flowName) {
            if(flowName == 'main') {
                this.mainOrdersList = orderList;
            } else {
                for(var i = 0; i < this.subflowList.length; ++i) {
                    if(this.subflowList[i].name == flowName) {
                        this.subflowList[i].orderList = orderList;
                    }
                }
            }
        }
    },
    computed: {
        flowNameList: function() {
            var stepNameArr = [];
            for(var i = 0; i < this.subflowList.length; i++) {
                stepNameArr.push(this.subflowList[i].name);
            }
            console.log(stepNameArr);
            return stepNameArr;
        },
        stepNameList: function() {
            var stepNameArr = [];
            for(var i = 0; i < this.stepList.length; i++) {
                stepNameArr.push(this.stepList[i].name);
            }
            return stepNameArr;
        }
        
    },
    watch: {
        saveSignal: function(newVal) {
            if(newVal == true) {
                console.log("editor newVal true");
                var self = this;
                $.ajax({
                    url: this.global.SERVER_ADDR + "testcase/save",
                    method: "POST",
                    data: {
                        suiteName:  this.$route.query.suiteName,
                        caseName: this.$route.query.caseName,
                        stepList: JSON.stringify(this.stepList),
                        subflowList: JSON.stringify(this.subflowList),
                        mainOrdersList: JSON.stringify(this.mainOrdersList)
                    },
                    success: function(data) {
                        console.log("ajax save content!");
                        if(data['code'] == 200) {
                            self.$emit('saveResponse', true);
                        } else {
                            self.$emit('saveResponse', false);
                        }
                    },
                    error: function(error) {
                        console.log("ajax save content!");
                        self.$emit('saveResponse', false);
                    }
                });
            }
        }
    }
}
</script>