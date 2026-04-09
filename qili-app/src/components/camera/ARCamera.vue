<template>
  <div class="ar-camera-page">
    <div class="camera-header">
      <button class="back-btn" @click="closeCamera">×</button>
      <div class="header-text">
        <div class="main-title">{{ pageMode === 'camera' ? 'AR 拍照' : '预览' }}</div>
      </div>
      <button
        v-if="pageMode === 'camera'"
        class="switch-btn"
        @click="switchCamera"
      >
        ↺
      </button>
      <div v-else class="header-placeholder"></div>
    </div>

    <div ref="viewContainerRef" class="view-container">
      <div v-if="loading || isGeneratingMask" class="loading-overlay">
        <div class="loader"></div>
        <p>{{ isGeneratingMask ? '正在生成相框遮罩...' : '正在启动相机...' }}</p>
      </div>

      <div
        v-show="!loading && !isGeneratingMask"
        class="camera-stage"
        :style="stageStyle"
      >
        <div v-show="pageMode === 'camera'" class="camera-layer">
          <video ref="videoRef" autoplay playsinline muted class="video-source"></video>
          <canvas ref="displayCanvasRef" class="render-canvas"></canvas>
          <div class="ar-screen-fx">
            <div class="fx-vignette"></div>
            <div class="fx-scanline"></div>
            <div class="fx-corners">
              <span class="corner corner-tl"></span>
              <span class="corner corner-tr"></span>
              <span class="corner corner-bl"></span>
              <span class="corner corner-br"></span>
            </div>
            <div class="fx-reticle">
              <span class="reticle-ring"></span>
              <span class="reticle-dot"></span>
            </div>
            <div class="fx-particles">
              <span v-for="i in 8" :key="i" class="particle" :style="{ '--i': i }"></span>
            </div>
            <div class="fx-status left">SUZHOU AR</div>
            <div class="fx-status right">{{ currentFrame?.name || 'AR 相框' }}</div>
          </div>
          <p class="hint-text text-shadow">请将脸部或景物对准中间圆框</p>
          <canvas ref="captureCanvasRef" class="capture-canvas"></canvas>
        </div>

        <div v-show="pageMode === 'preview'" class="preview-layer">
          <img :src="capturedImage" class="preview-img" alt="拍照预览" />
        </div>
      </div>
    </div>

      <div
        v-show="!loading && !isGeneratingMask && pageMode === 'camera'"
        class="bottom-controls"
        :class="{ 'bottom-controls--compact': frames.length <= 1 }"
      >
      <div v-if="frames.length > 1" class="frame-selector">
        <div
          v-for="frame in frames"
          :key="frame.id"
          class="frame-item"
          :class="{ active: selectedFrameId === frame.id }"
          @click="selectFrame(frame.id)"
        >
          <img :src="frame.url" class="frame-thumb" :alt="frame.name" />
          <span>{{ frame.name }}</span>
        </div>
      </div>

      <div class="action-bar">
        <div class="shutter-btn" :class="{ disabled: !cameraReady }" @click="takePhoto">
          <div class="inner-circle"></div>
        </div>
      </div>
    </div>

    <div v-show="!loading && pageMode === 'preview'" class="bottom-controls preview-actions">
      <button class="btn-cancel" :disabled="uploading" @click="retake">重拍</button>
      <button class="btn-confirm" :disabled="uploading" @click="uploadToServer">
        <span v-if="uploading" class="loader-small"></span>
        <span v-else>确认保存</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { frames } from '@/config/raccoonFrames'
import { post } from '@/utils/request'

const emit = defineEmits(['close', 'upload-success'])

const pageMode = ref('camera')
const loading = ref(true)
const cameraReady = ref(false)
const uploading = ref(false)
const facingMode = ref('user')
const isGeneratingMask = ref(false)

const videoRef = ref(null)
const viewContainerRef = ref(null)
const displayCanvasRef = ref(null)
const captureCanvasRef = ref(null)

