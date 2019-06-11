<template>
  <div class="Header">
    <el-menu :default-active="$route.path" mode="horizontal" :router="true">
      <el-menu-item>
        <h1 class="header-title"><img alt="Vue logo" src="../../assets/logo.png">部落格</h1>
      </el-menu-item>
      <el-menu-item index="/home">首页</el-menu-item>
      <el-menu-item index="/about">关于</el-menu-item>
      <div class="right-menu">
        <el-dropdown class="theme" trigger="click">
          <span class="el-dropdown-link">
            主题<i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>日间模式</el-dropdown-item>
            <el-dropdown-item>夜间模式</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style lang="scss" scoped>
.Header {
  .header-title {
    display: flex;
    align-items: center;
    color: rgb(65, 184, 131);
    height: 20px;
    img {
      width: 30px;
    }
  }
  .right-menu {
    float: right;
    height: 100%;
    &:focus {
      outline: none;
    }
    .theme {
      height: 60px;
      line-height: 60px;
      margin-right: 30px;
    }
  }
}
</style>
