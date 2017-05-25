<template>
  <v-dialog v-if="schema" v-model="dialog" width="650">
    <v-card v-show="!errorOther">
      <v-card-title>
        {{ operation }} un créneau
      </v-card-title>
      <v-card-row>
        <v-card-text>
          <div
            v-text="`Zone ${zone.num} - ${zone.desc}`"
            class="zone-info"
          ></div>
          <v-select
            v-model="slot.mode"
            :items="schema.mode.choices"
            :label="schema.mode.label"
            :required="schema.mode.required"
            :rules="[isValid('mode')]"
            item-text="display_name"
          ></v-select>
          <v-layout row wrap>
            <v-flex md6 xs12>
              <v-select
                v-model="slot.start_time"
                :items="startTimeItems"
                :label="schema.start_time.label"
                :max-height="240"
                :required="schema.start_time.required"
                :rules="[isValid('start_time')]"
              ></v-select>
            </v-flex>
            <v-flex md6 xs12>
              <v-select
                v-model="slot.end_time"
                :items="endTimeItems"
                :label="schema.end_time.label"
                :max-height="240"
                :required="schema.end_time.required"
                :rules="[isValid('end_time')]"
              ></v-select>
            </v-flex>
          </v-layout>
          <v-layout row>
            <v-flex v-for="day in days" :key="day" xs2>
              <v-checkbox
                v-model="slot[day]"
                :label="schema[day].label.substring(0, 3) + '.'"
                :required="schema[day].required"
                primary
              ></v-checkbox>
            </v-flex>
          </v-layout>
          <div
            v-for="error in errors.non_field_errors"
            class="error--text"
          >
            {{ error }}
          </div>
          <small>* Champs obligatoires</small>
        </v-card-text>
      </v-card-row>
      <v-card-row actions>
        <v-btn @click.native="dialog = false" class="primary--text" flat light>
          Annuler
        </v-btn>
        <v-btn @click.native="validate" class="primary--text" flat light>
          {{ operation }}
        </v-btn>
      </v-card-row>
    </v-card>
    <v-alert v-model="errorOther" error dismissible>
      Une erreur s'est produite.
      <br>
      Voir la console pour plus de détails.
    </v-alert>
  </v-dialog>
</template>

<script>
import _ from 'lodash'
import axios from 'axios'
import Days from '@/mixins/Days'

export default {

  name: 'slot-form',

  mixins: [Days],

  data () {
    return {
      action: null,
      dialog: false,
      errorOther: false,
      errors: {},
      originalSlot: null,
      schema: null,
      slot: {},
      zone: {}
    }
  },

  computed: {
    operation () {
      return {
        'create': 'Créer',
        'change': 'Modifier',
        'remove': 'Supprimer'
      }[this.action]
    },

    slotIsOriginal () {
      return _.isEqual(this.slot, this.originalSlot)
    },

    startTimeItems () {
      const items = this.timeItems()
      if (this.slot.end_time) {
        return items.slice(0, items.indexOf(this.slot.end_time))
      } else {
        return items
      }
    },

    endTimeItems () {
      const items = this.timeItems()
      const sliceStart = this.slot.start_time
        ? items.indexOf(this.slot.start_time)
        : 0
      return items.slice(sliceStart + 1).concat('00:00')
    }
  },

  methods: {
    isValid (fieldName) {
      return this.errors[fieldName] || true
    },

    resetErrors () {
      this.errors = {}
      this.errorOther = false
    },

    timeItems () {
      const hours = _.range(0, 24)
      const minutes = _.range(0, 60, 15)
      const padAll = arr => arr.map(n => _.padStart(n, 2, '0'))
      let items = []
      padAll(hours).map(hour => {
        padAll(minutes).map(minute => {
          items.push(`${hour}:${minute}`)
        })
      })
      return items
    },

    validate () {
      this.resetErrors()
      axios({
        method: {
          'create': 'post',
          'change': 'put',
          'remove': 'delete'
        }[this.action],
        url: this.slot.url,
        data: this.action !== 'remove' ? this.slot : undefined
      }).then(response => {
        this.$localBus.$emit('slot-form-success', this.zone.num)
        this.dialog = false
      }).catch(error => {
        if (error.response) {
          if (error.response.status === 400) {
            this.errors = error.response.data
          } else {
            console.log(error.response.data)
            console.log(error.response.status)
            console.log(error.response.headers)
            this.errorOther = true
          }
        } else if (error.request) {
          console.log(error.request)
        } else {
          console.log('Error', error.message)
        }
      })
    }
  },

  watch: {
    errorOther (newVal) {
      if (newVal === false) this.dialog = false
    },

    slotIsOriginal (newVal) {
      if (this.action === 'remove' && !newVal) this.action = 'change'
    }
  },

  created () {
    axios.options('/api/heating/slots/')
      .then(response => {
        this.schema = response.data.actions.POST
      })
  },

  mounted () {
    this.$localBus.$on('slot-change', (create, zone, slot) => {
      console.log(slot)
      this.action = create ? 'create' : 'remove'
      this.zone = Object.assign({}, zone)
      this.originalSlot = Object.assign({}, slot)
      this.slot = Object.assign({}, slot)
      if (create) {
        this.slot.mode = null
        this.slot.start_time = null
        this.slot.end_time = null
      }
      this.resetErrors()
      this.dialog = true
    })
  }
}
</script>

<style lang="stylus" scoped>
.card__title
  font-size: 1.3rem
  padding: 15px 24px 20px 24px !important

.zone-info
  margin-bottom: 2rem
</style>
