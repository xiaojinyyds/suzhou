<template>
  <div class="my-page">
    <!-- 顶部 Header -->
    <header class="top-card">
      <h1 class="header-title">个人主页</h1>
      <button class="ring-btn-header" @click="showRingPanel = true">
        更换个人主题
      </button>
    </header>

    <!-- 内容区 -->
    <div class="canvas-wrapper">
      <!-- 头像区域 -->
      <div
        class="avatar-block"
        :style="{ backgroundImage: `url(${RING_BACKGROUNDS[selectedRing.id]})` }"
      >
        <div class="avatar-block-inner">
          <!-- 左：头像 + 戒指 -->
          <div class="avatar-left">
            <div class="avatar-area">
              <div class="avatar-wrapper" @click="triggerUpload">
                <img v-if="avatarUrl" :src="avatarUrl" class="avatar-img" />
                <span v-else>🦝</span>
              </div>

              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                style="display: none"
                @change="onAvatarChange"
              />

              <img
                class="ring-frame"
                :src="selectedRing.img"
                :alt="selectedRing.label"
              />
            </div>
          </div>

          <!-- 右：信息 -->
          <div class="avatar-right">
            <div class="username">{{ username }}</div>
            <div class="user-tags">
              <div class="user-tag">{{ userTag }}</div>
              <div class="user-tag2">已打卡 {{ doneCount }}/{{ totalStatues }}</div>
            </div>
          </div>
        </div>
      </div>

      <div class="divider"></div>

      <!-- 编辑资料入口 -->
      <section class="section-block section-block--compact">
        <div class="menu-card" style="background: rgba(255, 255, 255, 0.45); display: flex; justify-content: space-between; padding: 12px 16px; align-items: center; border-radius: 14px; cursor: pointer; box-shadow: 0 2px 6px var(--skin-soft-chip);" @click="openEditProfile">
          <span style="font-size: 14px; color: var(--skin-primary-dark); font-weight: bold; letter-spacing: 1px;">✎ 编辑个人基本资料</span>
          <span style="font-size: 16px; color: var(--skin-sub-text); line-height: 1;">›</span>
        </div>
      </section>

      <!-- 档案入口 -->
      <section class="section-block section-block--compact">
        <div class="menu-card archive-card archive-card--compact">
          <div class="menu-item" @click="$router.push({ name: 'photo' })">
            <span class="menu-label">我的照片</span>
            <span class="menu-val">{{ photoCount }} 张</span>
            <span class="menu-arrow">›</span>
          </div>

          <div class="menu-item" @click="$router.push({ name: 'scratch' })">
            <span class="menu-label">刮彩票记录</span>
            <span class="menu-val">
              {{ scratchCount > 0 ? `已获奖 ${scratchCount} 次` : '暂无' }}
            </span>
            <span class="menu-arrow">›</span>
          </div>

          <div class="menu-item" @click="$router.push({ name: 'merchOrders' })">
            <span class="menu-label">周边订单</span>
            <span class="menu-val">
               {{ merchOrderCount > 0 ? `共 ${merchOrderCount} 件预约` : '暂无' }}
            </span>
            <span class="menu-arrow">›</span>
          </div>
        </div>
      </section>

      <!-- 弱化操作 -->
      <div class="soft-action-row">
        <button class="soft-reset-btn" @click="handleReset">清除打卡记录</button>
        <div style="height: 10px;"></div>
        <button class="soft-reset-btn" @click="showLogoutConfirm = true" style="color: #c96b6b; border-color: rgba(201, 107, 107, 0.4);">退出当前账号</button>
      </div>
    </div>

    <!-- 底部 Tab -->
    <nav class="tab-bar">
      <div
        class="tab-item"
        :class="{ 'tab-item--active': $route.name === 'home' }"
        @click="$router.push({ name: 'home' })"
      >
        <Home :size="22" />
        <span class="tab-label">首页</span>
      </div>

      <div
        class="tab-item"
        :class="{ 'tab-item--active': $route.name === 'checkin' }"
        @click="$router.push({ name: 'checkin' })"
      >
        <MapPin :size="22" />
        <span class="tab-label">打卡</span>
      </div>

      <div
        class="tab-item"
        :class="{ 'tab-item--active': $route.name === 'photo' }"
        @click="$router.push({ name: 'photo' })"
      >
        <Camera :size="22" />
        <span class="tab-label">拍照</span>
      </div>

      <div
        class="tab-item"
        :class="{ 'tab-item--active': $route.name === 'merch' }"
        @click="$router.push({ name: 'merch' })"
      >
        <ShoppingCart :size="22" />
        <span class="tab-label">周边</span>
      </div>

      <div
        class="tab-item"
        :class="{ 'tab-item--active': $route.name === 'my' }"
        @click="$router.push({ name: 'my' })"
      >
        <User :size="22" />
        <span class="tab-label">我的</span>
      </div>
    </nav>

    <!-- 头像框选择面板 -->
    <Transition name="panel">
      <div
        v-if="showRingPanel"
        class="ring-overlay"
        @click.self="showRingPanel = false"
      >
        <div class="ring-panel">
          <div class="ring-panel-header">
            <div class="ring-panel-title">✦ 选择头像框 ✦</div>
            <div class="ring-panel-sub">共 {{ RINGS.length }} 款狸子戒指</div>
          </div>

          <div class="ring-grid">
            <div
              v-for="ring in RINGS"
              :key="ring.id"
              class="ring-option"
              :class="{ selected: selectedRing?.id === ring.id }"
              @click="selectRing(ring)"
            >
              <div class="ring-option-img-wrap">
                <img :src="ring.img" class="ring-option-img" :alt="ring.label" />
                <div v-if="selectedRing?.id === ring.id" class="ring-check">✓</div>
              </div>
              <div class="ring-option-label">{{ ring.label }}</div>
            </div>
          </div>

          <button class="ring-close-btn" @click="showRingPanel = false">
            完 成
          </button>
        </div>
      </div>
    </Transition>

    <!-- 编辑资料面板 -->
    <Transition name="panel">
      <div v-if="showEditProfile" class="ring-overlay" @click.self="showEditProfile = false">
        <div class="ring-panel" style="padding-top: 24px;">
          <div class="ring-panel-header" style="margin-bottom: 24px;">
            <div class="ring-panel-title">编辑资料</div>
          </div>
          <div style="margin-bottom: 24px;">
            <label style="display: block; font-size: 13px; color: var(--skin-sub-text); margin-bottom: 8px;">个性昵称</label>
            <input v-model="editNickname" type="text" style="width: 100%; height: 48px; border-radius: 12px; border: 1px solid var(--skin-panel-border); padding: 0 16px; font-size: 15px; background: rgba(255, 255, 255, 0.8); outline: none; font-family: inherit; color: var(--skin-main-text);" placeholder="请输入新昵称" />
          </div>
          <div style="display: flex; gap: 12px;">
            <button class="ring-close-btn" style="background: rgba(0,0,0,0.05); color: var(--skin-sub-text);" @click="showEditProfile = false">取消</button>
            <button class="ring-close-btn" @click="saveProfile">保存</button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 退出登录确认弹窗 -->
    <Transition name="panel">
      <div v-if="showLogoutConfirm" class="logout-overlay" @click.self="showLogoutConfirm = false">
        <div class="logout-dialog">
          <div class="logout-icon">⚠️</div>
          <div class="logout-title">退出登录</div>
          <div class="logout-desc">确定要退出当前账号吗？</div>
          <div class="logout-actions">
            <button class="logout-btn-cancel" @click="showLogoutConfirm = false">取消</button>
            <button class="logout-btn-confirm" @click="confirmLogout">确定退出</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { Home, MapPin, Camera, ShoppingCart, User } from 'lucide-vue-next'
