<template>
  <div class="home">
    <div v-for="(item, index) in posts.items" :key="item.id">
      <Post :post="item"/>
      <el-divider v-if="index !== posts.items.length-1"/>
    </div>
  </div>
</template>

<script>

import userMixin from '@/mixins/user-mixin'
import { getPosts } from '@/api/post'
import Post from '@/components/Post'

export default {
  name: 'home',
  mixins: [userMixin],
  components: { Post },
  data () {
    return {
      posts: {}
    }
  },
  created () {
    this.get_posts()
  },
  methods: {
    get_posts () {
      getPosts().then(response => {
        this.posts = response.data
        // console.log(`>>>>>>>>getPosts>>>>>>>>>>${JSON.stringify(this.posts)}`)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  padding-top: 50px;
}
</style>
