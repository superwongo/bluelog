<template>
  <div class="Comment">
    <h3 class="comment-title">{{ total }} 评论 latest</h3>
    <div class="comment-content">
      <el-card shadow="hover" class="comment-card" v-for="item in data" :key="item.id">
        <div class="comment-card-line">
          <div class="comment-card-tag">
            <a href="" class="comment-card-author">
              {{ item.author }}
            </a>
            <el-tag class="badge-primary" v-if="item.from_admin" effect="dark">作者</el-tag>
            <div v-if="item.replied">&nbsp;&nbsp;回复</div>
          </div>
          <div class="comment-card-time">{{ item.timestamp | formatTimeFromNow }}</div>
        </div>
        <p class="comment-card-line comment-replay-content" v-if="item.replied">{{ item.replied.author }}:<br/>{{ item.replied.body }}</p>
        <div class="comment-card-line">{{ item.body }}</div>
        <div class="comment-card-line"><el-button size="medium" class="comment-card-replay" @click="replyComment(item.id, item.author)">回复</el-button></div>
      </el-card>
    </div>
    <el-pagination
      small
      background
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[5, 10, 15, 20]"
      :page-size="pageSize"
      :layout="layout"
      :total="total"
      v-if="total > 0">
    </el-pagination>
    <div class="comment-replied-anchor">
      <div class="comment-replied-info" v-show="repliedCommentAuthor">
        回复<strong>&nbsp;{{ repliedCommentAuthor }}</strong>
        <a @click="cancelReply()" class="fr">取消</a>
      </div>
    </div>
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
import { formatTimeFromNow } from '@/utils/filters'
import { submitComment } from '@/api/comment'

export default {
  name: 'Comment',
  props: {
    data: {
      type: Array,
      default () {
        return []
      }
    },
    postID: {
      type: String,
      required: true
    },
    layout: {
      type: String,
      default: 'prev, pager, next'
    },
    currentPage: {
      type: Number,
      default: 1
    },
    pageSize: {
      type: Number,
      default: 10
    },
    total: {
      type: Number,
      default: 0
    }
  },
  data () {
    return {
      repliedCommentAuthor: '',
      repliedCommentID: '',
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
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ],
        site: [
          { type: 'url', message: '请输入正确的网址', trigger: ['blur', 'change'] }
        ],
        body: [
          { required: true, message: '请输入评论内容', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    anchorOffsetTop (selector) {
      const anchor = this.$el.querySelector(selector)
      if (anchor) {
        document.documentElement.scrollTop = anchor.offsetTop
      }
    },
    replyComment (commentID, commentAuthor) {
      this.repliedCommentAuthor = commentAuthor
      this.repliedCommentID = commentID
      this.anchorOffsetTop('.comment-replied-anchor')
    },
    cancelReply () {
      this.repliedCommentAuthor = ''
      this.anchorOffsetTop('.comment-title')
    },
    handleSizeChange (val) {
      this.$emit('size-change', val)
    },
    handleCurrentChange (val) {
      this.$emit('current-change', val)
    },
    submitForm (formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          submitComment(this.postID, this.ruleForm, this.repliedCommentID).then(response => {
            if (response.status === 200 || response.status === 201) {
              this.$emit('refresh-comment')
              this.repliedCommentAuthor = ''
              this.repliedCommentID = ''
              this.resetForm(formName)
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
  },
  filters: {
    formatTimeFromNow
  }
}
</script>

<style lang="scss" scoped>
.Comment {
  .comment-title {
    font-size: 1.5rem;
    font-weight: 300;
    margin: 1rem 0;
  }
  .comment-replied-info {
    margin: 1rem 0;
    padding: 1rem 1rem;
    background-color: #d7d8d8;
  }
  .comment-card {
    border-radius: 0;
    border: 1px solid rgba(0,0,0,0.125);
    border-bottom: none;
    line-height: 1.75rem;
    .comment-card-line {
      .comment-card-tag {
        @include flex(row);
        font-size: 0.8rem;
        font-weight: 600;
        .comment-card-author {
          font-size: 1.25rem;
          font-weight: 200;
        }
        .badge-primary {
          padding: 0 0.25rem;
          margin: 0 0.25rem;
          border-radius: 0;
        }
      }
      .comment-card-time {
        font-size: 0.8rem;
        font-weight: 300;
      }
      .comment-card-replay {
        border: none;
        padding: 0.5rem;
      }
    }
    .comment-card-line:first-child {
      @include spaceBetween(row);
    }
    .comment-card-line:last-child {
      text-align: right;
    }
    .comment-replay-content {
      margin: 0.25rem;
      padding: 1rem;
      color: #1d1e1f;
      background-color: #d7d8d8;
      border-color: #c7c8c8;
    }
  }
  .comment-card:last-child{
    border-bottom: 1px solid rgba(0,0,0,0.125);
  }
  .el-pagination {
    padding-left: 0;
    margin-top: 0.25rem;
  }
}
</style>
