import moxios from 'moxios'
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
    expect(defaultData.logData).to.be.instanceof(Array).that.is.empty
    expect(defaultData.messageColWidth).to.be.null
    expect(defaultData.status).to.equal('undefined')
    expect(defaultData.tbodyHeight).to.be.null
  })

  describe('`fetchLog` method', function () {
    const url = '/api/heating/pilotwirelog/'

    beforeEach(function () {
      moxios.install()
      sinon.stub(console, 'error')
    })

    afterEach(function () {
      moxios.uninstall()
      console.error.restore()
    })

    it('should be declared', function () {
      expect(PilotwireLog.methods.fetchLog).to.be.a('function')
    })

    it('should react to success log fetching', function (done) {
      moxios.stubRequest(url, { status: 200, response: log })
      const vm = new Vue(PilotwireLog).$mount()
      vm.resize = Function.prototype // noop
      vm.fetchLog()
      moxios.wait(() => {
        expect(vm.logData).to.equal(log)
        expect(vm.status).to.equal('loaded')
        expect(console.error).to.not.have.been.called
        done()
      })
    })

    it('should react to failing log fetching', function (done) {
      moxios.stubRequest(url, { status: 500 })
      const vm = new Vue(PilotwireLog).$mount()
      vm.resize = Function.prototype // noop
      vm.fetchLog()
      moxios.wait(() => {
        expect(vm.logData).to.be.empty
        expect(vm.status).to.equal('error')
        expect(console.error).to.have.been.called
        done()
      })
    })
  })

  describe('`isActive` prop', function () {
    it('should be declared', function () {
      expect(PilotwireLog.props).to.have.key('isActive')
    })

    it('should not fetch log when going false', function (done) {
      const vm = new Vue(PilotwireLog).$mount()
      sinon.stub(vm, 'fetchLog')
      vm.isActive = false
      Vue.nextTick(() => {
        expect(vm.fetchLog).to.not.have.been.called
        done()
      })
    })

    it('should fetch log when going true', function (done) {
      const vm = new Vue(PilotwireLog).$mount()
      sinon.stub(vm, 'fetchLog')
      vm.isActive = true
      Vue.nextTick(() => {
        expect(vm.fetchLog).to.have.been.called.once
        done()
      })
    })
  })

  describe('`status` watcher', function () {
    it('should be declared', function () {
      expect(PilotwireLog.watch.status).to.be.a('function')
    })

    it('should call `resize` method when loaded', function (done) {
      const vm = new Vue(PilotwireLog).$mount()
      sinon.stub(vm, 'resize')
      expect(vm.resize).to.not.have.been.called
      vm.status = 'not loaded'
      expect(vm.resize).to.not.have.been.called
      vm.status = 'loaded'
      Vue.nextTick(() => {
        setTimeout(() => {
          expect(vm.resize).to.have.been.called.once
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
      vm.logData = log
      vm.status = 'loaded'
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
