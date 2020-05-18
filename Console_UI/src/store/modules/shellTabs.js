const state = {
  options: [],
  tabsLog: 'default'
}

const mutations = {
  // 添加Tabs
  add_shelltabs(state, data) {
    this.state.shellTabs.options.push(data)
    // console.log(this.state.shellTabs.options)
  },
  // 设置当前激活
  set_active_index(state, key) {
    this.state.shellTabs.tabsLog = key
  },
  // 删除Tabs
  del_shellTbas(state, key) {
    let index = 0
    for (var option of this.state.shellTabs.options) {
      if (option.key === key) {
        break
      }
      index++
    }
    this.state.shellTabs.options.splice(index, 1)
  }
}

export default {
  // namespaced 访问时需要加上模块名
  namespaced: true,
  state,
  mutations
}
