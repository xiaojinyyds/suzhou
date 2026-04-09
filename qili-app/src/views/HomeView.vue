<template>
  <div class="home-page">
    <!-- 顶部 Header 卡片 -->
    <header class="top-card">
      <div class="header-deco header-deco--left">
        <img class="character-body" src="@/assets/images/身体-08.png" alt="" />
        <img class="character-tail" src="@/assets/images/尾巴-08.png" alt="" />
      </div>

      

      <h1 class="header-title">打卡七狸山塘</h1>

     <button class="profile-entry-btn" @click="goTo('my')">
      我的
     </button>
    </header>

    <!-- 主体滚动区域 -->
    <main class="main-content">
      
      

      

      <!-- 板块二：打卡进度 -->
      <section
        class="card progress-card"
        @click="goTo('checkin')"
        style="cursor: pointer;"
      >
        <div class="section-label">打卡3个点可解锁奖励</div>

        <div class="progress-block">
          <div class="progress-header">
            <span class="progress-title">当前打卡进度</span>
            <span class="progress-count">{{ todayDone }} / {{ todayTotal }}</span>
          </div>

          <div class="progress-bar-bg">
            <div class="progress-bar-fill" :style="{ width: progressPercent + '%' }" />
          </div>

          <div class="tag-list">
            <span
              v-for="(tag, i) in progressTags"
              :key="i"
              class="tag"
              :class="{ 'tag--done': tag.done }"
            >
              {{ tag.name }}
            </span>
          </div>
          <button class="progress-action-btn" @click.stop="goTo('checkin')">
           继续打卡
          </button>
        </div>
      </section>

      <!-- 板块三：功能入口 -->
      <section class="card function-card">
        <div class="section-label">功能入口</div>

        <div class="function-list">
          <div class="function-item" @click="goTo('checkin')">
            <img class="function-icon" src="@/assets/images/icon-checkin.png" alt="景点打卡" />
            <span class="function-name">打卡</span>
          </div>

          <div class="function-item" @click="goTo('photo')">
            <img class="function-icon" src="@/assets/images/icon-photo.png" alt="娃娃拍照" />
            <span class="function-name">娃娃拍照</span>
          </div>

          <div class="function-item" @click="goTo('merch')">
            <img class="function-icon" src="@/assets/images/icon-merch.png" alt="周边商品" />
            <span class="function-name">周边</span>
          </div>
        </div>
      </section>

      <!-- 板块一：玩游戏 知典故 -->
      <section class="card story-card">
        <div class="section-label">玩游戏知典故</div>
        <div class="story-image-wrap" @click="$router.push('/merge')" style="cursor: pointer;">
          <img
            class="story-image"
            src="@/assets/images/characters-group.png"
            alt="七只小狸角色"
          />
          <p class="story-image-caption">
            点击该区域解锁狸猫故事
          </p>
        </div>
      </section>
    </main>

    
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Home, MapPin, Camera, ShoppingCart, User } from 'lucide-vue-next'
import { ref, computed, onActivated, onMounted } from 'vue'
import { get } from '@/utils/request'

const router = useRouter()

const allSpots = ref([
  { id: 'fenshui', name: '分水狸' },
  { id: 'haiyong', name: '海涌狸' },
  { id: 'baigong', name: '白公狸' },
  { id: 'caiyun', name: '彩云狸' },
  { id: 'wenchang', name: '文昌狸' },
  { id: 'tonggui', name: '通贵狸' },
  { id: 'meiren', name: '美仁狸' },
])

const savedDoneIds = ref([])

const todayTotal = ref(7)
const todayDone = computed(() => savedDoneIds.value.length)
const progressPercent = computed(() => (todayDone.value / todayTotal.value) * 100)
const progressTags = computed(() =>
  allSpots.value.map((s) => ({
    name: s.name,
    done: savedDoneIds.value.includes(s.id),
  }))
)

function goTo(name) {
  router.push({ name })
}

async function fetchProgress() {
  try {
    const statRes = await get('/api/v1/statues')
    const chkRes = await get('/api/v1/checkins/my')
    
    const backendStatues = statRes.data || []
    const myCheckins = chkRes.data || []

    const doneIcons = []
    myCheckins.forEach(chk => {
      const match = backendStatues.find(s => s.id === chk.statue_id)
      if (match && match.icon) {
        doneIcons.push(match.icon)
      }
    })
    savedDoneIds.value = doneIcons
  } catch (e) {
    console.error("Failed to fetch checkin progress:", e)
  }
}

onMounted(() => {
  fetchProgress()
})

onActivated(() => {
  fetchProgress()
})
</script>

