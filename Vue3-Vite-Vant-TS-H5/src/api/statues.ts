/**
 * 景点相关API
 */
import axiosInstance from '@/uitls/request'

// 获取景点列表
export const getStatues = (params?: { skip?: number; limit?: number }) => {
  return axiosInstance.get('/api/v1/statues', { params: params || {} })
}

// 获取景点详情
export const getStatue = (id: number) => {
  return axiosInstance.get(`/api/v1/statues/${id}`)
}

// 获取附近的景点
export const getNearbyStatues = (params: {
  latitude: number
  longitude: number
  radius?: number
}) => {
  return axiosInstance.get('/api/v1/statues/nearby', { params })
}
