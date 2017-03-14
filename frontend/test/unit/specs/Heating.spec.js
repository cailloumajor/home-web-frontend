import Vue from 'vue'
import Heating from '@/pages/Heating'

describe('Heating.vue page', function () {
  it('should set the correct default data', function () {
    expect(Heating.data).to.be.a('function')
    const defaultData = Heating.data()
    expect(defaultData.activeTab).to.be.null
    expect(defaultData.tabsItemsHeight).to.be.above(0)
  })

  it('should have `fetchURL` computed property', function () {
    expect(Heating.computed.fetchURL).to.be.a('function')
    expect(Heating.computed.fetchURL()).to.be.a('string')
  })

  it('should have an `updated` hook', function () {
    expect(Heating.updated).to.be.a('function')
  })

  describe('`created` hook', function () {
    it('should be declared', function () {
      expect(Heating.created).to.be.a('function')
    })

    it('should call the `fetch` method', function () {
      const Component = Object.assign({}, Heating)
      Component.mixins = [{
        data () {
          return { fetchCalled: false }
        },
        methods: {
          fetch () { this.fetchCalled = true }
        }
      }]
      const vm = new Vue(Component)
      expect(vm.fetchCalled).to.be.true
    })
  })
})