import { RING_THEME_MAP, applyThemeToRoot } from '@/config/ringThemeMap'
import { get, post, put } from '@/utils/request'
import { showToast } from '@/utils/toast'

const router = useRouter()

// ── 基础数据 ──────────────────────────────────────────
const doneCount = ref(0)
const totalStatues = ref(7)

async function fetchCheckinStats() {
  try {
    const res = await get('/api/v1/checkins/statistics')
    if (res.data) {
      doneCount.value = res.data.checked_statues
      totalStatues.value = res.data.total_statues || 7
    }
  } catch (err) {
    console.error('获取打卡统计失败:', err)
  }
}

const userTag = computed(() => {
  const n = doneCount.value
  if (n >= 7) return '七狸守护神'
  if (n >= 5) return '山塘百事通'
  if (n >= 3) return '姑苏漫步者'
  if (n >= 1) return '寻狸达人'
  return '初到山塘'
})

const photoCount = ref(0)
async function fetchPhotoCount() {
  try {
    const res = await get('/api/v1/photos/my')
    photoCount.value = res.data?.total || res.data?.items?.length || 0
  } catch (err) {
    console.error('获取照片数量失败:', err)
  }
}

const scratchCount = ref(0)
async function fetchScratchCount() {
  try {
    const res = await get('/api/v1/scratch/my')
    scratchCount.value = res.data.win_count
  } catch (err) {
    console.error(err)
  }
}

