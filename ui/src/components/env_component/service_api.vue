<template>
	<div class="panel panel-success">
            <div class="panel-heading">
            	<button type="button" class="btn btn-xs btn-danger pull-right" v-on:click="deleteApi(name)">Delete</button> 
                <h5 class="panel-title"> 
                    <a data-toggle="collapse" data-parent="panelParent" v-bind:href="'#' + name + '-collapse'" style="display:block;">{{ name }}</a> 
                </h5> 
            </div> 
            <div  v-bind:id="name + '-collapse'" class="panel-collapse collapse fade"> 
                <div class="panel-body"> 
                    <base-input name="name" v-model="name"></base-input> 
                    <base-input name="method" v-model="method"></base-input> 
                    <base-input name="uri" v-model="uri"></base-input> 
                    <api-param v-bind:params="params"></api-param> 
                </div> 
            </div> 
        </div>
</template>
<script>
import base_input from "./base_input.vue"
import api_param from "./api_param.vue"
export default {
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
    	'base-input': base_input,
    	'api-param': api_param
    },
    methods: {
        deleteApi: function(apiName) {
            this.$emit("delete", apiName);
        }
    }
}
</script>