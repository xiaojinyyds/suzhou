<template>
  <div class="merch-page">
    <!-- 顶部 Header -->
    <header class="top-card">
      <h1 class="header-title">狸趣周边</h1>
    </header>

    <!-- 图层叠加画布 -->
    <div class="canvas-wrapper">
      <!-- ① 女孩层 -->
      <img
        :src="decorLayers.find(d => d.key === 'girl').src"
        class="layer girl-layer"
        :style="girlStyle"
      />

      <!-- ② 台灯层 -->
      <img
        :src="isLightOn
          ? decorLayers.find(d => d.key === 'light').src
          : decorLayers.find(d => d.key === 'lightOff').src"
        class="layer light-layer"
        :style="lightStyle"
        @click="isLightOn = !isLightOn"
        style="cursor: pointer; pointer-events: auto;"
      />

      <!-- ④ 引导语 -->
      <div class="hint-badge">
        <span class="hint-text">点击下方周边名字<br>了解详情</span>
      </div>

      <!-- ③ 日历 + 所有普通商品 -->
      <div class="merch-group" :style="merchGroupStyle">
        <!-- 日历底图 -->
        <img
          :src="decorLayers.find(d => d.key === 'calendar').src"
          class="layer decor-layer"
        />

        <!-- 普通商品视觉图层，不包含隐藏的打卡棒 -->
        <img
          v-for="product in displayProducts"
          :key="product.id"
          :src="product.layerSrc"
          class="layer product-layer"
          style="pointer-events: none;"
          :class="{ 'is-active': activeProduct?.sourceId === product.id || activeProduct?.id === product.id }"
        />

        <!-- 普通热区 -->
        <div
          v-for="product in displayProducts"
          :key="'zone-' + product.id"
          :style="{
            position: 'absolute',
            cursor: 'pointer',
            zIndex: 5,
            top: product.hotspot.top + '%',
            left: product.hotspot.left + '%',
            width: product.hotspot.width + '%',
            height: product.hotspot.height + '%',
            background: debugMode ? product.debugColor : 'transparent',
          }"
          @click="openDrawer(product)"
        ></div>
      </div>
    </div>

    <!-- 遮罩 -->
    <Transition name="fade">
      <div v-if="drawerOpen" class="overlay" @click="closeDrawer"></div>
    </Transition>

    <!-- 底部抽屉 -->
    <Transition name="drawer">
      <div v-if="drawerOpen && activeProduct" class="drawer">
        <div class="drawer-handle" @click="closeDrawer">
          <span class="handle-bar"></span>
        </div>

        <div class="product-image-wrap">
          <img
            :src="activeProduct.detailSrc"
            :alt="activeProduct.name"
            class="product-detail-img"
          />
        </div>

        <div class="product-info">
          <div class="product-header">
            <h2 class="product-name">{{ activeProduct.name }}</h2>
            <span class="product-badge">{{ activeProduct.badge }}</span>
          </div>

          <p class="product-likes">❤️ 已有 {{ activeProduct.likes }} 人喜欢</p>
          <p class="product-desc">{{ activeProduct.desc }}</p>

          <button class="buy-btn" @click="handleBuy(activeProduct)">
            <span class="btn-text">立即预约</span>
            <span class="btn-arrow">→</span>
          </button>
        </div>
      </div>
    </Transition>

    <!-- 底部 TabBar -->
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Home, MapPin, Camera, ShoppingCart, User } from 'lucide-vue-next'
import { post } from '@/utils/request'
import { showToast } from '@/utils/toast'

const router = useRouter()
const activeTab = ref('merch')

/* 独立调整区 */
const girlConfig = ref({
  width: 65,
  bottom: 28,
  left: 40,
})

const lightConfig = ref({
  width: 60,
  top: 0,
  right: 10,
})

const merchConfig = ref({
  scale: 1,
  offsetX: 0,
  offsetY: -120,
})

/* 热区调试 */
const debugMode = ref(false)

const isLightOn = ref(true)

const girlStyle = computed(() => ({
  width: `${girlConfig.value.width}%`,
  bottom: `${girlConfig.value.bottom}%`,
  left: `${girlConfig.value.left}%`,
  top: 'auto',
  right: 'auto',
  transform: 'translateX(-50%)',
  height: 'auto',
  objectFit: 'contain',
}))

const lightStyle = computed(() => ({
  width: `${lightConfig.value.width}%`,
  top: `${lightConfig.value.top}%`,
  right: `${lightConfig.value.right}%`,
  left: 'auto',
  bottom: 'auto',
  height: 'auto',
  objectFit: 'contain',
}))

