<template>
  <div v-if="status === 'loading'" class="centering">
    <v-progress-circular :size="progressSize" :width="6" indeterminate>
    </v-progress-circular>
  </div>
  <table v-else-if="status === 'loaded'">
    <thead><tr>
      <th
        v-for="header in headers"
        :style="{ width: header.width + 'px' }"
        class="centered-cell"
      >
        {{ header.text }}
      </th>
    </tr></thead>
    <tbody :style="{ height: tbodyHeight + 'px' }">
      <template v-for="entry in logData">
        <tr :class="logColors[entry.level] + '--text'">
          <td v-text="new Date(entry.timestamp).toLocaleString()"></td>
          <td class="centered-cell">{{ entry.level }}</td>
          <td :style="{ width: messageColWidth + 'px' }">
            {{ entry.message }}
          </td>
        </tr>
      </template>
    </tbody>
  </table>
  <error v-else-if="status === 'error'">
    Erreur de récupération du journal.
  </error>
  <div v-else class="centering">
    <v-icon x-large>help_outline</v-icon>
  </div>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
import Error from 'components/Error'

export default {

  name: 'pilotwire-log',

  data () {
    return {
      headers: [
        { text: 'Date/Heure', width: null },
        { text: 'Niveau', width: null },
        { text: 'Message', width: null }
      ],
      logColors: {
        INFO: 'green',
        WARNING: 'orange',
        ERROR: 'red'
      },
      logData: [],
      messageColWidth: null,
      progressSize: 50,
      status: 'undefined',
      tbodyHeight: null
    }
  },

  components: {
    Error
  },

  methods: {
    fetchLog () {
      this.status = 'loading'
      axios.get('/api/heating/pilotwirelog/')
        .then(response => {
          this.logData = response.data
          this.status = 'loaded'
        })
        .catch(error => {
          console.error(error)
          this.status = 'error'
        })
    },

    resize () {
      const thead = this.$el.querySelector('thead')
      const tbody = this.$el.querySelector('tbody')
      const tbodyColumns = this.$el.querySelectorAll('tbody tr:first-child td')
      const columnWidths = [].map.call(tbodyColumns, el => el.offsetWidth)
      const lastColWidth = this.$el.offsetWidth - _.sum(_.initial(columnWidths))
      let scrollBarWidth

      // Resize tbody height
      this.tbodyHeight = (
        this.$el.parentElement.offsetHeight - thead.offsetHeight
      )

      // Resize columns width
      this.$nextTick(() => {
        scrollBarWidth = thead.scrollWidth - tbody.scrollWidth
        columnWidths.splice(-1, 1, lastColWidth)
        columnWidths.map((width, index) => {
          this.headers[index].width = width
        })
        this.$nextTick(() => {
          this.messageColWidth = _.last(columnWidths) - scrollBarWidth
        })
      })
    }
  },

  props: ['isActive'],

  watch: {
    isActive () {
      if (this.isActive) this.fetchLog()
    },

    status () {
      if (this.status === 'loaded') {
        this.$nextTick(() => {
          setTimeout(this.resize, 0)
        })
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
table
  thead
  tbody
    display: block

  tbody
    overflow-y: auto

    td
      padding-top: 4px
      padding-bottom: 4px

.centering
  display: flex
  height: 100%
  align-items: center
  justify-content: center

.centered-cell
  text-align: center
</style>
