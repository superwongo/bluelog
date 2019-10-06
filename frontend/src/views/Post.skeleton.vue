<template>
  <div class="skeleton-post">
    <div class="skeleton-post-title"><skeleton height="2.5rem" width="10rem"/></div>
    <div class="skeleton-post-subtitle">
      <p><skeleton height="1rem" width="2.5rem"/></p>
      <p><skeleton height="1rem" width="5rem"/></p>
    </div>
    <div class="skeleton-post-left-content fl">
      <div v-for="i in 50" :key="i" class="skeleton-post-line">
        <skeleton height="1rem" :width="`${getRndInteger(30,70)}rem`"/>
      </div>
    </div>
    <div class="skeleton-post-right-content fr">
      <div class="skeleton-post-right-title">
        <skeleton height="2.5rem" width="20rem"/>
      </div>
      <div v-for="i in 20" :key="i" class="skeleton-post-right-line">
        <skeleton height="1rem" :width="`${getRndInteger(5,10)}rem`"/>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'PostSkeleton',
  data () {
    return {
      msg: 'hello vue'
    }
  },
  methods: {
    getRndInteger (min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min
    }
  }
}
</script>
<style lang="scss" scoped>
.skeleton-post {
  .skeleton-post-title {
    padding-bottom: 0.5rem;
  }
  .skeleton-post-subtitle{
    padding-bottom: 0.5rem;
    p {
      margin: 0;
      padding: 0;
      padding-bottom: 0.25rem;
    }
  }
  .skeleton-post-left-content {
    padding-top: 2rem;
    .skeleton-post-line {
      padding-bottom: 0.5rem;
    }
  }
  .skeleton-post-right-content {
    padding-top: 2rem;
    .skeleton-post-right-title{
      padding-bottom: 0.5rem;
    }
    .skeleton-post-right-line{
      padding-bottom: 0.5rem;
    }
  }
}
</style>