const merchGroupStyle = computed(() => ({
  transform: `translate(${merchConfig.value.offsetX}px, ${merchConfig.value.offsetY}px) scale(${merchConfig.value.scale})`,
  transformOrigin: 'center bottom',
}))

const decorLayers = [
  { key: 'calendar', src: new URL('@/assets/merch/日历.png', import.meta.url).href },
  { key: 'girl', src: new URL('@/assets/merch/女孩.png', import.meta.url).href },
  { key: 'light', src: new URL('@/assets/merch/开灯.png', import.meta.url).href },
  { key: 'lightOff', src: new URL('@/assets/merch/关灯.png', import.meta.url).href },
]

/* 普通展示商品 */
const products = ref([
  {
    id: 'doll',
    name: '今日大吉 · 娃娃',
    badge: '限定',
    desc: '以狸猫为原型设计的软萌公仔，有磁吸毛绒配件，随身携带好运气。毛绒材质，适合随身携带。',
    layerSrc: new URL('@/assets/merch/娃娃.png', import.meta.url).href,
    detailSrc: new URL('@/assets/merch/娃娃.jpg', import.meta.url).href,
    debugColor: 'rgba(0,200,0,0.4)',
    hotspot: { top: 61, left: 30, width: 40, height: 10 },
    likes: 128,
  },
  {
    id: 'towel',
    name: '清颜 · 擦脸巾',
    badge: '日用',
    desc: '纯棉一次性洗脸巾，柔软亲肤，印有狸猫图案，让日常洁面仪式感满满。',
    layerSrc: new URL('@/assets/merch/擦脸巾.png', import.meta.url).href,
    detailSrc: new URL('@/assets/merch/擦脸巾实物.png', import.meta.url).href,
    debugColor: 'rgba(255,0,255,0.4)',
    hotspot: { top: 71, left: 30, width: 20, height: 10 },
    likes: 128,
  },
  {
    id: 'dish',
    name: '豆皿',
    badge: '生活',
    desc: '小巧精致的陶瓷豆皿，可用于放置首饰、零食或作为摆件装饰案头，狸猫图案釉下彩工艺。',
    layerSrc: new URL('@/assets/merch/豆皿.png', import.meta.url).href,
    detailSrc: new URL('@/assets/merch/豆皿实物.png', import.meta.url).href,
    debugColor: 'rgba(0,255,255,0.4)',
    hotspot: { top: 71, left: 50, width: 20, height: 10 },
    likes: 128,
  },
  {
    id: 'tail',
    name: '晃尾巴',
    badge: '挂件',
    desc: '仿真毛绒狸猫尾巴挂件，轻轻一碰便会摇摆，挂包上随步伐律动，萌系十足。',
    layerSrc: new URL('@/assets/merch/晃尾巴.png', import.meta.url).href,
    detailSrc: new URL('@/assets/merch/晃尾巴实物.png', import.meta.url).href,
    debugColor: 'rgba(255,165,0,0.4)',
    hotspot: { top: 61, left: 70, width: 20, height: 20 },
    likes: 73,
  },
  {
    id: 'wallet',
    name: '零钱包',
    badge: '配件',
    desc: '圆润可爱的零钱小包，内里大容量，印有¥印章图案，装满零钱装满好运。',
    layerSrc: new URL('@/assets/merch/零钱包.png', import.meta.url).href,
    detailSrc: new URL('@/assets/merch/零钱包实物.png', import.meta.url).href,
    debugColor: 'rgba(0,0,255,0.4)',
    hotspot: { top: 61, left: 10, width: 20, height: 20 },
    likes: 98,
  },
  {
    id: 'wood',
    name: '木头挂件',
    badge: '文创',
    desc: '原木激光雕刻狸猫挂件，纹理自然，手感温润，背面可定制刻字，送礼自留两相宜。',
    layerSrc: new URL('@/assets/merch/木头挂件.png', import.meta.url).href,
    detailSrc: new URL('@/assets/merch/木头挂件实物.png', import.meta.url).href,
    debugColor: 'rgba(255,0,0,0.4)',
    hotspot: { top: 56, left: 30, width: 40, height: 5 },
    likes: 38,
  },
  {
    id: 'pillow',
    name: '充绵包',
    badge: '限定',
    desc: '柔软蓬松的随身小包，手感轻软，适合日常收纳，也适合作为可爱摆件。',
    layerSrc: new URL('@/assets/merch/充棉包.png', import.meta.url).href,
    detailSrc: new URL('@/assets/merch/充棉包实物.png', import.meta.url).href,
    debugColor: 'rgba(255,255,0,0.4)',
    hotspot: { top: 54, left: 10, width: 20, height: 5 },
    likes: 128,
  },
  {
    id: 'gacha',
    name: '抽一发',
    badge: '限定',
    desc: '点击后随机抽取一款隐藏或普通周边，看看今天和哪只狸最有缘。',
    layerSrc: new URL('@/assets/merch/抽一发.png', import.meta.url).href,
    detailSrc: new URL('@/assets/merch/打卡棒.jpg', import.meta.url).href,
    debugColor: 'rgba(128,0,128,0.4)',
    hotspot: { top: 54, left: 70, width: 20, height: 5 },
    likes: 66,
  },
])

