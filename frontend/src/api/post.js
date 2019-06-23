import request from './index'

export function getPosts (currentPage, pageSize) {
  return request({
    url: `/posts?page=${currentPage}&per_page=${pageSize}`,
    method: 'get'
  })
}

export function getPost (postID) {
  return request({
    url: `/post/${postID}`,
    method: 'get'
  })
}
