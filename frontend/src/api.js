import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
const API = axios.create({ baseURL })

export default {
  chat: (payload) => API.post('/chat', payload).then(r => r.data),
  upload: (file) => {
    const fd = new FormData();
    fd.append('file', file)
    return API.post('/upload', fd, { headers: {'Content-Type':'multipart/form-data'} }).then(r => r.data)
  },
  tickets: () => API.get('/tickets').then(r => r.data),
  createTicket: (payload) => API.post('/ticket', payload).then(r => r.data),
  history: (sessionId) => API.get(`/history/${sessionId}`).then(r => r.data)
}
