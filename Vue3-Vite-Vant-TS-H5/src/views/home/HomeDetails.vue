<script setup lang="ts">
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Toast, Dialog } from 'vant'
import { getStatue } from '@/api/statues'
import { checkIn } from '@/api/checkin'
import { getCurrentPosition, calculateDistance, formatDistance } from '@/utils/geolocation'

const route = useRoute()
const router = useRouter()

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

const statue = ref<Statue | null>(null)
const loading = ref(false)
const activeImageIndex = ref(0)
const checkingIn = ref(false)
const userLocation = ref<{ latitude: number; longitude: number } | null>(null)
const mapInstance = ref<any>(null)
const showMap = ref(false)

// 获取景点详情
const fetchStatueDetail = async () => {
  const statueId = Number(route.params.id)
  if (!statueId) {
    Toast.fail('景点ID无效')
    router.back()
    return
  }

  loading.value = true
  try {
    const res: any = await getStatue(statueId)
    if (res.code === 200 && res.data) {
      statue.value = res.data
      // 检查打卡状态
      checkIfCheckedIn()
    } else {
      Toast.fail(res.message || '获取景点详情失败')
      setTimeout(() => router.back(), 1500)
    }
  } catch (error: any) {
    console.error('获取景点详情失败:', error)
    Toast.fail(error.detail || '获取景点详情失败')
    setTimeout(() => router.back(), 1500)
  } finally {
    loading.value = false
  }
}

// 检查是否已打卡
const checkIfCheckedIn = () => {
  if (!statue.value) return
  try {
    const checkIns = JSON.parse(localStorage.getItem('checkIns') || '[]')
    statue.value.is_checked = checkIns.some((c: any) => c.statueId === statue.value!.id)
  } catch (e) {
    console.error('检查打卡状态失败:', e)
  }
}

// 计算距离
const distance = computed(() => {
  if (!statue.value || !userLocation.value) {
    return '获取中...'
  }
  
  const dist = calculateDistance(
    userLocation.value.latitude,
    userLocation.value.longitude,
    statue.value.latitude,
    statue.value.longitude
  )
  
  return formatDistance(dist)
})

// 获取用户位置
const getUserLocation = async () => {
  try {
    const position = await getCurrentPosition()
    userLocation.value = {
      latitude: position.latitude,
      longitude: position.longitude
    }
    // 如果地图已初始化，更新标记
    if (mapInstance.value && statue.value) {
      updateMapMarkers()
    }
  } catch (error: any) {
    console.error('获取位置失败:', error)
    Toast.fail(error.message || '获取位置失败')
  }
}

// 返回上一页
const goBack = () => {
  router.back()
}

// 打卡功能
const handleCheckIn = async () => {
  if (!statue.value) return
  
  if (statue.value.is_checked) {
    Toast.success('您已经打卡过了！')
    return
  }

  // 获取当前位置
  if (!userLocation.value) {
    Toast.loading({ message: '正在获取位置...', forbidClick: true })
    try {
      await getUserLocation()
      Toast.clear()
    } catch (error) {
      Toast.clear()
      Dialog.confirm({
        title: '位置获取失败',
        message: '无法获取您的位置信息，请确保已授权位置权限。是否重试？',
      }).then(async () => {
        await getUserLocation()
      }).catch(() => {})
      return
    }
  }

  if (!userLocation.value) {
    Toast.fail('无法获取位置信息')
    return
  }

  checkingIn.value = true
  Toast.loading({ message: '打卡中...', forbidClick: true })

  try {
    const res: any = await checkIn({
      statue_id: statue.value.id,
      latitude: userLocation.value.latitude,
      longitude: userLocation.value.longitude
    })

    Toast.clear()

    if (res.code === 200 && res.data) {
      if (res.data.success) {
        // 打卡成功
        statue.value.is_checked = true
        // 更新本地存储
        const checkIns = JSON.parse(localStorage.getItem('checkIns') || '[]')
        checkIns.push({
          statueId: statue.value.id,
          statueName: statue.value.name,
          checkedAt: new Date().toISOString()
        })
        localStorage.setItem('checkIns', JSON.stringify(checkIns))
        
        Toast.success({
          message: `${res.data.message}\n距离: ${res.data.distance} 米`,
          duration: 2000
        })
      } else {
        // 打卡失败（距离太远或已打卡）
        Toast.fail({
          message: res.data.message,
          duration: 3000
        })
      }
    } else {
      Toast.fail(res.message || '打卡失败')
    }
  } catch (error: any) {
    console.error('打卡失败:', error)
    Toast.fail(error.detail || '打卡失败，请重试')
  } finally {
    checkingIn.value = false
  }
}

