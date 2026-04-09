<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Toast } from 'vant'
import { getStatues } from '@/api/statues'

// 导入本地图片
import imgLogo from '@/assets/images/logo.jpg'
import imgLogo1 from '@/assets/images/logo1.jpg'
import imgLogo2 from '@/assets/images/logo2.jpg'
import imgLogo3 from '@/assets/images/logo3.jpg'
import imgLogo4 from '@/assets/images/logo4.jpg'

// Banner轮播图片
const bannerImages = [
  imgLogo,
  imgLogo1,
  imgLogo2,
  imgLogo3,
  imgLogo4
]

const router = useRouter()

// 景点数据接口
interface Statue {
  id: number
  name: string
  icon?: string
  latitude: number
  longitude: number
  radius: number
  introduction?: string
  history?: string
  cultural_value?: string
  images: string[]
  order_index: number
  is_active: boolean
  is_checked: boolean
  created_at: string
}

const statues = ref<Statue[]>([])
const loading = ref(false)

// 获取景点列表
const fetchStatues = async () => {
  loading.value = true
  try {
    const res: any = await getStatues()
    if (res.code === 200 && res.data) {
      statues.value = res.data
      // 加载打卡记录
      loadCheckIns()
    } else {
      Toast.fail(res.message || '获取景点列表失败')
    }
  } catch (error: any) {
    console.error('获取景点列表失败:', error)
    Toast.fail(error.detail || '获取景点列表失败')
  } finally {
    loading.value = false
  }
}

// 计算打卡进度
const progress = computed(() => {
  const checked = statues.value.filter(s => s.is_checked).length
  const total = statues.value.length
  return {
    checked,
    total,
    percentage: total > 0 ? Math.round((checked / total) * 100) : 0
  }
})

// 从本地存储加载打卡记录
const loadCheckIns = () => {
  try {
    const checkIns = JSON.parse(localStorage.getItem('checkIns') || '[]')
    statues.value.forEach(statue => {
      statue.is_checked = checkIns.some((c: any) => c.statueId === statue.id)
    })
  } catch (e) {
    console.error('加载打卡记录失败:', e)
  }
}

// 点击石像卡片，跳转到详情页
const handleStatueClick = (statue: Statue) => {
  router.push({
    name: 'HomeDetails',
    params: { id: statue.id }
  })
}

onMounted(() => {
  fetchStatues()
})
</script>

<template>
  <div class="statues-page">
    <!-- 沉浸式头部背景 -->
    <div class="header-banner">
      <div class="overlay"></div>
      <!-- Banner轮播图 -->
      <van-swipe
        class="banner-swiper"
        :autoplay="5000"
        indicator-color="white"
        :show-indicators="false"
      >
        <van-swipe-item v-for="(image, index) in bannerImages" :key="index">
          <img :src="image" alt="Suzhou Banner" class="banner-img" />
        </van-swipe-item>
      </van-swipe>
      <div class="header-content">
        <div class="header-top">
          <div class="title-group">
            <h1 class="app-title">寻迹 · 姑苏</h1>
            <p class="app-subtitle">探索苏州七大历史地标</p>
          </div>
          <div class="camera-btn" @click="router.push('/camera')">
            <van-icon name="photograph" size="24" />
          </div>
        </div>
        
        <!-- 嵌入式进度条 -->
        <div class="header-progress">
          <div class="progress-label">
            <span>探索进度</span>
            <span class="count">{{ progress.checked }}<span class="total">/{{ progress.total }}</span></span>
          </div>
          <van-progress 
            :percentage="progress.percentage" 
            stroke-width="4"
            :show-pivot="false"
            color="#fff"
            track-color="rgba(255,255,255,0.3)"
          />
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-wrapper">
      <!-- Loading 状态 -->
      <div v-if="loading" class="loading-wrapper">
        <van-loading type="spinner" size="32" color="#1989fa">加载中...</van-loading>
      </div>
      
      <!-- 空状态 -->
      <div v-else-if="statues.length === 0" class="empty-wrapper">
        <van-empty description="暂无景点数据" />
      </div>
      
      <!-- 石像卡片列表 -->
      <div v-else class="statues-list">
        <div 
          v-for="statue in statues" 
          :key="statue.id"
          class="statue-card"
          :class="{ 'checked': statue.is_checked }"
          @click="handleStatueClick(statue)"
        >
          <!-- 图片区域 -->
          <div class="card-image-wrapper">
            <van-image 
              fit="cover"
              :src="statue.images && statue.images.length > 0 ? statue.images[0] : imgLogo"
              class="card-image"
            >
              <template v-slot:loading>
                <van-loading type="spinner" size="20" />
              </template>
              <template v-slot:error>
                <van-image :src="imgLogo" fit="cover" />
              </template>
            </van-image>
            
            <!-- 打卡印章 (仅已打卡显示) -->
            <div v-if="statue.is_checked" class="stamp-seal">
              <div class="seal-inner">
                <span>已打卡</span>
                <span class="seal-date">SUZHOU</span>
              </div>
            </div>
          </div>

          <!-- 信息区域 -->
          <div class="card-info">
            <div class="info-header">
              <h3 class="statue-name">
                <span v-if="statue.icon" class="statue-icon">{{ statue.icon }}</span>
                {{ statue.name }}
              </h3>
              <div class="status-indicator" :class="{ active: statue.is_checked }">
                {{ statue.is_checked ? '已点亮' : '待探索' }}
              </div>
            </div>
            <p class="statue-intro">{{ statue.introduction || '暂无简介' }}</p>
          </div>
        </div>
      </div>

      <!-- 底部留白 -->
      <div class="bottom-spacer"></div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.statues-page {
  min-height: 100%;
  background-color: #F5F7FA;
  position: relative;
  padding-bottom: 20px; // 额外的底部留白
}

