import moment from 'moment'

export function formatTimeFromNow (value) {
  return moment(value, 'YYYY-MM-DD HH-mm-ss', 'zh-cn').fromNow()
}

export function formatDatetime (value) {
  return moment(value, 'YYYY-MM-DD HH-mm-ss', 'zh-cn').format('LLL')
}

export function formatDate (value) {
  return moment(value, 'YYYY-MM-DD HH-mm-ss', 'zh-cn').format('LL')
}
