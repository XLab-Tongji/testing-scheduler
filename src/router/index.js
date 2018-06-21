import Vue from 'vue'
import Router from 'vue-router'
import page1 from '@/components/page1'
import page2 from '@/components/page2'
import page3 from '@/components/page3'
import environment from '@/components/environment'
import editor from '@/components/editor'
Vue.use(Router)
const Result = {template: "<div>please visit <a target='blank' href='http://lab205.jios.org:30002/dashboard/db/cluster?orgId=1'>grafana page.</a></div>"}
export default new Router({
  routes: [
    {
      path: '/',
      name: 'suite',
      component: page1
    },
    {
      path: '/stories',
      name: 'page2',
      component: page2
    },
    {
      path: '/content',
      name: 'page3',
      component: page3
    },
    {
      path: '/result',
      component: Result
    },
    {
      path: '/report',
      component: editor
    },
    {
      path: '/environment',
      component: environment
    }
  ]
})
