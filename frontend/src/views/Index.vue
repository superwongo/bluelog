<template>
  <div class="Index">
    <el-container>
      <el-header>
        <Header/>
      </el-header>
      <el-main>
        <router-view :key="key"/>
      </el-main>
      <el-footer>
        <Footer/>
      </el-footer>
      <el-backtop target=".el-container .is-vertical"></el-backtop>
    </el-container>
  </div>
</template>

<script>

import Header from '@/components/Header'
import Footer from '@/components/Footer'

export default {
  name: 'Index',
  components: {
    Header,
    Footer
  },
  computed: {
    key () {
      return this.$route.fullPath
    }
  }
}
</script>

<style lang="scss" scoped>
.Index{
  .el-container {
    margin-bottom: 40px;
    .el-header {
      position: fixed;
      width: 100%;
      left: 0;
      top: 0;
      z-index: 1500;
    }
    .el-main {
      margin-top: 40px;
      text-align: center;
    }
  }
}
</style>
