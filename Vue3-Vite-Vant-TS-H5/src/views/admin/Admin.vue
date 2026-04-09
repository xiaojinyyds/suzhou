<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Toast } from 'vant'
import { useRouter } from 'vue-router'

const router = useRouter()

// 管理功能模块
const modules = ref([
  {
    id: 1,
    title: '景点管理',
    icon: 'location-o',
    color: '#1989fa',
    bgColor: 'rgba(25, 137, 250, 0.1)',
    path: '/admin/statues',
    description: '管理打卡景点信息'
  },
  {
    id: 2,
    title: '用户管理',
    icon: 'friends-o',
    color: '#07c160',
    bgColor: 'rgba(7, 193, 96, 0.1)',
    path: '/admin/users',
    description: '管理用户账户'
  },
  {
    id: 3,
    title: '打卡记录',
    icon: 'clock-o',
    color: '#ff976a',
    bgColor: 'rgba(255, 151, 106, 0.1)',
    path: '/admin/checkins',
    description: '查看所有打卡记录'
  },
  {
    id: 4,
    title: '数据统计',
    icon: 'bar-chart-o',
    color: '#7232dd',
    bgColor: 'rgba(114, 50, 221, 0.1)',
    path: '/admin/statistics',
    description: '查看统计数据'
  }
])

const goToModule = (path: string) => {
  if (path === '/admin/statues') {
    router.push(path)
  } else {
    Toast('该功能正在开发中')
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  // 验证管理员权限
  const userStr = localStorage.getItem('current_user')
  if (userStr) {
    const user = JSON.parse(userStr)
    if (user.role !== 'admin') {
      Toast.fail('无权限访问')
      router.replace('/home')
    }
  } else {
    Toast.fail('请先登录')
    router.replace('/login')
  }
})
</script>

<template>
  <div class="admin-page">
    <!-- 头部 -->
    <div class="admin-header">
      <div class="header-content">
        <van-icon name="arrow-left" class="back-icon" @click="goBack" />
        <div class="header-title">
          <van-icon name="shield-o" />
          <span>管理员后台</span>
        </div>
        <div class="header-placeholder"></div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="admin-content">
      <!-- 欢迎卡片 -->
      <div class="welcome-card">
        <div class="welcome-icon">👨‍💼</div>
        <div class="welcome-text">
          <div class="title">欢迎回来，管理员</div>
          <div class="subtitle">请选择需要管理的功能模块</div>
        </div>
      </div>

      <!-- 功能模块网格 -->
      <div class="modules-grid">
        <div 
          v-for="module in modules" 
          :key="module.id"
          class="module-card"
          @click="goToModule(module.path)"
        >
          <div class="module-icon" :style="{ background: module.bgColor }">
            <van-icon :name="module.icon" :style="{ color: module.color }" size="28" />
          </div>
          <div class="module-info">
            <div class="module-title">{{ module.title }}</div>
            <div class="module-desc">{{ module.description }}</div>
          </div>
          <van-icon name="arrow" class="arrow-icon" />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.admin-page {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f7f8fa 0%, #fff 100%);
}

.admin-header {
  background: linear-gradient(135deg, #ee0a24 0%, #ff4d4f 100%);
  padding: 20px 16px;
  box-shadow: 0 4px 12px rgba(238, 10, 36, 0.2);
  
  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #fff;
    
    .back-icon {
      font-size: 20px;
      cursor: pointer;
      padding: 8px;
      margin-left: -8px;
    }
    
    .header-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 18px;
      font-weight: 700;
    }
    
    .header-placeholder {
      width: 36px;
    }
  }
}

.admin-content {
  padding: 20px 16px;
}

.welcome-card {
  background: linear-gradient(135deg, #fff 0%, #f0f9ff 100%);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  
  .welcome-icon {
    font-size: 48px;
  }
  
  .welcome-text {
    flex: 1;
    
    .title {
      font-size: 18px;
      font-weight: 700;
      color: #333;
      margin-bottom: 4px;
    }
    
    .subtitle {
      font-size: 13px;
      color: #969799;
    }
  }
}

.modules-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.module-card {
  background: #fff;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s;
  cursor: pointer;
  
  &:active {
    transform: scale(0.98);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  }
  
  .module-icon {
    width: 56px;
    height: 56px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  
  .module-info {
    flex: 1;
    
    .module-title {
      font-size: 16px;
      font-weight: 600;
      color: #333;
      margin-bottom: 4px;
    }
    
    .module-desc {
      font-size: 13px;
      color: #969799;
    }
  }
  
  .arrow-icon {
    font-size: 16px;
    color: #c8c9cc;
  }
}
</style>