const merchOrderCount = ref(0)
async function fetchMerchCount() {
  try {
    const res = await get('/api/v1/merch/orders/my')
    merchOrderCount.value = res.data.count
  } catch (err) {
    console.error(err)
  }
}

function handleReset() {
  if (!confirm('确定清除所有本地缓存记录？')) return
  localStorage.removeItem('checkin-done')
  localStorage.removeItem('scratch-notified')
  localStorage.removeItem('scratch-win-count')
}

const showLogoutConfirm = ref(false)

function confirmLogout() {
  showLogoutConfirm.value = false
  localStorage.removeItem('access_token')
  localStorage.removeItem('username')
  localStorage.removeItem('user-info')
  localStorage.removeItem('user-avatar')
  router.push({ name: 'login' })
}

// ── 登录页联动：头像 + 用户名 ─────────────────────────
const avatarUrl = ref('')
const username = ref('游客')
const fileInput = ref(null)

function syncUserInfo() {
  const userInfoStr = localStorage.getItem('user-info')
  if (userInfoStr) {
    try {
      const userInfo = JSON.parse(userInfoStr)
      avatarUrl.value = userInfo.avatar_url || localStorage.getItem('user-avatar') || ''
      username.value = userInfo.nickname || userInfo.username || localStorage.getItem('username') || '游客'
    } catch (e) {
      avatarUrl.value = localStorage.getItem('user-avatar') || ''
      username.value = localStorage.getItem('username') || '游客'
    }
  } else {
    avatarUrl.value = localStorage.getItem('user-avatar') || ''
    username.value = localStorage.getItem('username') || '游客'
  }
}

function triggerUpload() {
  fileInput.value?.click()
}

async function onAvatarChange(e) {
  const file = e.target.files?.[0];
  if (!file) return;

  // 1. 本地快速预览
  const reader = new FileReader();
  reader.onload = () => {
    avatarUrl.value = reader.result;
  };
  reader.readAsDataURL(file);

  showToast("正在上传头像中...", "info", 2000);

  try {
    // 2. 上传到服务器 OSS
    const formData = new FormData();
    formData.append("file", file);
    
    const uploadRes = await post("/api/v1/upload/avatar", formData);
    const newAvatarUrl = uploadRes.data.url;

    // 3. 更新用户资料
    await put("/api/v1/auth/update-profile", {
      avatar_url: newAvatarUrl
    });

    // 4. 更新本地存储
    avatarUrl.value = newAvatarUrl;
    localStorage.setItem('user-avatar', newAvatarUrl);
    
    // 更新 user-info 中的 avatar_url 以保持一致
    const userInfoStr = localStorage.getItem('user-info');
    if (userInfoStr) {
      try {
        const userInfo = JSON.parse(userInfoStr);
        userInfo.avatar_url = newAvatarUrl;
        localStorage.setItem('user-info', JSON.stringify(userInfo));
      } catch (e) {}
    }

    showToast("头像更新成功", "success");
  } catch (error) {
    showToast(error.message || "头像上传失败", "error");
    // 失败时回滚为原来的头像
    avatarUrl.value = localStorage.getItem('user-avatar') || '';
  }
  
  // 清空 input 使得选择同一个文件也能触发 change
  if (fileInput.value) {
    fileInput.value.value = '';
  }
}

// ── 编辑资料 ──────────────────────────────────────────
const showEditProfile = ref(false)
const editNickname = ref('')

function openEditProfile() {
  editNickname.value = username.value === '游客' ? '' : username.value
  showEditProfile.value = true
}

