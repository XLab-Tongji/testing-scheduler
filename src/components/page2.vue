<template>
  <div class="wrapper wrapper-content">
    <div class="row" style="margin-bottom: 20px;">
      <div>
        <ol class="breadcrumb" style="padding-left: 20px">
          <li>
            <router-link to="/" >.</router-link>
          </li>
          <li>
            <router-link :to="{ path: '/stories', query: { name: sname }}">{{this.$route.query.name}}</router-link>
          </li>
        </ol>
      </div>
    </div>
    <div id="p2_content1" style="width:1000px" class="row">
      <div class="title-section">
        <p class="subTitle">Test Stories</p>
        <div class="my-button-group">
          <input class="btn btn-info btn-sm my-button-sm" type="button" value="Run">
          <input class="btn btn-primary btn-sm my-button-sm" type="button" value="Create"  v-on:click="create" >
          <input class="btn btn-danger btn-sm my-button-sm" type="button" value="Delete"  v-on:click="deleteyaml" >
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
        <tr v-for="yaml in yamls">
          <td><input class="checkbox1" style="width:20px" type="checkbox" v-model="selected" :value="yaml.testcase"> </td>
          <td class="smallbox" style="with:250px;"><router-link :to="{ path: '/content', query: { suiteName: sname, caseName: yaml.testcase } }">{{yaml.testcase}}</router-link></td>
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
          <div>
            <div id="file-section1" class="col-sm-offset-1 col-md-3" style="margin-left: 200px;">
              <div id="workflow-content-div">
                <div class="dark-gray-bg">WORKFLOW YML CONTENT</div>
                <pre id="workflow-content">
{
 "name": "workflow_ts_yardstick_01(3886887794)",
 "description": "",
 "version": 1,
 "schemaVersion": 2,
 "tasks": [
  {
   "taskReferenceName": "task_4605256601",
   "type": "HTTP",
   "name": "test-tc-019",
   "inputParameters": {
    "http_request": {
     "body": {
      "action": "run_test_case",
      "args": {
       "testcase": "./opnfv_yardstick_tc019"
      }
     },
     "uri": "http://10.60.38.173:5000/yardstick/testcases/release/action",
     "method": "POST"
    }
   }
  }
 ],
 "outputParameters": {
  "test-tc-019(task_4605256601)": "${task_4605256601.output.response.body}"
 }
}
                                    </pre>
              </div>
            </div>

            <div class="col-sm-offset-1 col-md-3" id="graph-show-section" style="height:600px;">
              <div class="my-hidden1" id="workflow-graph" style="margin-top: 10px;margin-left: 70px;">
                <img src="image/graph.png" width="250px" height="300px">
              </div>
              <div class="spiner-example my-hidden" id="loading">
                <div class="sk-spinner sk-spinner-three-bounce">
                  <div class="sk-bounce1"></div>
                  <div class="sk-bounce2"></div>
                  <div class="sk-bounce3"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
var yamls;
var sname;
export default {

  name: 'page1',
  data () {
    return {
      yamls,
      sname: this.$route.query.name,
      newstory:'',
      addstory:'',
      selected: []
    }
  },
  created: function() {
    var self = this;
    $.ajax({
      url:"http://10.60.38.181:5202/testsuite/content",
      method:"GET",
      data:{
        suiteName:  this.$route.query.name
      },
      success:function (data) {
        if(data['code'] == 200) {
          self.yamls = data['result'];
        }
      }
    });
  },
  computed: {
    selectAll: {
      get: function () {
        return this.yamls ? this.selected.length == this.yamls.length : false;
      },
      set: function (value) {
        var selected = [];

        if (value) {
          this.yamls.forEach(function (yaml) {
            selected.push(yaml.testcase);
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
      if(storytext )
      {
        $.ajax({
          url:"http://10.60.38.181:5202/testcase/new",
          method:"GET",
          data:{
            suiteName: self.sname,
            caseName: storytext
          },
          success:function (data) {
            if(data['code'] == 200){
              self.yamls.push({
                id: self.yamls.length + 1 ,
                testcase: storytext,
              })
            }
          }
        })

      }
      var cbox = document.getElementById("create-box");
      cbox.style.display = "none";
      this.newstory = '';
    },
    deleteyaml:function () {
      var self = this;
      for(var n in self.selected)
      {
        alert(self.sname);
        alert(self.selected[n]);
        $.ajax({
          url:"http://10.60.38.181:5202/testcase/delete",
          method:"GET",
          data:{
            suiteName: self.sname,
            caseName: self.selected[n]
          },
          success:function (data) {
            alert(data['code']);
            if(data['code'] == 200)
            {
              self.yamls = self.yamls.filter(yaml => {
                return yaml.testcase !== self.selected[n]

              })
            }

          }
        })

      }

    },
    addyaml:function () {
      const  yamltext = this.addstory.trim()
      if(yamltext)
      {
        this.yamls.push({
          id: this.yamls.length + 1 ,
          storyname: yamltext,
        })
      }
      var cbox = document.getElementById("add-box");
      cbox.style.display = "none";
      this.addstory = '';

    }
  }
}
</script>
