<script>
var BASE_URL_PREFIX = 'http://' + window.location.hostname
var SERVER_ADDR = BASE_URL_PREFIX + ':' + 5310 + '/'
var AGENT_ADDR = BASE_URL_PREFIX + ':' + 5312 + '/'
var CONDUCTOR_ADDR = 'http://10.60.38.181:5000/'
var SELF_ADDR = window.location.href
export default {
	SERVER_ADDR,
	AGENT_ADDR,
	SELF_ADDR
}
</script>