async function saveProfile() {
  if (!editNickname.value.trim()) {
    showToast('昵称不能为空', 'error')
    return
  }
  showToast('正在保存...', 'info')
  try {
    await put('/api/v1/auth/update-profile', { nickname: editNickname.value.trim() })
    const userInfoStr = localStorage.getItem('user-info')
    if (userInfoStr) {
      try {
        const userInfo = JSON.parse(userInfoStr)
        userInfo.nickname = editNickname.value.trim()
        localStorage.setItem('user-info', JSON.stringify(userInfo))
      } catch (e) {}
    }
    username.value = editNickname.value.trim()
    showToast('资料已更新', 'success')
    showEditProfile.value = false
  } catch (err) {
    showToast(err.message || '更新失败', 'error')
  }
}

onMounted(() => {
  syncUserInfo()
  fetchCheckinStats()
  fetchPhotoCount()
  fetchScratchCount()
  fetchMerchCount()
})

onActivated(() => {
  syncUserInfo()
  fetchCheckinStats()
  fetchPhotoCount()
  fetchScratchCount()
  fetchMerchCount()
})

// ── 头像框戒指 ──────────────────────────────────────
const RINGS = [
  { id: 'wenchang', label: '文昌狸', img: new URL('@/assets/rings/_文昌狸.png', import.meta.url).href },
  { id: 'baigong', label: '白公狸', img: new URL('@/assets/rings/_白公狸.png', import.meta.url).href },
  { id: 'caiyun', label: '彩云狸', img: new URL('@/assets/rings/_彩云狸.png', import.meta.url).href },
  { id: 'fenshui', label: '分水狸', img: new URL('@/assets/rings/_分水狸.png', import.meta.url).href },
  { id: 'haiyong', label: '海涌狸', img: new URL('@/assets/rings/_海涌狸.png', import.meta.url).href },
  { id: 'meiren', label: '美仁狸', img: new URL('@/assets/rings/_美仁狸.png', import.meta.url).href },
  { id: 'tonggui', label: '通贵狸', img: new URL('@/assets/rings/_通贵狸.png', import.meta.url).href },
]

const RING_BACKGROUNDS = {
  wenchang: new URL('@/assets/backgrounds/1-07.png', import.meta.url).href,
  baigong: new URL('@/assets/backgrounds/1-03.png', import.meta.url).href,
  caiyun: new URL('@/assets/backgrounds/1-06.png', import.meta.url).href,
  fenshui: new URL('@/assets/backgrounds/1-02.png', import.meta.url).href,
  haiyong: new URL('@/assets/backgrounds/1-05.png', import.meta.url).href,
  meiren: new URL('@/assets/backgrounds/1-01.png', import.meta.url).href,
  tonggui: new URL('@/assets/backgrounds/1-04.png', import.meta.url).href,
}

const savedRingId = localStorage.getItem('selected-ring') || 'wenchang'
const selectedRing = ref(RINGS.find(r => r.id === savedRingId) || RINGS[0])
const showRingPanel = ref(false)

async function selectRing(ring) {
  selectedRing.value = ring
  applyThemeToRoot(ring.id)
  
  // Call API to persist theme profile
  try {
    await put('/api/v1/auth/update-profile', { theme: ring.id })
    // Update local user-info
    const userInfoStr = localStorage.getItem('user-info')
    if (userInfoStr) {
      try {
        const userInfo = JSON.parse(userInfoStr)
        userInfo.theme = ring.id
        localStorage.setItem('user-info', JSON.stringify(userInfo))
      } catch (e) {}
    }
  } catch (err) {
    console.error('Failed to sync theme to server:', err)
  }
}
</script>

<style scoped>
.my-page {
  display: flex;
  flex-direction: column;
  height: 100dvh;
  background-color: #fffdec;
  max-width: 430px;
  margin: 0 auto;
  overflow-y: auto;
  overflow-x: hidden;
  font-family: 'Ma Shan Zheng', cursive;
  position: relative;
}

/* Header */
.top-card {
  background: var(--skin-primary);
  border-bottom: 1.5px solid rgb(143, 141, 116);
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.12'/%3E%3C/svg%3E"),
    linear-gradient(135deg, rgba(255,255,255,0.18) 0%, transparent 50%, rgba(0,0,0,0.08) 100%);
  background-repeat: repeat, no-repeat;
  background-size: auto, 100% 100%;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0 0 28px 28px;
  flex-shrink: 0;
  position: relative;
  z-index: 20;
}

.header-title {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: 4px;
  color: #ffffff;
  margin: 0;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.15);
}

.ring-btn-header {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  padding: 4px 14px;
  background: rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  font-size: 11px;
  font-family: inherit;
  color: #ffffff;
  letter-spacing: 1.5px;
  cursor: pointer;
  transition: all 0.2s;
}

