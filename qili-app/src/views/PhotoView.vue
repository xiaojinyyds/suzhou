<template>
  <div class="photo-page">

    <!-- 顶部 Header -->
    <header class="top-card">
      <h1 class="header-title">打卡留念</h1>
    </header>

    <!-- 内容画布 -->
    <div class="canvas-wrapper">

      <!-- 提示文字 -->
      <p class="hint-text">使用 AR 相框留影，让你的山塘打卡更像一张限定纪念照</p>

      <!-- 拍照按钮区 -->
      <div class="action-row">
        <button class="action-btn main-action" @click="showCamera = true">
          <span class="action-icon">📸</span>
          <span class="action-label">AR 相框拍照</span>
        </button>
      </div>

      <!-- 照片网格 -->
      <div class="photo-grid" v-if="photos.length > 0">
        <div
          class="photo-item"
          v-for="photo in photos"
          :key="photo.id"
          @click="openPreview(photo)"
        >
          <img :src="getFullUrl(photo.image_url)" class="photo-thumb" alt="照片" />
        </div>
      </div>

      <!-- 空状态 -->
      <div class="empty-state" v-else-if="!loading">
        <div class="empty-icon">🦝</div>
        <p class="empty-text">还没有照片<br>快去拍一张吧</p>
      </div>

      <!-- 加载状态 -->
      <div class="empty-state" v-if="loading">
        <div class="loading-spinner"></div>
        <p class="empty-text">加载中...</p>
      </div>

    </div>

    <!-- 大图预览 -->
    <transition name="fade">
      <div class="preview-overlay" v-if="previewPhoto" @click="closePreview">
        <img :src="getFullUrl(previewPhoto.image_url)" class="preview-img" @click.stop />
        <button class="preview-close" @click="closePreview">✕</button>
        <div class="preview-actions-bar" @click.stop>
          <button class="preview-action-btn preview-download" @click="downloadPhoto(previewPhoto)">⬇ 保存到相册</button>
          <button class="preview-action-btn preview-delete" @click="confirmDelete(previewPhoto)">🗑 删除</button>
        </div>
      </div>
    </transition>

    <!-- AR 相机组件 -->
    <transition name="slide-up">
      <ARCamera 
        v-if="showCamera" 
        @close="showCamera = false" 
        @upload-success="fetchPhotos" 
      />
    </transition>

    <!-- Tab Bar -->
    <nav class="tab-bar">
      <div class="tab-item" :class="{ 'tab-item--active': $route.name === 'home' }" @click="$router.push({ name: 'home' })">
        <Home :size="22" />
        <span class="tab-label">首页</span>
      </div>
      <div class="tab-item" :class="{ 'tab-item--active': $route.name === 'checkin' }" @click="$router.push({ name: 'checkin' })">
        <MapPin :size="22" />
        <span class="tab-label">打卡</span>
      </div>
      <div class="tab-item" :class="{ 'tab-item--active': $route.name === 'photo' }" @click="$router.push({ name: 'photo' })">
        <Camera :size="22" />
        <span class="tab-label">拍照</span>
      </div>
      <div class="tab-item" :class="{ 'tab-item--active': $route.name === 'merch' }" @click="$router.push({ name: 'merch' })">
        <ShoppingCart :size="22" />
        <span class="tab-label">周边</span>
      </div>
      <div class="tab-item" :class="{ 'tab-item--active': $route.name === 'my' }" @click="$router.push({ name: 'my' })">
        <User :size="22" />
        <span class="tab-label">我的</span>
      </div>
    </nav>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Home, MapPin, Camera, ShoppingCart, User } from 'lucide-vue-next'
import { get, del } from '@/utils/request'
import ARCamera from '@/components/camera/ARCamera.vue'

const photos = ref([])
const loading = ref(true)
const showCamera = ref(false)
const previewPhoto = ref(null)

// 补全图片完整相对路径
const getFullUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
  return baseUrl + url
}

// 获取照片
const fetchPhotos = async () => {
  loading.value = true
  try {
    const res = await get('/api/v1/photos/my')
    photos.value = res.data?.items || []
  } catch (err) {
    console.error('获取照片失败:', err)
  } finally {
    loading.value = false
  }
}

// 预览
function openPreview(photo) { previewPhoto.value = photo }
function closePreview() { previewPhoto.value = null }

// 下载照片
const downloadPhoto = async (photo) => {
  try {
    const url = getFullUrl(photo.image_url)
    const response = await fetch(url)
    const blob = await response.blob()
    const blobUrl = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.style.display = 'none'
    a.href = blobUrl
    a.download = `苏州打卡_AR合影_${Date.now()}.jpg`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(blobUrl)
  } catch (err) {
    console.error('下载失败:', err)
    alert('下载失败，请长按图片保存。')
  }
}

