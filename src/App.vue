<template>
  <div id="app">
  	<div class="row border-bottom blue-bg my-page-header">
	    <p id="title">OPNFV Bottlenecks Portal</p>
	    <ul id="intr_table" class="nav navbar-nav">
	      <li><router-link to="/">Test Suites</router-link></li>
	      <li><router-link to="/">Test Results</router-link></li>
	      <li><router-link to="/">Reports</router-link></li>
	      <li><router-link to="/result">Enviroments</router-link></li>
	    </ul>
	</div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
