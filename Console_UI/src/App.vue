<template>
  <div id="app">
    <router-view />
  </div>

</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="scss">
  /* 解决表格线不整齐的样式 */
  body .el-table th.gutter {
      display: table-cell !important
  }

  ::-webkit-scrollbar {
    width: 14px;
    height: 14px;
  }

  ::-webkit-scrollbar-track,
  ::-webkit-scrollbar-thumb {
    border-radius: 999px;
    border: 4px solid transparent;
  }

  ::-webkit-scrollbar-track {
    box-shadow: 1px 1px 5px rgba(0,0,0,.5) inset;
  }

  ::-webkit-scrollbar-thumb {
    min-height: 20px;
    background-clip: content-box;
    box-shadow: 0 0 0 5px rgba(0,0,0,.5) inset;
  }

  ::-webkit-scrollbar-corner {
    background: transparent;
  }
</style>