.ring-btn-header:active {
  background: rgba(255, 255, 255, 0.5);
}

/* 画布 */
.canvas-wrapper {
  position: relative;
  width: 100%;
  flex: 1;
  padding: 10px 0 96px;
  background:
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.72), transparent 30%),
    linear-gradient(to bottom, #fffdec 0%, #f8f6ea 62%, #f1efdf 100%);
}

/* 头像卡片 */
.avatar-block {
  margin: 12px 16px 0;
  padding: 1px;
  background: linear-gradient(160deg, #eef7ee, #e6f2e8);
  border-radius: 22px;
  border: 1px solid rgba(74, 143, 111, 0.2);
  box-shadow: 0 2px 12px rgba(74, 143, 111, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.7);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 1;
  background-size: cover;
  background-position: right center;
  background-repeat: no-repeat;
}

.avatar-block::before {
  content: '';
  position: absolute;
  top: -20px;
  left: -20px;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.4), transparent 70%);
  pointer-events: none;
}

.avatar-block::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 80px;
  height: 80px;
  background: radial-gradient(circle, rgba(74, 143, 111, 0.08), transparent 70%);
  pointer-events: none;
}

.avatar-block-inner {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  padding: 0 20px;
  gap: 16px;
}

.avatar-left {
  flex-shrink: 0;
}

.avatar-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 8px;
  padding-right: 12px;
  z-index: 2;
  overflow: hidden;
}

.avatar-area {
  position: relative;
  width: 155px;
  height: 155px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-wrapper {
  position: absolute;
  width: 90px;
  height: 80px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -36%);
  overflow: hidden;
  border-radius: 50%;
  cursor: pointer;
  z-index: 1;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-wrapper span {
  font-size: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
}

.ring-frame {
  position: absolute;
  width: 155px;
  height: 155px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  object-fit: contain;
  z-index: 2;
  pointer-events: none;
}

.username {
  font-size: 22px;
  color: var(--skin-primary-dark);
  letter-spacing: 2px;
  font-weight: 800;
  text-shadow: 0 2px 8px rgba(255, 255, 255, 0.9);
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-tags {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.user-tag, .user-tag2 {
  font-size: 13px;
  color: var(--skin-primary-dark);
  letter-spacing: 1px;
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  padding: 5px 14px;
  border-radius: 999px;
  font-weight: 600;
}

.ring-btn {
  margin-top: 120px;
  margin-left: -180px;
}

/* 分割线 */
.divider {
  height: 1px;
  margin: 8px 24px 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--skin-soft-line) 15%,
    var(--skin-soft-line) 85%,
    transparent 100%
  );
  position: relative;
  z-index: 1;
}

/* 区块间距 */
.section-block {
  margin-top: 10px;
  position: relative;
  z-index: 1;
}

.section-block--compact {
  margin-top: 6px;
}

.section-block--game {
  margin-top: 10px;
}

/* 菜单卡片 */
.menu-card {
  margin: 0 16px;
  border: 1px solid var(--skin-panel-border);
  border-radius: 16px;
  overflow: hidden;
  background: var(--skin-panel-bg);
  box-shadow: 0 2px 6px var(--skin-shadow);
}

.archive-card {
  background: linear-gradient(180deg, var(--skin-panel-bg), var(--skin-panel-bg-2));
}

.archive-card--compact {
  border-radius: 14px;
}

.menu-item {
  display: flex;
  align-items: center;
  min-height: 34px;
  padding: 8px 14px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.menu-item:active {
  background: var(--skin-soft-chip);
}

.menu-item + .menu-item {
  border-top: 1px solid var(--skin-soft-line);
}

.menu-label {
  flex: 1;
  font-size: 13px;
  color: var(--skin-main-text);
  letter-spacing: 0.5px;
}

.menu-val {
  font-size: 10px;
  color: var(--skin-sub-text);
  margin-right: 5px;
  white-space: nowrap;
}

.menu-arrow {
  font-size: 12px;
  color: var(--skin-sub-text);
  line-height: 1;
}

/* 弱化操作 */
.soft-action-row {
  margin: 10px 16px 0;
  padding-bottom: 4px;
  position: relative;
  z-index: 1;
}

.soft-reset-btn {
  width: 100%;
  padding: 12px 16px;
  background: var(--skin-panel-bg);
  border: 1px dashed var(--skin-panel-border);
  border-radius: 16px;
  font-size: 13px;
  font-family: inherit;
  color: var(--skin-sub-text);
  letter-spacing: 1px;
  cursor: pointer;
  transition: background 0.15s;
}

.soft-reset-btn:active {
  background: var(--skin-soft-chip);
}

/* Tab Bar */
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  background: var(--skin-tab-bg);
  backdrop-filter: blur(16px) saturate(1.25);
  -webkit-backdrop-filter: blur(16px) saturate(1.25);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 8px 0 calc(8px + env(safe-area-inset-bottom));
  border-radius: 20px 20px 0 0;
  border-top: 1px solid rgba(201, 168, 76, 0.25);
  box-shadow: 0 -6px 18px rgba(0, 0, 0, 0.05);
  z-index: 100;
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  cursor: pointer;
  opacity: 0.6;
  flex: 1;
}

.tab-item--active {
  opacity: 1;
}

.tab-label {
  font-size: 11px;
  color: var(--skin-tab-text);
}

/* 选择面板 */
.ring-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 200;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.ring-panel {
  width: 100%;
  max-width: 430px;
  background: #fffef5;
  border-radius: 24px 24px 0 0;
  padding: 20px 16px calc(24px + env(safe-area-inset-bottom));
  border-top: 2px solid rgba(201, 168, 76, 0.4);
}

.ring-panel-header {
  text-align: center;
  margin-bottom: 18px;
}

.ring-panel-title {
  font-size: 16px;
  color: #2d5a3a;
  letter-spacing: 4px;
  margin-bottom: 4px;
}

.ring-panel-sub {
  font-size: 11px;
  color: #7aaa7a;
  letter-spacing: 1px;
}

.ring-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px 10px;
  margin-bottom: 20px;
}

