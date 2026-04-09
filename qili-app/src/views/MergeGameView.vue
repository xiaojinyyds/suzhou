<template>
  <div class="merge-page">
    <!-- 顶栏（带背景色） -->
    <div class="top-bar-main">
      <button class="back-btn" @click="$router.back()">← 返回</button>
      <div class="game-title">合成小狸猫</div>
      <div style="width: 80px;" />
    </div>

    <!-- 副栏（分数 + 重新开始） -->
    <div class="top-bar-sub">
      <div class="scores">
        <div class="score-box">
          <div class="score-label">分数</div>
          <div class="score-val">{{ score }}</div>
        </div>
        <div class="score-box">
          <div class="score-label">最高</div>
          <div class="score-val">{{ highScore }}</div>
        </div>
      </div>
      <button class="restart-btn-top" @click="initGame">重新开始</button>
    </div>

    <div class="merge-goal-tip">
      点击场上新出现的狸猫可解锁典故并获得奖励分数
    </div>

    <!-- 游戏区 -->
    <div class="game-wrap">
      <!-- 下一个预览 -->
      <div class="next-preview">
        <div class="next-label">下一个</div>
        <img :src="MASCOTS[nextLevel].img" alt="next" class="next-img" />
      </div>

      <!-- 画布容器 -->
      <div ref="containerRef" class="game-container">
        <canvas ref="canvasRef" class="game-canvas" />

        <!-- 投放线 -->
        <div class="drop-line" :style="{ left: dropLineX + 'px' }" />

        <!-- 当前要投的角色 -->
        <div class="drop-preview" :style="{ left: dropLineX + 'px' }">
          <img :src="MASCOTS[currentLevel].img" alt="cur" class="drop-img" />
        </div>

        <!-- 危险线 -->
        <div class="danger-line" />

        <!-- 连击显示 -->
        <div v-if="showCombo" class="combo-display" :style="{ color: comboColor }">
          {{ combo }}<span class="combo-text">COMBO</span>
        </div>

        <!-- 提示 -->
        <div v-if="hintVisible" class="hint-text">点击投放狸猫</div>

        <!-- 新手引导 -->
        <div v-if="showGuide" class="guide-tip" @click="showGuide = false">
          点击投放狸猫，相同狸猫会合成更大的狸猫<br />
          发现新狸猫后，点击可解锁典故<br />
          超过警戒线则游戏结束<br />
          <span class="guide-close">知道了 ✓</span>
        </div>

        <!-- toast 提示 -->
        <div v-if="showUnlockToast" class="unlock-toast">
          {{ unlockToast }}
        </div>

        <!-- 游戏结束 -->
        <div v-if="isGameOver && gameOverStats" class="gameover-overlay">
          <div class="gameover-title">游戏结束</div>
          <div v-if="isNewRecord" class="new-record"> 新纪录！</div>
          <div class="stats-box">
            <div class="stat-score-label">最终分数</div>
            <div class="stat-score-val">{{ gameOverStats.score }}</div>
            <div v-for="[l, v] in statRows" :key="l" class="stat-row">
              <span class="stat-label">{{ l }}</span>
              <span class="stat-value">{{ v }}</span>
            </div>
          </div>
          <button class="restart-btn" @click.stop="initGame">再来一局</button>
        </div>
      </div>
    </div>

    <!-- 已正式解锁狸猫 -->
    <div class="discovered-section">
      <div class="discovered-header">
        <span>已解锁狸猫 <strong>{{ unlocked.size }}/7</strong></span>
        <span class="discovered-hint">点击场上狸猫查看典故，可正式解锁并获得奖励 ↑</span>
      </div>
      <div class="discovered-bar-bg">
        <div class="discovered-bar-fill" :style="{ width: (unlocked.size / 7 * 100) + '%' }" />
      </div>
      <div class="mascot-grid">
        <div
          v-for="(m, i) in MASCOTS"
          :key="i"
          class="mascot-cell"
          :class="{ unlocked: unlocked.has(i), seen: seen.has(i) && !unlocked.has(i) }"
        >
          <img
            :src="m.img"
            :alt="m.name"
            class="mascot-thumb"
            :class="{ locked: !seen.has(i) && !unlocked.has(i), semi: seen.has(i) && !unlocked.has(i) }"
          />
          <span class="mascot-name">
            {{ unlocked.has(i) ? m.name : seen.has(i) ? '待解锁' : '???' }}
          </span>
          <div
            v-if="unlocked.has(i)"
            class="mascot-dot"
            :style="{ background: m.rarityColor }"
          />
        </div>
      </div>
    </div>

    <!-- 典故卡片 -->
    <div v-if="storyMascot" class="story-overlay" @click="storyMascot = null">
      <div class="story-card" @click.stop>
        <div class="story-rarity" :style="{ background: storyMascot.rarityColor }">
          {{ storyMascot.rarity }}
        </div>
        <div class="story-header">
          <div class="story-avatar">
            <img :src="storyMascot.img" :alt="storyMascot.name" class="story-avatar-img" />
          </div>
          <div>
            <div class="story-name">{{ storyMascot.name }}</div>
            <div class="story-location"> {{ storyMascot.location }}</div>
          </div>
        </div>
        <div class="story-divider" />
        <p class="story-text">{{ storyMascot.story }}</p>
        <button class="story-close" @click="storyMascot = null">收起典故</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { get, post } from '@/utils/request'
