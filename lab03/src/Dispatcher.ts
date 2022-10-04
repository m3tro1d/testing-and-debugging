interface Event {
  name: string
  id: number
}

interface Handler {
  handle(event: Event): void
}

interface Dispatcher {
  dispatch(event: Event): void
  subscribe(eventName: string, handler: Handler): void
}

export {
  Dispatcher,
  Event,
}
