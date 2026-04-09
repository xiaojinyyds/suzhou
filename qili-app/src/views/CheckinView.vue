<template>
  <div class="checkin-page">
    <!-- 顶部Header -->
    <header class="top-card">
      <h1 class="header-title">打卡地图</h1>
      <span class="progress-badge" @click="resetCheckin" style="cursor:pointer">
        {{ doneCount }}/7
      </span>
    </header>

    <!-- 主引导 -->
    <div class="map-main-tip">点击地图上的圆点开始打卡 <br>完成3个点可解锁刮彩票</div>

    <!-- 地图容器 -->
    <div class="map-outer">
      <div
        class="map-inner"
        ref="mapInner"
        :style="mapStyle"
        @mousedown="onDragStart"
        @touchstart="onTouchStart"
        @touchmove="onTouchMove"
        @touchend="onTouchEnd"
      >
        <!-- 底图 -->
        <img
          class="map-base"
          src="@/assets/checkin/map-full.png"
          alt="地图"
          draggable="false"
        />

        <!-- 7张碎片叠加，默认灰色，打卡后彩色 -->
        <img
          v-for="spot in spots"
          :key="spot.id"
          :src="spot.src"
          class="map-fragment"
          :class="{ 'is-done': spot.done }"
          draggable="false"
        />

        <!-- 可点击热点（狸猫位置） -->
        <div
          v-for="spot in spots"
          :key="'pin-' + spot.id"
          class="map-pin"
          :class="{ 'map-pin--highlight': shouldHighlightSpot(spot) }"
          :style="{ top: spot.pinY + '%', left: spot.pinX + '%' }"
          @click="openDetail(spot)"
        >
          <div
            class="pin-dot"
            :class="{ 'pin-dot--done': spot.done, 'pin-dot--explode': spot.exploding }"
            :style="
              spot.done
                ? {
                    background: `radial-gradient(circle at 35% 35%, ${spot.color}cc, ${spot.color})`,
                    borderColor: spot.color,
                  }
                : {}
            "
          ></div>

          <span class="pin-label">{{ spot.name }}</span>

          <!-- 首个点位的小标签 -->
          <span
            v-if="shouldHighlightSpot(spot)"
            class="pin-guide-tag"
          >
            从这里开始
          </span>

          <div class="burst" v-if="spot.exploding">
            <span
              v-for="i in 8"
              :key="i"
              class="burst-star"
              :style="{ '--i': i }"
            >✦</span>
          </div>
        </div>
      </div>

      <!-- 刮彩票入口 -->
      <transition name="pop">
        <div
          class="scratch-unlock-bar"
          v-if="scratchUnlocked"
          @click="$router.push({ name: 'scratch' })"
        >
          
          <div class="unlock-text">
            <span class="unlock-title">刮彩票已解锁</span>
            <span class="unlock-sub">点击领取奖励 →</span>
          </div>
        </div>
      </transition>
    </div>

    <!-- 底部详情卡片 -->
    <transition name="slide-up">
      <div class="detail-sheet" v-if="selected">
        <button class="sheet-close" @click="selected = null">✕</button>

        <div class="sheet-stars">
          <span
            v-for="i in 7"
            :key="i"
            class="sheet-star"
            :style="{ animationDelay: i * 0.12 + 's' }"
          >✦</span>
        </div>

        <div class="sheet-content">
          <div class="photo-wrap">
            <img
              v-if="selected.photo"
              :src="selected.photo"
              class="spot-photo"
              alt="现场照片"
            />
            <div v-else class="photo-placeholder">
              <span>📸 现场石像照片</span>
            </div>
          </div>

          <div class="sheet-info">
            <h2 class="sheet-name">{{ selected.name }}</h2>
            <p class="sheet-address">📍 {{ selected.address }}</p>
            <p class="sheet-desc">{{ selected.desc }}</p>
          </div>

          <div class="gps-status" :class="gpsStatusClass">
            {{ gpsStatusText }}
          </div>

          <div class="sheet-actions">
            <button class="btn-cancel" @click="selected = null">关闭</button>
            <button
              class="btn-checkin"
              :disabled="selected.done || !canCheckin"
              @click="doCheckin"
            >
              {{ selected.done ? '已打卡 ✓' : '确认打卡' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- 打卡成功提示 -->
    <transition name="pop">
      <div class="success-toast" v-if="showSuccess">
        {{ successName }} 打卡成功
      </div>
    </transition>
    <transition name="pop">
  <div class="help-overlay" v-if="showHelp" @click="showHelp = false">
    <div class="help-card" @click.stop>
      <h3 class="help-title">打卡规则</h3>
      <div class="help-list">
        <div>1. 点击地图圆点查看景点</div>
        <div>2. 距离景点 10000 米内点击“确认打卡”即可成功</div>
        <div>3. 打卡成功后，对应区域会由灰变彩</div>
        <div>4. 完成3处打卡可获得一次刮彩票机会</div>
        <div>5. 中奖后需完成全部打卡，方可在终点领取奖品</div>
      </div>
      <button class="help-close-btn" @click="showHelp = false">知道了</button>
    </div>
  </div>
</transition>

    <!-- 首次解锁刮彩票弹窗 -->
    <transition name="pop">
      <div class="scratch-overlay" v-if="showScratch">
        <div class="scratch-card">
          <h3 class="scratch-title">已完成 3/7 打卡</h3>
          <p class="scratch-desc">
            刮彩票奖励已解锁<br />
            <span>地图右上角可随时进入</span>
          </p>
          <div class="scratch-actions">
            <button class="scratch-btn-skip" @click="closeScratch">稍后再去</button>
            <button
              class="scratch-btn-go"
              @click="$router.push({ name: 'scratch' }); closeScratch()"
            >
              去刮卡 →
            </button>
          </div>
        </div>
      </div>
    </transition>
    <button class="help-chip" @click="showHelp = true">
     规则说明
    </button>
    <!-- Tab Bar -->
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
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, onMounted, onActivated } from 'vue'
import { useRouter } from 'vue-router'
import { Home, MapPin, Camera, ShoppingCart, User } from 'lucide-vue-next'
import { get, post } from '@/utils/request'
import { showToast } from '@/utils/toast'

const router = useRouter()

// ---- 打卡点数据 ----
const savedDone = JSON.parse(localStorage.getItem('checkin-done') || '[]')
const spots = ref([
  {
    id: 'fenshui',
    name: '分水狸',
    color: '#4297e6',
    photo: new URL('@/assets/checkin/photo-fenshui.jpg', import.meta.url).href,
    src: new URL('@/assets/checkin/map-fenshui.png', import.meta.url).href,
    pinX: 32,
    pinY: 16,
    address: '中国江苏省苏州市姑苏区西山庙桥（山塘街西）',
    desc: '分水狸守护着古运河的分流之处，传说能保佑旅人平安。',
    lat: 31.335581,
    lng: 120.573329,
    done: savedDone.includes('fenshui'),
    exploding: false,
  },
  {
    id: 'haiyong',
    name: '海涌狸',
    color: '#eb8392',
    src: new URL('@/assets/checkin/map-haiyong.png', import.meta.url).href,
    photo: new URL('@/assets/checkin/photo-haiyong.jpg', import.meta.url).href,
    pinX: 40,
    pinY: 27,
    address: '中国江苏省苏州市虎丘山风景名胜区（山塘街）',
    desc: '海涌狸镇守运河涌潮之地，是水乡的守护神。',
    lat: 31.334761,
    lng: 120.575063,
    done: savedDone.includes('haiyong'),
    exploding: false,
  },
  {
    id: 'baigong',
    name: '白公狸',
    color: '#9ce75b',
    src: new URL('@/assets/checkin/map-baigong.png', import.meta.url).href,
    photo: new URL('@/assets/checkin/photo-baigong.jpg', import.meta.url).href,
    pinX: 50,
    pinY: 43,
    address: '白公桥附近',
    desc: '白公狸是七狸中最年长的，传授古老的水利智慧。',
    lat: 30.002,
    lng: 120.002,
    done: savedDone.includes('baigong'),
    exploding: false,
  },
  {
    id: 'caiyun',
    name: '彩云狸',
    color: '#ee5c30',
    src: new URL('@/assets/checkin/map-caiyun.png', import.meta.url).href,
    photo: new URL('@/assets/checkin/photo-caiyun.jpg', import.meta.url).href,
    pinX: 54,
    pinY: 58,
    address: '中国江苏省苏州市姑苏区虎丘景区彩云桥东（山塘街）',
    desc: '彩云狸能预报天气，晴天时身上的颜色最为鲜艳。',
    lat: 31.327672,
    lng: 120.586627,
    done: savedDone.includes('caiyun'),
    exploding: false,
  },
  {
    id: 'wenchang',
    name: '文昌狸',
    color: '#4ee8bc',
    src: new URL('@/assets/checkin/map-wenchang.png', import.meta.url).href,
    photo: new URL('@/assets/checkin/photo-wenchang.jpg', import.meta.url).href,
    pinX: 62,
    pinY: 68,
    address: '中国江苏省苏州市姑苏区星桥东南（山塘街南）',
    desc: '文昌狸掌管文运，学子们常来此祈求金榜题名。',
    lat: 31.322563,
    lng: 120.594519,
    done: savedDone.includes('wenchang'),
    exploding: false,
  },
  {
    id: 'tonggui',
    name: '通贵狸',
    color: '#e8934a',
    src: new URL('@/assets/checkin/map-tonggui.png', import.meta.url).href,
    photo: new URL('@/assets/checkin/photo-tonggui.jpg', import.meta.url).href,
    pinX: 75,
    pinY: 77,
    address: '中国江苏省苏州市七里山塘景区',
    desc: '通贵狸象征富贵吉祥，全身金色鳞甲闪闪发光。',
    lat: 31.318288,
    lng: 120.599361,
    done: savedDone.includes('tonggui'),
    exploding: false,
  },
  {
    id: 'meiren',
    name: '美仁狸',
    color: '#8ebde9',
    src: new URL('@/assets/checkin/map-meiren.png', import.meta.url).href,
    photo: new URL('@/assets/checkin/photo-meiren.jpg', import.meta.url).href,
    pinX: 80,
    pinY: 85,
    address: '中国江苏省苏州市七里山塘景区（山塘街）',
    desc: '美仁狸是七狸中最温柔的，守护着这片水乡的美丽。',
    lat: 31.316192,
    lng: 120.603497,
    done: savedDone.includes('meiren'),
    exploding: false,
  },
])

const firstGuideSpotId = 'meiren'
const doneCount = computed(() => spots.value.filter((s) => s.done).length)
const scratchUnlocked = computed(() => doneCount.value >= 3)

function shouldHighlightSpot(spot) {
  return doneCount.value === 0 && spot.id === firstGuideSpotId
}

async function loadBackendData() {
  try {
    const statRes = await get('/api/v1/statues');
    const chkRes = await get('/api/v1/checkins/my');
    
    const backendStatues = statRes.data || [];
    const myCheckins = chkRes.data || [];

    spots.value.forEach(spot => {
      const bStatue = backendStatues.find(b => b.icon === spot.id);
      if (bStatue) {
        spot.backendId = bStatue.id;
        spot.lat = bStatue.latitude;
        spot.lng = bStatue.longitude;
        spot.desc = bStatue.introduction || spot.desc;
        
        // determine if checked in
        spot.done = myCheckins.some(c => c.statue_id === bStatue.id);
      }
    });

  } catch (err) {
    console.error("加载打卡数据失败", err);
  }
}

onMounted(() => {
  loadBackendData();
});
onActivated(() => {
  loadBackendData();
});

// ---- 地图拖拽/缩放 ----
const mapInner = ref(null)
const translateX = ref(0)
const translateY = ref(0)
const scale = ref(1)
const isDragging = ref(false)
let lastX = 0
let lastY = 0

const mapStyle = computed(() => ({
  transform: `translate(${translateX.value}px, ${translateY.value}px) scale(${scale.value})`,
  transformOrigin: '0 0',
  cursor: isDragging.value ? 'grabbing' : 'grab',
}))

function onDragStart(e) {
  isDragging.value = true
  lastX = e.clientX
  lastY = e.clientY
  window.addEventListener('mousemove', onDragMove)
  window.addEventListener('mouseup', onDragEnd)
}

function onDragMove(e) {
  if (!isDragging.value) return
  translateX.value += e.clientX - lastX
  translateY.value += e.clientY - lastY
  lastX = e.clientX
  lastY = e.clientY
}

function onDragEnd() {
  isDragging.value = false
  window.removeEventListener('mousemove', onDragMove)
  window.removeEventListener('mouseup', onDragEnd)
}

let lastPinchDist = 0

function onTouchStart(e) {
  if (e.touches.length === 1) {
    isDragging.value = true
    lastX = e.touches[0].clientX
    lastY = e.touches[0].clientY
  } else if (e.touches.length === 2) {
    lastPinchDist = getPinchDist(e)
  }
}

function onTouchMove(e) {
  e.preventDefault()
  if (e.touches.length === 1 && isDragging.value) {
    translateX.value += e.touches[0].clientX - lastX
    translateY.value += e.touches[0].clientY - lastY
    lastX = e.touches[0].clientX
    lastY = e.touches[0].clientY
  } else if (e.touches.length === 2) {
    const dist = getPinchDist(e)
    scale.value = Math.min(3, Math.max(0.5, (scale.value * dist) / lastPinchDist))
    lastPinchDist = dist
  }
}

function onTouchEnd() {
  isDragging.value = false
}

function getPinchDist(e) {
  const dx = e.touches[0].clientX - e.touches[1].clientX
  const dy = e.touches[0].clientY - e.touches[1].clientY
  return Math.sqrt(dx * dx + dy * dy)
}

// ---- 详情卡片 ----
const selected = ref(null)
const canCheckin = ref(false)
const gpsStatusText = ref('正在获取位置...')
const gpsStatusClass = ref('gps-checking')

function openDetail(spot) {
  selected.value = spot
  canCheckin.value = false
  gpsStatusText.value = '正在获取位置...'
  gpsStatusClass.value = 'gps-checking'
  checkGPS(spot)
}

const currentLat = ref(null)
const currentLng = ref(null)

function checkGPS() {
  canCheckin.value = false
  gpsStatusText.value = '正在定位您的真实位置...'
  gpsStatusClass.value = 'gps-checking'

  if (!navigator.geolocation) {
    gpsStatusText.value = '浏览器不支持定位权限，无法完成真实打卡'
    gpsStatusClass.value = 'gps-error'
    return
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      currentLat.value = position.coords.latitude
      currentLng.value = position.coords.longitude
      canCheckin.value = true
      gpsStatusText.value = '已获取定位，您可以尝试打卡'
      gpsStatusClass.value = 'gps-ok'
    },
    (err) => {
      let reason = err.message || '未知错误'
      if (err.code === 1) reason = '权限被拒绝'
      if (err.code === 2) reason = '无法获取位置'
      if (err.code === 3) reason = '获取超时'
      
      // 检测是否因为非 HTTPS 导致
      if (window.location.protocol === 'http:' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        reason = '必须使用HTTPS协议才能获取定位'
      }
      
      gpsStatusText.value = `定位失败: ${reason}`
      gpsStatusClass.value = 'gps-error'
    },
    { enableHighAccuracy: true, timeout: 8000, maximumAge: 0 }
  )
}