const selectedFrameId = ref(frames[0]?.id ?? '')
const currentFrame = computed(() => frames.find((frame) => frame.id === selectedFrameId.value))
const capturedImage = ref('')
const stageRatio = ref(9 / 16)
const stageSize = ref({ width: 0, height: 0 })

let mediaStream = null
let resizeObserver = null
let renderFrameId = 0
let frameLoadToken = 0

const imageCache = new Map()
const frameImageRef = ref(null)
const blockerImageRef = ref(null)

const stageStyle = computed(() => {
  if (!stageSize.value.width || !stageSize.value.height) {
    return {}
  }

  return {
    width: `${stageSize.value.width}px`,
    height: `${stageSize.value.height}px`
  }
})

const getSourceSize = (source) => {
  if (!source) {
    return { width: 0, height: 0 }
  }

  if (source instanceof HTMLVideoElement) {
    return {
      width: source.videoWidth || 0,
      height: source.videoHeight || 0
    }
  }

  return {
    width: source.naturalWidth || source.width || 0,
    height: source.naturalHeight || source.height || 0
  }
}

const loadImage = (url) => {
  if (!url) {
    return Promise.resolve(null)
  }

  if (imageCache.has(url)) {
    return imageCache.get(url)
  }

  const promise = new Promise((resolve, reject) => {
    const img = new Image()
    img.crossOrigin = 'Anonymous'
    img.onload = () => resolve(img)
    img.onerror = reject
    img.src = url
  })

  imageCache.set(url, promise)
  return promise
}

const updateStageLayout = () => {
  const container = viewContainerRef.value
  if (!container) return

  const containerWidth = container.clientWidth
  const containerHeight = container.clientHeight

  if (!containerWidth || !containerHeight) return

  const ratio = stageRatio.value || 9 / 16
  let width = containerWidth
  let height = width / ratio

  if (height > containerHeight) {
    height = containerHeight
    width = height * ratio
  }

  stageSize.value = {
    width: Math.round(width),
    height: Math.round(height)
  }
}

const setupCanvas = (canvas) => {
  const width = stageSize.value.width
  const height = stageSize.value.height

  if (!canvas || !width || !height) return null

  const dpr = window.devicePixelRatio || 1
  const displayWidth = Math.max(1, Math.round(width * dpr))
  const displayHeight = Math.max(1, Math.round(height * dpr))

  if (canvas.width !== displayWidth || canvas.height !== displayHeight) {
    canvas.width = displayWidth
    canvas.height = displayHeight
  }

  canvas.style.width = `${width}px`
  canvas.style.height = `${height}px`

  const ctx = canvas.getContext('2d')
  if (!ctx) return null

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, width, height)
  return ctx
}

const drawFittedImage = (ctx, source, fit = 'cover', mirror = false, scale = 1) => {
  const { width: sourceWidth, height: sourceHeight } = getSourceSize(source)
  const targetWidth = stageSize.value.width
  const targetHeight = stageSize.value.height

  if (!sourceWidth || !sourceHeight || !targetWidth || !targetHeight) return

  const sourceRatio = sourceWidth / sourceHeight
  const targetRatio = targetWidth / targetHeight

  let drawWidth = targetWidth
  let drawHeight = targetHeight
  let drawX = 0
  let drawY = 0

  if (fit === 'cover') {
    if (sourceRatio > targetRatio) {
      drawHeight = targetHeight
      drawWidth = drawHeight * sourceRatio
      drawX = (targetWidth - drawWidth) / 2
    } else {
      drawWidth = targetWidth
      drawHeight = drawWidth / sourceRatio
      drawY = (targetHeight - drawHeight) / 2
    }
  } else {
    if (sourceRatio > targetRatio) {
      drawWidth = targetWidth
      drawHeight = drawWidth / sourceRatio
      drawY = (targetHeight - drawHeight) / 2
    } else {
      drawHeight = targetHeight
      drawWidth = drawHeight * sourceRatio
      drawX = (targetWidth - drawWidth) / 2
    }
  }

  if (scale !== 1) {
    const scaledWidth = drawWidth * scale
    const scaledHeight = drawHeight * scale
    drawX -= (scaledWidth - drawWidth) / 2
    drawY -= (scaledHeight - drawHeight) / 2
    drawWidth = scaledWidth
    drawHeight = scaledHeight
  }

  ctx.save()
  if (mirror) {
    ctx.translate(targetWidth, 0)
    ctx.scale(-1, 1)
  }
  ctx.drawImage(source, drawX, drawY, drawWidth, drawHeight)
  ctx.restore()
}

