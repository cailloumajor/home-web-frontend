<template>
  <v-dialog v-if="schema" v-model="isActive" width="650">
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
            v-model="instance.mode"
            :items="schema.mode.choices"
            :label="schema.mode.label"
            :required="schema.mode.required"
            :rules="[isValid('mode')]"
            item-text="display_name"
          ></v-select>
          <v-layout row wrap>
            <v-flex md6 xs12>
              <v-select
                v-model="instance.start_time"
                :items="startTimeItems"
                :label="schema.start_time.label"
                :max-height="240"
                :required="schema.start_time.required"
                :rules="[isValid('start_time')]"
              ></v-select>
            </v-flex>
            <v-flex md6 xs12>
              <v-select
                v-model="instance.end_time"
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
                v-model="instance[day]"
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
        <v-btn @click.native="isActive = false" class="primary--text" flat light>
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
import Toggleable from '@/mixins/toggleable'
import Days from '@/mixins/Days'

export default {

  name: 'slot-form',

  mixins: [Days, Toggleable],

  props: ['create', 'formData', 'schemaURL', 'zone'],

  data () {
    return {
      action: null,
      errorOther: false,
      errors: {},
      originalData: null,
      schema: null,
      instance: {}
    }
  },

  computed: {
    dataIsOriginal () {
      return _.isEqual(this.instance, this.originalData)
    },

    operation () {
      return {
        'create': 'Créer',
        'change': 'Modifier',
        'remove': 'Supprimer'
      }[this.action]
    },

    startTimeItems () {
      const items = this.timeItems()
      if (this.instance.end_time) {
        return items.slice(0, items.indexOf(this.instance.end_time))
      } else {
        return items
      }
    },

    endTimeItems () {
      const items = this.timeItems()
      const sliceStart = this.instance.start_time
        ? items.indexOf(this.instance.start_time)
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
        url: this.instance.url,
        data: this.action !== 'remove' ? this.instance : undefined
      }).then(response => {
        this.isActive = false
        this.$nextTick(() => { this.$emit('success') })
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
      if (newVal === false) this.isActive = false
    },

    isActive (newVal) {
      if (newVal) {
        this.action = this.create ? 'create' : 'remove'
        this.originalData = Object.assign({}, this.formData)
        this.instance = Object.assign({}, this.formData)
        if (this.create) {
          this.instance.mode = null
          this.instance.start_time = null
          this.instance.end_time = null
        }
        this.resetErrors()
      }
    },

    dataIsOriginal (newVal) {
      if (this.action === 'remove' && !newVal) this.action = 'change'
    }
  },

  created () {
    axios.options(this.schemaURL)
      .then(response => {
        this.schema = response.data.actions.POST
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
