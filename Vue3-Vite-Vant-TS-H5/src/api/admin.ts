/**
 * 管理员相关API
 */
import axiosInstance from '@/uitls/request'

// 景点管理
export const getAdminStatues = (params?: any) => {
  return axiosInstance.get('/api/v1/admin/statues', { params: params || {} })
}

export const getAdminStatue = (id: number) => {
  return axiosInstance.get(`/api/v1/admin/statues/${id}`)
}

export const createStatue = (data: any) => {
  return axiosInstance.post('/api/v1/admin/statues', data)
}

export const updateStatue = (id: number, data: any) => {
  return axiosInstance.put(`/api/v1/admin/statues/${id}`, data)
}

export const deleteStatue = (id: number) => {
  return axiosInstance.delete(`/api/v1/admin/statues/${id}`)
}

export const toggleStatueStatus = (id: number) => {
  return axiosInstance.patch(`/api/v1/admin/statues/${id}/toggle`)
}

export const batchUpdateOrder = (orderList: Array<{id: number, order_index: number}>) => {
  return axiosInstance.post('/api/v1/admin/statues/batch-update-order', orderList)
}

// 上传景点图片
export const uploadPhoto = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return axiosInstance.post('/api/v1/upload/photo', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
