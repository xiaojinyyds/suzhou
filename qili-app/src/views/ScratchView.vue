<template>
  <div class="scratch-view">
    <header class="top-card">
  <div class="tc-texture"></div>
  <div class="tc-glow"></div>

  <!-- 主内容行：左侧文字 + 右侧狸猫 -->
  <div class="ticket-main-row">
    <!-- 左侧 -->
    <div class="ticket-left">
      <div class="ticket-top-meta">
        <button class="back-btn" @click="$router.back()">← 返回</button>
        <div class="serial-block">
          <span class="serial-label">NO.2024 · 山塘限定</span>
          <span class="serial-num">ST-{{ ticketNum }}</span>
        </div>
        
      </div>

      <div class="ticket-gold-rule"></div>

      <div class="ticket-text-block">
        <h1 class="header-title">七狸有缘</h1>
        <div class="header-subtitle">苏州山塘街 · 文化打卡活动纪念彩票</div>
        <div class="strip-rule-pill">同一行三格相同即中奖</div>
      </div>
    </div>

    <!-- 右侧：狸猫图 -->
    <div class="ticket-right">
      <img
        class="ticket-mascot"
        :src="getMascotImg(MASCOTS[winMascotIdx].img)"
        :alt="MASCOTS[winMascotIdx].name"
      />
    </div>
  </div>

  <!-- 波浪过渡 -->
  <div class="hero-wave">
    <svg viewBox="0 0 390 24" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M0,12 C65,24 130,0 195,12 C260,24 325,0 390,12 L390,24 L0,24 Z" fill="#e8eef4"/>
    </svg>
  </div>
</header>
    <!-- 滚动内容区 -->
    <div class="scroll-body">
      <section class="ticket-shell">

        <!-- 刮奖面板 -->
        <div class="scratch-panel">
          <div class="panel-header">
            <div class="panel-title-wrap">
              
              <span class="panel-title">开始刮奖</span>
            </div>
            <div class="panel-mini-tip">用手指刮开涂层</div>
          </div>

          <div class="rows-wrap">
            <div
              v-for="(row, r) in rowData"
              :key="r"
              class="scratch-row"
              :class="{ won: row.win && rowRevealed[r], revealed: rowRevealed[r] }"
            >
              <div class="row-label">
                <span>{{ rowLabels[r] }}</span>
              </div>
              <div class="row-cells">
                <div
                  v-for="c in 3"
                  :key="c - 1"
                  class="scratch-cell"
                  :id="`cell-${r}-${c - 1}`"
                >
                  <div class="cell-prize">
                    <img
                      class="cp-img"
                      :src="getMascotImg(MASCOTS[row.cells[c - 1]].img)"
                      :alt="MASCOTS[row.cells[c - 1]].name"
                    />
                  </div>
                  <canvas
                    class="cell-canvas"
                    :id="`canvas-${r}-${c - 1}`"
                    @mousedown="onMouseDown($event, r, c - 1)"
                    @mousemove="onMouseMove($event, r, c - 1)"
                    @mouseup="onMouseUp"
                    @touchstart.prevent="onTouchStart($event, r, c - 1)"
                    @touchmove.prevent="onTouchMove($event)"
                    @touchend="onTouchEnd"
                  ></canvas>
                </div>
              </div>
              <div class="row-result">
                <div
                  class="result-badge"
                  :class="{
                    show: rowRevealed[r],
                    win: row.win && rowRevealed[r],
                    lose: !row.win && rowRevealed[r]
                  }"
                >
                  {{ row.win && rowRevealed[r] ? '中奖！！' : rowRevealed[r] ? '未中奖' : '' }}
                </div>
              </div>
            </div>
          </div>

          <!-- 进度条 -->
          <div class="progress-strip">
            <span class="prog-label">刮开进度</span>
            <div class="prog-track">
              <div class="prog-fill" :style="{ width: progressPct + '%' }"></div>
              <div class="prog-glow" :style="{ left: progressPct + '%' }"></div>
            </div>
            <span class="prog-pct">{{ progressPct }}%</span>
          </div>

          <div class="skip-wrap" v-if="!allDone">
            <button class="btn-skip" :disabled="skipDisabled" @click="skipAll">
              <span>{{ skipDisabled ? '正在揭晓…' : '心急的话，直接看结果 →' }}</span>
            </button>
          </div>
        </div>

        <!-- 分隔装饰 -->
        <div class="section-divider">
          <span class="divider-icon">✦</span>
        </div>

        <!-- 玩法说明折叠 -->
        <details class="fold-card">
          <summary class="fold-summary">
            <div class="fold-summary-left">
              
              <span>玩法说明</span>
            </div>
            <em class="fold-arrow">›</em>
          </summary>
          <div class="fold-content">
            <div class="game-instruction">
              刮开下方格子，同一行三格图案相同即为中奖。<br />
              每行独立判定，一行三图相同立即揭晓结果。
            </div>
          </div>
        </details>

        <!-- 缘分签折叠 -->
        <details class="fold-card">
          <summary class="fold-summary">
            <div class="fold-summary-left">
              
              <span>今日缘分签</span>
            </div>
            <em class="fold-arrow">›</em>
          </summary>
          <div class="fold-content">
            <div class="lucky-numbers-row">
              <template v-for="(n, i) in luckyNums" :key="i">
                <div class="lucky-num">{{ n }}</div>
                <span v-if="i < luckyNums.length - 1" class="lucky-op">＋</span>
              </template>
            </div>
            <div class="lucky-hint-text">
              五数之和 ÷ 7 取余，余数对应你的缘分狸猫
            </div>
            <div class="lucky-table">
              <div v-for="(m, idx) in MASCOTS" :key="idx" class="lt-item">
                <div class="lt-remainder">{{ idx }}</div>
                <img class="lt-img" :src="getMascotImg(m.img)" :alt="m.name" />
                <span class="lt-name">{{ m.name }}</span>
              </div>
            </div>
            <div class="hint-row">
              <button v-if="!hintShown" class="btn-hint" @click="showHint">
                想直接知道缘分狸猫？
              </button>
              <div v-if="hintShown" class="lazy-answer">
                今日与你有缘的是：<strong>{{ MASCOTS[winMascotIdx].name }}</strong> 🦝
              </div>
            </div>
          </div>
        </details>

        <div class="footer-note">
          终点驿站：山塘街七狸文创店 &nbsp;·&nbsp;  今日有效 &nbsp;·&nbsp; 每人限领一次
        </div>
      </section>

      <div style="height: 96px"></div>
    </div>

    <!-- 中奖弹窗 -->
    <transition name="modal-fade">
      <div v-if="showModal" class="result-modal-overlay" @click.self="showModal = false">
        <div class="result-modal">
          <button class="modal-close" @click="showModal = false">✕</button>

          <div class="modal-confetti-strip">
            <span v-for="i in 8" :key="i" class="mc-dot" :style="{ animationDelay: (i * 0.12) + 's' }">✦</span>
          </div>

          <div class="modal-badge">山塘限定</div>
          <div class="win-title">恭喜! 与 {{ MASCOTS[winMascotIdx].name }} 有缘</div>

          <div class="win-prize-card">
            <div class="win-prize-bg-circle"></div>
            <img
              class="win-prize-img float-anim"
              :src="getMascotImg(MASCOTS[winMascotIdx].img)"
              :alt="MASCOTS[winMascotIdx].name"
            />
            <div class="win-prize-info">
              <div class="win-prize-name">{{ MASCOTS[winMascotIdx].name }}</div>
              <div class="win-prize-desc">{{ MASCOTS[winMascotIdx].desc }}</div>
              <div class="win-prize-label">七狸限定周边兑换资格</div>
            </div>
          </div>

          <div class="redeem-steps">
            <div class="rs-step">
              
              <div class="rs-label">出示<br />此页面</div>
            </div>
            <span class="rs-arrow">›</span>
            <div class="rs-step">
              
              <div class="rs-label">工作人员<br />核验</div>
            </div>
            <span class="rs-arrow">›</span>
            <div class="rs-step">
              
              <div class="rs-label">领取<br />周边</div>
            </div>
          </div>

          <div class="note-band">
             仅限今日有效 · 每人限领一次<br />终点驿站：山塘街七狸文创店
          </div>
          <button class="btn-save" @click="onSave">截图保存兑换凭证</button>
        </div>
      </div>
    </transition>

    <!-- 彩带 -->
    <div
      v-for="piece in confettiPieces"
      :key="piece.id"
      class="confetti-piece"
      :style="piece.style"
    ></div>

    
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { Home, MapPin, Camera, ShoppingCart, User } from 'lucide-vue-next'
import { get, post } from '@/utils/request'
import { showToast } from '@/utils/toast'
import html2canvas from 'html2canvas'

