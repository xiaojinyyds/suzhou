<template>
  <div class="page">
    <div class="phone-shell">
      <div
        class="login-page"
        :class="{ active: passwordFocused || password.length > 0 }"
      >
        <!-- 背景图 -->
        <div class="bg bg-default"></div>
        <div class="bg bg-active"></div>

        <!-- 轻遮罩 -->
        <div class="overlay"></div>

        <!-- 顶部标题栏 -->
        <header class="top-card">
          <h1 class="header-title">打卡七狸山塘</h1>
        </header>

        <!-- 页面内容 -->
        <div class="content">
          <p class="subtitle">登录后开启你的山塘打卡之旅</p>

          <div class="form-wrap">
            <div class="form-card">
              <!-- 切换标签 -->
              <div class="mode-toggle">
                <span :class="{ active: !isRegisterMode }" @click="isRegisterMode = false">登录</span>
                <span :class="{ active: isRegisterMode }" @click="isRegisterMode = true">注册</span>
              </div>

              <!-- 登录表单 -->
              <template v-if="!isRegisterMode">
                <input
                  v-model="username"
                  class="input-box"
                  type="text"
                  placeholder="请输入账号/邮箱/手机号"
                />

                <input
                  v-model="password"
                  class="input-box"
                  type="password"
                  placeholder="请输入密码"
                  @focus="passwordFocused = true"
                  @blur="passwordFocused = false"
                />

                <button class="login-btn" @click="handleLogin">登录</button>
              </template>

              <!-- 注册表单 -->
              <template v-else>
                <input
                  v-model="nickname"
                  class="input-box"
                  type="text"
                  placeholder="请输入用户名"
                />

                <input
                  v-model="email"
                  class="input-box"
                  type="email"
                  placeholder="请输入邮箱"
                />

                <div class="code-wrap">
                  <input
                    v-model="code"
                    class="input-box code-input"
                    type="text"
                    placeholder="请输入验证码"
                  />
                  <button class="send-code-btn" :disabled="countdown > 0" @click="handleSendCode">
                    {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
                  </button>
                </div>

                <input
                  v-model="password"
                  class="input-box"
                  type="password"
                  placeholder="设置密码"
                  @focus="passwordFocused = true"
                  @blur="passwordFocused = false"
                />

                <button class="login-btn" @click="handleRegister">注册</button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { post } from "@/utils/request";
import { showToast } from "@/utils/toast";

const router = useRouter();

const isRegisterMode = ref(false);

// 登录表单
const username = ref("");
const password = ref("");
const passwordFocused = ref(false);

// 注册表单
const nickname = ref("");
const email = ref("");
const code = ref("");
const countdown = ref(0);

onMounted(() => {
  username.value = localStorage.getItem("username") || "";
});

const handleSendCode = async () => {
  if (!email.value.trim()) {
    showToast("请输入邮箱", "error");
    return;
  }
  // 如果正在倒计时，直接返回
  if (countdown.value > 0) return;

  try {
    await post("/api/v1/auth/send-code", { email: email.value.trim() });
    showToast("验证码已发送至邮箱，请查收", "success");
    
    // 开启倒计时
    countdown.value = 60;
    const timer = setInterval(() => {
      countdown.value--;
      if (countdown.value <= 0) {
        clearInterval(timer);
      }
    }, 1000);
  } catch (error) {
    showToast(error.message || "获取验证码失败", "error");
  }
};

const handleRegister = async () => {
  if (!email.value.trim() || !code.value.trim() || !password.value.trim()) {
    showToast("请输入邮箱、验证码和密码", "error");
    return;
  }

  try {
    await post("/api/v1/auth/register", {
      email: email.value.trim(),
      code: code.value.trim(),
      password: password.value.trim(),
      nickname: nickname.value.trim(),
    });
    
    showToast("注册成功，请使用新账号登录", "success");
    isRegisterMode.value = false; // 切回登录模式
    username.value = email.value.trim(); // 自动填入刚才注册的邮箱
    password.value = ""; // 清空密码要求重新输入
  } catch (error) {
    showToast(error.message || "注册失败", "error");
  }
};

const handleLogin = async () => {
  if (!username.value.trim() || !password.value.trim()) {
    showToast("请输入账号和密码", "error");
    return;
  }

  try {
    const res = await post("/api/v1/auth/login", {
      account: username.value.trim(),
      password: password.value.trim()
    });

    const { access_token, user } = res.data;
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("username", user.username);
    localStorage.setItem("user-info", JSON.stringify(user));

    showToast("登录成功", "success");
    router.push("/home");
  } catch (error) {
    showToast(error.message || "登录失败", "error");
  }
};
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f8f8f8;
  display: flex;
  justify-content: center;
  align-items: center;
  --font-title: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  --font-body: "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif;
  font-family: var(--font-body);
}

