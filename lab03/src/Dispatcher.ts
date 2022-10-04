interface Event {
  name: string
  id: number
}

interface Dispatcher {
  dispatch(event: Event): void
}

export {
  Dispatcher,
  Event,
}
