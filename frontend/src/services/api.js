import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000, 
  headers: {
    'Content-Type': 'application/json'
  }
})

export const api = {

  async getDashboardData() {
    const response = await apiClient.get('/api/v1/dashboard')
    return response.data
  },
}