import { showToast } from '@/utils/toast'

import baigong from '@/assets/mascots/baigong.png'
import caiyun from '@/assets/mascots/caiyun.png'
import fenshui from '@/assets/mascots/fenshui.png'
import haiyong from '@/assets/mascots/haiyong.png'
import meiren from '@/assets/mascots/meiren.png'
import tonggui from '@/assets/mascots/tonggui.png'
import wenchang from '@/assets/mascots/wenchang.png'

const MASCOTS = [
  {
    name: '白工',
    img: baigong,
    radius: 20,
    points: 1,
    unlockBonus: 5,
    rarity: '普通',
    rarityColor: '#b0b8c1',
    story:
      '白工是苏州民间传说中最质朴的狸猫精灵，象征着初心与好奇。据说每逢月圆之夜，白工会悄悄溜进苏州的小巷，用天真无邪的眼睛凝望古城的灯火。它是所有狸猫的起点，也是一切故事的开始。',
    location: '常出没于山塘街的青石板路上',
  },
  {
    name: '彩云',
    img: caiyun,
    radius: 26,
    points: 3,
    unlockBonus: 8,
    rarity: '普通',
    rarityColor: '#b0b8c1',
    story:
      '彩云狸猫修炼百日后习得御风之术，能在苏州的天空中织出五彩云霞。古人相信，清晨看到彩云飞过虎丘塔顶，这一天必定诸事顺遂、心想事成。',
    location: '虎丘山顶的云雾之中',
  },
  {
    name: '分水',
    img: fenshui,
    radius: 34,
    points: 6,
    unlockBonus: 12,
    rarity: '稀有',
    rarityColor: '#5b9bd5',
    story:
      '分水狸猫掌管苏州纵横交错的水系，传说它能让河道自动分流，引水灌溉万亩良田。在苏州水乡，船夫们出行前都会向分水默默祈祷，希望水路顺畅、平安抵达。',
    location: '七里山塘的古运河畔',
  },
  {
    name: '海涌',
    img: haiyong,
    radius: 42,
    points: 10,
    unlockBonus: 18,
    rarity: '稀有',
    rarityColor: '#5b9bd5',
    story:
      '海涌是苏州渔民世代供奉的守护神兽，据说它能在太湖掀起波澜，也能在风暴来临时以身挡浪。它粉色的皮毛在晨光中折射出珍珠般的光泽，象征着太湖的馈赠与宽容。',
    location: '太湖之滨的渔港码头',
  },
  {
    name: '美人',
    img: meiren,
    radius: 50,
    points: 15,
    unlockBonus: 25,
    rarity: '史诗',
    rarityColor: '#9b6dbd',
    story:
      '美人狸猫是苏州园林的守护者，它能幻化为婉约的江南女子，在月下抚琴。相传拙政园深处的花影，有时便是美人轻舞的倩影。她的美不在妆容，而在能感受园林四季更迭的细腻之心。',
    location: '拙政园荷花池旁的回廊',
  },
  {
    name: '铜贵',
    img: tonggui,
    radius: 60,
    points: 21,
    unlockBonus: 35,
    rarity: '传说',
    rarityColor: '#d4a017',
    story:
      '铜贵狸猫是苏州商贾最敬重的财神化身。明清时期，丝绸商人开铺前必请铜贵像镇店，据说摸过铜贵尾巴的算盘，拨出的每个数字都能化为真金。苏绣中有一针法便以"铜贵纹"命名，象征生意兴隆。',
    location: '平江路上的百年老字号',
  },
  {
    name: '文昌',
    img: wenchang,
    radius: 70,
    points: 28,
    unlockBonus: 50,
    rarity: '神话',
    rarityColor: '#c0392b',
    story:
      '文昌狸猫是苏州七狸之首，集天地灵气而生。苏州历史上状元辈出，民间皆传是文昌在夜里悄悄为学子磨墨、续灯。相传每年科举放榜之日，若在文庙前看到一只翠色狸猫，便是文昌显灵、告知中第之兆。',
    location: '苏州文庙的古银杏树下',
  },
]

