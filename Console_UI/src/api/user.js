import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/M2/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/M2/userinfo',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/M2/logout',
    method: 'post'
  })
}
