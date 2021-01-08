import axios from 'axios'
// import Cookies from 'js-cookie'
axios.defaults.withCredentials = true
axios.defaults.baseURL = '/'

// const token = Cookies.get('OPSRAMP_JWT_TOKEN')

// axios.defaults.headers.common['Authorization'] = `bearer ${token}`
export default axios
