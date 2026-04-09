import { createRouter, createWebHashHistory, RouteRecordRaw } from "vue-router";
import Camera from '../views/camera/Camera.vue';
import PhotoGallery from '../views/photos/PhotoGallery.vue';

// 通过Vite的import.meta.glob()方法实现自动化导入路由
const mainRouterModules = import.meta.glob('../layout/*.vue')
const viewRouterModules = import.meta.glob('../views/**/*.vue')

// 子路由
const childRoutes = Object.keys(viewRouterModules).map((path)=>{	
	const childName = path.match(/\.\.\/views\/(.*)\.vue$/)[1].split('/')[1];
	return {
		path: `/${childName.toLowerCase()}`,
		name: childName,
		component: viewRouterModules[path]
	} 
})

// 手动添加管理员路由（支持嵌套路由）
const adminRoutes = [
	{
		path: '/admin',
		name: 'Admin',
		component: () => import('../views/admin/Admin.vue')
	},
	{
		path: '/admin/statues',
		name: 'AdminStatues',
		component: () => import('../views/admin/StatuesManagement.vue')
	}
]

// 手动添加景点详情路由
const detailRoutes = [
	{
		path: '/home/details/:id',
		name: 'HomeDetails',
		component: () => import('../views/home/HomeDetails.vue')
	}
]

// 拍照功能路由
const cameraRoutes = [
	{
		path: '/camera',
		name: 'Camera',
		component: Camera  // 使用静态导入以避免 Vite 缓存问题
	},
	{
		path: '/photos',
		name: 'PhotoGallery',
		component: PhotoGallery  // 照片墙页面
	}
]

// 根路由
const rootRoutes = Object.keys(mainRouterModules).map((path) => {
    const name = path.match(/\.\.\/layout\/(.*)\.vue$/)[1].toLowerCase();
    const routePath = `/${name}`;
    if (routePath === '/index') {
		return {
			path: '/',
			name,
			redirect: '/home',
			component: mainRouterModules[path],
			children: [...childRoutes, ...adminRoutes, ...detailRoutes, ...cameraRoutes]  // 合并所有路由
		};
    }
})

const routes: Array<RouteRecordRaw> = rootRoutes

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

// 简单解析 JWT，检查是否过期
function isTokenValid(token: string | null): boolean {
    if (!token) return false;
    try {
        const parts = token.split(".");
        if (parts.length !== 3) return false;
        // 处理 base64url -> base64
        const base64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
        const payloadJson = decodeURIComponent(
            atob(base64)
                .split("")
                .map(function (c) {
                    return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
                })
                .join("")
        );
        const payload: any = JSON.parse(payloadJson);
        if (!payload || !payload.exp) {
            // 没有 exp 就当作无效
            return false;
        }
        const now = Math.floor(Date.now() / 1000);
        return payload.exp > now;
    } catch (e) {
        return false;
    }
}

const whiteList = ["/login", "/register", "/forgotpassword"];

router.beforeEach((to, from, next) => {
    const path = to.path.toLowerCase();
    const token = (typeof window !== "undefined" && window.localStorage.getItem("access_token")) || null;
    const authed = isTokenValid(token);

    // 未登录或 token 过期：除了登录/注册，全部拦到登录页
    if (!authed) {
        if (whiteList.includes(path)) {
            return next();
        }
        return next({ path: "/login" });
    }

    // 已登录：访问登录/注册时，跳到首页
    if (whiteList.includes(path)) {
        return next({ path: "/home" });
    }

    return next();
});

export default router







