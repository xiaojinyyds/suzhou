<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Toast, Dialog } from 'vant'
import { useRouter } from 'vue-router'
import request from '@/uitls/request'
import { uploadPhoto } from '@/api/admin'
import type { UploaderFileListItem } from 'vant'

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
  created_at: string
}

const statues = ref<Statue[]>([])
const loading = ref(false)
const showEdit = ref(false)
const editMode = ref<'create' | 'edit'>('create')
const currentStatue = ref<Statue | null>(null)
const uploading = ref(false)
const fileList = ref<UploaderFileListItem[]>([])

// 表单数据
const formData = ref({
  name: '',
  icon: '',
  latitude: 0,
  longitude: 0,
  radius: 100,
  introduction: '',
  history: '',
  cultural_value: '',
  images: [] as string[],
  order_index: 0
})

// 获取景点列表
const fetchStatues = async () => {
  loading.value = true
  try {
    const response: any = await request.get('/api/v1/admin/statues')
    
    if (response.code === 200) {
      statues.value = response.data || []
    } else {
      Toast.fail(response.message || '获取景点列表失败')
    }
  } catch (error: any) {
    console.error('获取景点列表失败:', error)
    Toast.fail(error.detail || '获取景点列表失败')
  } finally {
    loading.value = false
  }
}

// 打开创建对话框
const openCreate = () => {
  editMode.value = 'create'
  formData.value = {
    name: '',
    icon: '',
    latitude: 0,
    longitude: 0,
    radius: 100,
    introduction: '',
    history: '',
    cultural_value: '',
    images: [],
    order_index: statues.value.length
  }
  fileList.value = []
  showEdit.value = true
}

// 打开编辑对话框
const openEdit = (statue: Statue) => {
  editMode.value = 'edit'
  currentStatue.value = statue
  formData.value = {
    name: statue.name,
    icon: statue.icon || '',
    latitude: statue.latitude,
    longitude: statue.longitude,
    radius: statue.radius,
    introduction: statue.introduction || '',
    history: statue.history || '',
    cultural_value: statue.cultural_value || '',
    images: statue.images || [],
    order_index: statue.order_index
  }
  // 初始化图片列表
  fileList.value = (statue.images || []).map((url: string, index: number) => ({
    url,
    isImage: true,
    status: 'done' as const,
    message: ''
  }))
  showEdit.value = true
}

// 关闭编辑对话框
const closeEdit = () => {
  showEdit.value = false
  currentStatue.value = null
  fileList.value = []
}

// 图片上传前的验证
const beforeRead = (file: File) => {
  const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
  if (!allowedTypes.includes(file.type)) {
    Toast.fail('请上传 JPG、PNG 或 WEBP 格式的图片')
    return false
  }
  
  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    Toast.fail('图片大小不能超过 5MB')
    return false
  }
  
  return true
}

// 图片上传后的处理
const afterRead = async (file: any) => {
  file.status = 'uploading'
  file.message = '上传中...'
  
  uploading.value = true
  try {
    const res: any = await uploadPhoto(file.file)
    if (!res || res.code !== 200) {
      Toast.fail(res?.message || '上传失败')
      file.status = 'failed'
      file.message = '上传失败'
      return
    }
    
    const uploadedUrl = res.data?.url
    if (uploadedUrl) {
      file.url = uploadedUrl
      file.status = 'done'
      file.message = ''
      
      // 添加到表单数据的 images 数组
      formData.value.images.push(uploadedUrl)
      Toast.success('上传成功')
    } else {
      Toast.fail('上传失败：未获取到图片地址')
      file.status = 'failed'
      file.message = '上传失败'
    }
  } catch (e: any) {
    Toast.fail(e?.detail || '上传失败')
    file.status = 'failed'
    file.message = '上传失败'
  } finally {
    uploading.value = false
  }
}

// 删除图片
const onDeleteImage = (file: UploaderFileListItem, detail: { index: number }) => {
  formData.value.images.splice(detail.index, 1)
  Toast.success('已删除')
}

