import Vue from 'vue'
import PilotwireLog from '@/components/PilotwireLog'

describe('PilotwireLog component', function () {
  const log = [0, 1, 2].map(el => {
    const dt = new Date()
    dt.setHours(el)
    return {
      timestamp: dt.toISOString(),
      level: ['INFO', 'WARNING', 'ERROR'][el],
      message: 'Message ' + el
    }
  })

  it('should set correct default data', function () {
    expect(PilotwireLog.data).to.be.a('function')
    const defaultData = PilotwireLog.data()
    expect(defaultData.headers).to.have.lengthOf(3)
      .and.to.all.have.keys('text', 'width')
    expect(defaultData.logColors).to.have.keys('INFO', 'WARNING', 'ERROR')
    expect(defaultData.messageColWidth).to.be.null
    expect(defaultData.tbodyHeight).to.be.null
  })

  describe('`isActive` property watcher', function () {
    it('should not fetch log when property becomes false', function (done) {
      const Ctor = Vue.extend(PilotwireLog)
      const propsData = { isActive: true }
      const vm = new Ctor({ propsData })
      sinon.stub(vm, 'fetch')
      vm.isActive = false
      Vue.nextTick(() => {
        expect(vm.fetch).to.not.have.been.called
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
        expect(vm.fetch).to.have.been.called.once
        done()
      })
    })
  })

  describe('`fetchStatus` watcher', function () {
    it('should be declared', function () {
      expect(PilotwireLog.watch.fetchStatus).to.be.a('function')
    })

    it('should call `resize` method when loaded', function (done) {
      const vm = new Vue(PilotwireLog).$mount()
      sinon.stub(vm, 'resize')
      expect(vm.resize).to.not.have.been.called
      vm.fetchStatus = 'loaded'
      Vue.nextTick(() => {
        setTimeout(() => {
          expect(vm.resize).to.have.been.called.once
          done()
        }, 50)
      })
    })

    it('should not call `resize` method when not loaded', function (done) {
      const vm = new Vue(PilotwireLog).$mount()
      sinon.stub(vm, 'resize')
      expect(vm.resize).to.not.have.been.called
      vm.fetchStatus = 'not loaded'
      Vue.nextTick(() => {
        setTimeout(() => {
          expect(vm.resize).to.not.have.been.called.once
          done()
        }, 50)
      })
    })
  })

  describe('`resize` method', function () {
    it('should be declared', function () {
      expect(PilotwireLog.methods.resize).to.be.a('function')
    })

    it('should serve its purpose', function (done) {
      const app = document.createElement('div')
      app.id = 'app'
      document.body.appendChild(app)
      const Ctor = Vue.extend(PilotwireLog)
      const vm = new Ctor({ el: '#app' })
      vm.fetchData = log
      vm.fetchStatus = 'loaded'
      Vue.nextTick(() => {
        setTimeout(() => {
          expect(vm.tbodyHeight).to.be.above(0, 'tbodyHeight')
          const widths = vm.headers.map((el) => el.width)
          expect(widths).to.all.be.above(0, 'headers.width')
          expect(vm.messageColWidth).to.be.above(0, 'messageColWidth')
          done()
        }, 50)
      })
    })
  })
})