// ---- 打卡 ----
const showSuccess = ref(false)
const successName = ref('')
const showScratch = ref(false)
const showHelp = ref(false)

async function doCheckin() {
  if (!selected.value || selected.value.done) return;
  const spot = spots.value.find((s) => s.id === selected.value.id);
  if (!spot || !spot.backendId) {
    showToast("打卡点数据未就绪", "error");
    return;
  }

  showToast("打卡校验中...", "info", 1000);

  try {
    // 真实定位上传（抛弃作弊模式）
    const payload = {
      statue_id: spot.backendId,
      latitude: currentLat.value,
      longitude: currentLng.value
    };

    const res = await post('/api/v1/checkins', payload);
    
    if (res.data && res.data.success) {
      spot.done = true;
      spot.exploding = true;
      setTimeout(() => {
        spot.exploding = false;
      }, 800);

      successName.value = spot.name;
      selected.value = null;
      showSuccess.value = true;
      setTimeout(() => {
        showSuccess.value = false;
      }, 2500);

      if (spots.value.filter((s) => s.done).length === 3 && !localStorage.getItem('scratch-notified')) {
        setTimeout(() => {
          showScratch.value = true;
        }, 800);
      }
    } else {
      showToast(res.message || "打卡失败，不在范围内", "error");
    }
  } catch (err) {
    showToast(err.message || "打卡请求失败", "error");
  }
}