const drawAREffects = (ctx, width, height) => {
  const now = Date.now() / 1000
  const pulse = 0.55 + Math.sin(now * 2.1) * 0.12
  const sweepY = (now * 90) % height

  ctx.save()

  const vignette = ctx.createRadialGradient(
    width * 0.5,
    height * 0.42,
    width * 0.12,
    width * 0.5,
    height * 0.5,
    width * 0.72
  )
  vignette.addColorStop(0, 'rgba(255,255,255,0)')
  vignette.addColorStop(1, 'rgba(8,18,26,0.24)')
  ctx.fillStyle = vignette
  ctx.fillRect(0, 0, width, height)

  const glow = ctx.createLinearGradient(0, 0, width, height)
  glow.addColorStop(0, 'rgba(114, 232, 255, 0.14)')
  glow.addColorStop(0.45, 'rgba(255,255,255,0)')
  glow.addColorStop(1, 'rgba(255, 191, 110, 0.12)')
  ctx.fillStyle = glow
  ctx.fillRect(0, 0, width, height)

  ctx.strokeStyle = `rgba(147, 248, 255, ${pulse})`
  ctx.lineWidth = 2
  ctx.beginPath()
  ctx.arc(width / 2, height / 2, Math.min(width, height) * 0.165, 0, Math.PI * 2)
  ctx.stroke()

  ctx.strokeStyle = `rgba(255,255,255,${0.32 + pulse * 0.18})`
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(width * 0.38, height / 2)
  ctx.lineTo(width * 0.62, height / 2)
  ctx.moveTo(width / 2, height * 0.38)
  ctx.lineTo(width / 2, height * 0.62)
  ctx.stroke()

  ctx.fillStyle = 'rgba(255,255,255,0.12)'
  for (let i = 0; i < 14; i += 1) {
    const y = ((i + 1) * height) / 15
    ctx.fillRect(0, y, width, 1)
  }

  ctx.fillStyle = 'rgba(132, 245, 255, 0.22)'
  ctx.fillRect(0, sweepY, width, 2)
  ctx.fillStyle = 'rgba(132, 245, 255, 0.08)'
  ctx.fillRect(0, Math.max(0, sweepY - 18), width, 24)

  const corner = Math.min(width, height) * 0.08
  const margin = 16
  ctx.strokeStyle = 'rgba(255, 235, 179, 0.85)'
  ctx.lineWidth = 3
  ctx.beginPath()
  ctx.moveTo(margin, margin + corner)
  ctx.lineTo(margin, margin)
  ctx.lineTo(margin + corner, margin)
  ctx.moveTo(width - margin - corner, margin)
  ctx.lineTo(width - margin, margin)
  ctx.lineTo(width - margin, margin + corner)
  ctx.moveTo(margin, height - margin - corner)
  ctx.lineTo(margin, height - margin)
  ctx.lineTo(margin + corner, height - margin)
  ctx.moveTo(width - margin - corner, height - margin)
  ctx.lineTo(width - margin, height - margin)
  ctx.lineTo(width - margin, height - margin - corner)
  ctx.stroke()

  ctx.restore()
}

