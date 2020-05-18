<template>
  <el-dialog
    v-loading="processLoading"
    element-loading-background="rgba(0, 0, 0, 0.5)"
    title="进程列表"
    width="50%"
    top="10vh"
    :visible.sync="pldata.processVisible"
    @close="processClose"
  >
    <div slot="title">
      {{ pldata.ip }} — 进程列表
    </div>
    <div>
      <el-button type="primary" icon="el-icon-refresh" plain @click="sendProcess">获取进程列表</el-button>
    </div>
    <br>
    <!-- processData.filter(searchData => searchData.name.toLowerCase().includes(search.toLowerCase())) -->
    <el-table
      :data="searchProcess"
      border
      height="500px"
      max-height="500px"
    >
      <el-table-column prop="pid" label="PID" width="100">
      </el-table-column>
      <el-table-column prop="name" label="进程名称" :show-overflow-tooltip="true" min-width="30%"></el-table-column>
      <el-table-column label="操作" align="center" width="200">
        <template slot="header" slot-scope="{}">
          <el-input
            v-model="search"
            size="mini"
            placeholder="进程名搜索"
          />
        </template>
        <template slot-scope="{row}">
          <el-button type="warning" size="mini" plain @click="killProcess(row)">结束进程</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
import { submitTask, getProcessList } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
export default {
  name: 'Processlist',
  props: {
    pldata: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      processLoading: false,
      timer: '',
      processData: [],
      search: ''
    }
  },
  computed: {
    // 模糊搜索
    searchProcess() {
      const search = this.search
      if (search) {
        // filter() 方法创建一个新的数组，新数组中的元素是通过检查指定数组中符合条件的所有元素。
        // 注意： filter() 不会对空数组进行检测。
        // 注意： filter() 不会改变原始数组。
        // return this.processData.filter(data => {
        //   // some() 方法用于检测数组中的元素是否满足指定条件;
        //   // some() 方法会依次执行数组的每个元素：
        //   // 如果有一个元素满足条件，则表达式返回true , 剩余的元素不会再执行检测;
        //   // 如果没有满足条件的元素，则返回false。
        //   // 注意： some() 不会对空数组进行检测。
        //   // 注意： some() 不会改变原始数组。
        //   return Object.keys(data).some(key => {
        //     // indexOf() 返回某个指定的字符在某个字符串中首次出现的位置，如果没有找到就返回-1；
        //     // 该方法对大小写敏感！所以之前需要toLowerCase()方法将所有查询到内容变为小写。
        //     console.log(String(data['name']).toLowerCase().indexOf(search.toLowerCase()))
        //     return String(data['name']).toLowerCase().indexOf(search.toLowerCase()) > -1
        //   })
        // })
        return this.processData.filter(searchData => {
          if (searchData.name !== '' && searchData.name !== null) {
            return searchData.name.toLowerCase().includes(search.toLowerCase())
          }
        })
      }
      return this.processData
    }
  },
  methods: {
    // 获取进程列表
    init(val) {
      const data = {
        'token': getToken(),
        'key': val.key
      }
      getProcessList(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.processData = response.data
          clearInterval(this.timer)
          this.processLoading = false
        }
      })
    },
    // 发送获取进程指令
    sendProcess() {
      const data = {
        'key': this.pldata.key,
        'content': 'process_list',
        'type': 'process_list',
        'token': getToken()
      }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.$notify.success({
            title: 'info',
            message: '进程指令发送成功!!',
            duration: 2000,
            showClose: false
          })
          this.processLoading = true
          // 多次提交，保留一个定时器
          clearInterval(this.timer)
          this.timer = setInterval(() => {
            this.init(data)
          }, 3000)
        }
      })
    },
    // kill 进程
    killProcess(row) {
      this.search = ''
      const data = {
        'key': this.pldata.key,
        'content': row.pid,
        'type': 'kill_process',
        'token': getToken()
      }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.$notify.success({
            title: 'info',
            message: 'Kill进程指令发送成功!!',
            duration: 2000,
            showClose: false
          })

          // 重新提交获取进程命令
          this.sendProcess()
        }
      })
    },
    // 关闭进程列表
    processClose() {
      clearInterval(this.timer)
      this.search = ''
      this.processData = []
      this.pldata.processVisible = false
    }
  }
}
</script>

<style>
</style>