// 初始化地图
const initMap = () => {
  if (!(window as any).AMap || !statue.value) return
  
  const AMap = (window as any).AMap
  
  // 创建地图实例
  mapInstance.value = new AMap.Map('amap-container', {
    zoom: 16,
    center: [statue.value.longitude, statue.value.latitude],
    mapStyle: 'amap://styles/normal'
  })
  
  updateMapMarkers()
}

// 更新地图标记
const updateMapMarkers = () => {
  if (!mapInstance.value || !statue.value) return
  
  const AMap = (window as any).AMap
  
  // 清除之前的标记
  mapInstance.value.clearMap()
  
  // 添加景点标记
  const statueMarker = new AMap.Marker({
    position: [statue.value.longitude, statue.value.latitude],
    title: statue.value.name,
    icon: new AMap.Icon({
      size: new AMap.Size(40, 50),
      image: '//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-red.png',
      imageSize: new AMap.Size(40, 50)
    })
  })
  
  mapInstance.value.add(statueMarker)
  
  // 如果有用户位置，添加用户标记
  if (userLocation.value) {
    const userMarker = new AMap.Marker({
      position: [userLocation.value.longitude, userLocation.value.latitude],
      title: '我的位置',
      icon: new AMap.Icon({
        size: new AMap.Size(30, 30),
        image: '//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-default.png',
        imageSize: new AMap.Size(30, 30)
      })
    })
    
    mapInstance.value.add(userMarker)
    
    // 添加圆形范围
    const circle = new AMap.Circle({
      center: [statue.value.longitude, statue.value.latitude],
      radius: statue.value.radius,
      fillColor: '#1989fa',
      fillOpacity: 0.2,
      strokeColor: '#1989fa',
      strokeWeight: 2
    })
    
    mapInstance.value.add(circle)
    
    // 调整视野以包含所有标记
    mapInstance.value.setFitView()
  }
}

// 显示/隐藏地图
const toggleMap = () => {
  showMap.value = !showMap.value
  if (showMap.value && !mapInstance.value) {
    // 延迟初始化以确保DOM已渲染
    setTimeout(() => {
      initMap()
    }, 100)
  }
}

onMounted(() => {
  fetchStatueDetail()
  getUserLocation()
})

onBeforeUnmount(() => {
  if (mapInstance.value) {
    mapInstance.value.destroy()
  }
})
</script>

