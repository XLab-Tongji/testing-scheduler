<template>
  <div class="wrapper wrapper-content animated fadeIn">
    <div class="row" style="margin-bottom: 20px;">
      <div class="col-md-8">
        <ol class="breadcrumb" style="padding-left: 20px; font-size: 17px;">
          <li>
            <router-link to="/" >root</router-link>
          </li>
        </ol>
      </div>
    </div>
    <div id="p2_content1" style="" class="row">
      <div class="col-lg-8">
        <div class="ibox">
            <div class="ibox-title">
                <h5 style="font-size:26px;margin-top: -3px;">Test Suite</h5>
                <div class="ibox-tools">
                    <button class="btn btn-info btn-sm my-button-sm" type="button" v-on:click="runTestsuites()">Run</button>
                    <button class="btn btn-success btn-sm my-button-sm" type="button" v-on:click="create()">Create</button>
                    <button class="btn btn-danger btn-sm my-button-sm" v-on:click="deletestory()" type="button">Delete</button>
                    <a class="collapse-link">
                        <i class="fa fa-chevron-up"></i>
                    </a>
                    <a class="fullscreen-link">
                        <i class="fa fa-expand"></i>
                    </a>
                </div>
            </div>
            <div class="ibox-content" style="text-align:center;">
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
        </div>
      </div>

    </div> 
    <hr />

    <div class="row">
      <div class="col-lg-12">
          <div class="ibox">
              <div class="ibox-title">
                  <h5 style="font-size:26px;margin-top: -3px;">Workflow</h5>
                  <div class="ibox-tools">
                      <a class="collapse-link">
                          <i class="fa fa-chevron-up"></i>
                      </a>
                      <a class="fullscreen-link">
                          <i class="fa fa-expand"></i>
                      </a>
                  </div>
              </div>
              <div class="ibox-content" style="padding-top: 30px;">
                <div id="executing" class="row" style="padding: 0 30px 60px;">
                  <div class="col-md-offset-2 col-md-8">
                      <div class="table-responsive">
                        <table class="table text-center" style="margin-top: 30px;">
                          <thead>
                            <tr>
                              <th class="text-center">#</th>
                              <th class="text-center">testcase</th>
                              <th class="text-center">status</th>
                            </tr>
                          </thead>
                          <tbody>                   
                            <tr v-for="testcase in casesInSuite">
                              <td>{{ testcase.id }}</td>
                              <td>{{ testcase.testcase }}</td>
                              <td v-bind:class="statusClass(testcase.status)">{{ testcase.status }}</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                  </div>
                </div>
                <hr class="hr-line-solid"> 
                <div class="row" style="margin-top: 60px;">
                  <wfresult v-bind:workflowId="workflowId" v-bind:wfloading='wfloading' v-bind:wfJson='wfJson' v-on:wfComplete="wfComplete = $event"></wfresult>
                </div>
              </div>
          </div>
      </div>

    </div>

  </div>
</template>
<script>
import {addClass, removeClass, isContainClass} from '../assets/js/my-util.js'
import wfresult from './workflow_graph/wfresult.vue'
import showMessage from './message/showMessage.js'
export default {
  name: 'testsuite',
  data () {
    return {
      newstory : '',
      storys : '',
      service_selected : '',
      workflowId: '',
      wfloading: false,
      wfJson: '',
      selected: [],
      casesInSuite: [],
      running: {
        suiteName: "",
        caseName: ""
      },
      curRunningId: 0,
      wfComplete: false
    }
  },
  created: function() {
    var self = this;
    $.ajax({
      url: this.global.SERVER_ADDR + "testsuite/list",
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
          url: this.global.SERVER_ADDR + "testsuite/new",
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
        // alert(self.selected[n]);
        $.ajax({
          url: this.global.SERVER_ADDR + "testsuite/delete",
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
      if(self.selected.length == 0) {
        showMessage("warning", "run testsuite", "please select one!");
        return;
      } else if(self.selected.length != 1) {
        showMessage("warning", "run testsuite", "sorry, one suite at a time!");
        return;
      }

      self.running.suiteName = self.selected[0];
      $.ajax({
        url: this.global.SERVER_ADDR + "testsuite/content",
        method: "GET",
        data: {
          "suiteName": self.running.suiteName
        },
        success: function(data) {
          if (data['code'] == 200) {
            var caseList = data['result'];
            for(var i=0; i < caseList.length; i++) {
              caseList[i]['status'] = "waiting";
            }
            self.casesInSuite = caseList;
            showMessage("info", "run testsuite", "start to run <strong>" + self.running.suiteName + "</strong>");
            self.runTestcase();
          }
          
        }
      });
   
    },
    runTestcase: function() {
        console.log("######################################## runTestcase!" + this.curRunningId);
        var self = this;
        if (self.curRunningId == self.casesInSuite.length) {
          self.curRunningId = 0;
          console.log("######################################## run at end!");
          return;
        }
        self.wfComplete = false;
        var i = self.curRunningId;
        self.casesInSuite[i]['status'] = "running";
        self.running.caseName = self.casesInSuite[i]['testcase'];
        $.ajax({
          url: self.global.SERVER_ADDR + "execute/testcase",
          method: "POST",
          data: {
              "suiteName": self.running.suiteName,
              "caseName": self.running.caseName
          },
          beforeSend: function(XHR) {
              self.wfloading = true;
              console.log("ajax wfloading true!" + self.running.caseName);
          },
          success: function(data) {
              console.log("ajax run test case success!");
              self.wfloading = false;
              console.log("ajax wfloading false!" + self.running.caseName);
              self.workflowId = data['result']['workflowId'];
              $.ajax({
                  url: self.global.SERVER_ADDR + "story-content",
                  method: "GET",
                  data: {
                      "service":  self.running.suiteName,
                      "story": self.running.caseName
                  },
                  success: function(data) {
                      if(data['code'] == 200) {
                          self.wfJson = data['result']['content'];
                      }
                  }
              });
          }
        });

    },
    statusClass: function(status) {
      if(status == "waiting") {
        return "text-primary";
      }
      if(status == "running") {
        return "text-warning";
      }
      if(status == "pass") {
        return "text-success";
      }
      if(status == "failed") {
        return "text-danger";
      }
    }
  },
  watch: {
    wfComplete: function(val) {
      console.log("################# wfCompelete change:" + val + "  " + this.curRunningId);
      if(val == false) return;
      var i = this.curRunningId++;
      this.casesInSuite[i]['status'] = "pass";
      this.runTestcase();
    }
  },
  components: {
    wfresult
  }
}

</script>
