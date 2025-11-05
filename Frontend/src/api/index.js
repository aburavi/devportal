import {axios, async} from 'axios'

export default {
  async request(method, uri, ddata = null, headers = {}, authorization = false) {
    if (!method) {
      return
    }
    if (!uri) {
      return
    }
    
    var token = ''
    if (authorization) {
      token = window.localStorage.getItem('openapi-token')
      headers['Authorization'] = 'Bearer '+ token
      headers['Content-Type'] = 'application/json'
      //headers['Content-Type'] = 'multipart/form-data'
      //headers['Content-Type'] = 'application/x-www-form-urlencoded'
    } else {
      headers['Content-Type'] = 'application/json'
      // headers['Content-Type'] = 'multipart/form-data'
      // headers['Content-Type'] = 'application/x-www-form-urlencoded'
    }
    
    try 
      {
        const {data:response} = await axios({method, uri, ddata, headers:headers})
        return response
      }
    catch (error) {
      console.log(error);
      return error
    }
  },
}
