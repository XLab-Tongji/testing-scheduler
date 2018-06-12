// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import './css/bootstrap.min.css'
import './css/font-awesome.css'
import './css/style.css'
import './css/animate.css'
import './css/TheStyle.css'
import './css/wf-graph.css'
import './css/toastr.min.css'
import './scri/jquery-3.3.1.js'
import './scri/bootstrap.min.js'
import './scri/jquery.metisMenu.js'
import './scri/jquery.slimscroll.min.js'
import './scri/inspinia.js'
import './scri/pace.min.js'
import './scri/toastr.min.js'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
