<template>
  <div class="Footer">
    <hr>
    <div class="footer">
      <small> &copy; 2019 &nbsp; &nbsp;
        <a href="https://github.com/superwongo" title="Written by Super Wong">Super Wong</a> -
        <a href="https://github.com/superwongo/bluelog" title="Fork me on GitHub">GitHub</a> -
        <a href="http://helloflask.com" title="A HelloFlask project">HelloFlask</a>
      </small>
      <small>
        登录
      </small>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style lang="scss" scoped>
.Footer {
  hr {
    color: #eeeeee;
  }
  .footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0px 30px;
    small > a {
      text-decoration: none;
    }
  }
}
</style>