const containerRef = ref(null)
const canvasRef = ref(null)
const score = ref(0)
const highScore = ref(+localStorage.getItem('tanukiHS') || 0)
const currentLevel = ref(0)
const nextLevel = ref(1)
const dropLineX = ref(200)
const combo = ref(0)
const showCombo = ref(false)
const isGameOver = ref(false)
const gameOverStats = ref(null)
const isNewRecord = ref(false)

const seen = ref(new Set())      // 见过/合成出过
const unlocked = ref(new Set())  // 点击典故后的正式解锁

const storyMascot = ref(null)
const hintVisible = ref(true)
const showGuide = ref(true)
const unlockToast = ref('')
const showUnlockToast = ref(false)

let engine, render, runner, Composite
let canDrop = true, gameRunning = true, gameStarted = false
let scoreVal = 0, currentLv = 0, nextLv = 1
let comboCount = 0, maxCombo = 0, lastMerge = 0
let totalMerges = 0, mergeCount = {}, highestLv = 0
let comboTimer = null, checkInterval = null, unlockToastTimer = null
let dropX = 200

const imagesCache = {}
const seenSet = new Set()
const unlockedSet = new Set()

const getRnd = () => Math.floor(Math.random() * 3)

const comboColor = computed(() =>
  combo.value >= 10 ? '#c0392b' : combo.value >= 5 ? '#e67e22' : '#e8896a'
)

const statRows = computed(() =>
  gameOverStats.value
    ? [
        ['最大连击', gameOverStats.value.maxCombo + 'x'],
        ['总合成', gameOverStats.value.totalMerges + '次'],
        ['最高等级', gameOverStats.value.highestName],
        ['正式解锁', gameOverStats.value.unlocked + '/7'],
      ]
    : []
)

function spawnParticles(x, y, color) {
  if (!containerRef.value) return
  for (let i = 0; i < 10; i++) {
    const el = document.createElement('div')
    Object.assign(el.style, {
      position: 'absolute',
      width: '7px',
      height: '7px',
      borderRadius: '50%',
      background: color,
      left: x + 'px',
      top: y + 'px',
      pointerEvents: 'none',
      zIndex: '120',
    })
    containerRef.value.appendChild(el)

    const angle = (Math.PI * 2 * i) / 10
    const v = 80 + Math.random() * 50
    const vx = Math.cos(angle) * v
    const vy = Math.sin(angle) * v
    const t0 = Date.now()

    const tick = () => {
      const p = (Date.now() - t0) / 700
      if (p >= 1) {
        el.remove()
        return
      }
      el.style.left = x + vx * p + 'px'
      el.style.top = y + vy * p + p * p * 180 + 'px'
      el.style.opacity = 1 - p
      requestAnimationFrame(tick)
    }

    requestAnimationFrame(tick)
  }
}

function showUnlockMessage(text) {
  unlockToast.value = text
  showUnlockToast.value = true

  if (unlockToastTimer) clearTimeout(unlockToastTimer)
  unlockToastTimer = setTimeout(() => {
    showUnlockToast.value = false
  }, 1500)
}

