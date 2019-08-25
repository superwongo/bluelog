<template>
  <div class="index">
    <el-container class="pl8 pr8">
      <el-header>
        <Header/>
      </el-header>
      <el-main class="pt6">
        <router-view :key="key"/>
      </el-main>
      <el-footer>
        <Footer/>
      </el-footer>
    </el-container>
    <el-backtop/>
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
.index{
  .el-container {
    .el-header {
      position: fixed;
      top: 0;
      left: 6rem;
      right: 6rem;
      z-index: 2000;
    }
  }
}
</style>
