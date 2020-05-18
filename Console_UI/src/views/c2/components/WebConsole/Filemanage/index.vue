<template>
  <el-dialog
    v-loading="filesLoading"
    title="文件管理"
    width="80%"
    top="10vh"
    element-loading-background="rgba(0, 0, 0, 0.5)"
    :visible.sync="fmdata.filesVisible"
    @close="filesClose"
  >
    <div slot="title">
      {{ fmdata.ip }} — 文件管理
    </div>
    <div class="file-container">
      <el-input v-model="currpath" style="width: 500px; margin-right: 8px;" placeholder="当前路径" @keyup.enter.native="jumppath">
        <el-select slot="prepend" v-model="selectvalue" filterable clearable placeholder="常见目录" style="width: 150px;" @change="commonpath">
          <el-option
            v-for="item in commondata"
            :key="item.label"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-button slot="append" type="primary" plain @click="jumppath">跳转</el-button>
      </el-input>
      <el-button size="medium" plain @click="defaultpath">默认目录</el-button>
      <el-button type="primary" size="medium" plain @click="alldisk">显示磁盘</el-button>
      <el-button type="primary" size="medium" plain @click="history">历史记录</el-button>
      <el-button type="success" size="medium" plain @click="publicFiles">公共文件</el-button>
      <el-button type="warning" size="medium" plain @click="uploadRecord">上传进度</el-button>
      <el-button type="warning" size="medium" plain @click="downloadRecord">下载进度</el-button>
    </div>
    <br>
    <el-table
      :data="filesData"
      border
      height="500px"
      max-height="500px"
      :default-sort="{prop: 'isfile', order: 'ascending'}"
      @row-dblclick="dblrow"
    >
      <el-table-column prop="isfile" align="center" sortable width="50">
        <template slot-scope="{row}">
          <svg-icon v-if="row.isfile === 'no'" icon-class="bp-folder" />
          <svg-icon v-if="row.isfile === 'yes'" icon-class="bp-file" />
        </template>
      </el-table-column>
      <el-table-column prop="filename" :show-overflow-tooltip="true" label="文件名" min-width="40%">
      </el-table-column>
      <el-table-column prop="modifytime" label="修改时间" min-width="20%"></el-table-column>
      <el-table-column prop="filesize" label="文件大小" min-width="15%"></el-table-column>
      <el-table-column label="操作" align="center" width="160">
        <template slot-scope="{row}">
          <el-button v-if="row.isfile === 'yes'" type="success" size="mini" plain @click="download(row)">下载到中转站</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 历史浏览 -->
    <el-dialog
      title="历史记录"
      width="50%"
      element-loading-background="rgba(0, 0, 0, 0.5)"
      :visible.sync="historyVisible"
      append-to-body
      @close="historyClose"
    >
      <div slot="title">
        {{ fmdata.ip }} — 历史记录
      </div>
      <el-table
        :data="historyData"
        border
        height="300px"
        max-height="300px"
        :default-sort="{prop: 'datetime', order: 'descending'}"
        @row-dblclick="dblhistory"
      >
        <el-table-column prop="key" label="key" min-width="15%"></el-table-column>
        <el-table-column prop="content" :show-overflow-tooltip="true" label="浏览目录" min-width="60%"></el-table-column>
        <el-table-column prop="datetime" label="浏览时间" min-width="25%"></el-table-column>
      </el-table>
    </el-dialog>

    <!-- 公共文件 -->
    <el-dialog
      v-loading="publicFilesLoading"
      title="公共文件区"
      width="60%"
      element-loading-background="rgba(0, 0, 0, 0.5)"
      :visible.sync="publicFilesVisible"
      append-to-body
      @close="publicFilesClose"
    >
      <div slot="title">
        {{ fmdata.ip }} — 公共文件区
      </div>
      <el-upload
        ref="upload_public"
        name="publicfile"
        :action="uploadPublicApi"
        :data="{ 'token': token }"
        :on-success="uploadSuccess"
        :show-file-list="false"
      >
        <el-button type="success" plain><i class="el-icon-upload el-icon--right"></i>上传到公共区</el-button>
      </el-upload>
      <br>
      <el-table
        :data="publicFilesData"
        border
        height="300px"
        max-height="300px"
        :default-sort="{prop: 'date', order: 'descending'}"
      >
        <el-table-column prop="name" :show-overflow-tooltip="true" label="文件名" min-width="15%"></el-table-column>
        <el-table-column prop="name64" :show-overflow-tooltip="true" label="加密文件名" min-width="40%"></el-table-column>
        <el-table-column prop="size" label="文件大小" min-width="20%"></el-table-column>
        <el-table-column prop="date" label="修改时间" min-width="25%"></el-table-column>
        <el-table-column label="操作" align="center" width="150">
          <template slot-scope="{row}">
            <el-button type="warning" size="mini" plain @click="upload(row)">上传到机器</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 上传记录 -->
    <el-dialog
      v-loading="uploadRecordLoading"
      title="上传记录"
      width="60%"
      element-loading-background="rgba(0, 0, 0, 0.5)"
      :visible.sync="uploadRecordVisible"
      append-to-body
      @close="uploadRecordClose"
    >
      <div slot="title">
        {{ fmdata.ip }} — 上传记录和进度
      </div>

      <el-table
        :data="uploadRecordData"
        border
        height="400px"
        max-height="400px"
      >
        <el-table-column prop="id" label="编号" width="50"></el-table-column>
        <el-table-column prop="content" :show-overflow-tooltip="true" label="目标位置" min-width="25%"></el-table-column>
        <el-table-column label="文件名" min-width="20%">
          <template slot-scope="{row}">
            <span>{{ JSON.parse(row.result)['save_name'] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="文件大小" min-width="12%">
          <template slot-scope="{row}">
            <span>{{ JSON.parse(row.result)['file_size'] }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="update_time" label="上传时间" width="180" :formatter="formatTime"></el-table-column>
        <el-table-column label="状态" width="110">
          <template slot-scope="{row}">
            <el-tag v-if="row.status === '0' && JSON.parse(row.result)['status'] === true" :type="info">
              指令已发送
            </el-tag>
            <el-tag v-else-if="row.status === '1' && JSON.parse(row.result)['status'] === true">
              指令已接收
            </el-tag>
            <el-tag v-else-if="row.status === '2' && JSON.parse(row.result)['status'] === true" type="success">
              上传完成
            </el-tag>
            <el-tag v-else type="danger">
              上传失败
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <!-- 下载记录 -->
    <el-dialog
      v-loading="downloadRecordLoading"
      title="下载记录"
      width="70%"
      element-loading-background="rgba(0, 0, 0, 0.5)"
      :visible.sync="downloadRecordVisible"
      append-to-body
      @close="downloadRecordClose"
    >
      <div slot="title">
        {{ fmdata.ip }} — 下载记录和进度
      </div>

      <el-table
        :data="downloadRecordData"
        border
        height="400px"
        max-height="400px"
      >
        <el-table-column prop="id" label="编号" width="50"></el-table-column>
        <el-table-column prop="content" :show-overflow-tooltip="true" label="目标位置" min-width="25%"></el-table-column>
        <el-table-column label="文件名" min-width="20%">
          <template slot-scope="{row}">
            <span>{{ JSON.parse(row.result)['save_name'] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="文件大小" min-width="12%">
          <template slot-scope="{row}">
            <span>{{ JSON.parse(row.result)['file_size'] + 'KB' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="update_time" label="下载时间" width="180" :formatter="formatTime"></el-table-column>
        <el-table-column label="状态" width="110">
          <template slot-scope="{row}">
            <el-tag v-if="row.status === '0' && JSON.parse(row.result)['status'] === true" :type="info">
              指令已发送
            </el-tag>
            <el-tag v-else-if="row.status === '1' && JSON.parse(row.result)['status'] === true">
              指令已接收
            </el-tag>
            <el-tag v-else-if="row.status === '2' && JSON.parse(row.result)['status'] === true" type="success">
              下载完成
            </el-tag>
            <el-tag v-else type="danger">
              下载失败
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="150">
          <template slot-scope="{row}">
            <el-button v-if="row.status === '2' && JSON.parse(row.result)['status'] === true" type="warning" size="mini" plain @click="loaclDownload(row)">下载到本地</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </el-dialog>
</template>

<script>
import { getCurpathAllfile, submitTask, getPublicFiles, upload, getUploadProgress, download, getDownloadProgress } from '@/api/consoleApi'
import { getToken } from '@/utils/auth'
import { Message } from 'element-ui'
import { parseTime } from '@/utils/common'
export default {
  name: 'Filemanage',
  props: {
    fmdata: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      commondata: [{
        value: 'C:/inetpub/wwwroot',
        label: 'wwwroot'
      }, {
        value: 'C:/Windows/System32/drivers/etc',
        label: 'hosts'
      }],
      baseUrl: 'https://baidu.com/index.php',
      token: getToken(),
      filesData: [],
      filesLoading: false,
      currpath: '',
      selectvalue: '',
      timer: '',
      historyVisible: false,
      historyData: [],
      publicFilesLoading: false,
      publicFilesVisible: false,
      publicFilesData: [],
      uploadPublicApi: '/api/M2/upload_public',
      uploadRecordVisible: false,
      uploadRecordData: [],
      uploadRecordLoading: false,
      downloadRecordVisible: false,
      downloadRecordData: [],
      downloadRecordLoading: false
    }
  },
  watch: {
    fmdata: {
      handler: function(data) {
        if (data.filesVisible === true) {
          this.filesLoading = true
          this.filesData = []
          this.timer = setInterval(() => {
            this.init(data)
          }, 3000)
        }
      },
      deep: true
    }
  },
  methods: {
    // 格式化时间戳
    formatTime(row) {
      return parseTime(row.update_time)
    },
    init(val) {
      var data = {
        'token': getToken(),
        'key': val.key,
        'path': val.content
      }
      getCurpathAllfile(data).then(response => {
        if (response.code === 20000 && response.status === true) {
          this.filesData = response.data
          this.currpath = response.data[0].path
          this.filesLoading = false
          // 获取成功, 取消定时器
          clearInterval(this.timer)
        } else if (response.code === 20000 && response.status === false) {
          Message({
            message: '目录不存在!!',
            type: 'error'
          })
          this.filesLoading = false
          clearInterval(this.timer)
        }
      })
    },
    // 常见路径选择
    commonpath() {
      this.openPath(this.selectvalue)
    },
    // 跳转目录
    jumppath() {
      this.openPath(this.currpath)
    },
    // 默认目录
    defaultpath() {
      this.openPath('default')
    },
    // 显示所有磁盘
    alldisk() {
      this.openPath('.')
    },
    // 双击单元行跳转目录
    dblrow(row) {
      if (row.isfile === 'no') {
        let path = ''
        if (row.filename === '..') {
          path = row.path.substring(0, row.path.lastIndexOf('/'))
        } else {
          if (row.path) {
            if (row.path.substr(row.path.length - 1, 1) === '/') {
              path = row.path + row.filename
            } else {
              path = row.path + '/' + row.filename
            }
          } else {
            path = row.filename + '/'
          }
        }
        this.openPath(path)
      } else {
        Message({
          message: '请选择目录!!',
          type: 'warning'
        })
      }
    },
    // 查看历史
    history() {
      this.historyVisible = true
      this.historyData = JSON.parse(sessionStorage.getItem(this.fmdata.key))
    },
    // 双击历史记录
    dblhistory(row) {
      this.openPath(row.content)
      this.historyVisible = false
    },
    // 获取指定目录
    openPath(path) {
      if (path.length === 2) {
        path = path + '/'
      }
      var data = {
        'key': this.fmdata.key,
        'content': path,
        'type': 'files',
        'token': getToken()
      }
      var localdata = { key: this.fmdata.key, content: path, datetime: parseTime(Math.round(new Date())) }
      // 提交
      submitTask(data).then(response => {
        if (response.code === 20000) {
          this.filesLoading = true
          // sessionStorage 存储 回话存储
          var historyData = []
          var hisValue = JSON.parse(sessionStorage.getItem(this.fmdata.key))
          var objValue = ''
          if (hisValue == null) {
            historyData.push(localdata)
            objValue = JSON.stringify(historyData)
            sessionStorage.setItem(this.fmdata.key, objValue)
          } else {
            hisValue.forEach((value, item) => {
              historyData.push(value)
            })
            historyData.push(localdata)
            objValue = JSON.stringify(historyData)
            sessionStorage.setItem(this.fmdata.key, objValue)
          }
          // 多次提交，保留一个定时器
          clearInterval(this.timer)
          this.timer = setInterval(() => {
            this.init(data)
          }, 3000)
        }
      })
    },
    // 公共文件区
    publicFiles() {
      this.publicFilesVisible = true
      this.getPublicFiles()
    },
    // 获取公共文件区文件列表
    getPublicFiles() {
      this.publicFilesLoading = true
      getPublicFiles({ 'token': getToken() }).then(response => {
        if (response.status === true) {
          this.publicFilesData = response.data
        }
        this.publicFilesLoading = false
      })
    },
    uploadSuccess(res) {
      if (res.code === 20000 && res.status === true) {
        Message({
          message: '上传成功!!',
          type: 'success'
        })
        this.getPublicFiles()
      }
    },
    // 上传到被控端机器
    upload(row) {
      var data = {
        'token': getToken(),
        'targetpath': this.currpath,
        'key': this.fmdata.key,
        'data': row
      }
      upload(data).then(response => {
        if (response.status === true) {
          this.$notify.success({
            title: 'info',
            message: '上传指令下发成功!!',
            duration: 2000,
            showClose: false
          })
        }
      })
    },
    // 上传记录
    uploadRecord() {
      this.uploadRecordVisible = true
      this.uploadRecordLoading = true
      var data = {
        'token': getToken(),
        'key': this.fmdata.key
      }
      getUploadProgress(data).then(response => {
        if (response.status === true) {
          this.uploadRecordData = response.data
        }
        this.uploadRecordLoading = false
      })
    },
    // 下载到中转站
    download(row) {
      var path = ''
      if (row.path.substr(row.path.length - 1, 1) === '/') {
        path = row.path + row.filename
      } else {
        path = row.path + '/' + row.filename
      }
      var data = {
        'token': getToken(),
        'key': this.fmdata.key,
        'path': path
      }
      download(data).then(response => {
        if (response.status === true) {
          this.$notify.success({
            title: 'info',
            message: '下载指令下发成功!!',
            duration: 2000,
            showClose: false
          })
        }
      })
    },
    // 下载记录
    downloadRecord() {
      this.downloadRecordVisible = true
      this.downloadRecordLoading = true
      var data = {
        'token': getToken(),
        'key': this.fmdata.key
      }
      getDownloadProgress(data).then(response => {
        if (response.status === true) {
          this.downloadRecordData = response.data
        }
        this.downloadRecordLoading = false
      })
    },
    // 下载到本地
    loaclDownload(row) {
      var downloadLink = this.baseUrl + '/M2/loacldownload?token=' + getToken() + '&id=' + row.id + '&t=' + Math.round(new Date())
      window.open(downloadLink)
    },
    filesClose() {
      // 关闭, 取消定时器
      clearInterval(this.timer)
      this.fmdata.filesVisible = false
    },
    historyClose() {
      clearInterval(this.timer)
      this.historyVisible = false
    },
    publicFilesClose() {
      this.publicFilesVisible = false
    },
    uploadRecordClose() {
      this.uploadRecordVisible = false
    },
    downloadRecordClose() {
      this.downloadRecordVisible = false
    }
  }
}
</script>

<style>
</style>