function markSeen(lv) {
  if (!seenSet.has(lv)) {
    seenSet.add(lv)
    seen.value = new Set(seenSet)
    showUnlockMessage(`发现新狸猫${MASCOTS[lv].name}，点击它可查看典故并解锁奖励`)
  }
}

function unlockMascot(lv) {
  if (!unlockedSet.has(lv)) {
    unlockedSet.add(lv)
    unlocked.value = new Set(unlockedSet)

    const bonus = MASCOTS[lv].unlockBonus || 10
    scoreVal += bonus
    score.value = scoreVal

    if (scoreVal > highScore.value) {
      highScore.value = scoreVal
    }

    if (lv > highestLv) highestLv = lv
    showUnlockMessage(`已解锁${MASCOTS[lv].name}，获得 +${bonus} 分奖励`)
  }
}

function syncScore() {
  if (scoreVal > 0) {
    post('/api/v1/merge-game', {
      score: scoreVal,
      max_combo: maxCombo,
      highest_level: highestLv
    }).catch(err => console.error('提前保存战绩失败', err))
  }
}

async function initGame() {
  if (scoreVal > 0 && !isGameOver.value) {
    syncScore()
  }
  const M = await import('matter-js')
  const { Engine, Render, Runner, Bodies, Events } = M
  Composite = M.Composite

  if (!containerRef.value || !canvasRef.value) return

  if (checkInterval) clearInterval(checkInterval)
  if (comboTimer) clearTimeout(comboTimer)
  if (unlockToastTimer) clearTimeout(unlockToastTimer)
  if (render) M.Render.stop(render)
  if (runner) M.Runner.stop(runner)
  if (engine) {
    Composite.clear(engine.world)
    Engine.clear(engine)
  }

  const W = containerRef.value.clientWidth
  const H = containerRef.value.clientHeight

  scoreVal = 0
  canDrop = true
  gameRunning = true
  gameStarted = false
  comboCount = 0
  maxCombo = 0
  lastMerge = 0
  totalMerges = 0
  mergeCount = {}
  dropX = W / 2
  currentLv = getRnd()
  nextLv = getRnd()
  highestLv = 0

  seenSet.clear()
  unlockedSet.clear()

  score.value = 0
  currentLevel.value = currentLv
  nextLevel.value = nextLv
  dropLineX.value = W / 2
  combo.value = 0
  showCombo.value = false
  isGameOver.value = false
  hintVisible.value = true
  storyMascot.value = null
  seen.value = new Set()
  unlocked.value = new Set()
  showUnlockToast.value = false

  engine = Engine.create({ gravity: { x: 0, y: 1 } })
  render = Render.create({
    canvas: canvasRef.value,
    engine,
    options: {
      width: W,
      height: H,
      wireframes: false,
      background: 'transparent',
    },
  })

  const wo = {
    isStatic: true,
    render: { fillStyle: 'transparent', strokeStyle: 'transparent', lineWidth: 0 },
    friction: 0.3,
  }

  Composite.add(engine.world, [
    Bodies.rectangle(W / 2, H + 10, W, 20, wo),
    Bodies.rectangle(-10, H / 2, 20, H, wo),
    Bodies.rectangle(W + 10, H / 2, 20, H, wo),
  ])

  Events.on(engine, 'collisionStart', ({ pairs }) => {
    for (const { bodyA, bodyB } of pairs) {
      if (
        bodyA.label === 'mascot' &&
        bodyB.label === 'mascot' &&
        bodyA.mascotLevel === bodyB.mascotLevel &&
        bodyA.mascotLevel < MASCOTS.length - 1 &&
        !bodyA.isMerging &&
        !bodyB.isMerging
      ) {
        bodyA.isMerging = bodyB.isMerging = true
        const lv = bodyA.mascotLevel
        const posX = (bodyA.position.x + bodyB.position.x) / 2
        const posY = (bodyA.position.y + bodyB.position.y) / 2

        Composite.remove(engine.world, bodyA)
        Composite.remove(engine.world, bodyB)

        Composite.add(
          engine.world,
          Bodies.circle(posX, posY, MASCOTS[lv + 1].radius, {
            restitution: 0.3,
            friction: 0.3,
            density: 0.001,
            render: { fillStyle: 'transparent', strokeStyle: 'transparent', lineWidth: 0 },
            label: 'mascot',
            mascotLevel: lv + 1,
            createdAt: Date.now(),
          })
        )

        // 标记新出现
        markSeen(lv + 1)

        const now = Date.now()
        let pts = MASCOTS[lv + 1].points

        if (now - lastMerge < 2000) {
          comboCount++
          if (comboCount > maxCombo) maxCombo = comboCount
          pts += Math.floor(pts * comboCount * 0.1)
          combo.value = comboCount
          showCombo.value = true
        } else {
          comboCount = 1
        }

        lastMerge = now
        if (comboTimer) clearTimeout(comboTimer)
        comboTimer = setTimeout(() => {
          comboCount = 0
          showCombo.value = false
        }, 2000)

        scoreVal += pts
        score.value = scoreVal

        if (scoreVal > highScore.value) {
          highScore.value = scoreVal
        }

        totalMerges++
        mergeCount[lv + 1] = (mergeCount[lv + 1] || 0) + 1

        if (lv + 1 > highestLv) highestLv = lv + 1

        spawnParticles(posX, posY, MASCOTS[lv + 1].rarityColor)
        break
      }
    }
  })

  Events.on(render, 'afterRender', () => {
    const ctx = render.context
    for (const b of Composite.allBodies(engine.world)) {
      if (b.label !== 'mascot') continue
      const img = imagesCache[b.mascotLevel]
      if (!img?.complete || !img.naturalWidth) continue

      const r = MASCOTS[b.mascotLevel].radius
      const size = r * 2.2

      ctx.save()
      ctx.translate(b.position.x, b.position.y)
      ctx.rotate(b.angle)
      ctx.shadowColor = 'rgba(0,0,0,0.1)'
      ctx.shadowBlur = 8
      ctx.shadowOffsetY = 3
      const breathe = Math.sin(Date.now() / 900 + b.id) * 0.025 + 1
      ctx.drawImage(
        img,
        (-size * breathe) / 2,
        (-size * breathe) / 2,
        size * breathe,
        size * breathe
      )
      ctx.restore()
    }
  })

  M.Render.run(render)
  runner = M.Runner.create()
  M.Runner.run(runner, engine)

  checkInterval = setInterval(() => {
    if (!gameRunning || !gameStarted) return
    const now = Date.now()

    for (const b of Composite.allBodies(engine.world)) {
      if (
        b.label === 'mascot' &&
        b.position.y < 120 &&
        Math.abs(b.velocity.y) < 1 &&
        Math.abs(b.velocity.x) < 1 &&
        now - (b.createdAt || now) > 2000
      ) {
        gameRunning = false
        const prevHS = highScore.value
        isNewRecord.value = scoreVal >= prevHS && scoreVal > 0
        gameOverStats.value = {
          score: scoreVal,
          maxCombo,
          totalMerges,
          highestName: MASCOTS[highestLv].name,
          unlocked: unlockedSet.size,
        }
        isGameOver.value = true
        
        // 游戏结束上报战绩到后端
        post('/api/v1/merge-game', {
          score: scoreVal,
          max_combo: maxCombo,
          highest_level: highestLv
        }).then(res => {
          if (res.data && res.data.max_score > highScore.value) {
            highScore.value = res.data.max_score
          }
        }).catch(err => console.error('战绩保存失败', err))

        break
      }
    }
  }, 200)
}