function resetCheckin() {
  showToast('正式版数据存储在服务端，无法直接清空哦', 'info')
}

function closeScratch() {
  showScratch.value = false
  localStorage.setItem('scratch-notified', '1')
}

onUnmounted(() => {
  window.removeEventListener('mousemove', onDragMove)
  window.removeEventListener('mouseup', onDragEnd)
})
</script>

<style scoped>
.checkin-page {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100dvh;
  background-color: #fffaf0;
  max-width: 430px;
  margin: 0 auto;
  overflow: hidden;
  font-family: 'Ma Shan Zheng', cursive;
}

/* Header */
.top-card {
  position: relative;
  background: var(--skin-primary);
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.12'/%3E%3C/svg%3E"),
    linear-gradient(
      135deg,
      rgba(255,255,255,0.18) 0%,
      transparent 50%,
      rgba(0,0,0,0.08) 100%
    );
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
  letter-spacing: 6px;
  color: #ffffff;
  margin: 0;
  text-shadow: 0 1px 3px rgba(0,0,0,0.15);
}

.progress-badge {
  position: absolute;
  right: 16px;
  background: rgba(76, 201, 163, 0.3);
  border: 1px solid rgba(56, 158, 141, 0.6);
  color: #fffaf0;
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 999px;
}

.map-main-tip {
  font-size: 13px;
  color: #64a18c;
  text-align: center;
  margin: 10px 0 6px;
  letter-spacing: 0.04em;
}

