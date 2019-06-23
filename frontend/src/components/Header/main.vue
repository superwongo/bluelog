<template>
  <div class="Header">
    <el-menu :default-active="$route.path" mode="horizontal" :router="true" class="header-menu">
      <el-menu-item>
        <h1 class="header-title-logo"><img alt="Vue logo" src="@/assets/logo.png">&nbsp;部落格</h1>
      </el-menu-item>
      <el-menu-item index="/home">首页</el-menu-item>
      <el-menu-item index="/about">关于</el-menu-item>
      <el-submenu index="theme" class="header-title-theme">
        <template slot="title">主题</template>
        <el-menu-item>日间模式</el-menu-item>
        <el-menu-item>夜间模式</el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style lang="scss" scoped>
@import "~styles/common.scss";
.Header {
  .header-menu{
    padding: 0 10rem;
    .header-title-logo {
      color: rgb(65, 184, 131);
      img {
        width: 1.5em;
      }
    }
    .header-title-theme {
      float: right;
    }
  }
}
</style>