const renderScene = (canvas) => {
  const ctx = setupCanvas(canvas)
  if (!ctx) return

  const width = stageSize.value.width
  const height = stageSize.value.height

  ctx.fillStyle = '#fffdec'
  ctx.fillRect(0, 0, width, height)

  if (videoRef.value && cameraReady.value) {
    drawFittedImage(ctx, videoRef.value, 'cover', facingMode.value === 'user')
  }

  drawAREffects(ctx, width, height)

  if (blockerImageRef.value) {
    drawFittedImage(ctx, blockerImageRef.value, 'cover', false, 1.1)
  }

  if (frameImageRef.value) {
    drawFittedImage(ctx, frameImageRef.value, 'cover', false, 1.1)
  }
}

const renderLoop = () => {
  if (pageMode.value !== 'camera') return

  renderScene(displayCanvasRef.value)
  renderFrameId = window.requestAnimationFrame(renderLoop)
}

const startRenderLoop = () => {
  cancelRenderLoop()
  renderLoop()
}

const cancelRenderLoop = () => {
  if (renderFrameId) {
    window.cancelAnimationFrame(renderFrameId)
    renderFrameId = 0
  }
}

const generateBlockerMask = (imageUrl, bgColor = '#fffdec') => {
  return new Promise((resolve) => {
    isGeneratingMask.value = true
    const img = new Image()
    img.crossOrigin = 'Anonymous'
    img.src = imageUrl
    img.onload = () => {
      const canvas = document.createElement('canvas')
      const scale = Math.min(1, 400 / img.naturalWidth)
      canvas.width = Math.floor(img.naturalWidth * scale)
      canvas.height = Math.floor(img.naturalHeight * scale)
      const ctx = canvas.getContext('2d', { willReadFrequently: true })
      if (!ctx) {
        isGeneratingMask.value = false
        resolve('')
        return
      }

      ctx.drawImage(img, 0, 0, canvas.width, canvas.height)

      const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height)
      const data = imgData.data
      const state = new Uint8Array(canvas.width * canvas.height)
      const stack = []

      const isTransparent = (index) => data[index * 4 + 3] < 30

      const maybePush = (x, y) => {
        if (x < 0 || x >= canvas.width || y < 0 || y >= canvas.height) return
        const idx = y * canvas.width + x
        if (state[idx] === 0 && isTransparent(idx)) {
          state[idx] = 1
          stack.push(idx)
        }
      }

      for (let x = 0; x < canvas.width; x += 1) {
        maybePush(x, 0)
        maybePush(x, canvas.height - 1)
      }

      for (let y = 0; y < canvas.height; y += 1) {
        maybePush(0, y)
        maybePush(canvas.width - 1, y)
      }

      while (stack.length > 0) {
        const idx = stack.pop()
        const x = idx % canvas.width
        const y = Math.floor(idx / canvas.width)

        maybePush(x - 1, y)
        maybePush(x + 1, y)
        maybePush(x, y - 1)
        maybePush(x, y + 1)
      }

      let r = 255
      let g = 253
      let b = 236
      if (bgColor.startsWith('#') && bgColor.length === 7) {
        r = parseInt(bgColor.slice(1, 3), 16)
        g = parseInt(bgColor.slice(3, 5), 16)
        b = parseInt(bgColor.slice(5, 7), 16)
      }

      for (let i = 0; i < canvas.width * canvas.height; i += 1) {
        const p = i * 4
        if (state[i] === 1) {
          data[p] = r
          data[p + 1] = g
          data[p + 2] = b
          data[p + 3] = 255
        } else {
          data[p + 3] = 0
        }
      }

      ctx.putImageData(imgData, 0, 0)
      isGeneratingMask.value = false
      resolve(canvas.toDataURL('image/png'))
    }

    img.onerror = () => {
      isGeneratingMask.value = false
      resolve('')
    }
  })
}

