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

  async getCategories() {
    const response = await apiClient.get('/api/v1/categories')
    return response.data
  },

  async addCategory(categoryData) {
    const response = await apiClient.post('/api/v1/categories', categoryData)
    return response.data
  },

  async updateCategory(categoryData) {
    const response = await apiClient.put(`/api/v1/categories/${categoryData.id}`, categoryData)
    return response.data
  },

  async unlinkSubCategory(categoryId, subCategoryId) {
    await apiClient.put(`/api/v1/categories/${categoryId}/sub/${subCategoryId}/unlink`)
  },

  async getTransactions() {
    const response = await apiClient.get('/api/v1/transactions')
    return response.data
  },

  async updateTransactionCategories(transactionId, primaryCategoryId, secondaryCategoryId) {
    const response = await apiClient.put(`/api/v1/transactions/${transactionId}`, {
      primary_category_id: primaryCategoryId,
      secondary_category_id: secondaryCategoryId
    })
    return response.data
  }
}