<template>
  <div class="Post">
    <h1 class="post-title">{{ post.title }}</h1>
    <small class="post-subtitle">
      &nbsp;分类: <router-link to="/category">{{post.category.name}}</router-link><br>
      &nbsp;日期: {{ post.timestamp | formatDate }}
    </small>
    <Markdown v-model="markdownValue" class="post-content" :editable="false" :subfield="false"/>
    <el-button type="primary" size="small" icon="el-icon-share" class="post-share">分享</el-button>
    <Comment :post_id="$route.params.post_id"/>
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

export default {
  name: 'Post',
  components: {
    Markdown,
    Comment
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
            alert('submit!')
          } else {
            console.log('error submit!!')
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
