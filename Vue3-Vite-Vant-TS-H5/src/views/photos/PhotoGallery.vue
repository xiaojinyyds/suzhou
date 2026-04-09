<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Toast, Dialog, ImagePreview } from 'vant'
import { getMyPhotos, getPublicPhotos, deletePhoto, updatePhotoPublicStatus, getPhotoStats } from '@/api/photo'

const router = useRouter()

// 照片数据类型
interface Photo {
  id: number
  user_id: number
  image_url: string
  oss_key?: string
  thumbnail_url?: string
  decoration_type: string
  file_size?: number
  width?: number
  height?: number
  is_public: boolean
  is_deleted: boolean
  view_count: number
  created_at: string
  updated_at?: string
}

// 统计数据类型
interface Stats {
  total_count: number
  public_count: number
  private_count: number
  user_id: number
}

// 状态管理
const activeTab = ref('public') // 'public' | 'my'
const loading = ref(false)
const refreshing = ref(false)

// 广场数据
const publicPhotos = ref<Photo[]>([])
const publicPage = ref(1)
const publicFinished = ref(false)

// 我的数据
const myPhotos = ref<Photo[]>([])
const myPage = ref(1)
const myFinished = ref(false)
const stats = ref<Stats | null>(null)

const pageSize = 20

// 加载广场照片
const loadPublicPhotos = async (isRefresh = false) => {
  // 防止并发请求导致数据重复
  if (loading.value && !isRefresh) return
  
  loading.value = true // 立即设置 loading，防止 van-list 重复触发
  
  if (isRefresh) {
    publicPage.value = 1
    publicFinished.value = false
    refreshing.value = true
  }

  try {
    const skip = (publicPage.value - 1) * pageSize
    const res: any = await getPublicPhotos(skip, pageSize)
    
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || '加载失败')
      return
    }
    
    const newPhotos = res.data.items || [] // 适配 Page 返回结构
    
    if (isRefresh) {
      publicPhotos.value = newPhotos
    } else {
      publicPhotos.value.push(...newPhotos)
    }
    
    if (newPhotos.length < pageSize) {
      publicFinished.value = true
    } else {
      publicPage.value++
    }
  } catch (error) {
    console.error('加载广场照片失败:', error)
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

// 加载我的照片
const loadMyPhotos = async (isRefresh = false) => {
  // 防止并发请求导致数据重复
  if (loading.value && !isRefresh) return
  
  loading.value = true // 立即设置 loading，防止 van-list 重复触发
  
  if (isRefresh) {
    myPage.value = 1
    myFinished.value = false
    refreshing.value = true
    loadStats()
  }

  try {
    const skip = (myPage.value - 1) * pageSize
    console.log(`📚 加载我的照片: page=${myPage.value}, skip=${skip}`)
    
    const res: any = await getMyPhotos(skip, pageSize)
    
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || '加载失败')
      myFinished.value = true // 发生错误时停止加载，防止死循环
      return
    }
    
    const newPhotos = res.data.items || [] // 适配分页返回结构
    console.log(`📸 获取到照片: ${newPhotos.length} 张`)
    
    if (isRefresh) {
      myPhotos.value = newPhotos
    } else {
      myPhotos.value.push(...newPhotos)
    }
    
    if (newPhotos.length < pageSize) {
      myFinished.value = true
      console.log('🏁 加载完毕')
    } else {
      myPage.value++
    }
  } catch (error) {
    console.error('加载我的照片失败:', error)
    myFinished.value = true // 发生异常时停止加载
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

// 统一加载入口
const onLoad = () => {
  if (activeTab.value === 'public') {
    if (!publicFinished.value) loadPublicPhotos()
  } else {
    if (!myFinished.value) loadMyPhotos()
  }
}

// 统一刷新入口
const onRefresh = () => {
  if (activeTab.value === 'public') {
    loadPublicPhotos(true)
  } else {
    loadMyPhotos(true)
  }
}

// 切换 Tab 时重新加载（如果是空的）
watch(activeTab, (val) => {
  if (val === 'public' && publicPhotos.value.length === 0) {
    loadPublicPhotos(true)
  } else if (val === 'my') {
    if (myPhotos.value.length === 0) loadMyPhotos(true)
    loadStats()
  }
})

// 加载统计信息
const loadStats = async () => {
  try {
    const res: any = await getPhotoStats()
    if (res && res.code === 200) {
      stats.value = res.data as Stats
    }
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

// 查看大图
const viewPhoto = (photo: Photo, index: number) => {
  const currentList = activeTab.value === 'public' ? publicPhotos.value : myPhotos.value
  const images = currentList.map(p => p.image_url)
  // 修正索引：要在当前列表中找到点击照片的正确索引
  const realIndex = currentList.findIndex(p => p.id === photo.id)
  
  ImagePreview({
    images,
    startPosition: realIndex > -1 ? realIndex : 0,
    closeable: true
  })
}

// 删除照片
const handleDelete = (photo: Photo) => {
  Dialog.confirm({
    title: '确认删除',
    message: '删除后无法恢复，确定要删除这张照片吗？',
  }).then(async () => {
    try {
      const res: any = await deletePhoto(photo.id)
      if (!res || res.code !== 200) {
        Toast.fail(res?.message || '删除失败')
        return
      }
      
      Toast.success('删除成功')
      myPhotos.value = myPhotos.value.filter(p => p.id !== photo.id)
      loadStats()
    } catch (error) {
      console.error('删除失败:', error)
      Toast.fail('删除失败，请重试')
    }
  }).catch(() => {})
}

// 切换公开状态
const togglePublic = async (photo: Photo) => {
  try {
    const newStatus = !photo.is_public
    const res: any = await updatePhotoPublicStatus(photo.id, newStatus)
    
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || '设置失败')
      return
    }
    
    photo.is_public = newStatus
    Toast.success(newStatus ? '已设为公开' : '已设为私密')
    loadStats()
    
    // 如果设为公开，刷新一下广场数据（可选，为了即时看到）
    if (newStatus) {
      // 简单处理：标记广场数据需要刷新，或者静默刷新
      // publicPage.value = 1; loadPublicPhotos(true);
    }
  } catch (error) {
    console.error('设置失败:', error)
    Toast.fail('设置失败，请重试')
  }
}

const goToCamera = () => router.push('/camera')

// 初始化
onMounted(() => {
  loadPublicPhotos(true) // 默认加载广场
})
</script>

<template>
  <div class="photo-gallery">
    <!-- 沉浸式头部 -->
    <div class="header-banner">
      <div class="overlay"></div>
      <img src="@/assets/images/logo3.jpg" alt="Banner" class="banner-bg" />
      
      <div class="header-content">
        <div class="header-top">
          <div class="title-group">
            <h1 class="app-title">光影 · 留念</h1>
            <p class="app-subtitle">记录你的每一次探索</p>
          </div>
          <div class="camera-btn" @click="goToCamera">
            <van-icon name="photograph" size="24" />
          </div>
        </div>

        <!-- 统计数据 (仅在我的相册显示) -->
        <div class="stats-bar" v-if="activeTab === 'my' && stats">
          <div class="stat-item">
            <span class="num">{{ stats.total_count }}</span>
            <span class="label">共拍摄</span>
          </div>
          <div class="divider"></div>
          <div class="stat-item">
            <span class="num">{{ stats.public_count }}</span>
            <span class="label">公开</span>
          </div>
          <div class="divider"></div>
          <div class="stat-item">
            <span class="num">{{ stats.private_count }}</span>
            <span class="label">私密</span>
          </div>
        </div>
      </div>
      
      <!-- Tabs 切换栏 (嵌入 Header 底部) -->
      <div class="header-tabs">
        <van-tabs v-model:active="activeTab" background="transparent" color="#fff" title-active-color="#fff" title-inactive-color="rgba(255,255,255,0.7)" line-width="20px">
          <van-tab title="光影广场" name="public"></van-tab>
          <van-tab title="我的相册" name="my"></van-tab>
        </van-tabs>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-wrapper">
      <van-pull-refresh v-model="refreshing" @refresh="onRefresh" class="refresh-container">
        <van-list
          v-model:loading="loading"
          :finished="activeTab === 'public' ? publicFinished : myFinished"
          finished-text="没有更多了"
          @load="onLoad"
        >
          <div class="photos-list">
            <!-- 广场/我的 列表复用结构 -->
            <div
              v-for="(photo, index) in (activeTab === 'public' ? publicPhotos : myPhotos)"
              :key="photo.id"
              class="photo-card"
              @click="viewPhoto(photo, index)"
            >
              <!-- 左侧图片 -->
              <div class="card-image-wrapper">
                <img
                  :src="photo.thumbnail_url || photo.image_url"
                  class="card-image"
                  loading="lazy"
                />
                <div v-if="photo.decoration_type && photo.decoration_type !== 'none'" class="effect-badge">
                  {{ photo.decoration_type }}
                </div>
              </div>

              <!-- 右侧信息 -->
              <div class="card-info">
                <div class="info-header">
                  <span class="date">{{ new Date(photo.created_at).toLocaleDateString() }}</span>
                  <span v-if="activeTab === 'my'" class="status-tag" :class="{ public: photo.is_public }">
                    {{ photo.is_public ? '已公开' : '仅自己可见' }}
                  </span>
                  <span v-else class="status-tag public">
                    来自用户 {{ photo.user_id }}
                  </span>
                </div>

                <!-- 仅在我的相册显示操作按钮 -->
                <div class="info-actions" v-if="activeTab === 'my'">
                  <button 
                    class="action-btn" 
                    :class="{ active: photo.is_public }"
                    @click.stop="togglePublic(photo)"
                  >
                    <van-icon :name="photo.is_public ? 'eye-o' : 'closed-eye'" />
                    {{ photo.is_public ? '设为私密' : '设为公开' }}
                  </button>
                  
                  <button class="action-btn delete" @click.stop="handleDelete(photo)">
                    <van-icon name="delete-o" />
                    删除
                  </button>
                </div>
                
                <!-- 广场模式下的互动占位 (后续可加点赞) -->
                <div class="info-actions" v-else>
                   <button class="action-btn">
                     <van-icon name="like-o" />
                     点赞
                   </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <van-empty
            v-if="!loading && (activeTab === 'public' ? publicPhotos.length === 0 : myPhotos.length === 0)"
            :description="activeTab === 'public' ? '广场还没有照片，快来发布第一张吧！' : '还没有拍照记录'"
            class="empty-state"
          >
            <van-button round type="primary" @click="goToCamera" color="#D32F2F">
              去拍照打卡
            </van-button>
          </van-empty>
        </van-list>
      </van-pull-refresh>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.photo-gallery {
  min-height: 100vh;
  background-color: #F5F7FA;
  position: relative;
}

.header-banner {
  position: relative;
  height: 280px; // 增加高度以容纳 Tabs
  width: 100%;
  overflow: hidden;
  border-bottom-left-radius: 24px;
  border-bottom-right-radius: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  
  .banner-bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    position: absolute;
    top: 0;
    left: 0;
  }

  .overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.8));
  }

  .header-content {
    position: absolute;
    top: 60px; // 调整位置
    left: 20px;
    right: 20px;
    color: #fff;
    z-index: 2;

    .header-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 20px;

      .title-group {
        .app-title {
          font-size: 32px;
          font-weight: 800;
          margin: 0;
          letter-spacing: 2px;
          font-family: "Songti SC", serif;
          text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        .app-subtitle {
          font-size: 14px;
          opacity: 0.9;
          margin: 6px 0 0 0;
          font-weight: 300;
        }
      }

      .camera-btn {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.3);
        
        &:active {
          transform: scale(0.95);
          background: rgba(255, 255, 255, 0.3);
        }
      }
    }

    .stats-bar {
      background: rgba(255,255,255,0.15);
      backdrop-filter: blur(8px);
      padding: 10px 0;
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.2);
      display: flex;
      justify-content: space-around;
      align-items: center;
      margin-bottom: 10px;

      .stat-item {
        text-align: center;
        display: flex;
        flex-direction: column;
        
        .num {
          font-size: 16px;
          font-weight: bold;
          margin-bottom: 2px;
        }
        .label {
          font-size: 10px;
          opacity: 0.8;
        }
      }

      .divider {
        width: 1px;
        height: 16px;
        background: rgba(255,255,255,0.3);
      }
    }
  }
  
  .header-tabs {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 3;
    
    :deep(.van-tabs__wrap) {
      height: 44px;
    }
    :deep(.van-tab) {
      font-size: 15px;
      font-weight: 600;
    }
  }
}