/* 地图容器 */
.map-outer {
  margin-top: -2px;
  flex: 1;
  overflow: hidden;
  position: relative;
  background: #fffaf0;
  touch-action: none;
}

.map-inner {
  position: relative;
  width: 100%;
  will-change: transform;
  user-select: none;
}

.map-base {
  width: 100%;
  display: block;
  pointer-events: none;
}

/* 碎片图 */
.map-fragment {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  pointer-events: none;
  filter: grayscale(100%) brightness(0.85);
  transition: filter 0.8s ease;
}

.map-fragment.is-done {
  filter: grayscale(0%) brightness(1);
  animation: fragment-pop 1.2s ease-in-out forwards;
}

@keyframes fragment-pop {
  0%   { transform: translateY(0px) scale(1); }
  30%  { transform: translateY(-6px) scale(1.015); }
  60%  { transform: translateY(2px) scale(0.995); }
  80%  { transform: translateY(-3px) scale(1.005); }
  100% { transform: translateY(0px) scale(1); }
}

/* 热点 */
.map-pin {
  position: absolute;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  cursor: pointer;
  z-index: 20;
}

.pin-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: rgba(150, 150, 150, 0.7);
  border: 2px solid #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.3);
  transition: background 0.5s, transform 0.2s;
}

.pin-dot--done {
  background: #3ae098;
  transform: scale(1.2);
}

