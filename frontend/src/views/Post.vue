<template>
  <div class="Post">
    <PostSkeleton v-if="!init"></PostSkeleton>
    <div v-else>
      <h1 class="post-title">{{ post.title }}</h1>
      <small class="post-subtitle">
        <p>分类: <router-link to="/category">{{post.category.name}}</router-link></p>
        <p>日期: {{ post.timestamp | formatDate }}</p>
      </small>
      <div class="post-left fl">
        <Markdown v-model="markdownValue" class="post-content" :editable="false" :subfield="false"/>
        <el-button type="primary" size="small" icon="el-icon-share" class="post-share">分享</el-button>
        <Comment
          :data="comments"
          :currentPage="currentPage"
          :pageSize="pageSize"
          :total="total"
          :postID="postID"
          @current-change="handleCurrentChange"
          @refresh-comment="refreshCommentsInfo"
          class="post-comments"/>
      </div>
      <el-card class="post-right fr" shadow :body-style="categoryBodyStyle">
        <div slot="header" class="category-title">
          <span>分类</span>
        </div>
        <div v-for="(item, index) in categories" :key="item.id" class="category-content">
          <el-row class="category-content-line">
            <el-col :span="18"><a>{{ item.name }}</a></el-col>
            <el-col :span="6"><el-tag effect="dark" size="small">{{ item.posts.length }}</el-tag></el-col>
          </el-row>
          <el-divider v-if="index !== categories.length-1"></el-divider>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { getPost } from '@/api/post'
import Markdown from '@/components/Markdown'
import Comment from '@/components/Comment'
import { formatDate } from '@/utils/filters'
import { getComments } from '@/api/comment'
import { getCategories } from '@/api/category'
import PostSkeleton from '@/views/Post.skeleton'

export default {
  name: 'Post',
  components: {
    Markdown,
    Comment,
    PostSkeleton
  },
  data () {
    return {
      init: false,
      postID: this.$route.params.post_id,
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
      },
      categories: [],
      categoryBodyStyle: {
        backgroundColor: '#fff',
        padding: '0'
      }
    }
  },
  created () {
    this.resetScrollTop()
    this.getPost()
    this.getCommentsInfo()
    this.getCategoriesInfo()
  },
  methods: {
    resetScrollTop () {
      document.documentElement.scrollTop = null
    },
    anchorOffsetTop (selector) {
      const anchor = this.$el.querySelector(selector)
      if (anchor) {
        document.documentElement.scrollTop = anchor.offsetTop
      }
    },
    getPost () {
      getPost(this.postID).then(response => {
        this.post = Object.assign({}, response.data)
        this.markdownValue = Object.assign({}, {
          markdown: response.data.body,
          html: ''
        })
      })
    },
    getCommentsInfo () {
      getComments(this.postID, this.currentPage, this.pageSize).then(response => {
        let result = response.data
        this.comments = Object.assign([], result.items)
        this.currentPage = result.current_page
        this.pageSize = result.per_page
        this.total = result.total
      })
    },
    refreshCommentsInfo () {
      this.getCommentsInfo()
      this.anchorOffsetTop('.post-share')
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.refreshCommentsInfo()
    },
    getCategoriesInfo () {
      getCategories().then(response => {
        this.categories = Object.assign([], response.data)
        this.init = true
      })
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
    margin-bottom: 0.5rem;
    p {
      margin: 0;
      padding: 0;
      font-weight: 300;
    }
  }
  .post-left {
    width: 70%;
    .post-content {
      padding-top: 1rem;
    }
    .post-share {
      margin: 1.25rem 0;
    }
  }
  .post-right {
    margin-top: 1rem;
    width: 20%;
    background-color: rgba(0,0,0,0.03);
    .category-title {
      padding: 0 1rem;
    }
    .category-content {
      .category-content-line {
        padding: 0 2rem;
      }
      .el-divider {
        margin: 0.75rem 0;
      }
    }
    .category-content:first-child {
      padding-top: 0.5rem;
    }
    .category-content:last-child {
      padding-bottom: 0.5rem;
    }
  }
}
</style>
