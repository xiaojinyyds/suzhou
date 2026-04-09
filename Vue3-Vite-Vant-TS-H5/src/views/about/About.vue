<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Toast, Dialog } from 'vant'
import logo from '@/assets/logo.png'
import { getCurrentUser, changePassword } from '@/api/auth'

interface UserInfo {
  id: number
  username: string
  email: string
  nickname?: string | null
  avatar_url?: string | null
  role?: string  // 用户角色：admin 或 user
  is_active?: boolean
  is_verified?: boolean
  created_at?: string | null
}

const router = useRouter()
const user = ref<UserInfo | null>(null)
const loading = ref(false)

// 修改密码弹窗相关状态
const showChangePwd = ref(false)
const oldPassword = ref('')
const newPassword = ref('')
const changePwdLoading = ref(false)

const loadFromStorage = () => {
  try {
    const raw = localStorage.getItem('current_user')
    if (raw) {
      user.value = JSON.parse(raw)
    }
  } catch (e) {}
}

const fetchProfile = async () => {
  loading.value = true
  try {
    const res: any = await getCurrentUser()
    if (res && res.code === 200 && res.data) {
      user.value = res.data
      localStorage.setItem('current_user', JSON.stringify(res.data))
    }
  } catch (e: any) {
    if (e?.detail) {
      Toast.fail(e.detail)
    }
  } finally {
    loading.value = false
  }
}

const displayName = () => {
  if (!user.value) return '未登录'
  return user.value.nickname || user.value.username || '未命名用户'
}

const goEditProfile = () => {
  router.push('/profileedit')
}

const goAdmin = () => {
  router.push('/admin')
}

const openChangePassword = () => {
  oldPassword.value = ''
  newPassword.value = ''
  showChangePwd.value = true
}

const closeChangePassword = () => {
  if (changePwdLoading.value) return
  showChangePwd.value = false
}

const submitChangePassword = async () => {
  if (!oldPassword.value || !newPassword.value) {
    Toast.fail('请填写当前密码和新密码')
    return
  }
  if (oldPassword.value === newPassword.value) {
    Toast.fail('新密码不能与当前密码相同')
    return
  }
  changePwdLoading.value = true
  try {
    const res: any = await changePassword({
      old_password: oldPassword.value,
      new_password: newPassword.value,
    })
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || res?.msg || '修改密码失败')
      return
    }
    Toast.success('修改密码成功，请使用新密码重新登录')
    showChangePwd.value = false
  } catch (e: any) {
    Toast.fail(e?.detail || e?.msg || '修改密码失败')
  } finally {
    changePwdLoading.value = false
  }
}

const handleLogout = () => {
  Dialog.confirm({
    title: '提示',
    message: '确定要退出当前账号吗？',
  }).then(() => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('current_user')
    router.replace('/login')
  }).catch(() => {
    // 用户取消，不做任何处理
  })
}

onMounted(() => {
  loadFromStorage()
  fetchProfile()
})

</script>