<template>
  <div class="statue-detail">
    <!-- Loading 状态 -->
    <div v-if="loading" class="loading-container">
      <van-loading type="spinner" size="48" color="#1989fa">加载中...</van-loading>
    </div>

    <!-- 详情内容 -->
    <div v-else-if="statue" class="detail-content">
      <!-- 头部导航 -->
      <div class="detail-header">
        <van-icon name="arrow-left" size="24" color="#fff" @click="goBack" />
        <div class="header-title">{{ statue.name }}</div>
        <div class="placeholder"></div>
      </div>

      <!-- 图片轮播 -->
      <div class="image-swiper">
        <van-swipe 
          :autoplay="3000" 
          indicator-color="white"
          @change="activeImageIndex = $event"
          v-if="statue.images && statue.images.length > 0"
        >
          <van-swipe-item v-for="(image, index) in statue.images" :key="index">
            <van-image
              :src="image"
              fit="cover"
              class="swiper-image"
            >
              <template v-slot:loading>
                <van-loading type="spinner" size="32" />
              </template>
            </van-image>
          </van-swipe-item>
        </van-swipe>
        
        <!-- 打卡印章（已打卡时显示） -->
        <div v-if="statue.is_checked" class="detail-stamp">
          <div class="stamp-inner">
            <span class="stamp-text">已打卡</span>
            <span class="stamp-date">CHECKED</span>
          </div>
        </div>
      </div>

      <!-- 基本信息卡片 -->
      <div class="info-card">
        <div class="card-header">
          <h1 class="statue-title">
            <span v-if="statue.icon" class="title-icon">{{ statue.icon }}</span>
            {{ statue.name }}
          </h1>
          <van-tag 
            :type="statue.is_checked ? 'success' : 'warning'" 
            size="large"
            round
          >
            {{ statue.is_checked ? '已点亮' : '待探索' }}
          </van-tag>
        </div>

        <!-- 简介 -->
        <div v-if="statue.introduction" class="section">
          <div class="section-title">
            <van-icon name="info-o" />
            景点简介
          </div>
          <p class="section-content">{{ statue.introduction }}</p>
        </div>

        <!-- 位置信息 -->
        <div class="section">
          <div class="section-title">
            <van-icon name="location-o" />
            位置信息
            <span class="view-map-btn" @click="toggleMap">
              {{ showMap ? '收起地图' : '查看地图' }}
            </span>
          </div>
          <div class="location-info">
            <div class="info-row">
              <span class="label">经纬度：</span>
              <span class="value">{{ statue.latitude.toFixed(6) }}, {{ statue.longitude.toFixed(6) }}</span>
            </div>
            <div class="info-row">
              <span class="label">打卡半径：</span>
              <span class="value">{{ statue.radius }}米</span>
            </div>
            <div class="info-row">
              <span class="label">距离您：</span>
              <span class="value">{{ distance }}</span>
            </div>
            
            <!-- 地图容器 (移动到这里) -->
            <div v-show="showMap" class="map-container">
              <div id="amap-container"></div>
            </div>
          </div>
        </div>

        <!-- 历史背景 -->
        <div v-if="statue.history" class="section">
          <div class="section-title">
            <van-icon name="notes-o" />
            历史背景
          </div>
          <p class="section-content">{{ statue.history }}</p>
        </div>

        <!-- 文化价值 -->
        <div v-if="statue.cultural_value" class="section">
          <div class="section-title">
            <van-icon name="star-o" />
            文化价值
          </div>
          <p class="section-content">{{ statue.cultural_value }}</p>
        </div>
      </div>

      <!-- 底部留白 -->
      <div class="bottom-spacer"></div>
    </div>

    <!-- 底部操作栏 -->
    <div v-if="statue" class="action-bar">
      <van-button 
        :type="statue.is_checked ? 'default' : 'primary'" 
        size="large" 
        round
        block
        :disabled="statue.is_checked"
        :loading="checkingIn"
        @click="handleCheckIn"
      >
        <van-icon v-if="!checkingIn" :name="statue.is_checked ? 'success' : 'location'" />
        {{ checkingIn ? '打卡中...' : (statue.is_checked ? '已完成打卡' : '立即打卡') }}
      </van-button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.statue-detail {
  min-height: 100vh;
  background: #fff; // 改为白色背景，更简洁
  padding-bottom: 80px;
  position: relative;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #fff;
}

.detail-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  background: linear-gradient(to bottom, rgba(0,0,0,0.6) 0%, transparent 100%);
  z-index: 100;
  transition: background 0.3s;
  
  .header-title {
    flex: 1;
    text-align: center;
    color: #fff;
    font-size: 18px;
    font-weight: 600;
    opacity: 0; // 默认隐藏，滚动显示
    transition: opacity 0.3s;
  }
  
  .placeholder {
    width: 24px;
  }
}

