<template>
  <div class="consolelog">
    <div>
      <el-tabs v-model="tabsLog" type="card" @tab-click="handleClick" @tab-remove="removeTab">
        <el-tab-pane label="Event Log" name="default">
          <div id="eventlog">
            <label style="color: rgb(0, 255, 0);">########################################## BIOPASS-最近10条上线记录 ##########################################</label>
            <div v-for="(item,i) in tendata" :key="i" style="margin-top: 3px;">
              <label style="color: rgb(16, 138, 36);">上线时间: {{ item.join_time }}</label>&nbsp;
              <label style="color: rgb(16, 138, 36);">IP地址:  {{ item.public_ip }}</label>&nbsp;
              <label style="color: rgb(16, 138, 36);">IP所在地: {{ item.note }}</label>
              <label style="color: rgb(16, 138, 36);">系统版本: {{ item.os_version }}</label>
              <label style="color: rgb(16, 138, 36);">当前用户: {{ item.current_user }}</label>
            </div>
            <!-- 日志版本 -->
            <!-- <div v-for="(item,i) in alllogList" :key="i">
              <label style="color: white;">{{ item.nowdate }}</label>&nbsp;
              <label style="color: rgb(156, 156, 26);">######</label>&nbsp;
              <label style="color: rgb(0, 255, 0);">to send {{ item.info }}</label>&nbsp;
              <label style="color: rgb(16, 138, 36);">{{ item.comm }}</label>
            </div> -->
          </div>
        </el-tab-pane>
        <el-tab-pane
          v-for="(item) in shelltabs"
          :key="item.key"
          :label="item.public_ip + ' @' + item.key"
          :name="item.key"
          closable
        >
          <div class="shelllog">
            <label style="color: rgb(0, 255, 0);">########################################## BIOPASS ##########################################</label>
            <template v-if="isshow">
              <div v-for="(v,i) in newreslist" :key="i">
                <template v-if="tabsLog === v.tab">
                  <label style="color: white;">{{ v.nowdate }}</label>&nbsp;
                  <label style="color: rgb(156, 156, 26);">######</label>&nbsp;
                  <label style="color: rgb(0, 255, 0);">to send {{ v.info }}</label>&nbsp;
                  <label style="color: rgb(16, 138, 36);">{{ v.comm }}</label>
                  <div v-for="(rl,ii) in v.result" :key="ii">
                    <pre style="color: rgb(0, 255, 0); margin: 0px;" v-text="rl.result">
                    {{ rl.result }}
                    </pre>
                  </div>
                  <br>
                </template>
              </div>
            </template>
            <template v-else>
              <div v-for="(v,i) in oldreslist" :key="i">
                <template v-if="tabsLog === v.tab">
                  <label style="color: white;">{{ v.nowdate }}</label>&nbsp;
                  <label style="color: rgb(156, 156, 26);">######</label>&nbsp;
                  <label style="color: rgb(0, 255, 0);">to send {{ v.info }}</label>&nbsp;
                  <label style="color: rgb(16, 138, 36);">{{ v.comm }}</label>
                  <div v-for="(rl,ii) in v.result" :key="ii">
                    <pre style="color: rgb(0, 255, 0); margin: 0px;" v-text="rl.result">
                    {{ rl.result }}
                    </pre>
                  </div>
                  <br>
                </template>
              </div>
            </template>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    <div style="margin-top: 10px;">
      <el-input
        v-model="commandText"
        style="padding-bottom: 15px;"
        placeholder="Please input ..."
        @keyup.enter.native="execCommand"
      >
        <template slot="prepend">Event-input</template>
      </el-input>
    </div>
  </div>
</template>

