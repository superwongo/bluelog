<template>
  <div class="Post">
    <h1 class="post-title">{{ post.title }}</h1>
    <small class="post-subtitle">
      &nbsp;分类: <router-link to="/category">{{post.category.name}}</router-link><br>
      &nbsp;日期: {{ post.timestamp }}
    </small>
    <markdown-editor v-model="post.body" height="800px" :options="{hideModeSwitch:true,previewStyle:'tab'}" />
  </div>
</template>

<script>
import { getPost } from '@/api/post'
import MarkdownEditor from '@/components/MarkdownEditor'

export default {
  name: 'Post',
  data () {
    return {
      post: {}
    }
  },
  components: { MarkdownEditor },
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
  .post-title {
    font-size: 2rem;
    font-weight: 300;
    line-height: 1.2;
    margin-bottom: 0.5rem;
  }
  .post-subtitle {
    font-weight: 300;
  }
}
</style>