async function drop(x) {
  if (!canDrop || !gameRunning) return
  const { Bodies } = await import('matter-js')

  canDrop = false
  gameStarted = true
  hintVisible.value = false

  // 当前投放出来的也算见过
  markSeen(currentLv)

  Composite.add(
    engine.world,
    Bodies.circle(x, 80, MASCOTS[currentLv].radius, {
      restitution: 0.3,
      friction: 0.3,
      density: 0.001,
      render: { fillStyle: 'transparent', strokeStyle: 'transparent', lineWidth: 0 },
      label: 'mascot',
      mascotLevel: currentLv,
      createdAt: Date.now(),
    })
  )

  currentLv = nextLv
  const nn = getRnd()
  nextLv = nn
  currentLevel.value = currentLv
  nextLevel.value = nn

  setTimeout(() => {
    canDrop = true
  }, 580)
}

function getMascotAt(x, y) {
  if (!engine || !Composite) return null
  for (const b of Composite.allBodies(engine.world)) {
    if (b.label === 'mascot') {
      const r = MASCOTS[b.mascotLevel].radius
      if (Math.hypot(b.position.x - x, b.position.y - y) <= r + 4) return b
    }
  }
  return null
}

onMounted(async () => {
  // 页面加载先获取后端历史最高分
  try {
    const res = await get('/api/v1/merge-game/my')
    if (res.data && res.data.high_score !== undefined) {
      highScore.value = res.data.high_score
    }
  } catch(e) {
    console.warn('获取分数失败', e)
  }

  MASCOTS.forEach((m, i) => {
    const img = new Image()
    img.src = m.img
    imagesCache[i] = img
  })

  initGame()

  const el = containerRef.value
  const W = () => el.clientWidth
  const clamp = raw => {
    const r = el.getBoundingClientRect()
    return Math.max(40, Math.min(W() - 40, raw - r.left))
  }

  const onMove = e => {
    const x = clamp(e.clientX)
    dropX = x
    dropLineX.value = x
  }

  const onTM = e => {
    e.preventDefault()
    const x = clamp(e.touches[0].clientX)
    dropX = x
    dropLineX.value = x
  }

  const onClick = e => {
    const rect = el.getBoundingClientRect()
    const x = clamp(e.clientX)
    const y = e.clientY - rect.top
    const m = getMascotAt(x, y)

    if (m) {
      const lv = m.mascotLevel
      unlockMascot(lv)
      storyMascot.value = { ...MASCOTS[lv], id: lv }
    } else {
      dropX = x
      dropLineX.value = x
      drop(x)
    }
  }

  const onTE = e => {
    const rect = el.getBoundingClientRect()
    const x = clamp(e.changedTouches[0].clientX)
    const y = e.changedTouches[0].clientY - rect.top
    const m = getMascotAt(x, y)

    if (m) {
      const lv = m.mascotLevel
      unlockMascot(lv)
      storyMascot.value = { ...MASCOTS[lv], id: lv }
    } else {
      drop(dropX)
    }
  }

  el.addEventListener('mousemove', onMove)
  el.addEventListener('touchmove', onTM, { passive: false })
  el.addEventListener('click', onClick)
  el.addEventListener('touchend', onTE)
})

