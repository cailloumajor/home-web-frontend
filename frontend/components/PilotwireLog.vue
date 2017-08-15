<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :loading="loading"
    :pagination.sync="pagination"
    hide-actions
  >
    <template slot="items" scope="props">
      <td
        v-for="field in headers.map(el => el.value)"
        v-text="props.item[field]"
        :class="colorClass(props.item.level)"
      ></td>
    </template>
  </v-data-table>
</template>

<script>
export default {

  name: 'pilotwire-log',

  props: ['isActive'],

  data () {
    return {
      headers: [
        { text: 'Date/Heure', value: 'timestamp', align: 'left' },
        { text: 'Niveau', value: 'level', align: 'left' },
        { text: 'Message', value: 'message', align: 'left' }
      ],
      items: [],
      loading: true,
      pagination: {}
    }
  },

  watch: {
    isActive (newVal) {
      if (newVal) {
        this.getData()
      }
    }
  },

  methods: {
    colorClass (level) {
      const color = {
        INFO: 'green',
        WARNING: 'orange',
        ERROR: 'red'
      }[level]
      return `${color}--text`
    },

    getData () {
      this.loading = true
      this.$axios.get('/heating/pilotwirelog/')
        .then(response => {
          this.items = response.data
          this.pagination.sortBy = 'timestamp'
          this.pagination.descending = true
          this.pagination.rowsPerPage = -1
          this.loading = false
        })
    }
  }
}
</script>

<style lang="scss" scoped>
/* satisfy stylelint */
</style>
