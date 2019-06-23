import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/views/Index'
import Home from '@/views/Home'
import About from '@/views/About'
import Post from '@/views/Post'

Vue.use(Router)

const IndexRoute = {
  path: '/',
  component: Index,
  redirect: '/home',
  children: [
    {
      path: 'home',
      component: Home
    },
    {
      path: 'about',
      component: About
    },
    {
      path: 'post/:post_id',
      component: Post
    }
  ]
}

let routes = [
  IndexRoute
]

const routerContext = require.context('./', true, /index\.js$/)
routerContext.keys().forEach(route => {
  // 排除根目录下的index.js
  if (route.startsWith('./index')) {
    return
  }
  const routerModule = routerContext(route)
  /**
   * 兼容 import export 和 require module.export 两种规范
   */
  routes = [...routes, ...(routerModule.default || routerModule)]
})

export default new Router({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: routes
})
