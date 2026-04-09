/**
 * 打卡相关API
 */
import axiosInstance from '@/uitls/request'

// 打卡
export const checkIn = (data: {
  statue_id: number
  latitude: number
  longitude: number
}) => {
  return axiosInstance.post('/api/v1/checkins', data)
}

// 获取我的打卡记录
export const getMyCheckIns = () => {
  return axiosInstance.get('/api/v1/checkins/my')
}

// 获取打卡统计
export const getCheckInStatistics = () => {
  return axiosInstance.get('/api/v1/checkins/statistics')
}
