<template>
  <div>
    <div id="nav">
      <router-link to="/home">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view :key="key"/>
  </div>
</template>

<script>
export default {
  name: 'Index',
  computed: {
    key () {
      return this.$route.fullPath
    }
  }
}
</script>

<style scoped>

</style>
