<template>
  <div class="Post">
    <h1 class="post-title">{{ post.title }}</h1>
    <small class="post-subtitle">
      &nbsp;分类: <router-link to="/category">{{post.category.name}}</router-link><br>
      &nbsp;日期: {{ post.timestamp }}
    </small>
    <Markdown style="max-height: 600px;" v-model="markdownValue" class="post-content" :editable="false" :subfield="false"/>
  </div>
</template>

<script>
import { getPost } from '@/api/post'
import Markdown from '@/components/Markdown'

export default {
  name: 'Post',
  components: {
    Markdown
  },
  data () {
    return {
      post: {
        category: {},
        body: '',
        timestamp: ''
      },
      markdownValue: {
        markdown: '',
        html: ''
      }
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
         this.markdownValue = Object.assign({}, {
           markdown: response.data.body,
           html: ''
         })
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
  .post-content {
    padding-top: 1rem;
  }
}
</style>
