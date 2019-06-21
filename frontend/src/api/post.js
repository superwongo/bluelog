import request from './index'

export function getPosts () {
  return request({
    url: '/posts',
    method: 'get'
  })
}
