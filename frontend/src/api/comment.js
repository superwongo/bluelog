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
