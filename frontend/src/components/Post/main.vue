<template>
  <div class="Post">
    <router-link class="post-title" :to="`/post/${post.id}`">{{ post.title }}</router-link>
    <p class="post-body" v-if="post.body">
      {{ post.body.length > 250 ? `${post.body.substr(0, 250)}...` : post.body }}
      <small>
        <router-link :to="`/post/${post.id}`">Read More</router-link>
      </small>
    </p>
    <p v-else>空</p>
    <small>
      评论: <router-link to="/comment">{{ post.comments.length }}</router-link>&nbsp;&nbsp;
      分类: <router-link to="/category">{{post.category.name}}</router-link>
      <span class="fr">{{ post.timestamp }}</span>
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
  .post-title {
    @include sc(1.5rem, $light-blue);
    font-weight: lighter;
  }
}
</style>
