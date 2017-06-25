import axios from 'axios'

export default {
  data () {
    return {
      fetchData: null,
      fetchStatus: 'undefined'
    }
  },

  methods: {
    fetch (url) {
      this.fetchStatus = 'loading'
      axios.get(url)
        .then(response => {
          this.fetchData = response.data
          this.fetchStatus = 'loaded'
        })
        .catch(error => {
          if (error.response) {
            const resp = error.response
            console.log(
              'Error: %s - %s\nResponse data: %s\nResponse headers: %o',
              resp.status, resp.statusText, resp.data, resp.headers
            )
          } else {
            console.log('Error:', error.message)
          }
          console.log('Axios config:', error.config)
          this.fetchStatus = 'error'
        })
    }
  }
}
