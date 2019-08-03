<template>
  <div class="Header">
    <el-menu :default-active="activeIndex" mode="horizontal" class="header-menu pl10 pr10">
      <el-menu-item>
        <h1 class="header-title-logo"><img alt="Vue logo" src="@/assets/logo.png">&nbsp;部落格</h1>
      </el-menu-item>
      <el-menu-item index="home"><router-link to="/home">首页</router-link></el-menu-item>
      <el-menu-item index="about"><router-link to="/about">关于</router-link></el-menu-item>
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
  name: 'Header',
  data () {
    return {
      activeIndex: 'home'
    }
  }
}
</script>

<style lang="scss" scoped>
.Header {
  .header-menu{
    .header-title-logo {
      color: $green;
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