const router = useRouter()

const MASCOTS = [
  { name: '白公狸', img: '白公狸.png', desc: '漫步白公堤边的温润之狸' },
  { name: '彩云狸', img: '彩云狸.png', desc: '映照彩云倒影的灵秀之狸' },
  { name: '分水狸', img: '分水狸.png', desc: '居于河道分叉处的水纹之狸' },
  { name: '海涌狸', img: '海涌狸.png', desc: '守护山塘入口的波浪之狸' },
  { name: '美仁狸', img: '美仁狸.png', desc: '踏遍美仁里弄的雅致之狸' },
  { name: '通贵狸', img: '通贵狸.png', desc: '守望通贵桥头的吉祥之狸' },
  { name: '文昌狸', img: '文昌狸.png', desc: '徘徊文昌阁下的文气之狸' },
]

const ROW_COUNT = 6
const CELLS_PER_ROW = 3
const rowLabels = ['第一行', '第二行', '第三行', '第四行', '第五行', '第六行']

function getMascotImg(filename) {
  return new URL(`../assets/mascots/${filename}`, import.meta.url).href
}

const winMascotIdx = ref(Math.floor(Math.random() * MASCOTS.length))

function genLuckyNums(targetMod) {
  let nums
  do { nums = Array.from({ length: 5 }, () => Math.floor(Math.random() * 9) + 1) }
  while (nums.reduce((a, b) => a + b, 0) % 7 !== targetMod)
  return nums
}

const luckyNums = ref(genLuckyNums(winMascotIdx.value))
const WIN_ROW = Math.floor(Math.random() * ROW_COUNT)
const ticketNum = Math.floor(Math.random() * 900000 + 100000)

const rowData = reactive([])
for (let r = 0; r < ROW_COUNT; r++) {
  const isWin = r === WIN_ROW
  let cells
  if (isWin) {
    cells = [winMascotIdx.value, winMascotIdx.value, winMascotIdx.value]
  } else {
    do { cells = Array.from({ length: CELLS_PER_ROW }, () => Math.floor(Math.random() * MASCOTS.length)) }
    while (cells.every(c => c === cells[0]))
  }
  rowData.push({ cells, win: isWin })
}

const hintShown = ref(false)
const rowRevealed = ref(Array(ROW_COUNT).fill(false))
const allDone = ref(false)
const showModal = ref(false)
const skipDisabled = ref(false)
const progressPct = ref(0)
const confettiPieces = ref([])

