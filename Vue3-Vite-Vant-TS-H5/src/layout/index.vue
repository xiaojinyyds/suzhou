<script setup lang="ts">
import { ref, reactive, toRefs, computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

// 判断是否显示TabBar（管理员页面、详情页、相机页隐藏）
const showTabBar = computed(() => {
  return !route.path.startsWith('/admin') && !route.path.includes('/details') && route.path !== '/camera';
});

//底部tab栏相关
const useTabBar = () => {
  const state = reactive({
    tabBar: [
      {
        title: "打卡",
        to: {
          name: "Home",
        },
        icon: "location-o",
      },
      {
        title: "照片墙",
        to: {
          name: "PhotoGallery",
        },
        icon: "photo-o",
      },
      {
        title: "拍照",
        to: {
          name: "Camera",
        },
        icon: "photograph",
      },
      {
        title: "甜品",
        to: {
          name: "Dessert",
        },
        icon: "shopping-cart-o",
      },
      {
        title: "我的",
        to: {
          name: "About",
        },
        icon: "user-o",
      },
    ],
  });
  return toRefs(state);
};
const { tabBar } = useTabBar();

const handleChange = (value) => {
  // console.log(value,'valueeeeeee');
};
</script>

<template>
  <div class="app-container">
    <div class="layout-content" :class="{ 'no-tabbar': !showTabBar }">
      <keep-alive v-if="$route.meta.keepAlive">
        <router-view></router-view>
      </keep-alive>
      <router-view v-else></router-view>
      <RequestLoading></RequestLoading>
    </div>
    <div class="layout-footer" v-if="showTabBar">
      <TabBar :data="tabBar" @chang="handleChange"></TabBar>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.app-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.layout-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch; // iOS 平滑滚动
  padding-bottom: 50px; // TabBar 高度
  
  &.no-tabbar {
    padding-bottom: 0; // 管理员页面无需底部留白
  }
}

.layout-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}
</style>