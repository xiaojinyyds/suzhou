<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Toast } from 'vant'
import { uploadPhoto } from '@/api/photo'
import { effects, getEffectById, type Effect } from '@/config/effects'
import frameBg from '@/assets/images/背景.png'

const router = useRouter()

// 定义响应类型
interface ApiResponse {
  code: number
  message?: string
  data?: any
}

// 页面状态：camera（相机模式）| preview（预览模式）
const pageMode = ref<'camera' | 'preview'>('camera')

// Refs
const videoRef = ref<HTMLVideoElement>()
const guideCanvasRef = ref<HTMLCanvasElement>()
const captureCanvasRef = ref<HTMLCanvasElement>()
const containerRef = ref<HTMLDivElement>()

// State
const loading = ref(true)
const cameraReady = ref(false)
const uploading = ref(false)
let mediaStream: MediaStream | null = null
let animationId: number | undefined

// 特效相关
const selectedEffect = ref<string>('icecream') // 默认冰激凌特效
const currentEffect = computed(() => getEffectById(selectedEffect.value))

// 相框背景图
const frameImage = ref<HTMLImageElement | null>(null)

// 预加载相框图片
const loadFrameImage = () => {
  const img = new Image()
  img.src = frameBg
  img.onload = () => {
    frameImage.value = img
    console.log('✅ 相框图片加载完成')
  }
}

// 预览相关
const capturedImage = ref<string>('') // 拍摄的照片（base64）

// 动画参数
let animationTime = 0

// 装饰元素数据
interface Decoration {
  emoji: string
  x: number
  y: number
  scale: number
  rotation: number
  opacity: number
  speed: number
  angle: number
}

const decorations = ref<Decoration[]>([])