/* 隐藏商品：不展示在普通组件里，只参与抽一发 */
const hiddenGachaItems = [
  {
    id: 'stamp-stick',
    name: '打卡棒',
    badge: '隐藏款',
    desc: '可以带着抽中的角色一起打卡，是只有在抽一发中才会出现的隐藏纪念款。',
    detailSrc: new URL('@/assets/merch/打卡棒.jpg', import.meta.url).href,
    likes: 88,
  },
]

/* 页面上真正显示的商品：全部普通商品 */
const displayProducts = computed(() => products.value)

/* 抽一发奖池：普通商品里除去 gacha 自身，再加隐藏打卡棒 */
const gachaPool = computed(() => {
  const normalItems = products.value
    .filter(item => item.id !== 'gacha')
    .map(item => ({
      ...item,
      sourceId: item.id,
    }))

  const hiddenItems = hiddenGachaItems.map(item => ({
    ...item,
    sourceId: item.id,
  }))

  return [...normalItems, ...hiddenItems]
})

const drawerOpen = ref(false)
const activeProduct = ref(null)

function openDrawer(product) {
  if (product.id === 'gacha') {
    const pool = gachaPool.value
    const randomIndex = Math.floor(Math.random() * pool.length)
    const randomProduct = pool[randomIndex]

    activeProduct.value = {
      ...randomProduct,
      name: `抽一发 · ${randomProduct.name}`,
      badge: randomProduct.badge === '隐藏款' ? '抽中隐藏款' : '抽中款',
      desc: `恭喜抽中了「${randomProduct.name}」！${randomProduct.desc}`,
    }
  } else {
    activeProduct.value = {
      ...product,
      sourceId: product.id,
    }
  }

  drawerOpen.value = true
}

function closeDrawer() {
  drawerOpen.value = false
  setTimeout(() => {
    activeProduct.value = null
  }, 360)
}

async function handleBuy(product) {
  const sourceId = product.id || product.sourceId
  try {
    await post('/api/v1/merch/orders', {
      product_id: sourceId,
      product_name: product.name
    })
    showToast('预约成功！可前往【我的 - 周边订单】处查看', 'success', 3000)
    closeDrawer()
  } catch (err) {
    showToast(err.message || '预约失败', 'error')
  }
}
</script>

<style scoped>
.merch-page {
  --font-title: 'Ma Shan Zheng', cursive;
  --font-body: 'ZCOOL XiaoWei', cursive;
  --color-bg: #fffdec;
  --color-header-bg: var(--skin-primary);
  --color-green-main: var(--skin-primary);
  --color-text-primary: #61b159;
  --color-text-secondary: #61b159;
  --color-text-on-green: #fffefb;

  display: flex;
  flex-direction: column;
  min-height: 100dvh;
  background-color: var(--color-bg);
  font-family: var(--font-title);
  max-width: 430px;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
}

.top-card {
  position: relative;
  background-color: var(--color-header-bg);
  border-radius: 0 0 28px 28px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1.5px solid rgb(143, 141, 116);
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)' opacity='0.12'/%3E%3C/svg%3E"),
    linear-gradient(135deg, rgba(255,255,255,0.18) 0%, transparent 50%, rgba(0,0,0,0.08) 100%);
  background-repeat: repeat, no-repeat;
  background-size: auto, 100% 100%;
  flex-shrink: 0;
}

.header-title {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: 6px;
  color: var(--color-text-on-green);
  margin: 0;
  text-shadow: 0 1px 3px rgba(0,0,0,0.15);
}



.canvas-wrapper {
  position: relative;
  width: 100%;
  flex: 1;
  min-height: 780px;
  overflow: visible;
  background: linear-gradient(to bottom, transparent 70%, var(--skin-primary) 100%);
}

.layer {
  position: absolute;
  display: block;
}

.girl-layer {
  width: 65%;
  bottom: 0;
  left: 45%;
  transform: translateX(-50%);
  height: auto;
  object-fit: contain;
  pointer-events: none;
  z-index: 3;
}

