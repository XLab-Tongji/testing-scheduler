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
          <li>
            <router-link to="/page2/page3">opnfv_yardstick_tc002.yaml</router-link>
          </li>
        </ol>
      </div>
    </div>
    <div id="p2_content1" style="width:1000px" class="row">
      <div class="title-section">
        <p class="subTitle">Test Story Content</p>
        <div class="my-button-group">
          <input class="btn btn-info btn-sm my-button-sm" type="button" value="Run">
          <input class="btn btn-success btn-sm my-button-sm" type="button" value="Edit">
          <input class="btn btn-danger btn-sm my-button-sm" type="button" value="Delete">
        </div>
      </div>
      <pre style="width: 1000px; height: 500px; margin-top: 20px;">
---
schema:
  steps:
    -
      id: 1
      name: inject-cpu-workload
      type: test
      service:
        name: yardtstick
        call: REST
      action: run_testcase
      args:
        method: POST
        args:
          testcase: opnfv_yardstick_tc019

    -
      id: 2
      name: monitor-cpu-utility
      type: test
      service:
        name: functest
        call: REST
      action: run_testcase
      args:
        method: POST
        args:
          testcase: functest_tc019
    -
      id: 3
      name: inject-cpu-faultload
      type: test
      service:
        name: yardtstick
        call: REST
      action: run_testcase
      args:
        method: POST
        command: answer
        args:
          testcase: opnfv_yardstick_tc050

  flows:
    -
      name: main
      orders:
        -
          type: normal
          step: 1
        -
          type: normal
          step: 2
        -
          type: normal
          step: 3
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
              <tr>
                <td>1</td>
                <td>opnfv_yardstick_tc002.yaml</td>
                <td><p class="text-success">running</p></td>
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
  name: 'page3',
  data () {
    return {
      stories: [],
      services: [
        'greet',
        'yardstick',
        'logic'
      ],
      tests: [
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
