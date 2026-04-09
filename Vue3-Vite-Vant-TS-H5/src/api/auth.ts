import axiosInstance, { AxiosResponseProps } from '@/uitls/request'

// 发送邮箱验证码
export const sendCode = (email: string) => {
  return axiosInstance.post<AxiosResponseProps>('/api/v1/auth/send-code', { email })
}

// 注册：邮箱 + 验证码 + 密码 + 昵称
export const register = (params: {
  email: string
  code: string
  password: string
  nickname: string
}) => {
  return axiosInstance.post<AxiosResponseProps>('/api/v1/auth/register', params)
}

// 登录：账号（用户名/邮箱/手机）+ 密码
export const login = (params: { account: string; password: string }) => {
  return axiosInstance.post<AxiosResponseProps>('/api/v1/auth/login', params)
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return axiosInstance.get<AxiosResponseProps>('/api/v1/auth/me')
}

// 更新个人资料：昵称 / 手机 / 邮箱 / 头像
export const updateProfile = (params: {
  nickname?: string
  phone?: string
  email?: string
  avatar_url?: string
}) => {
  return axiosInstance.put<AxiosResponseProps>('/api/v1/auth/update-profile', params)
}

// 修改密码：当前密码 + 新密码
export const changePassword = (params: { old_password: string; new_password: string }) => {
  return axiosInstance.post<AxiosResponseProps>('/api/v1/auth/change-password', params)
}

// 忘记密码：发送重置验证码到邮箱
export const forgotPassword = (email: string) => {
  return axiosInstance.post<AxiosResponseProps>('/api/v1/auth/forgot-password', { email })
}

// 重置密码：邮箱 + 验证码 + 新密码
export const resetPassword = (params: { email: string; code: string; new_password: string }) => {
  return axiosInstance.post<AxiosResponseProps>('/api/v1/auth/reset-password', params)
}

// 上传头像
export const uploadAvatar = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return axiosInstance.post<AxiosResponseProps>('/api/v1/upload/avatar', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