const canvases = {}
const clearedCells = new Set()
let isDown = false

function initCellCanvas(r, c) {
  const canvas = document.getElementById(`canvas-${r}-${c}`)
  const cell = document.getElementById(`cell-${r}-${c}`)
  if (!canvas || !cell) return
  const rect = cell.getBoundingClientRect()
  const dpr = window.devicePixelRatio || 1
  const W = rect.width || 60, H = rect.height || 40
  canvas.width = W * dpr; canvas.height = H * dpr
  canvas.style.width = W + 'px'; canvas.style.height = H + 'px'
  const ctx = canvas.getContext('2d')
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)

  /* ── 新涂层：和 app 主调一致的蓝灰渐变 ── */
  const g = ctx.createLinearGradient(0, 0, W, H)
  g.addColorStop(0,   '#7bc8b0')
  g.addColorStop(0.4, '#63b49a')
  g.addColorStop(0.7, '#6bb798')
  g.addColorStop(1,   '#50a086')
  ctx.fillStyle = g
  ctx.fillRect(0, 0, W, H)

  /* 柔和噪点纹理 */
  for (let i = 0; i < 600; i++) {
    const a = Math.random() * 0.07
    ctx.fillStyle = Math.random() > 0.5
      ? `rgba(255,255,255,${a})`
      : `rgba(0,0,0,${a})`
    ctx.fillRect(Math.random() * W, Math.random() * H, 1.5, 1.5)
  }

  /* 涟漪波纹装饰 */
  ctx.strokeStyle = 'rgba(255,255,255,0.14)'
  ctx.lineWidth = 0.8
  for (let y = 5; y < H; y += 8) {
    ctx.beginPath()
    for (let x = 0; x <= W; x += 2) {
      const wy = y + Math.sin((x + y) * 0.06) * 1.8
      x === 0 ? ctx.moveTo(x, wy) : ctx.lineTo(x, wy)
    }
    ctx.stroke()
  }

  /* 中心提示文字 */
  ctx.save()
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'
  ctx.font = `${Math.min(H * 0.44, 13)}px serif`
  ctx.fillStyle = 'rgba(255,255,255,0.28)'
  ctx.fillText('🦝', W / 2, H / 2 - 5)
  ctx.font = `bold ${Math.min(H * 0.18, 7)}px 'PingFang SC', sans-serif`
  ctx.fillStyle = 'rgba(255,255,255,0.55)'
  ctx.fillText('刮', W / 2, H / 2 + 7)
  ctx.restore()

  ctx.globalCompositeOperation = 'destination-out'
  canvases[`${r}-${c}`] = { canvas, ctx, W, H, cleared: false }
}

function scratchAt(r, c, x, y) {
  const cv = canvases[`${r}-${c}`]; if (!cv || cv.cleared) return
  cv.ctx.beginPath(); cv.ctx.arc(x, y, 22, 0, Math.PI * 2); cv.ctx.fill()
  checkCellCleared(r, c)
}

function checkCellCleared(r, c) {
  const cv = canvases[`${r}-${c}`]; if (!cv || cv.cleared) return
  const pw = cv.canvas.width, ph = cv.canvas.height
  const data = cv.ctx.getImageData(0, 0, pw, ph).data
  let cleared = 0
  for (let i = 3; i < data.length; i += 4) if (data[i] < 128) cleared++
  if (cleared / (pw * ph) > 0.4) markCellCleared(r, c)
}

function markCellCleared(r, c) {
  const key = `${r}-${c}`; const cv = canvases[key]
  if (!cv || cv.cleared) return
  cv.cleared = true; clearedCells.add(key)
  progressPct.value = Math.round(clearedCells.size / (ROW_COUNT * CELLS_PER_ROW) * 100)
  if (rowRevealed.value[r]) return
  const done = []
  for (let cc = 0; cc < CELLS_PER_ROW; cc++)
    if (canvases[`${r}-${cc}`]?.cleared) done.push(rowData[r].cells[cc])
  if (done.length >= 2) {
    if (!done.every(v => v === done[0])) revealRow(r)
    else if (done.length === 3) revealRow(r)
  }
}

function revealRow(r) {
  const arr = [...rowRevealed.value]; arr[r] = true; rowRevealed.value = arr
  if (rowData[r].win) {
    setTimeout(() => {
      for (let c = 0; c < CELLS_PER_ROW; c++) markCellCleared(r, c)
      finalReveal()
      for (let rr = 0; rr < ROW_COUNT; rr++)
        if (!rowRevealed.value[rr]) autoRevealRow(rr, rr * 80)
    }, 300)
  } else {
    setTimeout(() => {
      for (let c = 0; c < CELLS_PER_ROW; c++) markCellCleared(r, c)
      if (!allDone.value && rowRevealed.value.every(v => v)) finalReveal()
    }, 400)
  }
}

function autoRevealRow(r, delay) {
  setTimeout(() => {
    if (rowRevealed.value[r]) return
    const arr = [...rowRevealed.value]; arr[r] = true; rowRevealed.value = arr
    for (let c = 0; c < CELLS_PER_ROW; c++) markCellCleared(r, c)
  }, delay)
}

