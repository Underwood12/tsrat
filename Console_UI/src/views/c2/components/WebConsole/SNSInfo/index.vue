<template>
  <el-dialog
    v-loading="snsLoading"
    element-loading-background="rgba(0, 0, 0, 0.5)"
    title="社交信息"
    width="50%"
    top="10vh"
    :visible.sync="snsdata.snsVisible"
    @close="snsClose"
  >
    <div slot="title">
      {{ snsdata.ip }} — 社交信息
    </div>
    <div>
      <el-button type="primary" icon="el-icon-refresh" plain @click="sendSNS">获取社交信息</el-button>
    </div>
    <br>
    <el-table
      :data="snsData"
      border
      height="300px"
      max-height="300px"
    >
      <el-table-column prop="type" label="社交名称" width="120">
      </el-table-column>
      <el-table-column prop="content" label="社交号码" :show-overflow-tooltip="true" min-width="30%"></el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import { submitTask, getSNSInfo } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
export default {
  name: 'SNSinfo',
  props: {
    snsdata: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      snsLoading: false,
      timer: '',
      snsData: []
    }
  },
  methods: {
    // 获取社交信息
    init(val) {
      const data = {
        'token': getToken(),
        'key': val.key
      }
      getSNSInfo(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.snsData = response.data
          clearInterval(this.timer)
          this.snsLoading = false
        }
      })
    },
    // 发送获取社交信息指令
    sendSNS() {
      const data = {
        'key': this.snsdata.key,
        'content': 'get_sns_info',
        'type': 'get_sns_info',
        'token': getToken()
      }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.$notify.success({
            title: 'info',
            message: '社交指令发送成功!!',
            duration: 2000,
            showClose: false
          })
          this.snsLoading = true
          // 多次提交，保留一个定时器
          clearInterval(this.timer)
          this.timer = setInterval(() => {
            this.init(data)
          }, 3000)
        }
      })
    },
    // 关闭
    snsClose() {
      clearInterval(this.timer)
      this.snsData = []
      this.snsdata.snsVisible = false
    }
  }
}
</script>

<style>
</style>
