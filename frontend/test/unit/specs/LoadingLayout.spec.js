import LoadingLayout from '@/components/LoadingLayout'

describe('LoadingLayout component', function () {
  it('should set correct default data', function () {
    expect(LoadingLayout.data).to.be.a('function')
    const defaultData = LoadingLayout.data()
    expect(defaultData.progressSize).to.be.above(0)
  })

  it('should accept properties', function () {
    expect(LoadingLayout.props).to.have.keys('errorText', 'status')
  })
})
