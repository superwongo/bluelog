<template>
  <div class="Post">
    <h1 class="post-title">{{ post.title }}</h1>
    <small class="post-subtitle">
      &nbsp;分类: <router-link to="/category">{{post.category.name}}</router-link><br>
      &nbsp;日期: {{ post.timestamp | formatDate }}
    </small>
    <Markdown v-model="markdownValue" class="post-content" :editable="false" :subfield="false"/>
    <el-button type="primary" size="small" icon="el-icon-share" class="post-share">分享</el-button>
    <Comment
      :data="comments"
      :currentPage="currentPage"
      :pageSize="pageSize"
      :total="total"
      :postID="post_id"
      @current-change="handleCurrentChange"
      @refresh-comment="refreshCommentsInfo"
      class="post-comments"/>

  </div>
</template>

<script>
import { getPost } from '@/api/post'
import Markdown from '@/components/Markdown'
import Comment from '@/components/Comment'
import { formatDate } from '@/utils/filters'
import { getComments } from '@/api/comment'

export default {
  name: 'Post',
  components: {
    Markdown,
    Comment
  },
  data () {
    return {
      post_id: this.$route.params.post_id,
      post: {
        category: {},
        body: '',
        timestamp: ''
      },
      comments: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      markdownValue: {
        markdown: '',
        html: ''
      }
    }
  },
  created () {
    this.getPost()
    this.getCommentsInfo()
  },
  methods: {
    anchorOffsetTop (selector) {
      const anchor = this.$el.querySelector(selector)
      if (anchor) {
        document.documentElement.scrollTop = anchor.offsetTop
      }
    },
    getPost () {
      getPost(this.post_id).then(response => {
        this.post = Object.assign({}, response.data)
        this.markdownValue = Object.assign({}, {
          markdown: response.data.body,
          html: ''
        })
      })
    },
    getCommentsInfo () {
      getComments(this.post_id, this.currentPage, this.pageSize).then(response => {
        let result = response.data
        this.comments = Object.assign([], result.items)
        this.currentPage = result.current_page
        this.pageSize = result.per_page
        this.total = result.total
      })
    },
    refreshCommentsInfo() {
      this.getCommentsInfo()
      this.anchorOffsetTop('.post-share')
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.refreshCommentsInfo()
    }
  },
  filters: {
    formatDate
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
  .post-share {
    margin: 1.25rem 0;
  }
}
</style>