.light-layer {
  width: 28%;
  top: 0;
  right: 3%;
  height: auto;
  object-fit: contain;
  pointer-events: none;
  z-index: 4;
}

.merch-group {
  position: absolute;
  inset: 0;
  transform-origin: center bottom;
  z-index: 2;
}

.merch-group .layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: center bottom;
}

.decor-layer {
  pointer-events: none;
  z-index: 1;
}

.product-layer {
  pointer-events: none;
  z-index: 2;
  transition: filter 0.2s ease;
}

.product-layer.is-active {
  filter: brightness(1.2) drop-shadow(0 0 12px rgba(97, 177, 89, 0.7));
}

.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(3px);
  z-index: 10;
}

.drawer {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 430px;
  z-index: 20;
  background: var(--color-bg);
  border-top: 2px solid rgba(201, 168, 76, 0.5);
  border-radius: 20px 20px 0 0;
  padding: 0 0 80px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 -4px 30px rgba(74, 143, 111, 0.2);
}

.drawer-handle {
  display: flex;
  justify-content: center;
  padding: 14px 0 8px;
  cursor: pointer;
}

.handle-bar {
  width: 36px;
  height: 3px;
  background: rgba(201, 168, 76, 0.5);
  border-radius: 2px;
  display: block;
}

.product-image-wrap {
  width: 100%;
  padding: 16px 32px 8px;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
}

.product-detail-img {
  width: 55%;
  max-width: 200px;
  object-fit: contain;
  filter: drop-shadow(0 8px 20px rgba(74, 143, 111, 0.2));
}

.product-info {
  padding: 8px 24px 0;
}

.product-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.product-likes {
  font-size: 13px;
  color: #e07070;
  margin: 0 0 10px;
  font-family: var(--font-body);
}

.product-name {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-green-main);
  letter-spacing: 0.05em;
  margin: 0;
  font-family: var(--font-title);
}

.product-badge {
  font-size: 11px;
  color: var(--color-text-primary);
  border: 1px solid rgba(201, 168, 76, 0.6);
  border-radius: 4px;
  padding: 2px 7px;
  letter-spacing: 0.1em;
  font-family: var(--font-body);
}

.product-desc {
  font-size: 14px;
  color: #888;
  line-height: 1.75;
  margin: 0 0 20px;
  font-family: var(--font-body);
  letter-spacing: 0.03em;
}

.buy-btn {
  width: 100%;
  padding: 14px 0;
  background: var(--color-green-main);
  border: 1px solid rgba(201, 168, 76, 0.6);
  border-radius: 10px;
  color: var(--color-text-on-green);
  font-size: 15px;
  font-family: var(--font-title);
  letter-spacing: 0.15em;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.25s ease;
  box-shadow:
    0 3px 10px rgba(74, 143, 111, 0.3),
    inset 0 1px 0 rgba(255,255,255,0.2);
}

.buy-btn:active {
  transform: scale(0.98);
  opacity: 0.9;
}

.btn-arrow {
  font-size: 16px;
  transition: transform 0.2s;
}

.buy-btn:hover .btn-arrow {
  transform: translateX(4px);
}

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
  border-top: 1px solid rgba(201, 168, 76, 0.25);
  box-shadow:
    0 -1px 0 rgba(255,255,255,0.6),
    0 -8px 24px rgba(94, 193, 150, 0.12);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 8px 0 calc(8px + env(safe-area-inset-bottom));
  border-radius: 20px 20px 0 0;
  z-index: 100;
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  cursor: pointer;
  opacity: 0.55;
  transition: opacity 0.2s;
  flex: 1;
  color: #688e37;
}

.tab-item--active {
  opacity: 1;
}

.tab-label {
  font-size: 11px;
  color: #688e37;
  font-family: var(--font-body);
}

.hint-badge {
  position: absolute;
  top: 30%;
  right: 4%;
  z-index: 6;
  display: flex;
  align-items: center;
  gap: 5px;
  background: rgba(210, 210, 134, 0.12);
  border: 2px solid rgba(45, 88, 69, 0.35);
  border-radius: 20px;
  padding: 5px 12px 5px 8px;
  backdrop-filter: blur(4px);
  pointer-events: none;
}

.hint-text {
  font-family: var(--font-body);
  font-size: 14px;
  color: #4b7262;
  letter-spacing: 0.08em;
  white-space: nowrap;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.drawer-enter-active {
  transition: transform 0.36s cubic-bezier(0.22, 1, 0.36, 1);
}

.drawer-leave-active {
  transition: transform 0.28s cubic-bezier(0.55, 0, 1, 0.45);
}

.drawer-enter-from,
.drawer-leave-to {
  transform: translateX(-50%) translateY(100%);
}
</style>