// 提交表单
const submitForm = async () => {
  if (!formData.value.name) {
    Toast.fail('请输入景点名称')
    return
  }
  if (!formData.value.latitude || !formData.value.longitude) {
    Toast.fail('请输入经纬度')
    return
  }

  loading.value = true
  try {
    let response: any
    if (editMode.value === 'create') {
      response = await request.post('/api/v1/admin/statues', formData.value)
    } else {
      response = await request.put(
        `/api/v1/admin/statues/${currentStatue.value!.id}`,
        formData.value
      )
    }

    if (response.code === 200) {
      Toast.success(editMode.value === 'create' ? '创建成功' : '更新成功')
      closeEdit()
      fetchStatues()
    } else {
      Toast.fail(response.message || '操作失败')
    }
  } catch (error: any) {
    console.error('提交失败:', error)
    Toast.fail(error.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

// 切换景点状态
const toggleStatus = async (statue: Statue) => {
  const action = statue.is_active ? '禁用' : '启用'
  
  Dialog.confirm({
    title: '确认操作',
    message: `确定要${action}景点 "${statue.name}" 吗？`
  }).then(async () => {
    try {
      const response: any = await request.patch(
        `/api/v1/admin/statues/${statue.id}/toggle`
      )
      
      if (response.code === 200) {
        Toast.success(`${action}成功`)
        fetchStatues()
      } else {
        Toast.fail(response.message || `${action}失败`)
      }
    } catch (error: any) {
      console.error(`${action}失败:`, error)
      Toast.fail(error.detail || `${action}失败`)
    }
  }).catch(() => {
    // 用户取消
  })
}

// 删除景点
const deleteStatue = (statue: Statue) => {
  Dialog.confirm({
    title: '危险操作',
    message: `确定要删除景点 "${statue.name}" 吗？此操作不可恢复！`,
    confirmButtonText: '确认删除',
    confirmButtonColor: '#ee0a24'
  }).then(async () => {
    try {
      const response: any = await request.delete(
        `/api/v1/admin/statues/${statue.id}`
      )
      
      if (response.code === 200) {
        Toast.success('删除成功')
        fetchStatues()
      } else {
        Toast.fail(response.message || '删除失败')
      }
    } catch (error: any) {
      console.error('删除失败:', error)
      Toast.fail(error.detail || '删除失败')
    }
  }).catch(() => {
    // 用户取消
  })
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchStatues()
})
</script>

<template>
  <div class="statues-management">
    <!-- 头部 -->
    <div class="header">
      <van-icon name="arrow-left" class="back-icon" @click="goBack" />
      <span class="title">景点管理</span>
      <van-button type="primary" size="small" round @click="openCreate">
        <van-icon name="plus" /> 新增
      </van-button>
    </div>

    <!-- 景点列表 -->
    <div class="content">
      <van-pull-refresh v-model="loading" @refresh="fetchStatues">
        <div v-if="statues.length === 0" class="empty-state">
          <van-empty description="暂无景点数据" />
        </div>
        
        <div v-else class="statues-list">
          <div 
            v-for="statue in statues" 
            :key="statue.id"
            class="statue-item"
            :class="{ disabled: !statue.is_active }"
          >
            <div class="statue-header">
              <div class="name-section">
                <span class="icon">{{ statue.icon || '📍' }}</span>
                <span class="name">{{ statue.name }}</span>
                <van-tag v-if="!statue.is_active" type="danger" class="mini-tag">已禁用</van-tag>
              </div>
              <div class="actions">
                <van-icon name="edit" class="action-icon" @click="openEdit(statue)" />
              </div>
            </div>
            
            <div class="statue-info">
              <div class="info-row">
                <span class="label">坐标：</span>
                <span class="value">{{ statue.latitude.toFixed(6) }}, {{ statue.longitude.toFixed(6) }}</span>
              </div>
              <div class="info-row">
                <span class="label">半径：</span>
                <span class="value">{{ statue.radius }}米</span>
              </div>
              <div class="info-row" v-if="statue.introduction">
                <span class="label">简介：</span>
                <span class="value">{{ statue.introduction }}</span>
              </div>
            </div>
            
            <!-- 图片预览 -->
            <div class="statue-images" v-if="statue.images && statue.images.length > 0">
              <div class="images-label">图片：</div>
              <div class="images-grid">
                <van-image
                  v-for="(img, idx) in statue.images.slice(0, 4)"
                  :key="idx"
                  :src="img"
                  width="60"
                  height="60"
                  fit="cover"
                  radius="4"
                  class="image-item"
                />
                <div v-if="statue.images.length > 4" class="more-images">
                  +{{ statue.images.length - 4 }}
                </div>
              </div>
            </div>
            
            <div class="statue-footer">
              <van-button 
                size="small" 
                :type="statue.is_active ? 'warning' : 'success'" 
                @click="toggleStatus(statue)"
              >
                {{ statue.is_active ? '禁用' : '启用' }}
              </van-button>
              <van-button 
                size="small" 
                type="danger" 
                @click="deleteStatue(statue)"
              >
                删除
              </van-button>
            </div>
          </div>
        </div>
      </van-pull-refresh>
    </div>

    <!-- 编辑弹窗 -->
    <van-popup 
      v-model:show="showEdit" 
      position="bottom" 
      round 
      :style="{ height: '80%' }"
      closeable
    >
      <div class="edit-dialog">
        <div class="dialog-title">
          {{ editMode === 'create' ? '新增景点' : '编辑景点' }}
        </div>
        
        <van-form @submit="submitForm">
          <van-cell-group inset>
            <van-field
              v-model="formData.name"
              label="景点名称"
              placeholder="请输入景点名称"
              required
            />
            <van-field
              v-model="formData.icon"
              label="图标Emoji"
              placeholder="如：🗼 🏛️ 🌸"
            />
            <van-field
              v-model.number="formData.latitude"
              type="number"
              label="纬度"
              placeholder="如：31.329700"
              required
            />
            <van-field
              v-model.number="formData.longitude"
              type="number"
              label="经度"
              placeholder="如：120.596200"
              required
            />
            <van-field
              v-model.number="formData.radius"
              type="number"
              label="打卡半径"
              placeholder="单位：米"
            />
            <van-field
              v-model="formData.introduction"
              label="简介"
              type="textarea"
              rows="2"
              placeholder="简短介绍"
            />
            <van-field
              v-model="formData.history"
              label="历史背景"
              type="textarea"
              rows="2"
              placeholder="历史背景"
            />
            <van-field
              v-model="formData.cultural_value"
              label="文化价值"
              type="textarea"
              rows="2"
              placeholder="文化价值"
            />
            
            <!-- 图片上传 -->
            <van-field label="景点图片">
              <template #input>
                <van-uploader
                  v-model="fileList"
                  :max-count="9"
                  multiple
                  :before-read="beforeRead"
                  :after-read="afterRead"
                  @delete="onDeleteImage"
                  :disabled="uploading"
                >
                  <van-button 
                    icon="photograph" 
                    type="primary" 
                    size="small"
                    :loading="uploading"
                  >
                    {{ uploading ? '上传中...' : '上传图片' }}
                  </van-button>
                </van-uploader>
              </template>
            </van-field>
          </van-cell-group>
          
          <div style="margin: 16px;">
            <van-button 
              round 
              block 
              type="primary" 
              native-type="submit" 
              :loading="loading"
              :disabled="uploading"
            >
              {{ editMode === 'create' ? '创建' : '保存' }}
            </van-button>
          </div>
        </van-form>
      </div>
    </van-popup>
  </div>
</template>

<style lang="scss" scoped>
.statues-management {
  min-height: 100vh;
  background: #f7f8fa;
}

.header {
  background: linear-gradient(135deg, #1989fa 0%, #1a73e8 100%);
  padding: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #fff;
  box-shadow: 0 4px 12px rgba(25, 137, 250, 0.2);
  
  .back-icon {
    font-size: 20px;
    cursor: pointer;
  }
  
  .title {
    flex: 1;
    text-align: center;
    font-size: 18px;
    font-weight: 700;
  }
}

.content {
  padding: 16px;
}

.empty-state {
  padding: 60px 0;
}

.statues-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.statue-item {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  
  &.disabled {
    opacity: 0.6;
  }
  
  .statue-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    
    .name-section {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .icon {
        font-size: 24px;
      }
      
      .name {
        font-size: 16px;
        font-weight: 600;
        color: #333;
      }
    }
    
    .actions {
      .action-icon {
        font-size: 18px;
        color: #1989fa;
        padding: 4px;
        cursor: pointer;
      }
    }
  }
  
  .statue-info {
    margin-bottom: 12px;
    
    .info-row {
      display: flex;
      font-size: 13px;
      margin-bottom: 4px;
      
      .label {
        color: #969799;
        min-width: 60px;
      }
      
      .value {
        flex: 1;
        color: #333;
      }
    }
  }
  
  .statue-images {
    margin-bottom: 12px;
    
    .images-label {
      font-size: 13px;
      color: #969799;
      margin-bottom: 8px;
    }
    
    .images-grid {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      
      .image-item {
        border-radius: 4px;
        overflow: hidden;
      }
      
      .more-images {
        width: 60px;
        height: 60px;
        border-radius: 4px;
        background: #f7f8fa;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #969799;
        font-size: 13px;
        font-weight: 600;
      }
    }
  }
  
  .statue-footer {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
  }
}

.edit-dialog {
  padding: 16px;
  
  .dialog-title {
    font-size: 18px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 16px;
    color: #333;
  }
}

.mini-tag {
  font-size: 11px;
  padding: 0 8px;
  height: 20px;
  line-height: 20px;
}
</style>
