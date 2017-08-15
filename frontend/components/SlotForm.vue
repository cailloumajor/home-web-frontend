<template>
  <v-dialog v-if="schema" v-model="isActive" width="650">
    <v-card v-show="!errorOther">
      <v-card-title>
        {{ operation }} un créneau
      </v-card-title>
      <v-card-text>
        <div
          v-text="`Zone ${zone.num} - ${zone.desc}`"
          class="zone-info"
        ></div>
        <v-select
          v-model="instance.mode"
          :error-messages="errors.mode"
          :items="schema.mode.choices"
          :label="schema.mode.label"
          :required="schema.mode.required"
          item-text="display_name"
        ></v-select>
        <v-layout row wrap>
          <v-flex md6 xs12>
            <v-select
              v-model="instance.start_time"
              :error-messages="errors.start_time"
              :items="startTimeItems"
              :label="schema.start_time.label"
              :required="schema.start_time.required"
            ></v-select>
          </v-flex>
          <v-flex md6 xs12>
            <v-select
              v-model="instance.end_time"
              :error-messages="errors.end_time"
              :items="endTimeItems"
              :label="schema.end_time.label"
              :required="schema.end_time.required"
            ></v-select>
          </v-flex>
        </v-layout>
        <v-layout row>
          <v-flex v-for="day in days" :key="day" xs2>
            <v-checkbox
              v-model="instance[day]"
              :label="schema[day].label.substring(0, 3) + '.'"
              :required="schema[day].required"
              color="primary"
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
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="isActive = false" class="primary--text" flat dark>
          Annuler
        </v-btn>
        <v-btn @click="validate" class="primary--text" flat dark>
          {{ operation }}
        </v-btn>
      </v-card-actions>
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
import Days from '~/mixins/Days'
import HeatingForm from '~/mixins/heating-form'

export default {

  name: 'slot-form',

  mixins: [Days, HeatingForm],

  props: ['zone'],

  computed: {
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

  watch: {
    isActive (newVal) {
      if (newVal && this.create) {
        this.instance.mode = null
        this.instance.start_time = null
        this.instance.end_time = null
      }
    }
  },

  methods: {
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
    }
  }
}
</script>

<style lang="scss" scoped>
.card__title { /* stylelint-disable selector-class-pattern */
  font-size: 1.3rem;
  padding: 15px 24px 20px !important;
}

.zone-info {
  margin-bottom: 2rem;
}
</style>