function finalReveal() {
  if (allDone.value) return
  allDone.value = true
  setTimeout(() => { 
    showModal.value = true; 
    launchConfetti();
    
    // 取消了以前的纯前端存 localStorage，现在转为保存至后端记录
    // 只有当用户没有参与过时才发请求（防止已经中过奖的人刷新发复重记录）
    if (!hasPlayed.value) {
      const hasWon = rowData.some(r => r.win)
      if (hasWon) {
        post('/api/v1/scratch', {
          is_win: true,
          prize_name: MASCOTS[winMascotIdx.value].name
        }).catch(err => console.error('Failed to save record', err))
      }
    }
  }, 400)
}

function getXY(canvas, e) {
  const rect = canvas.getBoundingClientRect()
  const s = e.touches ? e.touches[0] : e
  return { x: s.clientX - rect.left, y: s.clientY - rect.top }
}
function onMouseDown(e, r, c) { isDown = true; const p = getXY(e.target, e); scratchAt(r, c, p.x, p.y) }
function onMouseMove(e, r, c) { if (!isDown) return; const p = getXY(e.target, e); scratchAt(r, c, p.x, p.y) }
function onMouseUp() { isDown = false }
function onTouchStart(e, r, c) { isDown = true; const p = getXY(e.target, e); scratchAt(r, c, p.x, p.y) }
function onTouchMove(e) {
  if (!isDown) return
  const t = e.touches[0], el = document.elementFromPoint(t.clientX, t.clientY)
  if (el?.classList.contains('cell-canvas') && el.id.startsWith('canvas-')) {
    const parts = el.id.split('-')
    const p = getXY(el, e); scratchAt(parseInt(parts[1]), parseInt(parts[2]), p.x, p.y)
  }
}
function onTouchEnd() { isDown = false }
function globalMouseUp() { isDown = false }

function skipAll() {
  if (allDone.value) return; skipDisabled.value = true
  for (let r = 0; r < ROW_COUNT; r++) {
    ;(function(row) {
      setTimeout(() => {
        for (let c = 0; c < CELLS_PER_ROW; c++) {
          const cv = canvases[`${row}-${c}`]
          if (cv && !cv.cleared) {
            cv.ctx.save(); cv.ctx.globalCompositeOperation = 'destination-out'
            cv.ctx.fillStyle = 'rgba(0,0,0,1)'; cv.ctx.fillRect(0, 0, cv.W, cv.H); cv.ctx.restore()
          }
          markCellCleared(row, c)
        }
      }, row * 100)
    })(r)
  }
}

function showHint() { hintShown.value = true }

async function onSave() { 
  const modalEl = document.querySelector('.result-modal')
  if (!modalEl) return

  showToast('正在生成截图...', 'info')
  const saveBtn = document.querySelector('.btn-save')
  const closeBtn = document.querySelector('.modal-close')
  if (saveBtn) saveBtn.style.visibility = 'hidden'
  if (closeBtn) closeBtn.style.visibility = 'hidden'

  try {
    const canvas = await html2canvas(modalEl, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#fffef5'
    })
    const imgData = canvas.toDataURL('image/png')
    
    const a = document.createElement('a')
    a.href = imgData
    a.download = `苏州七狸-山塘限定凭证-${Date.now()}.png`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    
    showToast('凭证已成功保存到相册！', 'success')
  } catch (e) {
    console.error(e)
    showToast('截图生成失败', 'error')
  } finally {
    if (saveBtn) saveBtn.style.visibility = 'visible'
    if (closeBtn) closeBtn.style.visibility = 'visible'
  }
}

function launchConfetti() {
  /* 使用 app 主调色 */
  const colors = ['#7baec8', '#f5c8a8', '#a8d8c8', '#f8e4b0', '#c8a8d8', '#fff', '#f8cdd0']
  for (let i = 0; i < 80; i++) {
    setTimeout(() => {
      const sz = 5 + Math.random() * 8
      const id = Date.now() + i + Math.random()
      confettiPieces.value.push({ id, style: {
        left: Math.random() * 100 + 'vw', top: 0,
        background: colors[Math.floor(Math.random() * colors.length)],
        width: sz + 'px', height: sz + 'px',
        borderRadius: Math.random() > 0.5 ? '50%' : '2px',
        animationDuration: 1.8 + Math.random() * 2.5 + 's',
        animationDelay: Math.random() * 0.5 + 's',
      }})
      setTimeout(() => { confettiPieces.value = confettiPieces.value.filter(p => p.id !== id) }, 4000)
    }, i * 20)
  }
}

const hasPlayed = ref(false)

onMounted(async () => {
  document.addEventListener('mouseup', globalMouseUp)
  
  try {
    const res = await get('/api/v1/scratch/my')
    if (res.data.win_count > 0 && res.data.records?.length > 0) {
      hasPlayed.value = true
      showToast('您已参与过刮奖活动啦！', 'info', 2000)
      
      const record = res.data.records[0]
      const idx = MASCOTS.findIndex(m => m.name === record.prize_name)
      if (idx !== -1) {
        winMascotIdx.value = idx
        // Update rowData immediately purely for visual matching in the modal logic
        const winRow = rowData.find(r => r.win)
        if (winRow) {
          winRow.cells = [idx, idx, idx]
        }
      }
      
      allDone.value = true
      showModal.value = true
    } else {
      setTimeout(() => {
        for (let r = 0; r < ROW_COUNT; r++)
          for (let c = 0; c < CELLS_PER_ROW; c++) initCellCanvas(r, c)
      }, 100)
    }
  } catch (err) {
    console.error(err)
    // 失败依然加载刮卡初始
    setTimeout(() => {
      for (let r = 0; r < ROW_COUNT; r++)
        for (let c = 0; c < CELLS_PER_ROW; c++) initCellCanvas(r, c)
    }, 100)
  }
})
onBeforeUnmount(() => { document.removeEventListener('mouseup', globalMouseUp) })
</script>

