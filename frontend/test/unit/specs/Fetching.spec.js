import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'
import Vue from 'vue'
import Fetching from '@/mixins/Fetching'

describe('Fetching mixin', function () {
  it('should set correct default data', function () {
    expect(Fetching.data).to.be.a('function')
    const defaultData = Fetching.data()
    expect(defaultData.fetchData).to.be.null()
    expect(defaultData.fetchStatus).to.equal('undefined')
  })

  describe('`fetch` method', function () {
    const url = 'test'
    const responseData = 'test_data'
    let mock, sandbox, vm

    beforeEach(function () {
      mock = new MockAdapter(axios)
      sandbox = sinon.sandbox.create()
      vm = new Vue(Fetching)
    })

    afterEach(function () {
      mock.restore()
      sandbox.restore()
    })

    it('should be declared', function () {
      expect(Fetching.methods.fetch).to.be.a('function')
    })

    it('should set loading status', function () {
      const noop = new Promise((resolve, reject) => null)
      sandbox.stub(axios, 'get').returns(noop)
      expect(vm.fetchStatus).to.equal('undefined')
      vm.fetch('')
      expect(vm.fetchStatus).to.equal('loading')
      axios.get.restore()
    })

    it('should react to successful fetching', function (done) {
      sandbox.stub(console, 'log')
      mock.onGet(url).reply(200, responseData)
      vm.fetch(url)
      setTimeout(() => {
        expect(vm.fetchData).to.equal(responseData)
        expect(vm.fetchStatus).to.equal('loaded')
        expect(console.log).to.not.have.been.called()
        done()
      }, 100)
    })

    it('should react to server error', function (done) {
      sandbox.stub(console, 'log')
      mock.onGet(url).reply(500)
      vm.fetch(url)
      setTimeout(() => {
        expect(vm.fetchData).to.be.null()
        expect(vm.fetchStatus).to.equal('error')
        expect(console.log).to.have.been.calledTwice()
        expect(console.log).to.have.been.calledWith(
          sinon.match.string, 500, sinon.match.any,
          sinon.match.any, sinon.match.any
        )
        done()
      }, 100)
    })

    it('should react to request error', function (done) {
      sandbox.stub(console, 'log')
      mock.onGet(url).reply(config => {
        return new Promise((resolve, reject) => {
          reject({ message: 'test_error' })
        })
      })
      vm.fetch(url)
      setTimeout(() => {
        expect(vm.fetchData).to.be.null()
        expect(vm.fetchStatus).to.equal('error')
        expect(console.log).to.have.been.calledTwice()
        expect(console.log).to.have.been.calledWith(
          sinon.match.string, 'test_error'
        )
        done()
      }, 100)
    })
  })
})
