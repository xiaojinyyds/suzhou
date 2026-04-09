<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Toast } from 'vant'
import { login } from '@/api/auth'
import logo from '@/assets/logo.png'

const router = useRouter()

const account = ref('')
const password = ref('')
const loading = ref(false)

const handleSubmit = async () => {
  if (!account.value || !password.value) {
    Toast.fail('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    const res: any = await login({ account: account.value, password: password.value })
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || res?.msg || '登录失败')
      return
    }
    const data = res.data || {}
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token)
    }
    if (data.user) {
      localStorage.setItem('current_user', JSON.stringify(data.user))
    }
    Toast.success('登录成功')
    router.replace('/home')
  } catch (e: any) {
    Toast.fail(e?.detail || e?.msg || '登录失败')
  } finally {
    loading.value = false
  }
}

const goRegister = () => {
  router.push('/register')
}

const goForgotPassword = () => {
  router.push('/forgotpassword')
}
</script>

<template>
  <div class="auth-page">
    <CustomHeader title="登录" :border="false" transparent />

    <!-- 头部品牌区 -->
    <div class="auth-header">
      <div class="logo-box">
        <van-image
          width="72"
          height="72"
          round
          fit="cover"
          :src="logo"
          class="logo-img"
        />
      </div>
      <div class="app-title">苏州打卡</div>
      <div class="app-subtitle">发现城市 · 记录每一次签到</div>
    </div>

    <!-- 登录卡片 -->
    <div class="auth-card">
      <div class="card-header">欢迎回来</div>
      <van-form @submit="handleSubmit">
        <van-field
          v-model="account"
          name="account"
          placeholder="请输入账号"
          class="custom-field"
          :border="false"
        >
          <template #left-icon>
            <i class="iconfont icon-user" style="font-size: 18px; color: #c0c4cc;"></i>
            <van-icon name="manager" class="field-icon" />
          </template>
        </van-field>
        
        <van-field
          v-model="password"
          name="password"
          type="password"
          placeholder="请输入密码"
          class="custom-field"
          :border="false"
        >
          <template #left-icon>
            <van-icon name="lock" class="field-icon" />
          </template>
        </van-field>

        <div class="auth-button-wrapper">
          <van-button
            round
            block
            type="primary"
            native-type="submit"
            :loading="loading"
            class="submit-btn"
          >
            立即登录
          </van-button>
        </div>

        <!-- 注册入口 -->
        <div class="card-footer-row">
          <span class="text">还没有账号？</span>
          <span class="link" @click="goRegister">立即注册</span>
        </div>
      </van-form>
    </div>

    <!-- 底部辅助链接 -->
    <div class="auth-bottom">
      <span class="link-sub" @click="goForgotPassword">忘记密码？</span>
    </div>
  </div>
</template>

<style scoped lang="scss">
.auth-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #eef5ff 0%, #f6f9fc 100%);
  display: flex;
  flex-direction: column;
  position: relative;
  
  // 背景装饰圆
  &::before {
    content: '';
    position: absolute;
    top: -100px;
    left: -50px;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(50, 150, 250, 0.08) 0%, rgba(255,255,255,0) 70%);
    border-radius: 50%;
    z-index: 0;
  }
}

.auth-header {
  position: relative;
  z-index: 1;
  padding: 40px 20px 20px;
  text-align: center;
  
  .logo-box {
    margin-bottom: 16px;
    .logo-img {
      box-shadow: 0 8px 20px rgba(25, 137, 250, 0.15);
    }
  }
}

.app-title {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  letter-spacing: 1px;
}

.app-subtitle {
  margin-top: 8px;
  font-size: 14px;
  color: #909399;
  letter-spacing: 0.5px;
}

.auth-card {
  position: relative;
  z-index: 1;
  margin: 10px 24px;
  padding: 32px 24px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(10px);
  
  .card-header {
    font-size: 20px;
    font-weight: 600;
    color: #333;
    margin-bottom: 24px;
    text-align: left;
    padding-left: 4px;
  }
}

// 自定义输入框样式
.custom-field {
  background-color: #f7f8fa;
  border-radius: 28px;
  margin-bottom: 20px;
  padding: 12px 20px;
  align-items: center;
  transition: all 0.3s;
  
  &:focus-within {
    background-color: #fff;
    box-shadow: 0 0 0 2px rgba(25, 137, 250, 0.1);
  }
  
  .field-icon {
    font-size: 18px;
    color: #c0c4cc;
    margin-right: 4px;
  }
  
  :deep(.van-field__control) {
    font-size: 15px;
  }
}

.auth-button-wrapper {
  margin-top: 32px;
  margin-bottom: 20px;
}

.submit-btn {
  height: 48px;
  border-radius: 24px;
  background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
  border: none;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 6px 16px rgba(25, 137, 250, 0.25);
  
  &:active {
    opacity: 0.9;
  }
}

.card-footer-row {
  text-align: center;
  font-size: 14px;
  color: #969799;
  
  .link {
    color: #1989fa;
    font-weight: 500;
    margin-left: 4px;
  }
}

.auth-bottom {
  position: relative;
  z-index: 1;
  margin-top: 20px;
  text-align: center;
  
  .link-sub {
    font-size: 13px;
    color: #999;
    padding: 10px;
  }
}
</style>
