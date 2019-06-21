<template>
  <div class="Post">
    <router-link tag="p" class="post-title" :to="`/about/${post.id}`">{{ post.title }}</router-link>
    <p class="post-body">
      {{ `${post.body.substr(0, 250)}...` }}
      <small>Read More</small>
    </p>
    <small>
      Comments: {{ post.comments.length }}&nbsp;&nbsp;
      Category: {{post.category.name}}
      <span class="post-timestamp">{{ post.timestamp }}</span>
    </small>
  </div>
</template>

<script>
export default {
  name: 'Post',
  props: {
    post: Object
  }
}
</script>

<style lang="scss" scoped>
.Post {
  text-align: left;
  .post-title {
    font-size: 24px;
    font-weight: lighter;
    color: #2780E3;
  }
  .post-timestamp {
    float: right;
  }
}
</style>