const syncFrameAssets = async () => {
  const frame = currentFrame.value
  const token = ++frameLoadToken

  if (!frame) {
    frameImageRef.value = null
    blockerImageRef.value = null
    return
  }

  try {
    const frameImage = await loadImage(frame.url)
    if (token !== frameLoadToken) return

    frameImageRef.value = frameImage
    if (frameImage?.naturalWidth && frameImage?.naturalHeight) {
      stageRatio.value = frameImage.naturalWidth / frameImage.naturalHeight
    }
    updateStageLayout()

    const blockerUrl = await generateBlockerMask(frame.url, '#fffdec')
    if (token !== frameLoadToken) return

    blockerImageRef.value = blockerUrl ? await loadImage(blockerUrl) : null
    if (token !== frameLoadToken) return

    renderScene(displayCanvasRef.value)
  } catch (error) {
    console.error('Frame asset load failed:', error)
    if (token !== frameLoadToken) return
    frameImageRef.value = null
    blockerImageRef.value = null
  }
}

const initCamera = async () => {
  cancelRenderLoop()

  if (mediaStream) {
    mediaStream.getTracks().forEach((track) => track.stop())
  }

  loading.value = true
  cameraReady.value = false

  try {
    mediaStream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: facingMode.value,
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    })

    if (videoRef.value) {
      videoRef.value.srcObject = mediaStream
      await new Promise((resolve) => {
        videoRef.value.onloadedmetadata = resolve
      })
      await videoRef.value.play().catch((error) => {
        console.warn('Video play error:', error)
      })
    }

    cameraReady.value = true
    loading.value = false
    updateStageLayout()
    startRenderLoop()
  } catch (error) {
    console.error('Camera init failed:', error)
    loading.value = false
    alert('无法访问相机，请确认已授予浏览器摄像头权限，并且当前环境为 HTTPS。')
    emit('close')
  }
}

const selectFrame = (id) => {
  if (selectedFrameId.value === id) return
  selectedFrameId.value = id
}

const switchCamera = () => {
  facingMode.value = facingMode.value === 'user' ? 'environment' : 'user'
  initCamera()
}

const takePhoto = () => {
  if (!cameraReady.value || !captureCanvasRef.value) return

  try {
    renderScene(captureCanvasRef.value)
    capturedImage.value = captureCanvasRef.value.toDataURL('image/jpeg', 0.9)
    pageMode.value = 'preview'
    cancelRenderLoop()
  } catch (error) {
    console.error('Take photo failed:', error)
    alert('拍照合成失败，请重试。')
  }
}

const retake = () => {
  capturedImage.value = ''
  pageMode.value = 'camera'
  startRenderLoop()
}

const uploadToServer = async () => {
  if (!capturedImage.value) return

  uploading.value = true

  try {
    const base64Data = capturedImage.value.split(',')[1]
    const byteString = atob(base64Data)
    const buffer = new ArrayBuffer(byteString.length)
    const bytes = new Uint8Array(buffer)

    for (let i = 0; i < byteString.length; i += 1) {
      bytes[i] = byteString.charCodeAt(i)
    }

    const blob = new Blob([buffer], { type: 'image/jpeg' })
    const formData = new FormData()
    formData.append('image', blob, `ar_photo_${Date.now()}.jpg`)
    formData.append('decoration_type', selectedFrameId.value)

    await post('/api/v1/photos/upload', formData)

    uploading.value = false
    emit('upload-success')
    emit('close')
  } catch (error) {
    console.error('Upload failed:', error)
    alert(error.message || '上传失败，请检查网络或后端配置。')
    uploading.value = false
  }
}

const closeCamera = () => {
  emit('close')
}

watch(currentFrame, () => {
  syncFrameAssets()
}, { immediate: true })

watch(pageMode, (mode) => {
  if (mode === 'camera' && cameraReady.value) {
    startRenderLoop()
  } else {
    cancelRenderLoop()
  }
})

