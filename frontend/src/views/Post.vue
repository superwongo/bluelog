<template>
  <div class="Post">
    <h1>{{ post.title }}</h1>
    <p>{{ post.body }}</p>
  </div>
</template>

<script>
import { getPost } from '@/api/post'

export default {
  name: 'Post',
  data () {
    return {
      post: {}
    }
  },
  created () {
    this.get_post()
  },
  methods: {
    get_post () {
      const postID = this.$route.params.post_id
      getPost(postID).then(response => {
        this.post = Object.assign({}, response.data)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.Post {

}
</style>