.image-swiper {
  position: relative;
  width: 100%;
  height: 420px; // 增加高度
  background: #e0e0e0;
  
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: linear-gradient(to top, rgba(0,0,0,0.4), transparent);
    z-index: 1;
  }
  
  .swiper-image {
    width: 100%;
    height: 100%;
  }
  
  .detail-stamp {
    position: absolute;
    top: 80px;
    right: 24px;
    width: 88px;
    height: 88px;
    border: 3px solid #D32F2F;
    border-radius: 50%;
    transform: rotate(-15deg);
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.95);
    z-index: 10;
    box-shadow: 0 4px 16px rgba(211, 47, 47, 0.25);
    animation: stamp-in 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    
    .stamp-inner {
      text-align: center;
      color: #D32F2F;
      
      .stamp-text {
        display: block;
        font-size: 16px;
        font-weight: 800;
        line-height: 1.2;
      }
      
      .stamp-date {
        display: block;
        font-size: 10px;
        letter-spacing: 1px;
        font-weight: 600;
        margin-top: 2px;
      }
    }
  }
}

@keyframes stamp-in {
  from { transform: scale(1.5) rotate(-15deg); opacity: 0; }
  to { transform: scale(1) rotate(-15deg); opacity: 1; }
}

.info-card {
  margin: -100px 16px 0; // 更大的上浮，减少灰色背景露出
  background: #fff;
  border-radius: 20px; // 更大的圆角
  padding: 24px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  position: relative;
  z-index: 2;
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid #F5F5F5;
    
    .statue-title {
      flex: 1;
      margin: 0;
      font-size: 26px;
      font-weight: 800;
      color: #1a1a1a;
      display: flex;
      align-items: center;
      gap: 10px;
      line-height: 1.3;
      
      .title-icon {
        font-size: 32px;
      }
    }
  }
  
  .section {
    margin-bottom: 32px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .section-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 17px;
      font-weight: 700;
      color: #1a1a1a;
      margin-bottom: 14px;
      
      .van-icon {
        color: #1989fa;
        font-size: 18px;
      }
      
      .view-map-btn {
        font-size: 12px;
        color: #1989fa;
        border: 1px solid #1989fa;
        padding: 2px 8px;
        border-radius: 4px;
        margin-left: auto;
        cursor: pointer;
        transition: all 0.3s;
        font-weight: normal;
        
        &:active {
          background: rgba(25, 137, 250, 0.1);
        }
      }
    }
    
    .section-content {
      margin: 0;
      font-size: 15px;
      line-height: 1.75;
      color: #555;
      text-align: justify;
      letter-spacing: 0.5px;
    }
    
    .location-info {
      background: #F9FAFB;
      border-radius: 12px;
      padding: 16px;
      
      .info-row {
        display: flex;
        font-size: 14px;
        margin-bottom: 10px;
        align-items: baseline;
        
        &:last-child {
          margin-bottom: 0;
        }
        
        .label {
          color: #858B9C;
          min-width: 70px;
        }
        
        .value {
          flex: 1;
          color: #333;
          font-weight: 500;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
      }
    }
    
    .map-container {
      margin-top: 16px;
      border-radius: 12px;
      overflow: hidden;
      border: 1px solid #EAEAEA;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
      
      #amap-container {
        width: 100%;
        height: 240px;
      }
    }
  }
}

.bottom-spacer {
  height: 40px;
}

.action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 20px 30px; // 适配 iPhone 底部
  background: #fff;
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.05);
  z-index: 100;
  
  .van-button {
    height: 50px;
    font-size: 17px;
    font-weight: 600;
    border: none;
    box-shadow: 0 4px 12px rgba(25, 137, 250, 0.3);
    background: linear-gradient(135deg, #1989fa 0%, #0570db 100%);
    transition: all 0.3s;
    
    &:active {
      transform: scale(0.98);
      box-shadow: 0 2px 6px rgba(25, 137, 250, 0.2);
    }
    
    &.van-button--default {
      background: #F5F7FA;
      color: #909399;
      box-shadow: none;
    }
    
    .van-icon {
      margin-right: 8px;
      font-size: 20px;
    }
  }
}
</style>
