import Vue from 'vue'
import Router from 'vue-router'
import page1 from '@/components/page1'
import page2 from '@/components/page2'
import page3 from '@/components/page3'
import environment from '@/components/environment'
Vue.use(Router)
const Result = {template: "<div>this is result</div>"}
export default new Router({
  routes: [
    {
      path: '/',
      name: 'page1',
      component: page1
    },
    {
      path: '/page2',
      name: 'page2',
      component: page2
    },
    {
      path: '/page2/page3',
      name: 'page3',
      component: page3
    },
    {
      path: '/result',
      component: environment
    }
  ]
})
