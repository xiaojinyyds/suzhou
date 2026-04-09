<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Toast } from 'vant'
import { sendCode, register } from '@/api/auth'
import logo from '@/assets/logo.png'

const router = useRouter()

const email = ref('')
const code = ref('')
const password = ref('')
const confirmPassword = ref('')
const nickname = ref('')

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
    const res: any = await sendCode(email.value)
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
  if (!email.value || !code.value || !password.value || !confirmPassword.value) {
    Toast.fail('请先填写邮箱、验证码和两次密码')
    return
  }
  if (password.value !== confirmPassword.value) {
    Toast.fail('两次密码输入不一致')
    return
  }
  loading.value = true
  try {
    const res: any = await register({
      email: email.value,
      code: code.value,
      password: password.value,
      nickname: nickname.value || email.value.split('@')[0]
    })
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || res?.msg || '注册失败')
      return
    }
    const data = res.data || {}
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token)
    }
    if (data.user) {
      localStorage.setItem('current_user', JSON.stringify(data.user))
    }
    Toast.success('注册成功')
    router.replace('/home')
  } catch (e: any) {
    Toast.fail(e?.detail || e?.msg || '注册失败')
  } finally {
    loading.value = false
  }
}

const goLogin = () => {
  router.push('/login')
}
</script>

<template>
  <div class="auth-page">
    <CustomHeader title="注册" :border="false" transparent />

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
      <div class="app-title">加入我们</div>
      <div class="app-subtitle">创建您的专属账号，开启打卡之旅</div>
    </div>

    <!-- 注册卡片 -->
    <div class="auth-card">
      <van-form @submit="handleSubmit">
        <van-field
          v-model="email"
          name="email"
          placeholder="请输入邮箱"
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
          v-model="password"
          name="password"
          type="password"
          placeholder="设置密码"
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
          placeholder="确认密码"
          class="custom-field"
          :border="false"
        >
          <template #left-icon>
            <van-icon name="lock" class="field-icon" />
          </template>
        </van-field>

        <van-field
          v-model="nickname"
          name="nickname"
          placeholder="昵称 (选填)"
          class="custom-field"
          :border="false"
        >
          <template #left-icon>
            <van-icon name="smile-o" class="field-icon" />
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
            立即注册
          </van-button>
        </div>

        <div class="card-footer-row">
          <span class="text">已有账号？</span>
          <span class="link" @click="goLogin">去登录</span>
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
    right: -50px;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0, 242, 254, 0.05) 0%, rgba(255,255,255,0) 70%);
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
</style>
