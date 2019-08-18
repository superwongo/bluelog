import request from './index'

export function getCategories () {
  return request({
    url: '/categories',
    method: 'get'
  })
}
