export const isAuthenticated = () => {
  return !!localStorage.getItem('token')
}

export const getAuthToken = () => {
  return localStorage.getItem('token')
}

export const getUserInfo = () => {
  return JSON.parse(localStorage.getItem('user') || '{}')
}

export const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  window.location.href = '/login'
}