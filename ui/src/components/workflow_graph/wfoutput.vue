<template>
    <div class="output row" style="padding-top: 20px;">
        <div class="col-md-offset-1 col-md-10">
            <div class="ibox">
                <div class="ibox-title">
                    <h5>Log</h5>
                    <div class="ibox-tools">
                        <a class="" v-on:click="refresh()">
                          <i class="fa fa-refresh"></i>
                        </a>
                    </div>
                </div>
                <div class="ibox-content">
                    <p><span class="log-item"></span><span></span></p>
                    <p><span class="log-item">status:</span><span>{{ status }}</span></p>
                    <p><span class="log-item">startime:</span><span>{{ startTime }}</span></p>
                    <p><span class="log-item">updatetime:</span><span>{{ updateTime }}</span></p>
                    <p><span class="log-item">endtime:</span><span>{{ endTime }}</span></p>
                    <p><span class="log-item">output:</span><pre>{{ wfoutput }}</pre></p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data: function() {
        return {
            wfId: this.$route.query.wfId,
            wfoutput: '',
            status: 'Unknown',
            startTime: '',
            endTime: '',
            updateTime: ''
        }
    },
    created: function() {
        this.getOutputData();
    },
    methods: {
        getOutputData: function() {
            var self = this;
            $.ajax({
                url: this.global.WF_SERVER_ADDR + "api/workflow/" + self.wfId,
                method:"GET",
                success:function (data) {
                    if(!data) return;
                    self.wfoutput = data['output'];
                    self.status = data['status'] ? data['status'] : self.status;
                    self.startTime = self.formattedTime(data['startTime']);
                    self.endTime = self.formattedTime(data['endTime']);
                    self.updateTime = self.formattedTime(data['updateTime']);
                }
            });
        },
        formattedTime: function(timeStamp) {
            console.log(typeof(timeStamp));
            if(typeof(timeStamp) != 'number') return '';
            var time = new Date(timeStamp);
            var y = time.getFullYear();
            var m = time.getMonth() + 1;
            var d = time.getDate();
            var h = time.getHours();
            var mi = time.getMinutes();
            var s = time.getSeconds();
            if(h < 10) {
                h = '0' + h;
            }
            if(mi < 10) {
                mi = '0' + mi;
            }
            if(s < 10) {
                s = '0' + s;
            }
            return y + '-' + m + '-' + d + ' ' + h + ':' + mi + ':' + s;
        },
        refresh: function() {
            this.getOutputData();
        }
    }
}
</script>

<style scoped>
.log-item {
    font-weight: bold;
    display: inline-block;
    width: 90px;
    padding-bottom: 3px;
}
</style>