onUnmounted(() => {
  if (!isGameOver.value) {
    syncScore()
  }
  if (checkInterval) clearInterval(checkInterval)
  if (comboTimer) clearTimeout(comboTimer)
  if (unlockToastTimer) clearTimeout(unlockToastTimer)

  import('matter-js').then(M => {
    if (render) M.Render.stop(render)
    if (runner) M.Runner.stop(runner)
    if (engine) {
      M.Composite.clear(engine.world)
      M.Engine.clear(engine)
    }
  })
})
</script>

<style scoped>
.merge-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background: #fffaf0;
  font-family: 'Noto Sans SC', sans-serif;
  max-width: 430px;
  margin: 0 auto;
  position: relative;
}

.top-bar-main {
  position: relative;
  height: 56px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--skin-primary);
  border-radius: 0 0 24px 24px;
  border-bottom: 2px solid rgb(143, 141, 116);
  box-shadow: 0 2px 10px rgba(122, 122, 70, 0.12);
}

.top-bar-sub {
  width: 100%;
  max-width: 420px;
  padding: 10px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.back-btn {
  background: rgba(255, 255, 255, 0.16);
  border: 1px solid rgba(255, 255, 255, 0.24);
  color: #ffffff;
  border-radius: 20px;
  position: relative;
  top: 2px;
  left: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  white-space: nowrap;
}

.game-title {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 1.5rem;
  color: #ffffff;
  letter-spacing: 2px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.12);
}

.restart-btn-top {
  background: rgba(161, 181, 177, 0.12);
  border: none;
  color: #357a64;
  border-radius: 20px;
  padding: 7px 16px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  white-space: nowrap;
}

