/**
 * 拍照相关 API
 */
import request from '@/uitls/request'

/**
 * 上传拍照
 */
export const uploadPhoto = (formData: FormData) => {
  return request({
    url: '/api/v1/photos/upload',
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data: formData
  })
}

/**
 * 获取广场公开照片列表
 */
export const getPublicPhotos = (skip: number = 0, limit: number = 20) => {
  return request({
    url: '/api/v1/photos/public',
    method: 'get',
    params: { skip, limit }
  })
}

/**
 * 获取我的拍照列表
 */
export const getMyPhotos = (skip: number = 0, limit: number = 20) => {
  return request({
    url: '/api/v1/photos/my',
    method: 'get',
    params: { skip, limit }
  })
}

/**
 * 删除拍照
 */
export const deletePhoto = (photoId: number) => {
  return request({
    url: `/api/v1/photos/${photoId}`,
    method: 'delete'
  })
}

/**
 * 获取拍照统计
 */
export const getPhotoStats = () => {
  return request({
    url: '/api/v1/photos/stats',
    method: 'get'
  })
}

/**
 * 更新照片公开状态
 */
export const updatePhotoPublicStatus = (photoId: number, isPublic: boolean) => {
  const formData = new FormData()
  formData.append('is_public', isPublic.toString())
  
  return request({
    url: `/api/v1/photos/${photoId}/public`,
    method: 'patch',
    data: formData
  })
}