<style scoped>
.home-page {
  --font-title: 'Ma Shan Zheng', cursive;
  --font-body: 'ZCOOL XiaoWei', cursive;

  --color-bg: #fffaf0;         /* 奶油白 */
  --color-surface: #fffdf8;    /* 卡片白 */
  --color-surface-soft: #faf6ee;

  --color-header-bg: var(--skin-primary);
  --color-header-bg-2: var(--skin-primary-dark);
  --color-progress-bg: var(--skin-primary-dark);
  --color-progress-bg-2: var(--skin-primary);
  --story-wrap-bg: var(--skin-storywrap);

  --color-text-primary: #4b7262;
  --color-text-secondary: #7f857d;
  --color-text-on-blue: #fffefb;

  --color-line: rgba(205, 186, 126, 0.52);
  --color-line-soft: rgba(205, 186, 126, 0.28);
  --color-gold: #e7c86f;
  --color-gold-soft: #f6e6b1;

  display: flex;
  flex-direction: column;
  min-height: 100dvh;
  background-color: var(--color-bg);
  font-family: var(--font-title);
  max-width: 430px;
  margin: 0 auto;
  position: relative;
}

/* 顶部 Header */
.top-card {
  position: relative;
  background: linear-gradient(180deg, var(--color-header-bg-2) 0%, var(--color-header-bg) 100%);
  border-radius: 0 0 28px 28px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
  border-bottom: 1.5px solid rgb(143, 141, 116);
  box-shadow: 0 2px 10px rgba(122, 111, 70, 0.08);
}

.header-title {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: 6px;
  color: var(--color-text-on-blue);
  margin: 0;
  position: relative;
  z-index: 1;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
}
.profile-entry-btn {
  position: absolute;
  right: 14px;
  top: 12px;
  height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.24);
  color: #ffffff;
  font-size: 14px;
  font-family: var(--font-body);
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 3;
}

.profile-entry-btn:active {
  transform: translateY(1px);
  opacity: 0.92;
}
.header-deco--left {
  position: absolute;
  left: 30px;
  bottom: -15px;
  height: 72px;
  display: flex;
  align-items: flex-end;
  z-index: 2;
}

.character-body {
  height: 100%;
  object-fit: contain;
  position: relative;
  z-index: 2;
  filter: drop-shadow(0 3px 5px rgba(0, 0, 0, 0.12));
}

.character-tail {
  position: absolute;
  bottom: 18%;
  right: 20%;
  height: 42%;
  object-fit: contain;
  z-index: 1;
  transform-origin: top center;
  animation: wag 0.9s ease-in-out infinite alternate;
}



/* 主体滚动区 */
.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 22px 18px 96px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

/* 通用卡片 */
.card {
  background-color: transparent;
  border-radius: 16px;
  padding: 4px 0;
}

/* 板块标题 */
.section-label {
  font-size: 13px;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.section-label::before,
.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-line), transparent);
}

/* 知识卡 */
.story-image-wrap {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  background: var(--story-wrap-bg);
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(99, 116, 113, 0.9);
  box-shadow: 0 6px 16px rgba(85, 103, 123, 0.08);
}

.story-image-wrap::after {
  content: '';
  position: absolute;
  inset: 8px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.55);
  pointer-events: none;
}

.story-image {
  width: 100%;
  height: auto;
  display: block;
  margin-top: -20px;
}

.story-image-caption {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--story-wrap-bg);
  border: 1px solid rgba(208, 220, 232, 0.95);
  box-shadow: 0 4px 10px rgba(85, 123, 105, 0.08);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  font-size: 14px;
  padding: 6px 22px;
  border-radius: 999px;
  color: var(--color-text-primary);
  white-space: nowrap;
}

/* 进度卡 */
.progress-block {
  background: linear-gradient(180deg, var(--color-progress-bg-2) 0%, var(--color-progress-bg) 100%);
  border-radius: 16px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-shadow: 0 8px 18px rgba(79, 105, 136, 0.12);
  border: 1px solid rgba(121, 150, 184, 0.35);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress-title,
.progress-count {
  font-size: 13px;
  color: var(--color-text-on-blue);
}

.progress-count {
  opacity: 0.92;
}

.progress-bar-bg {
  height: 6px;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 999px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #f1d17d, #f7e6b5);
  border-radius: 999px;
  transition: width 0.5s ease;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
  border: 1px solid rgba(241, 209, 125, 0.9);
}

.tag--done {
  background: var(--color-gold-soft);
  color: var(--color-text-primary);
  font-weight: 600;
  border-color: transparent;
}
.progress-action-btn {
  margin-top: 8px;
  align-self: flex-end;
  height: 20px;
  padding: 0 18px;
  border: none;
  border-radius: 999px;
  background: var(--color-gold-soft);
  color: var(--color-text-primary);
  font-size: 14px;
  font-family: var(--font-body);
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
}

.progress-action-btn:active {
  transform: translateY(1px);
}
/* 功能入口 */
.function-list {
  display: flex;
  justify-content: space-around;
  gap: 12px;
}

.function-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  flex: 1;
}

.function-icon {
  width: 74px;
  height: 74px;
  object-fit: cover;
  border: 1px solid var(--color-line-soft);
  background: var(--color-surface);
  box-shadow: 0 6px 14px rgba(90, 95, 82, 0.06);
  border-radius: 18px;
  padding: 6px;
}

.function-name {
  font-size: 15px;
  color: var(--color-text-primary);
}



/* 轻交互 */
.function-item:active,
.tab-item:active,
.story-image-caption:active {
  transform: translateY(1px);
}

/* 尾巴动效 */
@keyframes wag {
  from {
    transform: rotate(-7deg);
  }
  to {
    transform: rotate(7deg);
  }
}
</style>