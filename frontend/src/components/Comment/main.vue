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
            <span class="badge-primary" v-if="item.from_admin">作者</span>
            <div v-if="item.replied">&nbsp;&nbsp;回复</div>
          </div>
          <div class="comment-card-time">{{ item.timestamp | formatTimeFromNow }}</div>
        </div>
        <p class="comment-card-line comment-replay-content" v-if="item.replied">{{ item.replied.author }}:<br/>{{ item.replied.body }}</p>
        <div class="comment-card-line">{{ item.body }}</div>
        <div class="comment-card-line"><el-button size="medium" class="comment-card-replay">回复</el-button></div>
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
      :total="total">
    </el-pagination>
  </div>
</template>

<script>
import { formatTimeFromNow } from '@/filter'

export default {
  name: 'Comment',
  props: {
    data: {
      type: Array,
      default () {
        return []
      }
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
  methods: {
    handleSizeChange (val) {
      this.$emit('size-change', val)
    },
    handleCurrentChange (val) {
      this.$emit('current-change', val)
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
          display: inline-block;
          font-weight: 700;
          color: #ffffff;
          background-color: #2780E3;
          line-height: 1rem;
          padding: 0.25rem;
          margin: 0 0.25rem;
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