.content-wrapper {
  padding: 20px 16px;
  margin-top: 0;
  position: relative;
  z-index: 3;
  padding-bottom: 80px; 
}

.photos-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.photo-card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  display: flex;
  height: 120px;
  transition: transform 0.2s;

  &:active {
    transform: scale(0.98);
  }

  .card-image-wrapper {
    width: 120px;
    height: 120px;
    position: relative;
    flex-shrink: 0;

    .card-image {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .effect-badge {
      position: absolute;
      top: 6px;
      left: 6px;
      background: rgba(0,0,0,0.6);
      color: #fff;
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      backdrop-filter: blur(2px);
    }
  }

  .card-info {
    flex: 1;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    .info-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;

      .date {
        font-size: 14px;
        color: #333;
        font-weight: 600;
      }

      .status-tag {
        font-size: 11px;
        padding: 2px 6px;
        border-radius: 4px;
        background: #F5F7FA;
        color: #909399;
        
        &.public {
          color: #D32F2F;
          background: rgba(211, 47, 47, 0.08);
        }
      }
    }

    .info-actions {
      display: flex;
      gap: 12px;

      .action-btn {
        flex: 1;
        height: 32px;
        border: none;
        border-radius: 16px;
        background: #F5F7FA;
        color: #666;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        transition: all 0.2s;

        &:active {
          background: #e6e8eb;
        }

        &.active {
          background: rgba(25, 137, 250, 0.1);
          color: #1989fa;
        }

        &.delete {
          background: rgba(255, 76, 76, 0.08);
          color: #ff4c4c;
          
          &:active {
            background: rgba(255, 76, 76, 0.15);
          }
        }
      }
    }
  }
}

.empty-state {
  padding: 40px 0;
}
</style>