.phone-shell {
  width: 100%;
  max-width: 430px;
  min-height: 100vh;
  background: #fffaf0;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 24px rgba(0, 0, 0, 0.08);
}

.login-page {
  position: relative;
  width: 100%;
  min-height: 100vh;
  overflow: hidden;
}

/* 背景层 */
.bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  transition: opacity 0.5s ease;
}

.bg-default {
  background-image: url("@/assets/bg1.jpg");
  opacity: 1;
}

.bg-active {
  background-image: url("@/assets/bg2.jpg");
  opacity: 0;
}

.login-page.active .bg-default {
  opacity: 0;
}

.login-page.active .bg-active {
  opacity: 1;
}

/* 遮罩 */
.overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 248, 238, 0.12);
  z-index: 1;
}

/* 顶部标题栏 */
.top-card {
  position: relative;
  z-index: 3;
  height: 56px;
  background: #4f9674;
  border-bottom: 2px solid rgba(201, 168, 76, 0.62);
  border-bottom-left-radius: 22px;
  border-bottom-right-radius: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(70, 94, 122, 0.08);
}

.header-title {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: 2px;
  color: #fff;
  margin: 0;
  position: relative;
  z-index: 1;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
  font-family: var(--font-title);
}

/* 内容区 */
.content {
  position: relative;
  z-index: 2;
  min-height: calc(100vh - 56px);
  display: flex;
  flex-direction: column;
  padding: 14px 24px 28px;
  box-sizing: border-box;
}

.subtitle {
  margin: 10px 0 0;
  text-align: center;
  font-size: 14px;
  color: #6f7b67;
  line-height: 1.6;
  font-family: var(--font-body);
  font-weight: 500;
}

/* 表单整体位置 */
.form-wrap {
  margin-top: 60px;
  display: flex;
  justify-content: center;
}

/* 表单区 */
.form-card {
  width: 100%;
  max-width: 350px;
  padding: 30px 24px 24px;
  background: rgba(248, 252, 246, 0.82);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 28px;
  box-shadow: 0 10px 40px rgba(70, 110, 90, 0.12), inset 0 2px 0 rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.input-box {
  width: 100%;
  height: 52px;
  margin-bottom: 16px;
  padding: 0 18px;
  box-sizing: border-box;
  border: 1.5px solid rgba(120, 150, 130, 0.25);
  border-radius: 18px;
  font-size: 15px;
  color: #4b6b55;
  background: rgba(255, 255, 255, 0.6);
  outline: none;
  font-family: var(--font-body);
  font-weight: 500;
  transition: all 0.2s;
}

.input-box::placeholder {
  color: #7f8f86;
  font-weight: 400;
}

.input-box:focus {
  border-color: #72a889;
}

.login-btn {
  width: 100%;
  height: 50px;
  border: none;
  border-radius: 16px;
  background: #4f9674;
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 6px 14px rgba(79, 150, 116, 0.2);
  font-family: var(--font-body);
}

.login-btn:active {
  transform: translateY(1px);
}

.mode-toggle {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
  font-family: var(--font-body);
  font-size: 16px;
  font-weight: 500;
  color: #6f7b67;
  cursor: pointer;
}

.mode-toggle span {
  padding-bottom: 4px;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.mode-toggle span.active {
  color: #4f9674;
  font-weight: bold;
  border-bottom: 2px solid #4f9674;
}

.code-wrap {
  display: flex;
  gap: 10px;
  margin-bottom: 14px;
}

.code-wrap .code-input {
  margin-bottom: 0;
  flex: 1;
}

.send-code-btn {
  width: 100px;
  height: 48px;
  border: 1px solid rgba(120, 150, 130, 0.45);
  border-radius: 16px;
  background: #fffaf0;
  color: #4f9674;
  font-size: 14px;
  cursor: pointer;
  font-family: var(--font-body);
  font-weight: 500;
}

.send-code-btn:disabled {
  color: #999;
  cursor: not-allowed;
  background: #eee;
}

/* 小屏适配 */
@media (max-width: 430px) {
  .phone-shell {
    max-width: 100%;
    box-shadow: none;
  }

  .content {
    padding: 12px 20px 24px;
  }

  .header-title {
    font-size: 22px;
  }

  .subtitle {
    font-size: 13px;
  }

  .form-wrap {
    margin-top: 50px;
  }
}
</style>
