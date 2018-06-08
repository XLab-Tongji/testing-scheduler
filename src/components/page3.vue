<template>
  <div class="wrapper wrapper-content">
    <div class="row" style="margin-bottom: 20px;">
      <div>
        <ol class="breadcrumb" style="padding-left: 20px">
          <li>
            <router-link to="/" >.</router-link>
          </li>
          <li>
            <router-link :to="{ path: '/stories', query: { name: suitename }}" >{{this.$route.query.suiteName}}</router-link>
          </li>
          <li>
            <router-link :to="{ path: '/content', query: { suiteName: suitename, caseName: casename } }">{{this.$route.query.caseName}}</router-link>
          </li>
        </ol>
      </div>
    </div>
    <div id="p2_content1" style="width:1000px" class="row">
      <div class="title-section">
        <p class="subTitle">Test Story Content</p>
        <div class="my-button-group">
          <input class="btn btn-info btn-sm my-button-sm" type="button" v-on:click="runTestcase()" value="Run">
          <input class="btn btn-success btn-sm my-button-sm" type="button" value="Edit">
          <input class="btn btn-danger btn-sm my-button-sm" type="button" value="Delete">
        </div>
      </div>
      <pre style="width: 1000px; height: 500px; margin-top: 20px;">
        {{content}}
      </pre>
    </div>

    <hr />

    <div class="row">
      <div id="content-workflow">
        <div class="workflow-title-section">
          <p class="subTitle margin-right-100">Workflow</p>
          <input class="btn btn-info btn-sm my-button-sm" type="button" value="Save">
          <input class="btn btn-primary btn-sm my-button-sm" type="button" value="Validate">
          <input class="btn btn-danger btn-sm my-button-sm" type="button" value="Clear">
        </div>

        <div id="workflow-graph-section" class="row">
          <div id="executing" class="col-md-2" style="height:600px; margin-right: -20px;">
            <table class="table" style="margin-top: 30px;">
              <tr style="border-top-width: 1px;border-top-style: solid;">
                <td style="padding-right: 8px">1</td>
                <td style="padding-right: 8px">opnfv_bottleneck_ts001.yaml</td>
                <td style="padding-right: 8px"><p class="text-success">pass</p></td>
              </tr>
              <tr style="border-top-width: 1px;border-top-style: solid;">
                <td>2</td>
                <td>opnfv_bottleneck_ts002.yaml</td>
                <td><p class="text-success">pass</p></td>
              </tr >
              <tr style="border-top-width: 1px;border-top-style: solid;">
                <td>3</td>
                <td>opnfv_bottleneck_ts003.yaml</td>
                <td><p class="text-success">pass</p></td>
              </tr>
              <tr style="border-top-width: 1px;border-top-style: solid;">
                <td>4</td>
                <td>opnfv_bottleneck_ts004.yaml</td>
                <td><p class="text-warning">running</p></td>
              </tr>
            </table>
          </div>

          <wfresult v-bind:workflowId="workflowId" v-bind:wfloading='wfloading' v-bind:wfJson='wfJson'></wfresult>
        </div>
      </div>
    </div>

    <div class="row">
      <div id="iframeContainer"></div>
      <div id="workflowId" style="display:none">
          <input name="workflowId" type="hidden" />
          <input name="function" type="hidden" value="graphLoad"/>
          <button id="graphloadbtn" type="button" onclick="graphLoad()"></button>
      </div>
    </div>
  </div>
</template>
<script>
import {addClass, removeClass, isContainClass} from '../scri/my-util.js'
import wfresult from './wfresult.vue'
  var content;
  var suitename;

export default {
  name: 'page3',
  data () {
    return {
      content,
      suitename:this.$route.query.suiteName,
      casename:this.$route.query.caseName,
      SERVER_ADDR: "http://localhost:5000/",
      workflowId: '',
      wfloading: false,
      wfJson: '',
      stories: [],
      services: [
        'greet',
        'yardstick',
        'logic'
      ],
      service_selected: '',
      selected: []
    }
  },
  created: function() {
    var self = this;
    $.ajax({
      url:"http://10.60.38.181:5202/testcase/content",
      method:"GET",
      data:{
        suiteName:  this.$route.query.suiteName,
        caseName: this.$route.query.caseName
      },
      success:function (data) {
        if(data['code'] == 200) {
          self.content = data['result']['content'];
        }
      }
    });
  },
  computed: {
    selectAll: {
      get: function () {
        return this.stories ? this.selected.length == this.stories.length : false;
      },
      set: function (value) {
        var selected = [];

        if (value) {
          this.stories.forEach(function (story) {
            selected.push(story.id);
          });
        }
        this.selected = selected;
      }
    }
  },
  methods: {
    runTestcase: function(){
      var self = this;
      $.ajax({
          url: self.SERVER_ADDR + "run-test/story",
          method: "POST",
          data: {
              "service": this.$route.query.suiteName,
              "stories": this.$route.query.caseName
          },
          beforeSend: function(XHR) {
              self.wfloading = true;
          },
          success: function(data) {
              console.log("ajax run test story!");
              self.wfloading = false;
              self.workflowId = data['result']['workflowId'];
          }
      });

      $.ajax({
          url: self.SERVER_ADDR + "story-content",
          method: "GET",
          data: {
              "service": "logic",
              "story": "ts_logic_00.yaml"
          },
          success: function(data) {
              if(data['code'] == 200) {
                  self.wfJson = data['result']['content'];
              }
          }
      });
    },
    getOutput: function() {
        console.log("get output active!");
        var wfConfigDiv = document.getElementById("workflowId");
        var inputArr = wfDiv.getElementsByTagName("input");
        var idElem = inputArr[0];
        var workflowId = idElem.getAttribute("value");
        var url = "http://localhost:8600/workflow_server/workflow/" + workflowId + "?includeTasks=true";
        $.ajax({
            url: url,
            method: "GET",
            success: function(data) {
                console.log("get output:");
                console.log(data);
            }
        });
    }
  },
  components: {
    wfresult
  }
}
</script>
