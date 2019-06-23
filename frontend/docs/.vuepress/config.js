module.exports = {
  title: 'Hello VuePress',
  description: 'Just playing around',
  plugins: [
    '@vuepress/blog',
    {
      directories: [
        {
          id: 'post',
          dirname: '_posts',
          path: '/'
        }
      ]
    }
  ]
}