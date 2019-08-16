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
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      class="post-comments"/>
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" class="comment-submit mt1">
      <el-form-item label="姓名" prop="author">
        <el-input v-model="ruleForm.author"></el-input>
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="ruleForm.email"></el-input>
      </el-form-item>
      <el-form-item label="网址" prop="site">
        <el-input v-model="ruleForm.site"></el-input>
      </el-form-item>
      <el-form-item label="评论" prop="body">
        <el-input type="textarea" v-model="ruleForm.body"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" size="small" @click="submitForm('ruleForm')">提交</el-button>
        <el-button size="small" @click="resetForm('ruleForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getPost } from '@/api/post'
import Markdown from '@/components/Markdown'
import Comment from '@/components/Comment'
import { formatDate } from '@/filter'
import { getComments, submitComment } from '@/api/comment'

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
      },
      ruleForm: {
        author: '',
        email: '',
        site: '',
        body: ''
      },
      rules: {
        author: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        email: [
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ],
        site: [
          { type: 'url', message: '请输入正确的网址', trigger: ['blur', 'change'] }
        ],
        body: [
          { required: true, message: '请输入评论内容', trigger: 'blur' }
        ]
      },
      submitForm (formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            submitComment(this.post_id, this.ruleForm).then(response => {
              if (response.data.code === 200 || response.data.code === 201) {
                this.get_comments()
                this.$message({
                  type: 'success',
                  message: '评论提交成功'
                })
              }
            })
          } else {
            return false
          }
        })
      },
      resetForm (formName) {
        this.$refs[formName].resetFields()
      }
    }
  },
  created () {
    this.get_post()
    this.get_comments()
  },
  methods: {
    get_post () {
      getPost(this.post_id).then(response => {
        this.post = Object.assign({}, response.data)
        this.markdownValue = Object.assign({}, {
          markdown: response.data.body,
          html: ''
        })
      })
    },
    get_comments () {
      getComments(this.post_id, this.currentPage, this.pageSize).then(response => {
        let result = response.data
        this.comments = Object.assign([], result.items)
        this.currentPage = result.current_page
        this.pageSize = result.per_page
        this.total = result.total
      })
    },
    handleSizeChange (val) {
      this.pageSize = val
      this.get_comments()
    },
    handleCurrentChange (val) {
      this.currentPage = val
      this.get_comments()
      const anchor = this.$el.querySelector('.post-comments')
      document.documentElement.scrollTop = anchor.offsetTop
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