onMounted(() => {
  resizeObserver = new ResizeObserver(() => {
    updateStageLayout()
    renderScene(displayCanvasRef.value)
  })

  if (viewContainerRef.value) {
    resizeObserver.observe(viewContainerRef.value)
  }

  window.addEventListener('resize', updateStageLayout)
  initCamera()
})

onUnmounted(() => {
  cancelRenderLoop()
  resizeObserver?.disconnect()
  window.removeEventListener('resize', updateStageLayout)

  if (mediaStream) {
    mediaStream.getTracks().forEach((track) => track.stop())
  }
})
</script>

<style scoped>
.ar-camera-page {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  background: #000;
  color: #fff;
  font-family: 'Ma Shan Zheng', cursive;
}

.camera-header {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 16px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(8px);
}

.back-btn,
.switch-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: none;
  color: #fff;
  font-size: 24px;
  cursor: pointer;
}

.header-placeholder {
  width: 40px;
  height: 40px;
}

.main-title {
  font-size: 18px;
  letter-spacing: 2px;
}

.view-container {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 12px;
  background:
    radial-gradient(circle at top, rgba(255, 255, 255, 0.12), transparent 55%),
    #2c241d;
}

.camera-stage {
  position: relative;
  max-width: 100%;
  max-height: 100%;
  overflow: hidden;
  border-radius: 28px;
  background: #fffdec;
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.08),
    0 20px 60px rgba(0, 0, 0, 0.45);
}

.camera-layer,
.preview-layer {
  position: absolute;
  inset: 0;
}

.ar-screen-fx {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 2;
}

.fx-vignette,
.fx-scanline,
.fx-corners,
.fx-reticle,
.fx-particles {
  position: absolute;
  inset: 0;
}

.fx-vignette {
  background:
    radial-gradient(circle at center, rgba(255,255,255,0) 32%, rgba(8, 18, 26, 0.28) 100%),
    linear-gradient(135deg, rgba(114, 232, 255, 0.14), transparent 40%, rgba(255, 191, 110, 0.1));
}

.fx-scanline::before {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  top: -8%;
  height: 20%;
  background: linear-gradient(180deg, rgba(120, 245, 255, 0), rgba(120, 245, 255, 0.22), rgba(120, 245, 255, 0));
  filter: blur(8px);
  animation: ar-sweep 4.2s linear infinite;
}

.corner {
  position: absolute;
  width: 14%;
  height: 14%;
  border-color: rgba(255, 235, 179, 0.9);
  border-style: solid;
  border-width: 0;
}

.corner-tl {
  top: 16px;
  left: 16px;
  border-top-width: 3px;
  border-left-width: 3px;
  border-top-left-radius: 18px;
}

.corner-tr {
  top: 16px;
  right: 16px;
  border-top-width: 3px;
  border-right-width: 3px;
  border-top-right-radius: 18px;
}

.corner-bl {
  bottom: 16px;
  left: 16px;
  border-bottom-width: 3px;
  border-left-width: 3px;
  border-bottom-left-radius: 18px;
}

.corner-br {
  right: 16px;
  bottom: 16px;
  border-right-width: 3px;
  border-bottom-width: 3px;
  border-bottom-right-radius: 18px;
}

.fx-reticle {
  display: flex;
  align-items: center;
  justify-content: center;
}

.reticle-ring {
  width: 34%;
  aspect-ratio: 1;
  border-radius: 50%;
  border: 2px solid rgba(147, 248, 255, 0.78);
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.2) inset,
    0 0 24px rgba(114, 232, 255, 0.22);
  animation: reticle-pulse 2.4s ease-in-out infinite;
}

.reticle-dot {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255,255,255,0.9);
  box-shadow: 0 0 12px rgba(255,255,255,0.75);
}

.particle {
  position: absolute;
  left: calc(8% + (var(--i) * 10.5%));
  bottom: -12px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.92), rgba(119, 243, 255, 0.15));
  box-shadow: 0 0 12px rgba(119, 243, 255, 0.45);
  animation: float-particle calc(4.5s + (var(--i) * 0.2s)) linear infinite;
  animation-delay: calc(var(--i) * -0.45s);
  opacity: 0.72;
}

