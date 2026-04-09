<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Toast } from 'vant'
import { forgotPassword, resetPassword } from '@/api/auth'
import logo from '@/assets/logo.png'

const router = useRouter()

const email = ref('')
const code = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

const sending = ref(false)
const countdown = ref(0)
let timer: number | undefined

const startCountdown = () => {
  countdown.value = 60
  timer && clearInterval(timer)
  timer = window.setInterval(() => {
    if (countdown.value <= 1) {
      clearInterval(timer)
      timer = undefined
      countdown.value = 0
      sending.value = false
    } else {
      countdown.value -= 1
    }
  }, 1000)
}

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})

const handleSendCode = async () => {
  if (!email.value) {
    Toast.fail('请输入邮箱')
    return
  }
  if (sending.value || countdown.value > 0) return
  sending.value = true
  try {
    const res: any = await forgotPassword(email.value)
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || res?.msg || '验证码发送失败')
      sending.value = false
      return
    }
    Toast.success('验证码已发送')
    startCountdown()
  } catch (e: any) {
    Toast.fail(e?.detail || e?.msg || '验证码发送失败')
    sending.value = false
  }
}

const loading = ref(false)

const handleSubmit = async () => {
  if (!email.value || !code.value || !newPassword.value || !confirmPassword.value) {
    Toast.fail('请填写邮箱、验证码和两次新密码')
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    Toast.fail('两次新密码输入不一致')
    return
  }
  loading.value = true
  try {
    const res: any = await resetPassword({
      email: email.value,
      code: code.value,
      new_password: newPassword.value,
    })
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || res?.msg || '重置密码失败')
      return
    }
    Toast.success('密码重置成功，请使用新密码登录')
    router.replace('/login')
  } catch (e: any) {
    Toast.fail(e?.detail || e?.msg || '重置密码失败')
  } finally {
    loading.value = false
  }
}

</script>

<template>
  <div class="auth-page">
    <CustomHeader title="重置密码" :border="false" transparent />

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
      <div class="app-title">找回密码</div>
      <div class="app-subtitle">验证身份后即可重置您的登录密码</div>
    </div>

    <!-- 重置密码卡片 -->
    <div class="auth-card">
      <van-form @submit="handleSubmit">
        <van-field
          v-model="email"
          name="email"
          placeholder="请输入注册邮箱"
          class="custom-field"
          :border="false"
        >
          <template #left-icon>
            <van-icon name="envelop-o" class="field-icon" />
          </template>
        </van-field>

        <van-field
          v-model="code"
          name="code"
          placeholder="请输入验证码"
          class="custom-field"
          :border="false"
        >
          <template #left-icon>
            <van-icon name="certificate" class="field-icon" />
          </template>
          <template #button>
            <van-button
              size="small"
              type="primary"
              plain
              round
              :disabled="sending || countdown > 0"
              @click.stop="handleSendCode"
              class="code-btn"
            >
              <span v-if="countdown === 0">获取验证码</span>
              <span v-else>{{ countdown }}s</span>
            </van-button>
          </template>
        </van-field>

        <van-field
          v-model="newPassword"
          name="newPassword"
          type="password"
          placeholder="请输入新密码"
          class="custom-field"
          :border="false"
        >
          <template #left-icon>
            <van-icon name="lock" class="field-icon" />
          </template>
        </van-field>

        <van-field
          v-model="confirmPassword"
          name="confirmPassword"
          type="password"
          placeholder="请再次输入新密码"
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
            提交重置
          </van-button>
        </div>
      </van-form>
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
  padding-bottom: 40px;
  
  // 背景装饰
  &::before {
    content: '';
    position: absolute;
    top: -100px;
    left: 50%;
    transform: translateX(-50%);
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(50, 150, 250, 0.06) 0%, rgba(255,255,255,0) 70%);
    border-radius: 50%;
    z-index: 0;
  }
}

.auth-header {
  position: relative;
  z-index: 1;
  padding: 30px 20px 20px;
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
}

// 自定义输入框样式
.custom-field {
  background-color: #f7f8fa;
  border-radius: 28px;
  margin-bottom: 16px;
  padding: 10px 20px;
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

.code-btn {
  height: 30px;
  padding: 0 12px;
  font-size: 12px;
  border-color: #4facfe;
  color: #4facfe;
}

.auth-button-wrapper {
  margin-top: 32px;
  margin-bottom: 10px;
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
</style>
