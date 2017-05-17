import Vue from 'vue'
import PilotwireLog from '@/components/PilotwireLog'

describe('PilotwireLog component', function () {
  it('should set correct default data', function () {
    expect(PilotwireLog.data).to.be.a('function')
    const defaultData = PilotwireLog.data()
    expect(defaultData.headers).to.have.lengthOf(3)
    expect(defaultData.logColors).to.have.keys('INFO', 'WARNING', 'ERROR')
  })

  describe('`isActive` property watcher', function () {
    it('should not fetch log when property becomes false', function (done) {
      const Ctor = Vue.extend(PilotwireLog)
      const propsData = { isActive: true }
      const vm = new Ctor({ propsData })
      sinon.stub(vm, 'fetch')
      vm.isActive = false
      Vue.nextTick(() => {
        expect(vm.fetch).to.not.have.been.called()
        done()
      })
    })

    it('should fetch log when property becomes true', function (done) {
      const Ctor = Vue.extend(PilotwireLog)
      const propsData = { isActive: false }
      const vm = new Ctor({ propsData })
      sinon.stub(vm, 'fetch')
      vm.isActive = true
      Vue.nextTick(() => {
        expect(vm.fetch).to.have.been.calledOnce()
        done()
      })
    })
  })
})