// 删除照片
const confirmDelete = async (photo) => {
  if (!confirm('确定要删除这张照片吗？')) return
  try {
    await del(`/api/v1/photos/${photo.id}`)
    photos.value = photos.value.filter(p => p.id !== photo.id)
    closePreview()
  } catch (err) {
    console.error('删除失败:', err)
    alert('删除失败，请重试')
  }
}

onMounted(() => {
  fetchPhotos()
})
</script>

<style scoped>
.photo-page {
  display: flex;
  flex-direction: column;
  height: 100dvh;
  background-color: #fffdec;
  max-width: 430px;
  margin: 0 auto;
  overflow: hidden;
  font-family: 'Ma Shan Zheng', cursive;
  position: relative;
}

/* Header */
.top-card {
  position: relative;
  background: var(--skin-primary);
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.12'/%3E%3C/svg%3E"),
    linear-gradient(135deg, rgba(255, 255, 255, 0.18) 0%, transparent 50%, rgba(0, 0, 0, 0.08) 100%);
  background-repeat: repeat, no-repeat;
  background-size: auto, 100% 100%;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0 0 28px 28px;
  border-bottom: 1.5px solid rgb(143, 141, 116);
  flex-shrink: 0;
}
.header-title {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: 4px;
  color: #fff;
  margin: 0;
  text-shadow: 0 1px 3px rgba(0,0,0,0.15);
}

/* canvas-wrapper */
.canvas-wrapper {
  position: relative;
  width: 100%;
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  background: linear-gradient(to bottom, transparent 70%, var(--skin-primary) 200%);
  padding-bottom: 90px;
}


/* 提示文字 */
.hint-text {
  text-align: center;
  font-size: 13px;
  color: #aaa;
  padding: 16px 0 12px;
  position: relative;
  z-index: 1;
  letter-spacing: 1px;
}

/* 拍照按钮区 */
.action-row {
  display: flex;
  justify-content: center;
  padding: 0 16px 16px;
  position: relative;
  z-index: 1;
}
.main-action {
  width: 80%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 0;
  background: linear-gradient(135deg, var(--skin-primary), #4ca98e);
  color: #fff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(76, 169, 142, 0.4);
  transition: transform 0.2s, box-shadow 0.2s;
}
.main-action:active { 
  transform: translateY(2px); 
  box-shadow: 0 2px 6px rgba(76, 169, 142, 0.4);
}
.action-icon { font-size: 24px; }
.action-label { font-size: 16px; font-family: 'Ma Shan Zheng', cursive; letter-spacing: 2px; }

/* 照片网格 */
.photo-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3px;
  padding: 0 16px;
  position: relative;
  z-index: 1;
}
.photo-item {
  aspect-ratio: 1;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid rgba(201, 168, 76, 0.3);
  background: rgba(0,0,0,0.05);
}
.photo-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.2s;
}
.photo-thumb:active { transform: scale(0.96); }

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 0 40px;
  gap: 14px;
  position: relative;
  z-index: 1;
}
.empty-icon { font-size: 52px; line-height: 1; }
.empty-text {
  font-size: 14px;
  color: #bbb;
  text-align: center;
  line-height: 2;
}
.loading-spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(0,0,0,0.1);
  border-top: 3px solid var(--skin-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 大图预览 */
.preview-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.88);
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
}
.preview-img {
  max-width: 92%;
  max-height: 80vh;
  border-radius: 12px;
  object-fit: contain;
}
.preview-close {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255,255,255,0.15);
  border: none;
  color: #fff;
  font-size: 18px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}
.preview-actions-bar {
  position: absolute;
  bottom: 48px;
  left: 0;
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 20px;
}
.preview-action-btn {
  background: rgba(60, 60, 60, 0.85);
  border: none;
  color: #fff;
  font-size: 14px;
  font-family: 'Ma Shan Zheng', cursive;
  padding: 10px 24px;
  border-radius: 999px;
  cursor: pointer;
  letter-spacing: 2px;
}
.preview-download {
  background: rgba(76, 169, 142, 0.85); /* 主题绿 */
}
.preview-delete {
  background: rgba(220, 80, 60, 0.85);
}

/* Tab Bar */
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  background: rgba(252, 248, 240, 0.98);
  backdrop-filter: blur(16px) saturate(1.4);
  -webkit-backdrop-filter: blur(16px) saturate(1.4);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 8px 0 calc(8px + env(safe-area-inset-bottom));
  border-radius: 20px 20px 0 0;
  border-top: 1px solid rgba(201, 168, 76, 0.25);
  z-index: 100;
}
.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  cursor: pointer;
  opacity: 0.55;
  flex: 1;
}
.tab-item--active { opacity: 1; }
.tab-label { font-size: 11px; color: var(--skin-primary); } /* modified to use theme */

/* 动画 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.25s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.slide-up-enter-active, .slide-up-leave-active { transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); opacity: 0; }
</style>