<style scoped>
/* ══════════════════════════════════════════
   设计令牌 — 与 app 整体色系保持一致
   主调：蓝灰 #7baec8 / 米白 #f0f4f8
   强调：暖橙米 #f5c8a8 / 薄荷绿 #a8d8c8
   ══════════════════════════════════════════ */
:root {
  --bg-base:   #e8f4ef;
  --bg-card:   #f0f8f4;
  --blue-main: #7bc8a4;
  --blue-deep: #5aaa82;
  --blue-soft: #ddf3e8;
  --mint:      #a8d8bc;
  --mint-soft: #d6f0e8;
  --warm:      #f5c8a8;
  --warm-soft: #fef3e8;
  --text-main: #3a604b;
  --text-sub:  #6a907b;
  --gold:      #c9973e;
  --gold-soft: #f5e9cc;
}

.scratch-view {
  position: relative;
  display: flex;
  flex-direction: column;
  height: 100dvh;
  max-width: 430px;
  margin: 0 auto;
  /* ★ 与截图一致的蓝灰背景 */
  background: #e0ede7;
  overflow: hidden;
  font-family: 'PingFang SC', 'Noto Sans SC', 'Hiragino Sans GB', sans-serif;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}

/* ══ 顶栏 ══ */
.top-card {
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
  background: linear-gradient(158deg, #4eb97b 0%, #328e60 45%, #1c7649 100%);
  z-index: 10;
}

.tc-texture {
  position: absolute; inset: 0;
  background-image: repeating-linear-gradient(
    48deg,
    rgba(255,255,255,0.018) 0px, rgba(255,255,255,0.018) 1px,
    transparent 1px, transparent 9px
  );
  pointer-events: none; z-index: 0;
}

.tc-glow {
  position: absolute;
  top: -40px; right: 60px;   /* 光晕偏左，给狸猫让位 */
  width: 140px; height: 140px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(201,168,76,0.16) 0%, transparent 65%);
  pointer-events: none; z-index: 0;
}

/* ── 主内容：左文右图 ── */
.ticket-main-row {
  position: relative; z-index: 1;
  display: flex;
  align-items: flex-end;      /* 狸猫底部对齐波浪线 */
  padding: 10px 12px 0 14px;
  gap: 6px;
}

.ticket-left {
  flex: 1;
  min-width: 0;
  padding-bottom: 10px;
}

/* meta 行：返回键 + 编号 + 角标 */
.ticket-top-meta {
   display: flex;
  align-items: center;
  margin-bottom: 7px;
}

.back-btn {
  background: #50b67b;
  border: 1px solid #3cae73;
  color: #ffffff;
  border-radius: 20px;
  position: relative;
  top: 2px;
  left: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  white-space: nowrap;
  padding: 6px 14px;
  line-height: 1;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background 0.18s, border-color 0.18s, transform 0.18s;
}

.back-btn:active {
  background: #4ab16b;
  border-color: #47a86a;
  transform: scale(0.98);
}

.serial-block {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center; 
  gap: 2px;
}

.serial-label {
  font-size: 0.52rem;
  color: rgba(255, 255, 255, 0.52);
  letter-spacing: 0.06em;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1px 6px;
  border-radius: 4px;
  line-height: 1.5;
  display: inline-block;
}

.serial-num {
  font-size: 0.50rem;
  color: rgba(255,255,255,0.38);
  letter-spacing: 0.06em;
  padding-left: 2px;
}



/* 金色分割线 */
.ticket-gold-rule {
  height: 1px;
  margin-bottom: 8px;
  background: linear-gradient(
    90deg,
    rgba(201,168,76,0.55) 0%,
    rgba(245,228,168,0.95) 50%,
    rgba(201,168,76,0.20) 100%
  );
}

/* 文字区 */
.ticket-text-block {text-align: center; }

.header-title {
  margin: 0 0 3px;
  
  font-size: 1.9rem;
  font-weight: 900;
  letter-spacing: 0.20em;
  color: #fffdf5;
  font-family: 'Ma Shan Zheng', 'STKaiti', 'Kaiti SC', cursive;
  text-shadow:
    0 0 28px rgba(198, 187, 156, 0.3),
    0 2px 8px rgba(0,0,0,0.32);
  line-height: 1;
}

.header-subtitle {
  font-size: 0.58rem;
  letter-spacing: 0.10em;
  color: rgba(255,255,255,0.55);
  margin-bottom: 7px;
  
}

.strip-rule-pill {
  display: inline-block;
  font-size: 0.52rem;
  padding: 3px 10px;
  border-radius: 999px;
  background: rgba(255, 251, 240, 0.9);
  border: 1px solid rgba(76, 201, 151, 0.48);
  color: #3da069;
  letter-spacing: 0.04em;
  font-weight: 600;
}

/* ── 右侧狸猫 ── */
.ticket-right {
  flex-shrink: 0;
  width: 90px;
  display: flex;
  align-items: flex-end;
   position: absolute;
  right: 12px;
  bottom: 14px;  /* 24px 是波浪高度，让狸猫底部对齐波浪 */
  width: 90px;
}

.ticket-mascot {
  width: 88px;
  height: 88px;
  object-fit: contain;
  filter: drop-shadow(0 4px 16px rgba(20, 100, 69, 0.22));
  animation: mascotFloat 3.5s ease-in-out infinite;
}

@keyframes mascotFloat {
  0%,100% { transform: translateY(0); }
  50%     { transform: translateY(-6px); }
}

