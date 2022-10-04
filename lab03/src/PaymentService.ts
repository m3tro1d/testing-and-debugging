import { Dispatcher, Event } from './Dispatcher'

type Invoice = {
  id: number
  total: number
}

function createInvoiceCreatedEvent(invoiceId: number): Event {
  return {
    name: 'invoice_created',
    id: invoiceId,
  }
}

function createInvoiceRevokedEvent(invoiceId: number): Event {
  return {
    name: 'invoice_revoked',
    id: invoiceId,
  }
}

class PaymentService {
  private invoices: Invoice[] = []
  private invoiceId = 0

  private readonly dispatcher: Dispatcher

  public constructor(dispatcher: Dispatcher) {
    this.dispatcher = dispatcher
  }

  public createInvoice(total: number): void {
    this.validateTotal(total)

    const invoiceId = this.nextInvoiceId()
    this.invoices.push({
      id: invoiceId,
      total: total,
    })
    this.dispatcher.dispatch(createInvoiceCreatedEvent(invoiceId))
  }

  public revokeInvoice(invoiceId: number): void {
    const index = this.invoices.findIndex(invoice => invoice.id == invoiceId)
    if (index === -1) {
      return
    }

    this.invoices.splice(index, 1)
    this.dispatcher.dispatch(createInvoiceRevokedEvent(invoiceId))
  }

  public getInvoices(): Invoice[] {
    return this.invoices.slice()
  }

  public getInvoice(invoiceId: number): Invoice | undefined {
    return this.invoices.find(invoice => invoice.id === invoiceId)
  }

  private nextInvoiceId(): number {
    ++this.invoiceId
    return this.invoiceId
  }

  private validateTotal(total: number): void {
    if (total <= 0) {
      throw new RangeError('Invalid invoice total')
    }
  }
}

export {
  PaymentService,
}
