<template>
  <div class="Comment">
    <h3 class="comment-title">15 评论 latest</h3>
    <div class="comment-content">
      <el-card :body-style="{ padding: '1px' }" shadow="hover" class="comment-card">
        <div class="comment-card-line">
          <div class="comment-card-line1">
            <a href="">刘桂芳</a>
            <div>5天前</div>
          </div>
          <div class="comment-card-line2">发生网络威望一直控制包括其中.</div>
          <div class="comment-card-line3 fr">回复</div>
        </div>
      </el-card>
      <el-card :body-style="{ padding: '1px' }" shadow="hover" class="comment-card">
        <div class="comment-card-line">
          <div class="comment-card-line1">
            <a href="">刘桂芳</a>
            <div>5天前</div>
          </div>
          <div class="comment-card-line2">发生网络威望一直控制包括其中.</div>
          <div class="comment-card-line3 fr">回复</div>
        </div>
      </el-card>
      <el-card :body-style="{ padding: '1px' }" shadow="hover" class="comment-card">
        <div class="comment-card-line">
          <div class="comment-card-line1">
            <a href="">刘桂芳</a>
            <div>5天前</div>
          </div>
          <div class="comment-card-line2">发生网络威望一直控制包括其中.</div>
          <div class="comment-card-line3 fr">回复</div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Comment'
}
</script>

<style lang="scss" scoped>
.Comment {
  .comment-title {
    font-size: 1.5rem;
    font-weight: 300;
    line-height: 1.2;
    margin: 1rem 0;
  }
  .comment-content {}
  .comment-card {
    border-radius: 0;
    border: 1px solid rgba(0,0,0,0.125);
    border-bottom: none;
    .comment-card-line {
      padding: 1rem;
      line-height: 1.5rem;
      .comment-card-line1 {
        @include spaceBetween(row)
      }
    }
  }
  .comment-card:last-child{
    border-bottom: 1px solid rgba(0,0,0,0.125);
  }
}
</style>