/* 波浪 */
.hero-wave {
  position: relative; z-index: 1;
  height: 24px; line-height: 0;
}
.hero-wave svg { width: 100%; height: 100%; display: block; }
/* ══ 滚动区 ══ */
.scroll-body {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
}


/* ══ 主体 ══ */
.ticket-shell {
  padding: 0 14px 14px;
  background: #deede7;
}

/* ══ 刮奖面板 ══ */
.scratch-panel {
  margin-top: 14px;
  padding: 16px 14px 14px;
  border-radius: 22px;
  background: #fffaf0;
  box-shadow: 0 4px 20px rgba(90, 180, 128, 0.08), 0 1px 4px rgba(90, 180, 123, 0.06);
  border: 1px solid rgba(140, 215, 176, 0.25);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.panel-title-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
}

.panel-icon { font-size: 1rem; }

.panel-title {
  font-size: 0.88rem;
  color: #3a7860;
  font-weight: 700;
  letter-spacing: 0.08em;
}

.panel-mini-tip {
  font-size: 0.8rem;
  color: #4c6c60;
  padding: 4px 10px;
  border-radius: 999px;
  background: #deede7;
  border: 1px solid rgba(120, 200, 173, 0.3);
}

/* ══ 刮奖表格 ══ */
.rows-wrap {
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(140, 220, 185, 0.3);
  background: #e9f3ed;
  box-shadow: 0 2px 8px rgba(90, 180, 156, 0.04);
}

.scratch-row {
  display: flex;
  align-items: stretch;
  min-height: 64px;
  border-bottom: 1px solid rgba(140, 220, 209, 0.15);
  transition: background 0.4s ease;
}

.scratch-row:nth-child(even) { background: rgba(210, 228, 221, 0.726); }
.scratch-row:last-child { border-bottom: none; }

.scratch-row.revealed { animation: rowReveal 0.55s ease forwards; }

