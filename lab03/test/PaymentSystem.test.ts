import { PaymentService } from '../src/PaymentService'
import { Dispatcher } from '../src/Dispatcher'
import { mock, mockClear } from 'jest-mock-extended'

describe('payment service', () => {
  const mockDispatcher = mock<Dispatcher>()
  let service: PaymentService

  beforeEach(() => {
    mockClear(mockDispatcher)
    service = new PaymentService(mockDispatcher)
  })

  describe('invoice creation', () => {
    test('creating an invoice dispatches an event and populates invoices', () => {
      const total = 200
      service.createInvoice(total)

      expect(mockDispatcher.dispatch).toHaveBeenCalledTimes(1)
      expect(mockDispatcher.dispatch).toHaveBeenCalledWith({
        name: 'invoice_created',
        id: 1,
      })

      expect(service.getInvoices()).toHaveLength(1)
      expect(service.getInvoice(1)).toStrictEqual({
        id: 1,
        total: total,
      })
    })

    test('creating and removing invoices do not break numbering', () => {
      service.createInvoice(1)
      service.revokeInvoice(1)
      service.createInvoice(2)

      expect(service.getInvoices()).toHaveLength(1)
      expect(service.getInvoice(2)).toHaveProperty('id', 2)
    })

    test('creating invoice with invalid total value throws an error', () => {
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

    test('revoking existing invoice dispatches an event and removes it from invoices', () => {
      service.revokeInvoice(1)

      expect(mockDispatcher.dispatch).toHaveBeenCalledTimes(1)
      expect(mockDispatcher.dispatch).toHaveBeenCalledWith({
        name: 'invoice_revoked',
        id: 1,
      })

      expect(service.getInvoices).toHaveLength(0)
    })

    test('revoking non existing invoice throws an error', () => {
      expect(() => service.revokeInvoice(0)).toThrowError()

      expect(mockDispatcher.dispatch).not.toHaveBeenCalled()
      expect(service.getInvoices()).toHaveLength(1)
    })
  })

  describe('finding invoice by ID', () => {
    const total = 200

    beforeEach(() => {
      service.createInvoice(total)
    })

    test('finding existing invoice returns corresponding invoice', () => {
      expect(service.getInvoice(1)).toStrictEqual({
        id: 1,
        total: total,
      })
    })

    test('finding non existing invoice throws error', () => {
      expect(() => service.getInvoice(42)).toThrowError()
    })
  })

  describe('changing invoice total', () => {
    const total = 200

    beforeEach(() => {
      service.createInvoice(total)
      mockClear(mockDispatcher)
    })

    test('change existing invoice total modifies the invoice total value', () => {
      const newTotal = 150
      service.changeInvoiceTotal(1, newTotal)

      expect(mockDispatcher.dispatch).toHaveBeenCalledTimes(1)
      expect(mockDispatcher.dispatch).toHaveBeenCalledWith({
        name: 'invoice_changed_total',
        id: 1,
      })

      expect(service.getInvoice(1).total).toStrictEqual(newTotal)
    })

    test('changing non existing invoice total throws error', () => {
      expect(() => service.changeInvoiceTotal(2, 150)).toThrowError()
      expect(mockDispatcher.dispatch).not.toHaveBeenCalled()
    })

    test('changing invoice total with invalid value throws error', () => {
      expect(() => service.changeInvoiceTotal(1, 0)).toThrowError(RangeError)
      expect(() => service.changeInvoiceTotal(1, -1)).toThrowError(RangeError)
      expect(mockDispatcher.dispatch).not.toHaveBeenCalled()
    })
  })
})
