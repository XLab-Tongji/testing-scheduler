<template>
<div>
  <iframe src='http://0.0.0.0:5000/#/workflow?q=&h=&workflowTypes=&status=&start=0' id="conductor-ui"></iframe>
</div>
</template>

<script>
export default {
  data () {
    return {
    }
  },
  mounted () {
    /**
       * iframe-宽高自适应显示
       */
    function changeConductorUIfIframe () {
      const conductorUI = document.getElementById('conductor-ui')
      const deviceWidth = document.body.clientWidth
      const deviceHeight = document.body.clientHeight
      conductorUI.style.width = Number(deviceWidth) + 'px' // 数字是页面布局宽度差值
      conductorUI.style.height = Number(deviceHeight) + 'px' // 数字是页面布局高度差
    }

    changeConductorUIfIframe()

    window.onresize = function () {
      changeConductorUIfIframe()
    }
  }
}
</script>

<style scoped>

</style>
