<template>
  <div class="home">
    <img alt="Vue logo" src="../../assets/logo.png">
    <HelloWorld :msg="`Welcome to Your Vue.js App, ${this.getUserInfo.name}`"/>
  </div>
</template>

<script>

import userMixin from '@/mixins/user-mixin'

export default {
  name: 'home',
  mixins: [userMixin]
}
</script>
