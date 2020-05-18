<template>
  <el-dialog
    v-loading="networkLoading"
    element-loading-background="rgba(0, 0, 0, 0.5)"
    title="网络代理"
    width="70%"
    top="10vh"
    :visible.sync="nadata.networkVisible"
    @close="networkClose"
  >
    <div slot="title">
      {{ nadata.ip }} — 网络代理
    </div>
    <div>
      <el-button type="primary" icon="el-icon-circle-plus-outline" plain @click="sendAddNetwork">开启网络代理</el-button>
      <el-button type="danger" icon="el-icon-circle-close" plain @click="sendCloseNetwork">关闭网络代理</el-button>
    </div>
    <br>
    <el-table
      :data="networkData"
      height="400px"
      max-height="400px"
      border
    >
      <el-table-column prop="id" label="ID" width="60"></el-table-column>
      <el-table-column prop="host" label="代理服务器" :show-overflow-tooltip="true" min-width="30%"></el-table-column>
      <el-table-column prop="out_port" label="代理端口" min-width="20%"></el-table-column>
      <el-table-column prop="time" label="创建时间" min-width="20%"></el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import { submitTask, addNetworkAgent, getNetworkAgent } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
export default {
  name: 'Networkagent',
  props: {
    nadata: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      networkLoading: false,
      timer: '',
      networkData: []
    }
  },
  watch: {
    nadata: {
      handler: function(data) {
        if (data.networkVisible === true) {
          this.networkLoading = true
          this.init(data)
        }
      },
      deep: true
    }
  },
  methods: {
    // 获取网络代理列表
    init(val) {
      this.networkLoading = true
      const data = {
        'token': getToken(),
        'key': val.key
      }
      getNetworkAgent(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.networkData = response.data
        } else {
          this.$message({
            message: response.msg,
            type: 'error'
          })
        }
        this.networkLoading = false
      })
    },
    // 发送添加网络代理指令
    sendAddNetwork() {
      const data = {
        'key': this.nadata.key,
        'type': 'open_proxy',
        'token': getToken()
      }
      // 提交
      addNetworkAgent(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.$notify.success({
            title: 'info',
            message: '开启网络代理指令发送成功!!',
            duration: 2000,
            showClose: false
          })
          this.networkData = []
          this.networkLoading = true
          // 多次提交，保留一个定时器
          clearInterval(this.timer)
          this.timer = setInterval(() => {
            this.init(data)
          }, 3000)
        } else {
          this.$message({
            message: response.msg,
            type: 'error'
          })
        }
      })
    },
    // 关闭网络代理
    sendCloseNetwork() {
      const data = {
        'key': this.nadata.key,
        'type': 'close_proxy',
        'content': 'close_proxy',
        'token': getToken()
      }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.$notify.success({
            title: 'info',
            message: '关闭网络代理指令发送成功!!',
            duration: 2000,
            showClose: false
          })
        }
      })
    },
    // 关闭
    networkClose() {
      clearInterval(this.timer)
      this.networkData = []
      this.nadata.networkVisible = false
    }
  }
}
</script>

<style>
</style>
