<template>
  <el-dialog
    v-loading="screenshotLoading"
    element-loading-background="rgba(0, 0, 0, 0.5)"
    title="截屏"
    width="60%"
    top="10vh"
    :visible.sync="scdata.screenshotVisible"
    @close="screenshotClose"
  >
    <div slot="title">
      {{ scdata.ip }} — 截屏
    </div>
    <el-row>
      <el-button type="primary" icon="el-icon-picture-outline-round" plain @click="screenshot()">执行截屏</el-button>
    </el-row>
    <br>
    <el-table
      :data="screenshotData"
      border
      height="400px"
      max-height="400px"
    >
      <el-table-column prop="id" label="编号" min-width="10%"></el-table-column>
      <el-table-column :show-overflow-tooltip="true" label="图片路径" min-width="45%">
        <template slot-scope="{row}">
          <span>{{ row.result.split('|')[0] }}</span>
        </template>
      </el-table-column>
      <el-table-column label="图片大小" min-width="15%">
        <template slot-scope="{row}">
          <span>{{ (row.result.split('|')[1] / 1024).toFixed(2) + 'KB' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="截图时间" prop="update_time" min-width="20%" :formatter="screenshotTime"></el-table-column>
      <el-table-column label="查看" min-width="10%">
        <template slot-scope="{row}">
          <el-image
            style="width: 40px; height: 40px;"
            :src="row.imgurl"
            :preview-src-list="imglist"
          >
          </el-image>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import { showScreenshotList, submitTask } from '@/api/consoleApi'
import { parseTime } from '@/utils/common'
import { getToken } from '@/utils/auth'
export default {
  name: 'Screenshot',
  props: {
    scdata: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      screenshotLoading: false,
      timer: '',
      screenshotData: [],
      baseUrl: 'https://baidu.com/', //服务器地址
      imglist: []
    }
  },
  watch: {
    scdata: {
      handler: function(data) {
        if (data.screenshotVisible === true) {
          this.screenshotLoading = true
          this.init(data)
        }
      },
      deep: true
    }
  },
  methods: {
    // 加载截屏列表
    init(val) {
      const data = {
        'token': getToken(),
        'key': val.key
      }
      showScreenshotList(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.imglist = []
          this.screenshotData = response.data.map(v => {
            var imgurl = this.baseUrl + v.result.split('|')[0]
            this.$set(v, 'imgurl', imgurl)
            this.imglist.push(imgurl)
            return v
          })
        }
        this.screenshotLoading = false
      })
    },
    screenshotTime(row) {
      return parseTime(row.update_time)
    },
    // 截屏
    screenshot() {
      const data = {
        'key': this.scdata.key,
        'content': 'screenshot',
        'type': 'screenshot',
        'token': getToken()
      }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.$notify.success({
            title: 'info',
            message: '截屏指令发送成功!!',
            duration: 2000,
            showClose: false
          })
          this.screenshotLoading = true
          // 多次提交，保留一个定时器
          clearInterval(this.timer)
          this.timer = setInterval(() => {
            this.init(data)
          }, 3000)
        }
      })
    },
    // 关闭截图
    screenshotClose() {
      clearInterval(this.timer)
      this.screenshotData = []
      this.scdata.screenshotVisible = false
    }
  }
}
</script>

<style>
</style>
