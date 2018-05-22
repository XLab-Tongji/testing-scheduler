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
          <input class="btn btn-info btn-sm my-button-sm" type="button" value="Run">
          <input class="btn btn-info btn-sm my-button-sm" type="button" value="Create">
          <input class="btn btn-success btn-sm my-button-sm" type="button" value="Edit">
          <input class="btn btn-danger btn-sm my-button-sm" type="button" value="Delete">
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
        <tr v-for="test in tests">
          <td><input class="checkbox1" style="width:20px" type="checkbox" v-model="selected" :value="test.id"> </td>
          <td class="smallbox" style="with:250px;"><router-link to="/page2" >{{test.storyname}}</router-link></td>
          <td class="smallbox" style="with:100px;">{{test.testname}}</td>
        </tr>
        </tbody>
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
              <tr>
                <td>1</td>
                <td>opnfv_bottleneck_ts001.yaml</td>
                <td><p class="text-success">pass</p></td>
              </tr>
              <tr>
                <td>2</td>
                <td>opnfv_bottleneck_ts002.yaml</td>
                <td><p class="text-success">pass</p></td>
              </tr>
              <tr>
                <td>3</td>
                <td>opnfv_bottleneck_ts003.yaml</td>
                <td><p class="text-success">pass</p></td>
              </tr>
              <tr>
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
      stories: [],
      services: [
        'greet',
        'yardstick',
        'logic'
      ],
      tests: [
        {id: 1, storyname: 'opnfv_k8-nosdn-stor4nfv-ha_daily', testname: 'failed'},
        {id: 2, storyname: 'opnfv_os-nosdn-nofeature-ha_daily', testname: 'pass'},
        {id: 3, storyname: 'opnfv_os-nosdn-nofeature-noha_daily', testname: 'runnig'},
        {id: 4, storyname: 'opnfv_os-nosdn-ovs-noha_daily', testname: 'failed'},
        {id: 5, storyname: 'opnfv_os-odl-dvr-noha_daily', testname: 'pass'},
        {id: 6, storyname: 'opnfv_os-odl-fdio-noha_daily', testname: 'running'}
      ],
      service_selected: '',
      selected: []
    }
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
}
}
</script>