<script>
import { Message } from 'element-ui'
import { parseTime } from '@/utils/common'
import { submitTask, getTaskRes, updTaskResStatus, getLatelyTen } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
import NProgress from 'nprogress'
export default {
  name: 'ConsoleLog',
  data() {
    return {
      commandText: '', // 命令输入框
      alllogList: [], // 日志列表
      oldreslist: [], // 上一次命令结果
      newreslist: [], // 最新命令结果
      isshow: false,
      dataLog: null,
      timer: null,
      tentimer: null,
      tendata: []
    }
  },
  computed: {
    shelltabs() {
      return this.$store.state.shellTabs.options
    },
    // 激活选中
    tabsLog: {
      get() {
        return this.$store.state.shellTabs.tabsLog
      },
      set(key) {
        this.$store.commit('shellTabs/set_active_index', key)
      }
    }
  },
  mounted() {
    this.getLatelyTen()
    // 防止多次提交，保留一个定时器
    clearInterval(this.tentimer)
    this.tentimer = setInterval(() => {
      this.getLatelyTen()
    }, 60000)
  },
  updated() {
    // 滚动条自动到底部
    this.$nextTick(() => {
      var shelllog = this.$el.querySelector('.shelllog')
      if (shelllog) {
        shelllog.scrollTop = shelllog.scrollHeight
      }

      // var eventlog = this.$el.querySelector('#eventlog')
      // eventlog.scrollTop = eventlog.scrollHeight
    })
  },
  methods: {
    // 点击切换 Tab
    handleClick(tab) {
      this.$store.commit('shellTabs/set_active_index', tab.name)
    },
    // 关闭 Tab
    removeTab(targetName) {
      // 关闭一个清空一个日志
      this.oldreslist.forEach((v, i) => {
        if (v.tab === targetName) {
          this.oldreslist.splice(i, 1)
        }
      })
      this.newreslist.forEach((v, i) => {
        if (v.tab === targetName) {
          this.newreslist.splice(i, 1)
        }
      })
      this.$store.commit('shellTabs/del_shellTbas', targetName)
      if (this.$store.state.shellTabs.options && this.$store.state.shellTabs.options.length >= 1) {
        this.$store.commit('shellTabs/set_active_index', this.$store.state.shellTabs.options[this.$store.state.shellTabs.options.length - 1].key)
      } else {
        this.$store.state.shellTabs.tabsLog = 'default'
        // 所有选项卡关闭, 清空
        this.alllogList = []
      }
    },
    // 提交执行命令
    execCommand() {
      if (this.commandText.length > 0) {
        if (this.$store.state.shellTabs.tabsLog === 'default') {
          Message({
            message: '请连接或选中已经连接的..',
            type: 'error'
          })
          this.commandText = ''
        } else {
          NProgress.start()
          // 提交成功追加日志
          for (var option of this.$store.state.shellTabs.options) {
            if (option.key === this.$store.state.shellTabs.tabsLog) {
              var tabinfo = option.public_ip + ' @' + option.key
            }
          }
          this.dataLog = {
            nowdate: parseTime(Math.round(new Date())),
            info: tabinfo,
            comm: this.commandText,
            tab: this.$store.state.shellTabs.tabsLog
          }

          var postData = {
            'key': this.$store.state.shellTabs.tabsLog,
            'content': this.commandText,
            'type': 'shell',
            'token': getToken()
          }
          // 提交
          submitTask(postData).then(response => {
            if (response.code === 20000) {
              // 防止多次提交，保留一个定时器
              clearInterval(this.timer)
              this.timer = setInterval(() => {
                this.getTaskRes()
              }, 2000)
            }
          })

          // 追加公共日志
          // this.alllogList.push(this.dataLog)
          this.oldreslist.push(this.dataLog)
          this.commandText = ''
          this.isshow = false
        }
      } else {
        Message({
          message: '请输入命令..',
          type: 'warning'
        })
      }
    },
    // 获取命令结果
    getTaskRes() {
      var postData = {
        'key': this.$store.state.shellTabs.tabsLog,
        'token': getToken()
      }
      getTaskRes(postData).then(response => {
        if (response.code === 20000 && response.data !== null) {
          this.isshow = true
          this.dataLog.result = response.data
          this.newreslist.push(this.dataLog)
          clearInterval(this.timer)
          updTaskResStatus(postData)
          NProgress.done()
        }
      })
    },
    // 获取最近10条上线记录
    getLatelyTen() {
      getLatelyTen({ 'token': getToken() }).then(response => {
        if (response.code === 20000) {
          this.tendata = response.data
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.consolelog {
  padding: 10px;
}
#eventlog {
  padding: 10px;
  width: 100%;
  height: 350px;
  border: 1px solid #2d343e;
  font-size: 14px;
  & label{
    font-weight: 100;
  }
}

.shelllog {
  padding: 6px;
  width: 100%;
  height: 350px;
  border: 1px solid #2d343e;
  font-size: 14px;
  overflow:auto;
  & label{
    font-weight: 100;
  }
}
</style>