.scratch-row.won {
  background: linear-gradient(90deg, #dde3e2 0%, #dae4e1 50%, #d2e6e0 100%);
}

@keyframes rowReveal {
  0%   { background: #d8ede7; }
  50%  { background: #c3ebdb; }
  100% { background: rgba(236, 241, 239, 0.96); }
}

.row-label {
  width: 40px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(120, 210, 189, 0.08);
  border-right: 1px solid rgba(86, 137, 113, 0.18);
}

.row-label span {
  font-size: 0.46rem;
  color: #5aaa85;
  writing-mode: vertical-lr;
  letter-spacing: 0.1em;
  font-weight: 600;
}

.row-cells {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 10px;
}

/* ══ 刮奖格： ══ */
.scratch-cell {
  flex: 1;
  height: 44px;
  border-radius: 12px;
  position: relative;
  overflow: hidden;
  cursor: crosshair;
  /* 柔和蓝灰描边 */
  border: 1.5px solid rgba(80, 161, 138, 0.35);
  /* 底层背景 */
  background: linear-gradient(145deg, #d4ebe5 0%, #dceae9 100%);
  box-shadow:
    0 2px 6px rgba(90, 180, 170, 0.1),
    inset 0 1px 0 rgba(255,255,255,0.80);
}

.cell-prize {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  background: linear-gradient(180deg, #fffaf0 0%, #fffaf0 100%);
  pointer-events: none;
}

.cp-img {
  width: 30px; height: 30px;
  object-fit: contain;
  filter: drop-shadow(0 1px 3px rgba(0,0,0,0.08));
}

.cell-canvas {
  position: absolute; inset: 0;
  width: 100%; height: 100%;
  display: block;
  touch-action: none;
  border-radius: 11px;
}

.row-result {
  width: 58px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-left: 1px solid rgba(140, 220, 192, 0.15);
  padding: 6px;
}

.result-badge {
  min-width: 44px;
  font-size: 0.44rem;
  padding: 4px 6px;
  border-radius: 999px;
  letter-spacing: 0.02em;
  text-align: center;
  line-height: 1.5;
  opacity: 0;
  transition: opacity 0.35s, transform 0.35s;
  transform: scale(0.84);
}

.result-badge.show  { opacity: 1; transform: scale(1); }

.result-badge.win {
  background: linear-gradient(135deg, #ade1d5, #7ad8bf80);
  color: #2e6858;
  border: 1px solid rgba(80, 200, 154, 0.5);
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(80, 94, 200, 0.18);
}

.result-badge.lose {
  background: #dce0de;
  color: #3c4b45;
  border: 1px solid rgba(140, 190, 178, 0.2);
}

/* ══ 进度条 ══ */
.progress-strip {
  margin: 14px 0 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.prog-label {
  font-size: 0.58rem;
  color: #639e90;
  white-space: nowrap;
}

.prog-track {
  flex: 1;
  height: 7px;
  background: #ddebe9;
  border-radius: 999px;
  overflow: visible;
  position: relative;
}

.prog-fill {
  height: 100%;
  background: linear-gradient(90deg, #7bc8b6 0%, #4e9f87 100%);
  border-radius: 999px;
  transition: width 0.25s ease;
  position: relative;
}

.prog-glow {
  position: absolute;
  top: 50%; transform: translate(-50%, -50%);
  width: 10px; height: 10px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 0 6px 3px rgba(123, 200, 167, 0.55);
  pointer-events: none;
  transition: left 0.25s ease;
}

.prog-pct {
  font-size: 0.62rem;
  color: #5aaa97;
  font-weight: 700;
  white-space: nowrap;
  min-width: 28px;
  text-align: right;
}

/* ══ 跳过按钮 ══ */
.skip-wrap {
  margin: 14px 0 2px;
  text-align: center;
}

.btn-skip {
  background: #deede7;
  border: 1.5px dashed rgba(100, 210, 150, 0.55);
  color: #498966;
  font-family: inherit;
  font-size: 0.62rem;
  letter-spacing: 0.06em;
  padding: 9px 22px;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.2s, opacity 0.2s;
}

.btn-skip:hover:not(:disabled) { background: #deede7; }
.btn-skip:disabled { opacity: 0.45; cursor: default; }

/* ══ 分隔装饰 ══ */
.section-divider {
  text-align: center;
  margin: 16px 0 0;
  color: rgba(120, 215, 185, 0.55);
  font-size: 0.7rem;
  letter-spacing: 0.3em;
}

.divider-icon { opacity: 0.5; }

/* ══ 折叠卡 ══ */
.fold-card {
  margin-top: 10px;
  border-radius: 18px;
  background: #fffaf0;
  border: 1px solid rgba(140, 220, 203, 0.25);
  box-shadow: 0 2px 10px rgba(90, 180, 165, 0.05);
  overflow: hidden;
}

.fold-summary {
  list-style: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  padding: 14px 16px;
  color: #3a786a;
  font-size: 0.76rem;
  font-weight: 600;
  letter-spacing: 0.06em;
}

.fold-summary::-webkit-details-marker { display: none; }

.fold-summary-left {
  display: flex;
  align-items: center;
  gap: 7px;
}

.fold-icon { font-size: 0.9rem; }

.fold-arrow {
  font-style: normal;
  font-size: 1rem;
  color: #7eb9b0;
  transition: transform 0.25s;
}

details[open] .fold-arrow { transform: rotate(90deg); }

.fold-content { padding: 0 14px 14px; }

.game-instruction {
  text-align: center;
  font-size: 0.62rem;
  color: #467869;
  letter-spacing: 0.03em;
  line-height: 2;
  padding: 12px;
  background: #deede7;
  border-radius: 12px;
  border: 1px solid rgba(140, 220, 203, 0.2);
}

/* ══ 幸运数字 ══ */
.lucky-numbers-row {
  padding: 4px 0 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.lucky-num {
  width: 40px; height: 40px;
  border: 1.5px solid rgba(120, 215, 185, 0.55);
  border-radius: 12px;
  background: linear-gradient(180deg, #f1fcf8 0%, #d4e5e0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: #3a785d;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(90, 180, 161, 0.08);
  flex-shrink: 0;
}

.lucky-op {
  font-size: 0.8rem;
  color: #8ac8c2;
  flex-shrink: 0;
}

.lucky-hint-text {
  text-align: center;
  font-size: 0.6rem;
  color: #558986;
  padding: 2px 8px 8px;
  line-height: 1.7;
  letter-spacing: 0.04em;
}

.lucky-table {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 4px 0 10px;
  justify-content: center;
}

.lt-item {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  min-height: 28px;
  background: #fbfbef;
  border: 1px solid rgba(117, 198, 198, 0.3);
  border-radius: 999px;
  padding: 4px 10px 4px 6px;
  white-space: nowrap;
}

.lt-remainder {
  width: 17px; height: 17px;
  background: rgba(90, 180, 162, 0.14);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.52rem;
  color: #4a9a8d;
  font-weight: 700;
  flex-shrink: 0;
}

.lt-img { width: 17px; height: 17px; object-fit: contain; }

.lt-name {
  font-size: 0.50rem;
  color: #5a9a8f;
  letter-spacing: 0.03em;
}

.hint-row {
  display: flex;
  justify-content: center;
  padding: 6px 0 2px;
}

.btn-hint {
  background: #deede7;
  border: 1.5px dashed rgba(85, 181, 151, 0.55);
  color: #428070;
  font-family: inherit;
  font-size: 0.62rem;
  letter-spacing: 0.06em;
  padding: 8px 18px;
  border-radius: 999px;
  cursor: pointer;
}

.lazy-answer {
  font-size: 0.66rem;
  color: #3a8a77;
  letter-spacing: 0.05em;
  padding: 6px 0;
  animation: fadeInUp 0.35s ease;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ══ 底部说明 ══ */
.footer-note {
  text-align: center;
  font-size: 0.54rem;
  color: #8ac8b3;
  padding: 16px 18px 0;
  letter-spacing: 0.04em;
  line-height: 1.9;
}

/* ══ 弹窗 ══ */
.result-modal-overlay {
  position: absolute; inset: 0;
  background: rgba(30, 70, 68, 0.4);
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  backdrop-filter: blur(6px);
}

.modal-fade-enter-active,
.modal-fade-leave-active { transition: opacity 0.35s ease; }
.modal-fade-enter-from,
.modal-fade-leave-to { opacity: 0; }

.result-modal {
  position: relative;
  width: 100%;
  max-width: 340px;
  /* 和 app 卡片一致的米白色 */
  background: linear-gradient(180deg, #eef7f5 0%, #def9f5 100%);
  border: 1.5px solid rgba(120, 220, 190, 0.4);
  border-radius: 26px;
  padding: 28px 20px 20px;
  text-align: center;
  box-shadow:
    0 16px 40px rgba(31, 95, 77, 0.18),
    inset 0 1px 0 rgba(233, 241, 237, 0.9);
  animation: modalPop 0.4s cubic-bezier(0.34,1.56,0.64,1) forwards;
}

@keyframes modalPop {
  from { transform: scale(0.88) translateY(18px); opacity: 0; }
  to   { transform: scale(1) translateY(0); opacity: 1; }
}

.modal-close {
  position: absolute;
  top: 14px; left: 16px;
  background: #bfdfd1;
  border: 1px solid rgba(140, 220, 208, 0.35);
  width: 28px; height: 28px;
  border-radius: 50%;
  font-size: 0.8rem;
  color: #6aaa9a;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}

/* 弹窗顶部装饰星星 */
.modal-confetti-strip {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 8px;
  
}

.mc-dot {
  font-size: 0.6rem;
  color: #6ab09a;
  animation: starPulse 1.6s ease-in-out infinite;
  opacity: 0.7;
}

@keyframes starPulse {
  0%,100% { opacity: 0.4; transform: scale(0.8); }
  50%     { opacity: 1;   transform: scale(1.2); }
}

.modal-badge {
  display: inline-block;
  margin-bottom: 8px;
  padding: 4px 14px;
  border-radius: 999px;
  background: rgba(90,140,180,0.10);
  border: 1px solid rgba(93, 171, 149, 0.4);
  color: #4a9a85;
  font-size: 0.56rem;
  letter-spacing: 0.12em;
  font-weight: 600;
}

.win-title {
  font-size: 1.10rem;
  color: #2e6a5f;
  letter-spacing: 0.06em;
  margin-bottom: 14px;
  font-weight: 800;
}

/* 获奖卡片 */
.win-prize-card {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  margin-bottom: 14px;
  background: linear-gradient(135deg, #cff1e8 0%, #b8f3ea 100%);
  border: 1px solid rgba(140, 230, 217, 0.35);
  border-radius: 18px;
  padding: 14px;
  overflow: hidden;
}

.win-prize-bg-circle {
  position: absolute;
  width: 120px; height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(87, 143, 127, 0.15) 0%, transparent 70%);
  left: -10px; top: -20px;
  pointer-events: none;
}

.win-prize-img {
  width: 72px; height: 72px;
  object-fit: contain;
  filter: drop-shadow(0 4px 14px rgba(32, 81, 68, 0.14));
  flex-shrink: 0;
  position: relative; z-index: 1;
}

.float-anim { animation: floatPrize 3s ease-in-out infinite; }

@keyframes floatPrize {
  0%,100% { transform: translateY(0); }
  50%     { transform: translateY(-8px); }
}

.win-prize-info { text-align: left; position: relative; z-index: 1; }

.win-prize-name {
  font-size: 1.16rem;
  color: #204c41;
  letter-spacing: 0.05em;
  font-weight: 800;
}

.win-prize-desc {
  font-size: 0.58rem;
  color: #5a989a;
  margin-top: 4px;
  line-height: 1.75;
  
}

.win-prize-label {
  font-size: 0.54rem;
  color: #318f6e;
  background: rgba(90, 220, 166, 0.12);
  border: 1px solid rgba(90, 220, 159, 0.25);
  display: inline-block;
  padding: 3px 8px;
  border-radius: 999px;
  margin-top: 5px;
  letter-spacing: 0.04em;
  
}

/* 兑换步骤 */
.redeem-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-bottom: 12px;
  border-top: 1px dashed rgba(33, 73, 57, 0.4);
  padding-top: 12px;
}

.rs-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  flex: 1;
}

.rs-arrow {
  font-size: 0.9rem;
  color: #9de2c6;
  padding-bottom: 18px;
}

.rs-icon {
  width: 34px; height: 34px;
  background: #caeadb;
  border: 1px solid rgba(140, 220, 188, 0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.rs-label {
  font-size: 0.58rem;
  color: #5a9a8b;
  text-align: center;
  line-height: 1.6;
}

.note-band {
  background: #ade6cd;
  border: 1px solid rgba(140, 220, 201, 0.25);
  border-radius: 12px;
  padding: 9px 12px;
  font-size: 0.56rem;
  color: #114933;
  line-height: 1.9;
  text-align: center;
  margin-bottom: 12px;
}

.btn-save {
  width: 100%;
  padding: 13px;
  /* 和 app 主色一致的蓝色按钮 */
  background: linear-gradient(135deg, #7bc8b3 0%, #5aaa99 100%);
  color: #fff;
  border: none;
  border-radius: 14px;
  font-family: inherit;
  font-size: 0.86rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  cursor: pointer;
  box-shadow: 0 6px 18px rgba(90, 180, 159, 0.28);
  transition: opacity 0.2s;
}

.btn-save:active { opacity: 0.85; }

/* ══ Tab Bar ══ */
.tab-bar {
  position: fixed;
  bottom: 0;
  left: 50%; transform: translateX(-50%);
  width: 100%; max-width: 430px;
  background: rgba(255,255,255,0.96);
  border-top: 1px solid rgba(140, 220, 201, 0.2);
  backdrop-filter: blur(16px) saturate(1.2);
  -webkit-backdrop-filter: blur(16px) saturate(1.2);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 8px 0 calc(8px + env(safe-area-inset-bottom));
  border-radius: 20px 20px 0 0;
  box-shadow: 0 -4px 16px rgba(90, 180, 164, 0.06);
  z-index: 100;
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  cursor: pointer;
  flex: 1;
  color: #a0ccba;
  transition: color 0.2s;
}

.tab-item--active { color: #5ab896; }

.tab-label {
  font-size: 10px;
  color: inherit;
  letter-spacing: 0.05em;
}

/* ══ 彩带 ══ */
.confetti-piece {
  position:absolute;
  pointer-events: none;
  z-index: 999;
  animation: confettiFall linear forwards;
}

@keyframes confettiFall {
  0%   { transform: translateY(-10px) rotate(0deg); opacity: 1; }
  100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}
</style>