.merge-goal-tip {
  width: 100%;
  max-width: 420px;
  font-size: 0.78rem;
  color: #70b09e;
  text-align: center;
  margin: 4px 0 10px;
}

.scores {
  display: flex;
  gap: 8px;
}

.score-box {
  background: rgba(80, 180, 158, 0.1);
  padding: 5px 12px;
  border-radius: 16px;
  text-align: center;
}

.score-label {
  font-size: 0.6rem;
  color: #4b7262;
}

.score-val {
  font-weight: 700;
  color: #4b7262;
  font-size: 1rem;
}

.game-wrap {
  position: relative;
  width: 100%;
  max-width: 420px;
}

.next-preview {
  position: absolute;
  top: 12px;
  left: 14px;
  z-index: 100;
  background: rgba(209, 208, 179, 0.3);
  backdrop-filter: blur(8px);
  padding: 8px 12px;
  border-radius: 16px;
  text-align: center;
}

.next-label {
  font-size: 0.6rem;
  color: #4b7262;
  margin-bottom: 4px;
}

.next-img {
  width: 38px;
  height: 38px;
  object-fit: contain;
}

.game-container {
  position: relative;
  width: 100%;
  aspect-ratio: 9 / 14;
  max-height: 68vh;
  background: var(--skin-storywrap);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 6px 30px rgba(60, 160, 138, 0.1);
  cursor: crosshair;
  background-image: url('@/assets/images/彩云狸5.png');
  background-size: cover;
}

.game-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

.drop-line {
  position: absolute;
  top: 0;
  width: 1.5px;
  height: 100%;
  pointer-events: none;
  z-index: 50;
  background: linear-gradient(180deg, rgba(60, 200, 170, 0.5) 0%, rgba(60, 200, 170, 0) 22%);
}

.drop-preview {
  position: absolute;
  top: 28px;
  transform: translateX(-50%);
  pointer-events: none;
  z-index: 60;
}

.drop-img {
  width: 48px;
  height: 48px;
  object-fit: contain;
  filter: drop-shadow(0 3px 6px rgba(0, 0, 0, 0.12));
}

.danger-line {
  position: absolute;
  top: 60px;
  left: 0;
  right: 0;
  height: 2px;
  background: repeating-linear-gradient(
    90deg,
    rgba(80, 220, 197, 0.46) 0,
    rgba(12, 34, 30, 0.95) 8px,
    transparent 8px,
    transparent 16px
  );
  pointer-events: none;
  z-index: 10;
}

.combo-display {
  position: absolute;
  top: 18%;
  left: 50%;
  transform: translateX(-50%);
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 2.8rem;
  text-shadow: 0 0 18px currentColor;
  pointer-events: none;
  z-index: 150;
}

.combo-text {
  font-size: 0.4em;
  display: block;
  text-align: center;
  margin-top: -8px;
  letter-spacing: 3px;
}

.hint-text {
  position: absolute;
  bottom: 35%;
  left: 50%;
  transform: translateX(-50%);
  color: rgb(255, 255, 255);
  font-size: 1rem;
  pointer-events: none;
  z-index: 40;
  white-space: nowrap;
}

.guide-tip {
  position: absolute;
  bottom: 20%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(76, 190, 184, 0.75);
  color: rgb(255, 255, 255);
  font-size: 0.78rem;
  padding: 10px 16px;
  border-radius: 20px;
  pointer-events: all;
  z-index: 130;
  white-space: nowrap;
  cursor: pointer;
  text-align: center;
}

.guide-close {
  display: block;
  font-size: 0.68rem;
  opacity: 0.7;
  margin-top: 4px;
}

.unlock-toast {
  position: absolute;
  top: 16%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 244, 210, 0.96);
  color: #b3ae78;
  font-size: 0.8rem;
  padding: 8px 14px;
  border-radius: 999px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  z-index: 140;
  white-space: nowrap;
  border: 1px solid rgba(230, 180, 120, 0.55);
}

