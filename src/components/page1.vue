<template>
  <div class="wrapper wrapper-content">
    <div class="row" style="margin-bottom: 20px;">
      <div>
        <ol class="breadcrumb" style="padding-left: 20px">
          <li>
            <router-link to="/" >.</router-link>
          </li>
        </ol>
      </div>
    </div>
    <div id="p2_content1" style="width:1000px" class="row">
      <div class="title-section">
        <p class="subTitle">Test Suites</p>
        <div class="my-button-group">
          <input class="btn btn-info btn-sm my-button-sm" type="button" v-on:click="runTestsuites()" value="Run">
          <input class="btn btn-primary btn-sm my-button-sm" type="button" value="Create"  v-on:click="create">

          <input class="btn btn-danger btn-sm my-button-sm" type="button" value="Delete" v-on:click="deletestory">
        </div>
      </div>
      <table class="my-table table table-bordered" cellspacing="0" cellpadding="0" style="text-align: center;">
        <thead>
        <tr>
          <td class="checkbox1" style="width:20px"><input type="checkbox" v-model="selectAll"> All</td>
          <td class="smallbox" style="with:250px;">TestSuite Name</td>
        </tr>
        </thead>
        <tbody>
        <tr v-for="story in storys">
          <td><input class="checkbox1" style="width:20px" type="checkbox" v-model="selected" :value="story.testsuite"> </td>
          <td class="smallbox" style="with:250px;"><router-link :to="{ path: '/stories', query: { name: story.testsuite }}" >{{story.testsuite}}</router-link></td>

        </tr>
        </tbody>
        <tfoot id="create-box" style="display: none">
        <tr>
          <td class="checkbox1" style="width:20px"><input type="checkbox"> </td>
          <td class="smallbox" style="with:250px;"><input type="text" v-model="newstory" @keydown.enter="additem" ></td>
        </tr>
        </tfoot>
      </table>
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
  </div>
</template>
<script>
import {addClass, removeClass, isContainClass} from '../scri/my-util.js'
import wfresult from './wfresult.vue'
export default {
  name: 'page1',
  data () {
    return {
      newstory : '',
      storys : '',
      service_selected : '',
      SERVER_ADDR: "http://localhost:5000/",
      workflowId: '',
      wfloading: false,
      wfJson: '',
      selected: []
    }
  },
  created: function() {
    var self = this;
    $.ajax({
      url:"http://10.60.38.181:5202/testsuite/list",
      method:"GET",
      data:{},
      success:function (data) {
        if(data['code'] == 200) {
          self.storys = data['result'];

        }
      }
    });
  },
  computed: {
    selectAll: {
      get: function () {
        return this.storys ? this.selected.length == this.storys.length : false;
      },
      set: function (value) {
        var selected = [];

        if (value) {
          this.storys.forEach(function (story) {
            selected.push(story.testsuite);
          });
        }
        this.selected = selected;
      }
    }
},
  methods:{
    create: function () {
      var cbox = document.getElementById("create-box");
      cbox.style.display = "table-footer-group";
    },
    additem: function () {
      var self = this;
      const  storytext = self.newstory.trim()
      if(storytext)
      {
        $.ajax({
          url:"http://10.60.38.181:5202/testsuite/new",
          method:"GET",
          data:{
            suiteName:storytext
          },
          success:function(data){
            if(data['code'] == 200){
              self.storys.push({
                id: self.storys.length + 1 ,
                testsuite: storytext,
              })
            }
          }
        })

      }

      var cbox = document.getElementById("create-box");
      cbox.style.display = "none";
      this.newstory = '';
    },
    deletestory:function () {

      var self = this;
      for(var n in self.selected)
      {
        alert(self.selected[n]);
        $.ajax({
          url:"http://10.60.38.181:5202/testsuite/delete",
          method:"GET",
          data:{
            suiteName: self.selected[n]
          },
          success:function (data) {
            if(data['code'] == 200){
              self.storys = self.storys.filter(story => {
                return story.testsuite !== self.selected[n];
              })
            }
          }
        });
      }
    },
    runTestsuites: function() {
      var self = this;
      $.ajax({
          url: self.SERVER_ADDR + "run-test/story",
          method: "POST",
          data: {
              "service": "logic",
              "stories": "ts_logic_00.yaml"
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
    }
  },
  components: {
    wfresult
  }
}

</script>
