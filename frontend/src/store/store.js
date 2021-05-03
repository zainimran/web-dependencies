import { createStore, action, persist } from 'easy-peasy'

const store = createStore(persist({
	theme: 'light',
    toggleTheme: action((state, payload) => {
        state.theme = payload
    }),
    type: '',
    changeType: action((state, payload) => {
        state.type = String(payload).toLowerCase()
    }),
}))

export default store;