.gameover-overlay {
  position: absolute;
  inset: 0;
  background: rgb(18, 15, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 200;
  border-radius: 22px;
  padding: 24px;
}

.gameover-title {
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 2.2rem;
  color: #d3cf92;
  margin-bottom: 16px;
}

.new-record {
  background: #bca532;
  color: #7a7800;
  padding: 5px 18px;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.85rem;
  margin-bottom: 14px;
}

.stats-box {
  background: rgba(255, 255, 255, 0.08);
  padding: 20px;
  border-radius: 16px;
  margin-bottom: 18px;
  width: 100%;
  max-width: 260px;
}

.stat-score-label {
  font-size: 0.8rem;
  color: #7ec1a4;
  text-align: center;
  opacity: 0.8;
}

.stat-score-val {
  font-size: 2.2rem;
  font-weight: 800;
  color: #08b58f;
  text-align: center;
  margin-bottom: 12px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  margin: 6px 0;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.stat-label {
  color: rgba(255, 255, 255, 0.5);
}

.stat-value {
  color: #0fc3a8;
  font-weight: 600;
}

.restart-btn {
  padding: 12px 44px;
  font-size: 0.95rem;
  font-weight: 700;
  border: none;
  border-radius: 24px;
  cursor: pointer;
  background: linear-gradient(135deg, #51ccc0, #2aa48a);
  color: white;
  letter-spacing: 1px;
}

.discovered-section {
  width: 100%;
  max-width: 420px;
  padding: 14px 16px 20px;
}

.discovered-header {
  font-size: 0.7rem;
  color: #70b0a5;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
}

.discovered-hint {
  font-size: 0.63rem;
  color: #67b3a1;
}

.discovered-bar-bg {
  height: 4px;
  background: #bfd8d4;
  border-radius: 4px;
  margin-bottom: 10px;
  overflow: hidden;
}

.discovered-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #377666, #349c92);
  border-radius: 4px;
  transition: width 0.6s ease;
}

.mascot-grid {
  display: flex;
  gap: 6px;
  justify-content: center;
}

.mascot-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  padding: 8px 3px;
  border-radius: 14px;
  background: rgba(200, 180, 160, 0.18);
  transition: all 0.3s;
}

.mascot-cell.unlocked {
  background: rgba(230, 230, 192, 0.9);
  box-shadow: 0 2px 10px rgba(160, 100, 60, 0.1);
}

.mascot-cell.seen {
  background: rgba(192, 226, 212, 0.65);
}

.mascot-thumb {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.mascot-thumb.locked {
  filter: grayscale(100%) brightness(0.7);
  opacity: 0.4;
}

.mascot-thumb.semi {
  opacity: 0.75;
  filter: saturate(0.75);
}

.mascot-name {
  font-size: 0.5rem;
  color: #84aeaa;
  margin-top: 3px;
}

.mascot-cell.unlocked .mascot-name {
  color: #357a6a;
}

.mascot-cell.seen .mascot-name {
  color: #6b9a8d;
}

.mascot-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  margin-top: 3px;
}

.story-overlay {
  position: absolute;
  inset: 0;
  background: rgba(30, 80, 68, 0.35);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 400;
  padding: 24px;
}

.story-card {
  background: #fffbf5;
  border-radius: 24px;
  padding: 28px 24px;
  max-width: 340px;
  width: 100%;
  box-shadow: 0 20px 60px rgba(60, 152, 160, 0.18);
  position: relative;
}

.story-rarity {
  position: absolute;
  top: 20px;
  right: 20px;
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 20px;
}

.story-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 18px;
}

.story-avatar {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: linear-gradient(135deg, #fffde0, #fff8cc);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.story-avatar-img {
  width: 64px;
  height: 64px;
  object-fit: contain;
}

.story-name {
  font-size: 1.6rem;
  font-weight: 800;
  color: #1a3a33;
  font-family: 'Ma Shan Zheng', cursive;
  letter-spacing: 2px;
}

.story-location {
  font-size: 0.72rem;
  color: #6aa095;
  margin-top: 4px;
}

.story-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, #c0e8e5, transparent);
  margin-bottom: 16px;
}

.story-text {
  font-size: 0.92rem;
  line-height: 1.9;
  color: #284a45;
  margin-bottom: 22px;
  text-align: justify;
}

.story-close {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  background: linear-gradient(135deg, #64dbc4, #3aaf9c);
  color: white;
  letter-spacing: 1px;
}
</style>