<template>
  <div class="about">
    <!-- 沉浸式头部背景 -->
    <div class="page-bg"></div>
    
    <CustomHeader title="个人中心" :border="false" transparent style="color: #fff;" />
    
    <div class="wrapper">
      <!-- 用户信息卡片 -->
      <div class="profile-card">
        <div class="user-info">
          <van-image
            round
            width="64"
            height="64"
            fit="cover"
            :src="user?.avatar_url || logo"
            class="avatar-img"
          />
          <div class="info-text">
            <div class="nickname">{{ displayName() }}</div>
            <div class="email">{{ user?.email || '暂无邮箱' }}</div>
            <div class="tags">
              <van-tag type="primary" plain round class="mini-tag" v-if="user?.is_verified">已认证</van-tag>
              <van-tag type="warning" plain round class="mini-tag" v-else>未认证</van-tag>
              <van-tag type="success" plain round class="mini-tag" style="margin-left: 4px;">ID: {{ user?.id }}</van-tag>
            </div>
          </div>
        </div>
      </div>

      <!-- 功能菜单 -->
      <div class="menu-section">
        <!-- 管理员入口（仅管理员可见） -->
        <van-cell-group inset class="custom-group" v-if="user?.role === 'admin'">
          <van-cell title="管理员后台" is-link @click="goAdmin">
            <template #icon>
              <div class="icon-box red">
                <van-icon name="shield-o" />
              </div>
            </template>
            <template #right-icon>
              <van-tag type="danger" class="admin-badge">管理员</van-tag>
            </template>
          </van-cell>
        </van-cell-group>
        
        <van-cell-group inset class="custom-group" :style="user?.role === 'admin' ? 'margin-top: 12px;' : ''">
          <van-cell title="修改资料" is-link @click="goEditProfile">
            <template #icon>
              <div class="icon-box blue">
                <van-icon name="edit" />
              </div>
            </template>
          </van-cell>
          <van-cell title="修改密码" is-link @click="openChangePassword">
            <template #icon>
              <div class="icon-box purple">
                <van-icon name="lock" />
              </div>
            </template>
          </van-cell>
        </van-cell-group>

        <van-cell-group inset class="custom-group mt-12">
          <van-cell title="账号状态" :value="user?.is_active ? '正常' : '异常'">
            <template #icon>
              <div class="icon-box green">
                <van-icon name="user-circle-o" />
              </div>
            </template>
          </van-cell>
          <van-cell title="注册时间" :value="user?.created_at ? user.created_at.split('T')[0] : '-'">
            <template #icon>
              <div class="icon-box orange">
                <van-icon name="clock-o" />
              </div>
            </template>
          </van-cell>
        </van-cell-group>
      </div>

      <!-- 退出登录 -->
      <div class="logout-section">
        <van-button block round class="logout-btn" @click="handleLogout">
          退出登录
        </van-button>
      </div>
    </div>
  </div>
  
  <!-- 修改密码弹窗 -->
  <transition name="fade">
    <div v-if="showChangePwd" class="overlay" @click.self="closeChangePassword">
      <div class="dialog-card">
        <div class="dialog-header">
          <span class="title">修改密码</span>
          <van-icon name="cross" class="close-icon" @click="closeChangePassword" />
        </div>
        <div class="dialog-body">
          <van-field
            v-model="oldPassword"
            type="password"
            placeholder="请输入当前密码"
            class="dialog-field"
            :border="false"
          >
            <template #left-icon><van-icon name="lock" /></template>
          </van-field>
          <van-field
            v-model="newPassword"
            type="password"
            placeholder="请输入新密码"
            class="dialog-field"
            :border="false"
          >
            <template #left-icon><van-icon name="key" /></template>
          </van-field>
        </div>
        <div class="dialog-footer">
          <van-button block round type="primary" :loading="changePwdLoading" @click="submitChangePassword">
            确认修改
          </van-button>
        </div>
      </div>
    </div>
  </transition>
  
</template>

<style lang="scss" scoped>
.about {
  min-height: 100vh;
  background-color: #f7f8fa;
  position: relative;
}

.page-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 220px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  border-bottom-left-radius: 24px;
  border-bottom-right-radius: 24px;
  z-index: 0;
}

.wrapper {
  position: relative;
  z-index: 1;
  padding: 60px 16px 20px;
}

.profile-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  backdrop-filter: blur(10px);
  
  .user-info {
    display: flex;
    align-items: center;
    width: 100%;
  }
  
  .avatar-img {
    border: 2px solid #fff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin-right: 16px;
    flex-shrink: 0;
  }
  
  .info-text {
    flex: 1;
    overflow: hidden;
    
    .nickname {
      font-size: 18px;
      font-weight: 700;
      color: #333;
      margin-bottom: 4px;
    }
    
    .email {
      font-size: 13px;
      color: #969799;
      margin-bottom: 8px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    
    .tags {
      display: flex;
      align-items: center;
    }
  }
}

.menu-section {
  margin-bottom: 24px;
}

.custom-group {
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
}

.mt-12 {
  margin-top: 12px;
}

.icon-box {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  font-size: 16px;
  
  &.red { background: rgba(238, 10, 36, 0.1); color: #ee0a24; }
  &.blue { background: rgba(25, 137, 250, 0.1); color: #1989fa; }
  &.purple { background: rgba(114, 50, 221, 0.1); color: #7232dd; }
  &.green { background: rgba(7, 193, 96, 0.1); color: #07c160; }
  &.orange { background: rgba(255, 151, 106, 0.1); color: #ff976a; }
}

.admin-badge {
  font-size: 11px;
  padding: 0 8px;
  height: 20px;
  line-height: 20px;
}

.logout-section {
  padding: 0 16px;
}

.logout-btn {
  background: #fff;
  color: #ee0a24;
  border: 1px solid #ebedf0;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
  
  &:active {
    background: #f2f3f5;
  }
}

// 弹窗样式优化
.overlay {
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.dialog-card {
  width: 85%;
  max-width: 320px;
  background-color: #fff;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 12px 32px rgba(0,0,0,0.1);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  
  .title {
    font-size: 18px;
    font-weight: 600;
    color: #333;
  }
  
  .close-icon {
    font-size: 20px;
    color: #ccc;
    padding: 4px;
  }
}

.dialog-field {
  background-color: #f7f8fa;
  border-radius: 12px;
  margin-bottom: 16px;
  padding: 10px 16px;
}

.dialog-footer {
  margin-top: 8px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.mini-tag {
  font-size: 11px;
  padding: 0 6px;
  height: 18px;
  line-height: 18px;
}
</style>