.header-banner {
  position: relative;
  height: 260px;
  width: 100%;
  overflow: hidden;
  border-bottom-left-radius: 24px;
  border-bottom-right-radius: 24px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  
  .banner-swiper {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    z-index: 0;
  }
  
  .banner-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.6));
    z-index: 1;
    pointer-events: none;
  }
  
  .header-content {
    position: absolute;
    bottom: 30px;
    left: 20px;
    right: 20px;
    color: #fff;
    z-index: 2;
    
    .header-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 20px;
    }
    
    .title-group {
      flex: 1;
    }
    
    .camera-btn {
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.2);
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.3s;
      border: 1px solid rgba(255, 255, 255, 0.3);
      flex-shrink: 0;
      position: relative;
      z-index: 10;
      
      &:active {
        transform: scale(0.95);
        background: rgba(255, 255, 255, 0.3);
      }
    }
    
    .app-title {
      font-size: 32px;
      font-weight: 800;
      margin: 0;
      letter-spacing: 2px;
      font-family: "Songti SC", serif; // 尝试使用衬线体增加文化感
      text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .app-subtitle {
      font-size: 14px;
      opacity: 0.9;
      margin: 6px 0 0 0;
      font-weight: 300;
    }
    
    .header-progress {
      background: rgba(255,255,255,0.15);
      backdrop-filter: blur(4px);
      padding: 12px 16px;
      border-radius: 12px;
      border: 1px solid rgba(255,255,255,0.2);
      
      .progress-label {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 8px;
        font-size: 12px;
        
        .count {
          font-size: 18px;
          font-weight: bold;
          .total {
            font-size: 12px;
            opacity: 0.8;
            font-weight: normal;
          }
        }
      }
    }
  }
}

.content-wrapper {
  padding: 20px 16px;
  margin-top: -20px; // 上移一点，与Header重叠
  position: relative;
  z-index: 3;
  min-height: 400px;
}

.loading-wrapper, .empty-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  min-height: 300px;
}

.statues-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.statue-card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: row; // 改为左右布局或保持上下布局？这里尝试上下布局的大卡片，更有质感
  // 或者做成左右布局：左图右文
  height: 110px;
  
  &:active {
    transform: scale(0.98);
  }
  
  &.checked {
    .status-indicator {
      color: #D32F2F;
      background: rgba(211, 47, 47, 0.1);
    }
  }

  .card-image-wrapper {
    width: 110px;
    height: 110px;
    position: relative;
    flex-shrink: 0;
    
    .card-image {
      width: 100%;
      height: 100%;
    }
    
    // 印章样式
    .stamp-seal {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) rotate(-15deg);
      width: 70px;
      height: 70px;
      border: 3px solid #D32F2F;
      border-radius: 50%;
      color: #D32F2F;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(255, 255, 255, 0.85);
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      z-index: 10;
      
      .seal-inner {
        text-align: center;
        display: flex;
        flex-direction: column;
        
        span:first-child {
          font-size: 14px;
          font-weight: bold;
          border-bottom: 1px solid #D32F2F;
          padding-bottom: 2px;
          margin-bottom: 2px;
        }
        
        .seal-date {
          font-size: 8px;
          letter-spacing: 1px;
        }
      }
    }
  }
  
  .card-info {
    flex: 1;
    padding: 14px 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    
    .info-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      
      .statue-name {
        margin: 0;
        font-size: 17px;
        color: #333;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 6px;
        
        .statue-icon {
          font-size: 20px;
        }
      }
      
      .status-indicator {
        font-size: 11px;
        padding: 2px 8px;
        border-radius: 10px;
        background: #F0F2F5;
        color: #909399;
        transition: all 0.3s;
        
        &.active {
          color: #D32F2F;
          background: rgba(211, 47, 47, 0.08);
          font-weight: 600;
        }
      }
    }
    
    .statue-intro {
      margin: 0;
      font-size: 13px;
      color: #666;
      line-height: 1.5;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }
}

.bottom-spacer {
  height: 60px;
}
</style>