// 初始化相机
const initCamera = async () => {
  try {
    if (!videoRef.value) return

    // 请求相机权限
    mediaStream = await navigator.mediaDevices.getUserMedia({
      video: { 
        facingMode: 'user',
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    })

    // 绑定视频流
    videoRef.value.srcObject = mediaStream

    // 等待视频元数据加载
    await new Promise<void>((resolve) => {
      if (videoRef.value) {
        videoRef.value.onloadedmetadata = () => resolve()
      }
    })

    // 播放视频（非阻塞）
    videoRef.value.play().catch(e => console.warn('视频播放警告:', e))

    // 初始化 canvas
    await nextTick()
    initCanvas()

    // 初始化特效
    initDecorations()

    // 开始绘制
    startRenderLoop()

    cameraReady.value = true
    loading.value = false
  } catch (error: any) {
    console.error('相机初始化错误:', error)
    loading.value = false
    
    if (!mediaStream) {
      let message = '无法访问相机'
      if (error.name === 'NotAllowedError') message = '请允许相机权限'
      else if (error.name === 'NotFoundError') message = '未找到相机设备'
      else if (error.name === 'NotReadableError') message = '相机被占用'
      
      Toast.fail(message)
      setTimeout(() => router.back(), 2000)
    } else {
      cameraReady.value = true
    }
  }
}

// 初始化 Canvas
const initCanvas = () => {
  if (!containerRef.value || !guideCanvasRef.value) {
    console.error('❌ Canvas 初始化失败: 容器或 canvas ref 为空')
    return
  }
  
  const { clientWidth, clientHeight } = containerRef.value
  
  if (clientWidth === 0 || clientHeight === 0) {
    console.error('❌ Canvas 初始化失败: 容器尺寸为 0')
    setTimeout(initCanvas, 100)
    return
  }
  
  guideCanvasRef.value.width = clientWidth
  guideCanvasRef.value.height = clientHeight
  
  console.log('✅ Canvas 初始化成功:', { width: clientWidth, height: clientHeight })
}

// 初始化装饰元素
const initDecorations = () => {
  if (!currentEffect.value || currentEffect.value.decorations.length === 0) {
    decorations.value = []
    return
  }
  
  decorations.value = []
  const count = Math.min(10, currentEffect.value.decorations.length)
  
  for (let i = 0; i < count; i++) {
    const emojis = currentEffect.value.decorations
    decorations.value.push({
      emoji: emojis[Math.floor(Math.random() * emojis.length)],
      x: 0,
      y: 0,
      scale: 0.5 + Math.random() * 0.5,
      rotation: Math.random() * 360,
      opacity: 1,
      speed: 0.002 + Math.random() * 0.003,
      angle: (Math.PI * 2 / count) * i
    })
  }
}

// 切换特效
const selectEffect = (effectId: string) => {
  selectedEffect.value = effectId
  initDecorations()
}

// 渲染循环
const startRenderLoop = () => {
  const animate = () => {
    if (pageMode.value === 'camera') {
      drawFrame()
    }
    animationId = requestAnimationFrame(animate)
  }
  animate()
}

// 绘制每一帧
const drawFrame = () => {
  if (!guideCanvasRef.value) return
  const canvas = guideCanvasRef.value
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  
  if (canvas.width === 0 || canvas.height === 0) {
    console.warn('⚠️ Canvas 尺寸为 0，跳过绘制')
    return
  }
  
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  animationTime += 1
  
  // 绘制冰淇淋相框背景
  if (frameImage.value) {
    const img = frameImage.value
    const imgRatio = img.width / img.height
    const canvasRatio = canvas.width / canvas.height
    const scale = 1.3
    
    let drawWidth, drawHeight, drawX, drawY
    
    if (imgRatio > canvasRatio) {
      drawHeight = canvas.height*scale
      drawWidth = drawHeight * imgRatio
      drawX = (canvas.width - drawWidth) / 2
      drawY = 0
    } else {
      drawWidth = canvas.width*scale
      drawHeight = drawWidth / imgRatio
      drawX = 0
      drawY = (canvas.height - drawHeight) / 2
    }
    
    ctx.drawImage(img, drawX, drawY, drawWidth, drawHeight)
  }
  
  // 绘制提示文字
  ctx.font = 'bold 16px sans-serif'
  ctx.fillStyle = '#fff'
  ctx.textAlign = 'center'
  ctx.shadowColor = 'rgba(0, 0, 0, 0.8)'
  ctx.shadowBlur = 4
  ctx.fillText('请将面部对准圆框', canvas.width / 2, canvas.height - 180)
}

// 绘制装饰元素
const drawDecorations = (ctx: CanvasRenderingContext2D, cx: number, cy: number, r: number) => {
  decorations.value.forEach((deco, i) => {
    const currentAngle = deco.angle + animationTime * deco.speed * 5
    const distance = r + 40 + Math.sin(animationTime * 0.05 + i) * 10
    
    deco.x = cx + Math.cos(currentAngle) * distance
    deco.y = cy + Math.sin(currentAngle) * distance
    deco.rotation += 0.5
    
    ctx.save()
    ctx.translate(deco.x, deco.y)
    ctx.rotate(deco.rotation * Math.PI / 180)
    ctx.scale(deco.scale, deco.scale)
    
    ctx.shadowColor = '#FF69B4'
    ctx.shadowBlur = 10
    
    ctx.font = '32px Arial'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(deco.emoji, 0, 0)
    ctx.restore()
  })
}

// 拍照
const takePhoto = () => {
  if (!cameraReady.value || !captureCanvasRef.value || !videoRef.value || !guideCanvasRef.value) return
  
  try {
    const video = videoRef.value
    const guideCanvas = guideCanvasRef.value
    const canvas = captureCanvasRef.value
    const ctx = canvas.getContext('2d')
    
    if (!ctx) throw new Error('Canvas context missing')
    
    // 设置拍照 Canvas 尺寸
    canvas.width = guideCanvas.width
    canvas.height = guideCanvas.height
    
    // 计算视频绘制参数（object-fit: cover）
    const videoRatio = video.videoWidth / video.videoHeight
    const screenRatio = canvas.width / canvas.height
    
    let drawWidth, drawHeight, startX, startY
    
    if (videoRatio > screenRatio) {
      drawHeight = canvas.height
      drawWidth = drawHeight * videoRatio
      startX = -(drawWidth - canvas.width) / 2
      startY = 0
    } else {
      drawWidth = canvas.width
      drawHeight = drawWidth / videoRatio
      startX = 0
      startY = -(drawHeight - canvas.height) / 2
    }
    
    // 绘制视频底图（镜像）
    ctx.save()
    ctx.translate(canvas.width, 0)
    ctx.scale(-1, 1)
    ctx.drawImage(video, startX, startY, drawWidth, drawHeight)
    ctx.restore()
    
// 合成冰淇淋相框
if (frameImage.value) {
  const img = frameImage.value
  const imgRatio = img.width / img.height
  const canvasRatio = canvas.width / canvas.height
  const scale = 1.3
  
  let drawWidth, drawHeight, drawX, drawY
  
  if (imgRatio > canvasRatio) {
    drawHeight = canvas.height*scale
    drawWidth = drawHeight * imgRatio
    drawX = (canvas.width - drawWidth) / 2
    drawY = 0
  } else {
    drawWidth = canvas.width*scale
    drawHeight = drawWidth / imgRatio
    drawX = 0
    drawY = (canvas.height - drawHeight) / 2
  }
  
  ctx.drawImage(img, drawX, drawY, drawWidth, drawHeight)
}
    // 转换为 base64
    capturedImage.value = canvas.toDataURL('image/jpeg', 0.9)
    
    // 切换到预览模式
    pageMode.value = 'preview'
    
    Toast.success('拍照成功！')
  } catch (error) {
    console.error('拍照失败:', error)
    Toast.fail('拍照失败，请重试')
  }
}

// 重拍
const retake = () => {
  capturedImage.value = ''
  pageMode.value = 'camera'
}

// 上传
const uploadToServer = async () => {
  if (!capturedImage.value) return
  
  uploading.value = true
  
  try {
    // base64 转 Blob
    const base64Data = capturedImage.value.split(',')[1]
    const byteCharacters = atob(base64Data)
    const byteNumbers = new Array(byteCharacters.length)
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i)
    }
    const byteArray = new Uint8Array(byteNumbers)
    const blob = new Blob([byteArray], { type: 'image/jpeg' })
    
    // 上传
    const formData = new FormData()
    formData.append('image', blob, 'photo.jpg')
    formData.append('decoration_type', selectedEffect.value)
    
    const res: any = await uploadPhoto(formData)
    
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || '上传失败')
      uploading.value = false
      return
    }
    
    Toast.success('美好瞬间已记录！')
    setTimeout(() => {
      router.push('/photos') // 跳转到照片墙
    }, 1500)
  } catch (error: any) {
    console.error('❌ 上传异常:', error)
    console.error('❌ 错误详情:', error.response?.data || error.message)
    Toast.fail('上传失败，请重试')
    uploading.value = false
  }
}

