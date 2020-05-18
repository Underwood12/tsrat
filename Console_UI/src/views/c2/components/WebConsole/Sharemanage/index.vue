<template>
  <el-dialog
    v-loading="shareLoading"
    element-loading-background="rgba(0, 0, 0, 0.5)"
    title="进程列表"
    width="50%"
    top="10vh"
    :visible.sync="shdata.shareVisible"
    @close="shareClose"
  >
    <div slot="title">
      {{ shdata.ip }} — 分享管理
    </div>
    <br>
    <el-table
      :data="shareData"
      border
      height="400px"
      max-height="400px"
    >
      <el-table-column prop="id" label="ID" width="60"></el-table-column>
      <el-table-column prop="username" label="用户名" :show-overflow-tooltip="true" min-width="30%"></el-table-column>
      <el-table-column label="操作" align="center" width="150">
        <template slot-scope="{row}">
          <el-button v-if="row.is_share === false" type="primary" size="mini" plain @click="share(row)">分享</el-button>
          <el-button v-else type="warning" size="mini" plain @click="cancelshare(row)">取消分享</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import { getShareUsers, setShare, cancelShare } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
export default {
  name: 'Sharemanage',
  props: {
    shdata: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      shareLoading: false,
      shareData: []
    }
  },
  watch: {
    shdata: {
      handler: function(data) {
        if (data.shareVisible === true) {
          this.shareLoading = true
          this.init(data)
        }
      },
      deep: true
    }
  },
  methods: {
    // 加载除开自己的用户列表
    init(val) {
      const data = {
        'token': getToken(),
        'key': val.key
      }
      getShareUsers(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.shareData = response.data
          this.shareLoading = false
        }
      })
    },
    // 分享
    share(row) {
      const data = {
        'key': this.shdata.key,
        'share_users': row.username,
        'token': getToken()
      }
      this.$confirm('确定分享吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 设置分享
        setShare(data).then(response => {
          if (response.code === 20000 && response.status === true) {
            this.$notify.success({
              title: 'info',
              message: '分享成功!!',
              duration: 2000,
              showClose: false
            })
            this.shareLoading = true
            setTimeout(() => {
              this.init(data)
            }, 1000)
          } else {
            this.$notify.error({
              title: 'error',
              message: '分享失败!!',
              duration: 2000,
              showClose: false
            })
          }
        })
      }).catch(() => {

      })
    },
    cancelshare(row) {
      const data = {
        'key': this.shdata.key,
        'share_users': row.username,
        'token': getToken()
      }
      this.$confirm('确定取消分享吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 取消分享
        cancelShare(data).then(response => {
          if (response.code === 20000 && response.status === true) {
            this.$notify.success({
              title: 'info',
              message: '取消分享成功!!',
              duration: 2000,
              showClose: false
            })
            this.shareLoading = true
            setTimeout(() => {
              this.init(data)
            }, 1000)
          } else {
            this.$notify.error({
              title: 'error',
              message: '取消分享失败!!',
              duration: 2000,
              showClose: false
            })
          }
        })
      }).catch(() => {

      })
    },
    // 关闭分享
    shareClose() {
      this.shareData = []
      this.shdata.shareVisible = false
    }
  }
}
</script>

<style>
</style>
