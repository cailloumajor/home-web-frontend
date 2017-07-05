import _ from 'lodash'
import Toggleable from './toggleable'

export default {

  mixins: [Toggleable],

  props: {
    create: Boolean,
    formData: Object,
    schemaURL: {
      type: String,
      required: true
    }
  },

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

    validate () {
      this.resetErrors()
      this.$request({
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
      })
    }
  },

  watch: {
    dataIsOriginal (newVal) {
      if (this.action === 'remove' && !newVal) this.action = 'change'
    },

    errorOther (newVal) {
      if (newVal === false) this.isActive = false
    },

    isActive (newVal) {
      if (newVal) {
        this.action = this.create ? 'create' : 'remove'
        this.originalData = Object.assign({}, this.formData)
        this.instance = Object.assign({}, this.formData)
        this.resetErrors()
      }
    }
  },

  created () {
    this.$request({ url: this.schemaURL, method: 'options' })
      .then(response => {
        this.schema = response.data.actions.POST
      })
  }
}
