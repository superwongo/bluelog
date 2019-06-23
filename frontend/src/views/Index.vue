<template>
  <div class="index">
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
      width: 100%;
      z-index: 1500;
    }
    .el-main {
      text-align: center;
      padding: 4.5rem 10rem;
    }
    .el-footer {
      padding: 0rem 10rem;
    }
  }
}
</style>
