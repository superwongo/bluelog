export function ResponseErrorHandle (response) {
  const result = response.data
  const errorMessage = []
  if (typeof result === 'object') {
    for (const key in result) {
      errorMessage.push(key + ': ' + result[key].join('，'))
    }
    return errorMessage.join('；')
  } else {
    return result
  }
}