// 清理资源
const cleanup = () => {
  if (animationId) cancelAnimationFrame(animationId)
  if (mediaStream) mediaStream.getTracks().forEach(track => track.stop())
}

// 生命周期
onMounted(() => {
  loadFrameImage()
  initCamera()
})
onUnmounted(cleanup)
const goBack = () => router.back()
</script>

<template>
  <div class="camera-page">
    <!-- 顶部导航 -->
    <div class="camera-header">
      <van-icon name="arrow-left" size="24" @click="goBack" />
      <div class="header-text">
        <div class="main-title">📸 {{ pageMode === 'camera' ? '拍照' : '预览' }}</div>
        <div class="sub-title">{{ pageMode === 'camera' ? '记录美好瞬间' : '确认后上传' }}</div>
      </div>
      <div style="width: 24px;"></div>
    </div>

    <!-- 加载中 -->
    <div v-if="loading" class="loading-overlay">
      <van-loading vertical color="#fff">启动相机中...</van-loading>
    </div>

    <!-- 相机模式 -->
    <div v-show="!loading && pageMode === 'camera'" class="camera-container" ref="containerRef">
      <!-- 视频底层 -->
      <video ref="videoRef" autoplay playsinline muted class="video-layer"></video>
      <!-- 特效覆盖层 -->
      <canvas ref="guideCanvasRef" class="overlay-layer"></canvas>
      <!-- 隐藏的合成 Canvas -->
      <canvas ref="captureCanvasRef" style="display: none;"></canvas>
    </div>

    <!-- 预览模式 -->
    <div v-show="!loading && pageMode === 'preview'" class="preview-container">
      <img :src="capturedImage" alt="拍摄照片" class="preview-image" />
    </div>

    <!-- 底部操作栏 - 相机模式 -->
    <div v-show="!loading && pageMode === 'camera'" class="camera-controls">
      <!-- 特效选择器 -->
      <div class="effect-selector">
        <div
          v-for="effect in effects"
          :key="effect.id"
          class="effect-item"
          :class="{ active: selectedEffect === effect.id }"
          @click="selectEffect(effect.id)"
        >
          <span class="effect-icon">{{ effect.icon }}</span>
          <span class="effect-name">{{ effect.name }}</span>
        </div>
      </div>

      <!-- 拍照按钮 -->
      <div class="action-bar">
        <div class="action-placeholder"></div>
        <div class="shutter-btn" @click="takePhoto" :class="{ disabled: !cameraReady }">
          <div class="inner-circle"></div>
        </div>
        <div class="action-placeholder"></div>
      </div>
    </div>

    <!-- 底部操作栏 - 预览模式 -->
    <div v-show="!loading && pageMode === 'preview'" class="preview-controls">
      <button class="preview-btn cancel-btn" @click="retake" :disabled="uploading">
        <van-icon name="replay" size="24" />
        <span>重拍</span>
      </button>
      <button class="preview-btn upload-btn" @click="uploadToServer" :disabled="uploading">
        <van-loading v-if="uploading" color="#fff" size="24" />
        <template v-else>
          <van-icon name="success" size="24" />
          <span>确认上传</span>
        </template>
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.camera-page {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: #000;
  display: flex;
  flex-direction: column;
}

