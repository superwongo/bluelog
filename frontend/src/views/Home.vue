<template>
  <div class="Home">
    <h1 class="home-title">Blueblog</h1>
    <h4 class="home-subtitle">No, I'm the real thing.</h4>
    <div v-for="(item, index) in posts" :key="item.id">
      <Post :post="item"/>
      <el-divider v-if="index !== posts.length-1"/>
    </div>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[5, 10, 15, 20]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total">
    </el-pagination>
  </div>
</template>

<script>

import userMixin from '@/mixins/user-mixin'
import { getPosts } from '@/api/post'
import Post from '@/components/Post'

export default {
  name: 'Home',
  mixins: [userMixin],
  components: { Post },
  data () {
    return {
      posts: [],
      currentPage: 1,
      pageSize: 10,
      total: 0
    }
  },
  created () {
    this.get_posts()
  },
  methods: {
    get_posts () {
      getPosts(this.currentPage, this.pageSize).then(response => {
        let result = response.data
        this.posts = Object.assign([], result.items)
        this.currentPage = result.current_page
        this.pageSize = result.per_page
        this.total = result.total
      })
    },
    handleSizeChange (val) {
      this.pageSize = val
      this.get_posts()
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.get_posts()
    }
  }
}
</script>

<style lang="scss" scoped>
.Home {
  .home-title {
    font-size: 4.5rem;
    font-weight: 300;
    line-height: 1.2;
    text-align: left;
    margin-bottom: 0.5rem;
  }
  .home-subtitle {
    color: #868e96 !important;
    font-size: 1.4rem;
    font-weight: 300;
    line-height: 1.2;
    text-align: left;
    margin-left: 0.5rem;
    margin-bottom: 1.5rem;
  }
  .el-pagination {
    padding-top: 3rem;
    text-align: left;
  }
}
</style>
