<template>
  <div class="wrapper wrapper-content">
    <div class="row" style="margin-bottom: 20px;">
      <div>
        <ol class="breadcrumb" style="padding-left: 20px">
          <li>
            <router-link to="/" >.</router-link>
          </li>
          <li>
            <router-link to="/page2">opnfv_os-nosdn-nofeature-ha_daily</router-link>
          </li>
        </ol>
      </div>
    </div>
    <div id="p2_content1" style="width:1000px" class="row">
      <div class="title-section">
        <p class="subTitle">Test Stories</p>
        <div class="my-button-group">
          <input class="btn btn-info btn-sm my-button-sm" type="button" value="Run">
          <input class="btn btn-info btn-sm my-button-sm" type="button" value="Create"  v-on:click="create" >
          <input class="btn btn-success btn-sm my-button-sm" type="button" value="Add" v-on:click="Theadd">
          <input class="btn btn-danger btn-sm my-button-sm" type="button" value="Delete"  v-on:click="deleteyaml" >
        </div>
      </div>
      <table class="my-table table table-bordered" cellspacing="0" cellpadding="0" style="text-align: center;">
        <thead>
        <tr>
          <td class="checkbox1" style="width:20px"><input type="checkbox" v-model="selectAll"> All</td>
          <td class="smallbox" style="with:250px;">TestSuite Name</td>
          <td class="smallbox" style="with:100px;">Test Result</td>
        </tr>
        </thead>
        <tbody>
        <tr v-for="yaml in yamls">
          <td><input class="checkbox1" style="width:20px" type="checkbox" v-model="selected" :value="yaml.id"> </td>
          <td class="smallbox" style="with:250px;"><router-link to='/page2/page3'>{{yaml.storyname}}</router-link></td>
          <td class="smallbox" style="with:100px;">{{yaml.testname}}</td>
        </tr>
        </tbody>
        <tfoot id="create-box" style="display: none">
        <tr>
          <td class="checkbox1" style="width:20px"><input type="checkbox" v-model="selectAll"> </td>
          <td class="smallbox" style="with:250px;"><input type="text" v-model="newstory" @keydown.enter="additem" ></td>
          <td class="smallbox" style="with:100px;">-</td>
        </tr>
        </tfoot>
        <tfoot id="add-box" style="display: none">
        <tr>
          <td class="checkbox1" style="width:20px"><input type="checkbox" v-model="selectAll"> </td>
          <td class="smallbox" style="with:250px;"><select v-model="addstory" @keydown.enter="addyaml"><option v-for="yamlfile in yamlfiles">{{yamlfile.storyname}}</option></select></td>
          <td class="smallbox" style="with:100px;">-</td>
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

export default {

  name: 'page1',
  data () {
    return {

      services: [
        'greet',
        'yardstick',
        'logic'
      ],
      yamls: [
        {id: 1, storyname: 'opnfv_bottleneck_ts001.yaml', testname: 'failed'},
        {id: 2, storyname: 'opnfv_bottleneck_ts002.yaml', testname: 'pass'},
        {id: 3, storyname: 'opnfv_bottleneck_ts003.yaml', testname: 'runnig'},
        {id: 4, storyname: 'opnfv_bottleneck_ts004.yaml', testname: 'failed'},
        {id: 5, storyname: 'opnfv_bottleneck_ts005.yaml', testname: 'pass'},
        {id: 6, storyname: 'opnfv_bottleneck_ts006.yaml', testname: 'running'},
        {id: 7, storyname: 'opnfv_bottleneck_ts007.yaml', testname: 'running'},
        {id: 8, storyname: 'opnfv_bottleneck_ts008.yaml', testname: 'running'},
        {id: 9, storyname: 'opnfv_bottleneck_ts009.yaml', testname: 'running'}
      ],
      yamlfiles:[
        {id: 11, storyname: 'opnfv_bottleneck_ts011.yaml', testname: 'failed'},
        {id: 12, storyname: 'opnfv_bottleneck_ts012.yaml', testname: 'pass'},
        {id: 13, storyname: 'opnfv_bottleneck_ts013.yaml', testname: 'runnig'},
        {id: 14, storyname: 'opnfv_bottleneck_ts014.yaml', testname: 'failed'},
        {id: 15, storyname: 'opnfv_bottleneck_ts015.yaml', testname: 'pass'},
        {id: 16, storyname: 'opnfv_bottleneck_ts016.yaml', testname: 'running'},
        {id: 17, storyname: 'opnfv_bottleneck_ts017.yaml', testname: 'running'},
        {id: 18, storyname: 'opnfv_bottleneck_ts018.yaml', testname: 'running'},
        {id: 19, storyname: 'opnfv_bottleneck_ts019.yaml', testname: 'running'}
      ],
      newstory:'',
      addstory:'',
      service_selected: '',
      selected: []
    }
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
            selected.push(yaml.id);
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
      const  storytext = this.newstory.trim()
      if(storytext )
      {
        this.yamls.push({
          id: this.yamls.length + 1 ,
          storyname: storytext,
          testname: 'new'
        })
      }
      var cbox = document.getElementById("create-box");
      cbox.style.display = "none";
      this.newstory = '';
    },
    deleteyaml:function () {

      for(var n in this.selected)
      {
        this.yamls = this.yamls.filter(yaml => {
          return yaml.id !== this.selected[n]

        })
      }

    },
    Theadd: function () {
      var cbox = document.getElementById("add-box");
      cbox.style.display = "table-footer-group";
    },
    addyaml:function () {
      const  yamltext = this.addstory.trim()
      if(yamltext)
      {
        this.yamls.push({
          id: this.yamls.length + 1 ,
          storyname: yamltext,
          testname: 'new'
        })
      }
      var cbox = document.getElementById("add-box");
      cbox.style.display = "none";
      this.addstory = '';

    }
  }
}
</script>
