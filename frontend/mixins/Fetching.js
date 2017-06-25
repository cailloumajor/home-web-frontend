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
      this.$get(url)
        .then(response => {
          this.fetchData = response.data
          this.fetchStatus = 'loaded'
        })
        .catch(() => {
          this.fetchStatus = 'error'
        })
    }
  }
}
