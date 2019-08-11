<template>
  <div class="Comment">
    <h3 class="comment-title">{{ total }} 评论 latest</h3>
    <div class="comment-content">
      <el-card shadow="hover" class="comment-card" v-for="item in comments" :key="item.id">
        <div class="comment-card-line">
          <div class="comment-card-tag">
            <a href="" class="comment-card-author">
              {{ item.author }}
            </a>
            <span class="badge-primary" v-if="item.from_admin">作者</span>
            &nbsp;&nbsp;回复
          </div>
          <div class="comment-card-time">5天前</div>
        </div>
        <p class="comment-card-line comment-replay-content">陈芳:<br/>准备那些如此投资.</p>
        <div class="comment-card-line">{{ item.body }}</div>
        <div class="comment-card-line"><el-button size="medium" class="comment-card-replay">回复</el-button></div>
      </el-card>
    </div>
    <el-pagination
      small
      hide-on-single-page
      background
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[5, 10, 15, 20]"
      :page-size="pageSize"
      layout="prev, pager, next"
      :total="total">
    </el-pagination>
  </div>
</template>

<script>
import { getComments } from '@/api/comment'

export default {
  name: 'Comment',
  props: {
    post_id: {
      type: String
    }
  },
  data () {
    return {
      comments: [],
      currentPage: 1,
      pageSize: 10,
      total: 0
    }
  },
  created () {
    this.get_comments()
  },
  methods: {
    get_comments () {
      getComments(this.post_id, this.currentPage, this.pageSize).then(response => {
        let result = response.data
        console.log(result)
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
    }
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
  .comment-card {
    border-radius: 0;
    border: 1px solid rgba(0,0,0,0.125);
    border-bottom: none;
    line-height: 1.75rem;
    .comment-card-line:first-child {
      @include spaceBetween(row);
      .comment-card-tag {
        font-size: 0.8rem;
        font-weight: 600;
        .comment-card-author {
          font-size: 1.25rem;
          font-weight: 200;
        }
        .badge-primary {
          display: inline-block;
          font-weight: 700;
          color: #ffffff;
          background-color: #2780E3;
          line-height: 1rem;
          padding: 0.2rem;
        }
      }
      .comment-card-time {
        font-size: 0.8rem;
        font-weight: 300;
      }
    }
    .comment-card-line:last-child {
      text-align: right;
      .comment-card-replay {
        border: none;
        padding: 0.5rem;
      }
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