.pin-label {
  font-size: 10px;
  color: #333;
  background: rgba(255, 255, 255, 0.75);
  padding: 1px 5px;
  border-radius: 4px;
  white-space: nowrap;
  backdrop-filter: blur(4px);
}

/* 首个引导点 */
.map-pin--highlight .pin-dot {
  animation: pinPulse 1s infinite alternate;
  box-shadow: 0 0 0 6px rgba(132, 251, 221, 0.18);
}

.pin-guide-tag {
  position: absolute;
  top: -18px;
  left: 18px;
  background: #fff6fb;
  color: #51a18b;
  border: 1px solid rgba(115, 164, 147, 0.95);
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 11px;
  line-height: 1;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

@keyframes pinPulse {
  0% {
    transform: scale(1);
    opacity: 0.75;
  }
  100% {
    transform: scale(1.22);
    opacity: 1;
  }
}

/* 右上角刮彩票入口 */
.scratch-unlock-bar {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 50;
  background: rgba(216, 225, 222, 0.9);
  border: 1.5px solid rgba(132, 251, 221, 0.265);
  border-radius: 0 0 28px 28px;
  padding: 8px 12px 8px 10px;
  display: flex;
  align-items: center;
  gap: 7px;
  cursor: pointer;
 
  
  transition: transform 0.18s;
}

.scratch-unlock-bar:active {
  transform: scale(0.96);
}



.unlock-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.unlock-title {
  font-size: 0.70rem;
  color: #37715e;
  font-weight: 700;
  letter-spacing: 0.06em;
  white-space: nowrap;
}

.unlock-sub {
  font-size: 0.56rem;
  color: #4e6e67;
  white-space: nowrap;
  letter-spacing: 0.04em;
}

@keyframes gentle-pulse {
  0%,100% { box-shadow: 0 4px 16px rgba(171, 225, 210, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.9); }
  50%     { box-shadow: 0 4px 22px rgba(181, 255, 239, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.9); }
}
/* 规则说明按钮：放在刮彩票下面，弱入口 */
.help-chip {
  position: absolute;
  top: 66px;              /* 在刮彩票下面 */
  right: 12px;
  z-index: 50;

  height: 28px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid rgba(132, 251, 199, 0.148);
  background: rgba(216, 225, 222, 0.9);
  color: #456d5d;
  font-size: 12px;
  font-family: inherit;
  cursor: pointer;

  box-shadow: 0 3px 10px rgba(132, 251, 213, 0.1);
  backdrop-filter: blur(8px);
}

.help-chip:active {
  transform: scale(0.96);
}

/* 规则说明弹窗 */
.help-overlay {
  position: absolute;
  inset: 0;
  background: rgba(40, 60, 56, 0.18);
  backdrop-filter: blur(6px);
  z-index: 380;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.help-card {
  width: 88%;
  max-width: 310px;
  background: linear-gradient(180deg, #fdfdf4 0%, #f2f1eb 100%);
  border: 1.5px solid rgba(93, 184, 176, 0.35);
  border-radius: 24px;
  box-shadow:
    0 16px 40px rgba(132, 251, 211, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  padding: 24px 20px 18px;
}

.help-title {
  margin: 0 0 12px;
  text-align: center;
  font-size: 1.1rem;
  color: #44a583;
  letter-spacing: 0.08em;
}

.help-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 0.76rem;
  line-height: 1.75;
  color: #5e8a7c;
}

.help-close-btn {
  margin-top: 16px;
  width: 100%;
  padding: 11px 0;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #67c5ab 0%, #369e84 100%);
  color: #fff;
  font-size: 0.9rem;
  font-family: inherit;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 0.08em;
  box-shadow: 0 5px 16px rgba(132, 251, 215, 0.3);
}

.help-close-btn:active {
  opacity: 0.88;
}
/* 底部详情卡片 */
.detail-sheet {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  background: linear-gradient(180deg, #fffcfe 0%, #fffaf0 100%);
  border-radius: 24px 24px 0 0;
  border-top: 1.5px solid rgba(132, 251, 223, 0.3);
  box-shadow: 0 -6px 32px rgba(132, 251, 221, 0.14);
  z-index: 200;
  padding-bottom: env(safe-area-inset-bottom);
}

.sheet-close {
  position: absolute;
  top: 14px;
  left: 16px;
  width: 30px;
  height: 30px;
  background: #d7e7e1;
  border: 1px solid rgba(132, 251, 213, 0.35);
  border-radius: 50%;
  color: #60c09a;
  font-size: 0.78rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  transition: background 0.18s;
}

.sheet-close:active {
  background: #b7dbd4;
}

.sheet-stars {
  display: flex;
  justify-content: center;
  gap: 8px;
  padding: 16px 0 4px;
}

.sheet-star {
  font-size: 0.58rem;
  color: #5cb394;
  animation: sheetStarPulse 1.8s ease-in-out infinite;
  opacity: 0.6;
}

@keyframes sheetStarPulse {
  0%,100% { opacity: 0.30; transform: scale(0.8); }
  50%     { opacity: 1;    transform: scale(1.25); }
}

.sheet-content {
  padding: 8px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.photo-wrap {
  border-radius: 16px;
  overflow: hidden;
  max-height: 200px;
  box-shadow: 0 3px 14px rgba(132, 251, 233, 0.12);
}

.spot-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.photo-placeholder {
  background: #fffaf0;
  border: 1px dashed rgba(132, 251, 213, 0.5);
  border-radius: 16px;
  height: 130px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #80c0b0;
  font-size: 14px;
}

.sheet-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.sheet-name {
  font-size: 1.2rem;
  color: #2a5a4e;
  margin: 0;
  letter-spacing: 0.10em;
  font-weight: 800;
}

.sheet-address {
  font-size: 0.72rem;
  color: #70a095;
  margin: 0;
  letter-spacing: 0.03em;
}

.sheet-desc {
  font-size: 0.72rem;
  color: #507a70;
  line-height: 1.75;
  margin: 0;
}

.gps-status {
  font-size: 0.68rem;
  padding: 7px 14px;
  border-radius: 10px;
  text-align: center;
  letter-spacing: 0.04em;
}

.gps-checking { background: #f4f8f7; color: #aaaaaa; }
.gps-ok       { background: #f4f8f7; color: #53a48e; border: 1px solid rgba(132, 251, 223, 0.25); }
.gps-far      { background: #f4f8f7; color: #2f7fdc; }

.sheet-actions {
  display: flex;
  gap: 10px;
}

.btn-cancel {
  flex: 1;
  padding: 12px;
  border-radius: 14px;
  border: 1.5px solid rgba(132, 251, 229, 0.35);
  background: transparent;
  color: #80b0a1;
  font-size: 0.9rem;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.18s;
}

.btn-cancel:active {
  background: #fffaf0;
}

.btn-checkin {
  flex: 2;
  padding: 12px;
  border-radius: 14px;
  border: none;
  background: linear-gradient(135deg, #4b917e 0%, #45a68f 100%);
  color: #fffaf0;
  font-size: 0.9rem;
  font-family: inherit;
  font-weight: 700;
  cursor: pointer;
  letter-spacing: 0.10em;
  box-shadow: 0 4px 14px rgba(132, 251, 227, 0.38);
  transition: opacity 0.2s;
}

.btn-checkin:disabled {
  background: linear-gradient(135deg, #8eb4ad, #8abcb6);
  box-shadow: none;
  cursor: not-allowed;
  opacity: 0.6;
}

/* 成功提示 */
.success-toast {
  position: fixed;
  top: 120px;
  left: 50%;
  transform: translateX(-50%);
  background: #7ccfb2;
  color: #f2f8f8;
  padding: 10px 28px;
  border-radius: 999px;
  font-size: 15px;
  z-index: 999;
  border: 1px solid rgba(76, 201, 184, 0.5);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  white-space: nowrap;
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

.tab-item--active {
  opacity: 1;
}

.tab-label {
  font-size: 11px;
  color: #688e37;
}

/* 爆炸粒子 */
.pin-dot--explode {
  animation: explode 0.6s ease-out forwards;
}

@keyframes explode {
  0%   { transform: scale(1); box-shadow: 0 0 0 0 rgba(53, 202, 145, 0.8); }
  40%  { transform: scale(1.8); box-shadow: 0 0 0 12px rgba(58, 224, 185, 0.3); }
  70%  { transform: scale(1.4); box-shadow: 0 0 0 20px rgba(224, 90, 58, 0); }
  100% { transform: scale(1.2); box-shadow: 0 0 0 0 rgba(224, 90, 58, 0); }
}

.burst {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 20;
}

.burst-star {
  position: absolute;
  font-size: 12px;
  color: #9ddcc9;
  text-shadow: 0 0 4px rgba(76, 201, 176, 0.8);
  animation: burst-fly 0.7s ease-out forwards;
  --angle: calc((var(--i) - 1) * 45deg);
  transform-origin: center;
}

@keyframes burst-fly {
  0%   { opacity: 1; transform: rotate(var(--angle)) translateY(0px) scale(0.5); }
  60%  { opacity: 1; transform: rotate(var(--angle)) translateY(-28px) scale(1.2); }
  100% { opacity: 0; transform: rotate(var(--angle)) translateY(-40px) scale(0.6); }
}

/* 刮彩票首次弹窗 */
.scratch-overlay {
  position: absolute;
  inset: 0;
  backdrop-filter: blur(6px);
  z-index: 400;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.scratch-card {
  background: rgba(231, 241, 238, 0.9);
  border-radius: 26px;
  padding: 28px 24px 22px;
  max-width: 300px;
  width: 88%;
  text-align: center;
  border: 1.5px solid rgba(85, 171, 138, 0.669);
  box-shadow:
    0 16px 40px rgba(132, 251, 231, 0.22),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.scratch-card::before {
  content: '✿  ✿  ✿  ✿  ✿  ✿  ✿';
  display: block;
  font-size: 0.58rem;
  color: #44af8f;
  letter-spacing: 0.15em;
  opacity: 0.7;
  animation: dotWave 2.4s ease-in-out infinite;
}

@keyframes dotWave {
  0%,100% { opacity: 0.25; }
  50%     { opacity: 0.90; }
}

.scratch-title {
  font-size: 1.3rem;
  color: #318e6f;
  margin: 3px;
  letter-spacing: 0.12em;
  font-weight: 800;
  font-family: 'Ma Shan Zheng', cursive;
  text-shadow: 0 1px 4px rgba(132, 251, 215, 0.2);
}

.scratch-desc {
  font-size: 0.76rem;
  color: #55907f;
  line-height: 1.9;
  margin: 0;
}

.scratch-desc span {
  color: #48b38c;
  font-size: 0.68rem;
}

.scratch-actions {
  display: flex;
  gap: 10px;
  width: 100%;
  margin-top: 6px;
}

.scratch-btn-skip {
  flex: 1;
  padding: 12px;
  border-radius: 14px;
  border: 2px solid rgba(109, 209, 177, 0.3);
  background: transparent;
  color: #94cdba;
  font-size: 0.86rem;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.18s;
}

.scratch-btn-skip:active {
  background: #f3fcf9;
}

.scratch-btn-go {
  flex: 2;
  padding: 12px;
  border-radius: 14px;
  border: none;
  background: linear-gradient(135deg, #3c967e 0%, #3aad85 100%);
  color: #fff;
  font-size: 0.90rem;
  font-family: inherit;
  font-weight: 700;
  letter-spacing: 0.10em;
  cursor: pointer;
  box-shadow: 0 5px 16px rgba(132, 251, 221, 0.4);
  transition: opacity 0.2s;
}

.scratch-btn-go:active {
  opacity: 0.88;
}

/* 动画 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.35s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateX(-50%) translateY(100%);
}

.pop-enter-active,
.pop-leave-active {
  transition: all 0.3s ease;
}

.pop-enter-from,
.pop-leave-to {
  opacity: 0;
  transform: scale(0.8);
}
</style>
