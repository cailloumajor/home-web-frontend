import moxios from 'moxios'
import Vue from 'vue'
import Heating from 'src/pages/Heating'

describe('Heating.vue page', function () {
  it('should set the correct default data', function () {
    expect(Heating.data).to.be.a('function')
    const defaultData = Heating.data()
    expect(defaultData.tabsItemsHeight).to.be.above(0)
    expect(defaultData.zones).to.be.instanceof(Array).that.is.empty
    expect(defaultData.zonesError).to.be.false
    expect(defaultData.zonesReady).to.be.false
  })

  it('should declare an `updated` hook', function () {
    expect(Heating.updated).to.be.a('function')
  })

  describe('`created` hook', function () {
    const url = '/api/heating/zones/'

    beforeEach(function () {
      moxios.install()
      sinon.stub(console, 'error')
    })

    afterEach(function () {
      moxios.uninstall()
      console.error.restore()
    })

    it('should be declared', function () {
      expect(Heating.created).to.be.a('function')
    })

    it('should react to success zones fetching', function (done) {
      const zones = [
        { num: 1, desc: 'Zone de test 1' },
        { num: 2, desc: 'Zone de test 2' }
      ]
      moxios.stubRequest(url, { status: 200, response: zones })
      const vm = new Vue(Heating).$mount()
      moxios.wait(() => {
        expect(vm.zones).to.equal(zones)
        expect(vm.zonesError).to.be.false
        expect(vm.zonesReady).to.be.true
        expect(console.error).to.not.have.been.called
        done()
      })
    })

    it('should react to failing zones fetching', function (done) {
      moxios.stubRequest(url, { status: 500 })
      const vm = new Vue(Heating).$mount()
      moxios.wait(() => {
        expect(vm.zones).to.be.empty
        expect(vm.zonesError).to.be.true
        expect(vm.zonesReady).to.be.false
        expect(console.error).to.have.been.called
        done()
      })
    })
  })
})