.camera-header {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  color: #fff;
  z-index: 10;
  flex-shrink: 0;

  .header-text {
    text-align: center;
    .main-title { font-size: 16px; font-weight: bold; }
    .sub-title { font-size: 10px; opacity: 0.8; }
  }
}

.camera-container, .preview-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #000;
}

.video-layer {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scaleX(-1);
  display: block;
}

.overlay-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  background: #000;
}

.loading-overlay {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-controls {
  background: rgba(0, 0, 0, 0.9);
  padding: 16px;
  z-index: 10;
  flex-shrink: 0;
}

.effect-selector {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 16px;
  
  &::-webkit-scrollbar {
    display: none;
  }
  
  .effect-item {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 8px 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.1);
    border: 2px solid transparent;
    cursor: pointer;
    transition: all 0.3s;
    
    &.active {
      border-color: #00ff88;
      background: rgba(0, 255, 136, 0.2);
    }
    
    &:active {
      transform: scale(0.95);
    }
    
    .effect-icon {
      font-size: 28px;
    }
    
    .effect-name {
      font-size: 12px;
      color: #fff;
      white-space: nowrap;
    }
  }
}

.action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 0;
}

.action-placeholder {
  width: 72px;
}

.shutter-btn {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #fff;
  border: 4px solid rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  
  .inner-circle {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: #fff;
    border: 2px solid #000;
  }
  
  &:active:not(.disabled) {
    transform: scale(0.9);
  }
  
  &.disabled {
    opacity: 0.5;
  }
}

.preview-controls {
  display: flex;
  gap: 16px;
  padding: 24px 16px;
  background: rgba(0, 0, 0, 0.9);
  z-index: 10;
  flex-shrink: 0;
}

.preview-btn {
  flex: 1;
  height: 56px;
  border-radius: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  
  &:active:not(:disabled) {
    transform: scale(0.95);
  }
  
  &:disabled {
    opacity: 0.6;
  }
  
  &.cancel-btn {
    background: rgba(255, 255, 255, 0.15);
    color: #fff;
  }
  
  &.upload-btn {
    background: linear-gradient(135deg, #00ff88, #00aaff);
    color: #fff;
  }
}
</style>