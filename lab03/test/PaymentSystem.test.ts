import { PaymentService } from '../src/PaymentService'
import { Dispatcher } from '../src/Dispatcher'
import { mock, mockClear } from 'jest-mock-extended'

describe('payment service', () => {
  const mockDispatcher = mock<Dispatcher>();
  let service: PaymentService

  beforeEach(() => {
    mockClear(mockDispatcher)
    service = new PaymentService(mockDispatcher)
  })

  describe('invoice creation', () => {
    test('create an invoice', () => {
      const total = 200;
      service.createInvoice(total)

      expect(mockDispatcher.dispatch).toHaveBeenCalledTimes(1)
      expect(mockDispatcher.dispatch).toHaveBeenCalledWith({
        name: 'invoice_created',
        id: 1
      })

      expect(service.getInvoices()).toHaveLength(1)
      expect(service.getInvoice(1)).toStrictEqual({
        id: 1,
        total: total,
      })
    })

    test('persistent invoice numbering', () => {
      service.createInvoice(1)
      service.revokeInvoice(1)
      service.createInvoice(2)

      expect(service.getInvoices()).toHaveLength(1)
      expect(service.getInvoice(2)).toHaveProperty('id', 2)
    })

    test('invoice total validation', () => {
      expect(() => service.createInvoice(0)).toThrowError(RangeError)
      expect(() => service.createInvoice(-1)).toThrowError(RangeError)

      expect(mockDispatcher.dispatch).not.toHaveBeenCalled()
      expect(service.getInvoices()).toHaveLength(0)
    })
  })

  describe('invoice revoking', () => {
    beforeEach(() => {
      const total = 200
      service.createInvoice(total)
      mockClear(mockDispatcher)
    })

    test('revoke existing invoice', () => {
      service.revokeInvoice(1)

      expect(mockDispatcher.dispatch).toHaveBeenCalledTimes(1)
      expect(mockDispatcher.dispatch).toHaveBeenCalledWith({
        name: 'invoice_revoked',
        id: 1,
      })

      expect(service.getInvoices).toHaveLength(0)
    })

    test('revoke nonexisting invoice', () => {
      service.revokeInvoice(0)

      expect(mockDispatcher.dispatch).not.toHaveBeenCalled()
      expect(service.getInvoices()).toHaveLength(1)
    })
  })

  describe('finding invoice by ID', () => {
    const total = 200

    beforeEach(() => {
      service.createInvoice(total)
    })

    test('find existing invoice', () => {
      expect(service.getInvoice(1)).toStrictEqual({
        id: 1,
        total: total,
      })
    })

    test('find nonexisting invoice', () => {
      expect(service.getInvoice(42)).toBeUndefined()
    })
  })
})
