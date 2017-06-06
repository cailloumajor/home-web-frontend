<template>
  <v-dialog v-if="schema" v-model="isActive" width="650">
    <v-card v-show="!errorOther">
      <v-card-title>
        {{ operation }} une dérogation
      </v-card-title>
      <v-card-row>
        <v-card-text>
          <v-select
            v-model="instance.zones"
            :items="schema.zones.choices"
            :label="schema.zones.label"
            :required="schema.zones.required"
            :rules="[isValid('zones')]"
            item-text="desc"
            item-value="url"
            multiple
          ></v-select>
        </v-card-text>
      </v-card-row>
    </v-card>
  </v-dialog>
</template>

<script>
import HeatingForm from '~/mixins/heating-form'

export default {

  name: 'derogation-form',

  mixins: [HeatingForm],

  watch: {
    isActive (newVal) {
      if (newVal && this.create) {
        /* this.instance.mode = null
         * this.instance.start_time = null
         * this.instance.end_time = null */
      }
    },

    schema (newVal) {
      if (newVal.zones) {
        this.schema.zones.choices = this.$store.state.heating.zones
      }
    }
  }
}
</script>

<style lang="stylus" scoped>
.card__title
  font-size: 1.3rem
  padding: 15px 24px 20px 24px !important
</style>
