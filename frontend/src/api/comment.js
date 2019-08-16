import request from './index'

export function getComments (postID, currentPage, pageSize) {
  return request({
    url: `/comments?post_id=${postID}&page=${currentPage}&per_page=${pageSize}`,
    method: 'get'
  })
}

export function getComment (commentID) {
  return request({
    url: `/comment/${commentID}`,
    method: 'get'
  })
}

export function submitComment (postID, commentInfo) {
  return request({
    url: '/comments',
    method: 'post',
    data: {
      post_id: postID,
      author: commentInfo.author,
      email: commentInfo.email,
      site: commentInfo.site,
      body: commentInfo.body
    }
  })
}
