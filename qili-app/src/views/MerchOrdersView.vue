<template>
  <div class="orders-page">
    <header class="top-card">
      <button class="back-btn" @click="$router.back()">←</button>
      <h1 class="header-title">周边预约记录</h1>
      <div style="width: 32px"></div>
    </header>

    <div class="orders-content">
       <div v-if="orders.length === 0" class="empty-state">
          📝 还没有预约过任何周边哦~
       </div>
       <div v-else class="orders-list">
          <div v-for="order in orders" :key="order.id" class="order-card">
              <img :src="getImgUrl(order.product_id)" class="order-img" />
              <div class="order-info">
                 <div class="order-name">{{ order.product_name }}</div>
                 <div class="order-time">
                    <span class="icon">🕗</span>
                    预定于 {{ formatDate(order.created_at) }}
                 </div>
                 <div class="order-status">未提货</div>
              </div>
          </div>
       </div>
       
       <div v-if="orders.length > 0" class="pickup-hint">
          请凭此页面到「山塘街七狸文创店」出示给工作人员提货专属周边
       </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { get } from '@/utils/request'

const router = useRouter()
const orders = ref([])

onMounted(async () => {
  try {
    const res = await get('/api/v1/merch/orders/my')
    if (res.data && res.data.orders) {
      orders.value = res.data.orders
    }
  } catch(e) {
    console.error('获取订单列表失败:', e)
  }
})

// 复用一下原本图层的映射，或者简化成预先设定好的字典
const imgMap = {
  doll: new URL('@/assets/merch/娃娃.jpg', import.meta.url).href,
  towel: new URL('@/assets/merch/擦脸巾实物.png', import.meta.url).href,
  dish: new URL('@/assets/merch/豆皿实物.png', import.meta.url).href,
  tail: new URL('@/assets/merch/晃尾巴实物.png', import.meta.url).href,
  wallet: new URL('@/assets/merch/零钱包实物.png', import.meta.url).href,
  wood: new URL('@/assets/merch/木头挂件实物.png', import.meta.url).href,
  pillow: new URL('@/assets/merch/充棉包实物.png', import.meta.url).href,
  gacha: new URL('@/assets/merch/打卡棒.jpg', import.meta.url).href,
  'stamp-stick': new URL('@/assets/merch/打卡棒.jpg', import.meta.url).href
}

function getImgUrl(pid) {
  return imgMap[pid] || new URL('@/assets/merch/打卡棒.jpg', import.meta.url).href
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleString('zh-CN', {
    month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}
</script>

<style scoped>
.orders-page {
  display: flex;
  flex-direction: column;
  min-height: 100dvh;
  background-color: #f7f9f2;
  font-family: 'Ma Shan Zheng', cursive;
  max-width: 430px;
  margin: 0 auto;
}
.top-card {
  background: var(--skin-primary);
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  color: white;
  border-radius: 0 0 24px 24px;
  box-shadow: 0 2px 10px rgba(70, 94, 122, 0.12);
}
.back-btn {
  background: rgba(255,255,255,0.2);
  border: 1px solid rgba(255,255,255,0.4);
  color: white;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  padding-bottom: 2px;
}
.header-title {
  font-size: 20px;
  letter-spacing: 2px;
  margin: 0;
}
.orders-content {
  padding: 24px 16px;
}
.empty-state {
  text-align: center;
  color: #888;
  margin-top: 100px;
  font-family: 'ZCOOL XiaoWei', cursive;
  font-size: 16px;
  letter-spacing: 2px;
}
.orders-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.order-card {
  display: flex;
  background: white;
  border-radius: 16px;
  padding: 12px;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(74, 143, 111, 0.08);
  border: 1px solid rgba(74, 143, 111, 0.2);
}
.order-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  background: #fdfbf7;
  border-radius: 12px;
}
.order-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex: 1;
}
.order-name {
  font-size: 18px;
  color: var(--skin-main-text);
  margin-bottom: 4px;
  font-weight: 600;
  letter-spacing: 1px;
}
.order-time {
  font-size: 11px;
  color: #888;
  font-family: 'ZCOOL XiaoWei', cursive;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.order-time .icon {
  font-size: 12px;
}
.order-status {
  font-size: 12px;
  color: #d8832a;
  font-weight: bold;
  font-family: 'ZCOOL XiaoWei', cursive;
  background: rgba(216, 131, 42, 0.1);
  padding: 3px 10px;
  border-radius: 10px;
  align-self: flex-start;
}
.pickup-hint {
  text-align: center;
  color: var(--skin-primary);
  font-family: 'ZCOOL XiaoWei', cursive;
  font-size: 13px;
  margin-top: 30px;
  padding: 14px;
  background: rgba(74, 143, 111, 0.1);
  border: 1px dashed rgba(74, 143, 111, 0.4);
  border-radius: 12px;
  line-height: 1.6;
}
</style>
