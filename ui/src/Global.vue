<script>
const SERVER_ADDR = '/parser/'
const WF_GRAPH_ADDR = '/wf-graph/'
const WF_SERVER_ADDR = '/wf-server/'
const CONDUCTOR_UI_PORT = 5000
const CONDUCTOR_UI_ADDR = 'http://' + window.location.hostname + ':' + CONDUCTOR_UI_PORT + '/#/workflow?q=&h=&workflowTypes=&status=&start=0'

export default {
	SERVER_ADDR,
	WF_GRAPH_ADDR,
	WF_SERVER_ADDR,
  CONDUCTOR_UI_ADDR
}
</script>