.fx-status {
  position: absolute;
  top: 16px;
  padding: 7px 10px;
  border-radius: 999px;
  backdrop-filter: blur(8px);
  background: rgba(12, 28, 38, 0.35);
  border: 1px solid rgba(255,255,255,0.16);
  color: rgba(242, 249, 250, 0.94);
  font-size: 11px;
  letter-spacing: 1.4px;
  text-transform: uppercase;
}

.fx-status.left {
  left: 16px;
}

.fx-status.right {
  right: 16px;
}

.video-source,
.capture-canvas {
  display: none;
}

.render-canvas,
.preview-img {
  display: block;
  width: 100%;
  height: 100%;
}

.preview-img {
  object-fit: cover;
}

.hint-text {
  position: absolute;
  left: 16px;
  right: 16px;
  bottom: 18px;
  z-index: 3;
  text-align: center;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.88);
}

.text-shadow {
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.75);
}

.loading-overlay {
  position: absolute;
  z-index: 20;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.loader {
  width: 36px;
  height: 36px;
  border: 4px solid rgba(255, 255, 255, 0.2);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loader-small {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.bottom-controls {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 16px 16px 32px;
  background: rgba(0, 0, 0, 0.85);
}

.bottom-controls--compact {
  padding-top: 20px;
}

.frame-selector {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 12px;
  scrollbar-width: none;
}

.frame-selector::-webkit-scrollbar {
  display: none;
}

.frame-item {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 6px;
  border: 2px solid transparent;
  border-radius: 12px;
  opacity: 0.6;
  transition: 0.2s;
}

.frame-item.active {
  border-color: #f7d06e;
  background: rgba(255, 255, 255, 0.1);
  opacity: 1;
}

.frame-thumb {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: contain;
  background: #333;
}

.frame-item span {
  font-size: 11px;
}

@keyframes ar-sweep {
  0% {
    transform: translateY(-115%);
  }

  100% {
    transform: translateY(620%);
  }
}

@keyframes reticle-pulse {
  0%, 100% {
    transform: scale(0.98);
    opacity: 0.72;
  }

  50% {
    transform: scale(1.03);
    opacity: 1;
  }
}

@keyframes float-particle {
  0% {
    transform: translate3d(0, 0, 0) scale(0.75);
    opacity: 0;
  }

  15% {
    opacity: 0.8;
  }

  100% {
    transform: translate3d(calc(((var(--i) % 2) * 10px) - 5px), -108%, 0) scale(1.1);
    opacity: 0;
  }
}

.action-bar {
  display: flex;
  align-items: center;
  justify-content: center;
}

.shutter-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  background: #fff;
  cursor: pointer;
  transition: transform 0.2s;
}

.shutter-btn:active {
  transform: scale(0.92);
}

.shutter-btn.disabled {
  pointer-events: none;
  opacity: 0.5;
}

.inner-circle {
  width: 60px;
  height: 60px;
  border: 2px solid #222;
  border-radius: 50%;
  background: #fff;
}

.preview-actions {
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  padding: 32px 16px 48px;
}

.btn-cancel,
.btn-confirm {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 140px;
  height: 48px;
  border: none;
  border-radius: 24px;
  font-family: inherit;
  font-size: 16px;
  font-weight: bold;
  letter-spacing: 2px;
  cursor: pointer;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.btn-confirm {
  background: linear-gradient(135deg, #a8d58c, #6eb770);
  color: #fff;
  box-shadow: 0 4px 12px rgba(110, 183, 112, 0.4);
}

@media (min-width: 768px) {
  .view-container {
    padding: 24px;
  }

  .bottom-controls {
    padding-left: 24px;
    padding-right: 24px;
  }
}
</style>
