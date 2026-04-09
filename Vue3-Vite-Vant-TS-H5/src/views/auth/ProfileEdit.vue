<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Toast } from 'vant'
import { getCurrentUser, updateProfile, uploadAvatar } from '@/api/auth'
import type { UploaderFileListItem } from 'vant'
import logo from '@/assets/logo.png'

const router = useRouter()

const nickname = ref('')
const phone = ref('')
const email = ref('')
const avatarUrl = ref('')

const loading = ref(false)
const uploading = ref(false)

const loadFromStorage = () => {
  try {
    const raw = localStorage.getItem('current_user')
    if (raw) {
      const user = JSON.parse(raw)
      nickname.value = user.nickname || ''
      phone.value = user.phone || ''
      email.value = user.email || ''
      avatarUrl.value = user.avatar_url || ''
    }
  } catch (e) {}
}

const fetchProfile = async () => {
  try {
    const res: any = await getCurrentUser()
    if (res && res.code === 200 && res.data) {
      const user = res.data
      nickname.value = user.nickname || ''
      phone.value = user.phone || ''
      email.value = user.email || ''
      avatarUrl.value = user.avatar_url || ''
      
      localStorage.setItem('current_user', JSON.stringify(user))
    }
  } catch (e) {}
}

// 处理头像上传
const handleAvatarUpload = async (file: File) => {
  uploading.value = true
  try {
    const res: any = await uploadAvatar(file)
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || res?.msg || '上传失败')
      return false
    }
    
    // 上传成功，更新头像 URL
    const uploadedUrl = res.data?.url
    if (uploadedUrl) {
      avatarUrl.value = uploadedUrl
      Toast.success('头像上传成功')
      return true
    } else {
      Toast.fail('上传失败：未获取到图片地址')
      return false
    }
  } catch (e: any) {
    Toast.fail(e?.detail || e?.msg || '上传失败')
    return false
  } finally {
    uploading.value = false
  }
}

// Vant Uploader 的 before-read 回调
const beforeRead = (file: File) => {
  // 验证文件类型
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    Toast.fail('请上传 JPG、PNG 或 WEBP 格式的图片')
    return false
  }
  
  // 验证文件大小（5MB）
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    Toast.fail('图片大小不能超过 5MB')
    return false
  }
  
  return true
}

// Vant Uploader 的 after-read 回调
const afterRead = async (file: any) => {
  // 显示上传中状态
  file.status = 'uploading'
  file.message = '上传中...'
  
  const success = await handleAvatarUpload(file.file)
  
  if (success) {
    file.status = 'done'
    file.message = ''
  } else {
    file.status = 'failed'
    file.message = '上传失败'
  }
}

const handleSubmit = async () => {
  const payload: any = {}
  if (nickname.value) payload.nickname = nickname.value
  if (phone.value) payload.phone = phone.value
  if (email.value) payload.email = email.value
  if (avatarUrl.value) payload.avatar_url = avatarUrl.value

  if (Object.keys(payload).length === 0) {
    Toast.fail('请至少修改一项信息')
    return
  }

  loading.value = true
  try {
    const res: any = await updateProfile(payload)
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || res?.msg || '更新失败')
      return
    }
    Toast.success('资料已更新')
    // 再次拉取最新用户信息
    await fetchProfile()
    router.replace('/about')
  } catch (e: any) {
    Toast.fail(e?.detail || e?.msg || '更新失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadFromStorage()
  fetchProfile()
})
</script>

<template>
  <div class="profile-edit">
    <CustomHeader title="编辑资料" />
    <div class="body">
      <van-form @submit="handleSubmit">
        <!-- 头像上传 -->
        <van-cell title="头像" center>
          <template #right-icon>
            <van-uploader
              :max-count="1"
              :before-read="beforeRead"
              :after-read="afterRead"
            >
              <div class="avatar-upload">
                <van-image
                  v-if="avatarUrl"
                  :src="avatarUrl"
                  round
                  width="60"
                  height="60"
                  fit="cover"
                  class="avatar-preview"
                />
                <van-image
                  v-else
                  :src="logo"
                  round
                  width="60"
                  height="60"
                  fit="cover"
                  class="avatar-preview"
                />
                <div class="upload-tip">点击上传</div>
              </div>
            </van-uploader>
          </template>
        </van-cell>
        
        <van-field
          v-model="nickname"
          name="nickname"
          label="昵称"
          placeholder="请输入昵称"
          clearable
        />
        <van-field
          v-model="phone"
          name="phone"
          label="手机号"
          type="tel"
          placeholder="请输入手机号"
          clearable
        />
        <van-field
          v-model="email"
          name="email"
          label="邮箱"
          type="email"
          placeholder="请输入邮箱"
          clearable
        />
        
        <div style="margin: 16px 0;">
          <van-button
            round
            block
            type="primary"
            native-type="submit"
            :loading="loading || uploading"
          >
            保存
          </van-button>
        </div>
      </van-form>
    </div>
  </div>
</template>

<style scoped lang="scss">
.profile-edit {
  min-height: 100vh;
  background-color: #f7f8fa;
}

.body {
  padding: 16px;
}

.avatar-upload {
  position: relative;
  text-align: center;
  cursor: pointer;
  
  .avatar-preview {
    border: 2px solid #ebedf0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .upload-tip {
    margin-top: 6px;
    font-size: 12px;
    color: #1989fa;
    font-weight: 500;
    background: rgba(25, 137, 250, 0.1);
    padding: 2px 8px;
    border-radius: 10px;
    display: inline-block;
  }
}
</style>