.ring-option {
  flex: 0 0 calc(25% - 8px);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

.ring-option-img-wrap {
  position: relative;
  width: 64px;
  height: 64px;
  border-radius: 12px;
  background: rgba(74, 143, 111, 0.06);
  border: 1.5px solid rgba(201, 168, 76, 0.2);
  overflow: hidden;
  transition: all 0.2s;
}

.ring-option.selected .ring-option-img-wrap {
  border-color: #4a8f6f;
  background: rgba(74, 143, 111, 0.12);
  box-shadow: 0 0 0 2px rgba(74, 143, 111, 0.3);
}

.ring-option-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.ring-check {
  position: absolute;
  inset: 0;
  background: rgba(74, 143, 111, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #2d5a3a;
  font-weight: bold;
}

.ring-option-label {
  font-size: 13px;
  color: var(--skin-primary);
  font-weight: bold;
}

.ring-close-btn {
  width: 100%;
  padding: 12px;
  background: var(--skin-primary);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-family: inherit;
  letter-spacing: 2px;
  cursor: pointer;
}

/* 退出登录弹窗 */
.logout-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(2px);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 40px;
}

.logout-dialog {
  width: 100%;
  max-width: 320px;
  background: white;
  border-radius: 20px;
  padding: 24px 20px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  font-family: 'ZCOOL XiaoWei', cursive;
}

.logout-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.logout-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  font-family: 'Ma Shan Zheng', cursive;
}

.logout-desc {
  font-size: 14px;
  color: #888;
  margin-bottom: 24px;
}

.logout-actions {
  display: flex;
  gap: 12px;
}

.logout-btn-cancel,
.logout-btn-confirm {
  flex: 1;
  padding: 10px 0;
  border-radius: 12px;
  font-size: 15px;
  cursor: pointer;
  border: none;
  font-family: 'Ma Shan Zheng', cursive;
  letter-spacing: 1px;
}

.logout-btn-cancel {
  background: #f0f0f0;
  color: #666;
}

.logout-btn-confirm {
  background: #c96b6b;
  color: white;
  box-shadow: 0 4px 10px rgba(201, 107, 107, 0.2);
}

/* 面板动画 */
.panel-enter-active,
.panel-leave-active {
  transition: opacity 0.25s ease;
}

.panel-enter-active .ring-panel,
.panel-leave-active .ring-panel {
  transition: transform 0.25s ease;
}

.panel-enter-from,
.panel-leave-to {
  opacity: 0;
}

.panel-enter-from .ring-panel,
.panel-leave-to .ring-panel {
  transform: translateY(100%);
}
</style>