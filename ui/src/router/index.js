import Vue from 'vue'
import Router from 'vue-router'
import testsuite from '@/components/testsuite'
import testcase from '@/components/testcase'
import testcase_content from '@/components/testcase_content'
import environment from '@/components/environment'
import wfoutput from '@/components/workflow_graph/wfoutput'
import conductorUI from '@/components/external/conductor-ui'
Vue.use(Router)
const Result = {
  template: "<div>please visit <a target='blank' href='http://lab205.jios.org:30002/dashboard/db/cluster?orgId=1'>grafana page.</a></div>"
}
export default new Router({
  routes: [
    {
      path: '/',
      name: 'testsuite',
      component: testsuite
    },
    {
      path: '/testcase',
      name: 'testcase',
      component: testcase
    },
    {
      path: '/content',
      name: 'testcase_content',
      component: testcase_content
    },
    {
      path: '/result',
      component: Result
    },
    {
      path: '/report',
      component: conductorUI
    },
    {
      path: '/environment',
      component: environment
    },
    {
      path: '/output',
      component: wfoutput
    }
  ]
})
