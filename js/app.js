// 苏州打卡网站 - 主应用逻辑

// ========== 全局状态 ==========
let currentPage = 'statues';
let checkInData = [];
let cartData = [];
let currentStatue = null;

// ========== 初始化 ==========
document.addEventListener('DOMContentLoaded', function() {
    // 检查登录状态
    checkLoginStatus();
    
    // 加载用户数据
    loadUserData();
    
    // 渲染石像列表
    renderStatues();
    
    // 渲染甜品列表
    renderDesserts();
    
    // 加载购物车数据
    loadCartData();
});

// 检查登录状态
function checkLoginStatus() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    if (isLoggedIn !== 'true') {
        // 未登录，跳转到欢迎页
        location.href = 'welcome.html';
    }
}

// 加载用户数据
function loadUserData() {
    const userName = localStorage.getItem('userName') || '探索者';
    document.getElementById('userName').textContent = userName;
    document.getElementById('profileName').textContent = userName;
    
    // 加载打卡记录
    const savedCheckIns = localStorage.getItem('checkIns');
    if (savedCheckIns) {
        checkInData = JSON.parse(savedCheckIns);
        updateCheckInStatus();
    }
}

// 更新打卡状态
function updateCheckInStatus() {
    statuesData.forEach(statue => {
        const checked = checkInData.some(item => item.statueId === statue.id);
        statue.isChecked = checked;
    });
    
    // 更新进度
    updateProgress();
}

// 更新进度统计
function updateProgress() {
    const checkedCount = statuesData.filter(s => s.isChecked).length;
    const total = statuesData.length;
    const percentage = (checkedCount / total * 100).toFixed(1);
    
    document.getElementById('checkedCount').textContent = checkedCount;
    document.getElementById('statsProgressFill').style.width = percentage + '%';
}

// ========== 页面切换 ==========
function switchPage(page) {
    currentPage = page;
    
    // 更新导航状态
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
    
    // 更新页面内容
    document.querySelectorAll('.page-content').forEach(content => {
        content.classList.remove('active');
    });
    
    const pageConfig = {
        'statues': { 
            id: 'statuesPage', 
            title: '石像打卡', 
            subtitle: '发现苏州的历史印记' 
        },
        'face': { 
            id: 'facePage', 
            title: '人脸装饰', 
            subtitle: '记录美好瞬间' 
        },
        'dessert': { 
            id: 'dessertPage', 
            title: '苏式甜品', 
            subtitle: '品味江南美食' 
        },
        'progress': { 
            id: 'progressPage', 
            title: '我的进度', 
            subtitle: '查看探索成果' 
        }
    };
    
    const config = pageConfig[page];
    document.getElementById(config.id).classList.add('active');
    document.getElementById('headerTitle').textContent = config.title;
    document.getElementById('headerSubtitle').textContent = config.subtitle;
    
    // 显示/隐藏购物车按钮
    const cartFloat = document.getElementById('cartFloat');
    if (page === 'dessert' && getTotalCartQuantity() > 0) {
        cartFloat.classList.add('show');
    } else {
        cartFloat.classList.remove('show');
    }
}

// ========== 石像功能 ==========
function renderStatues() {
    const grid = document.getElementById('statuesGrid');
    grid.innerHTML = statuesData.map(statue => `
        <div class="statue-card ${statue.isChecked ? 'checked' : ''}" onclick="openStatueDetail(${statue.id})">
            <div class="statue-image">
                <div class="statue-badge ${statue.isChecked ? 'checked' : ''}">
                    ${statue.isChecked ? '已打卡' : '未打卡'}
                </div>
                <div style="font-size: 3.5rem;">${statue.icon}</div>
            </div>
            <div class="statue-info">
                <div class="statue-name">${statue.name}</div>
                <div class="statue-meta">
                    <div class="statue-distance">
                        📍 ${statue.distance}km
                    </div>
                    <div style="color: var(--primary-color); font-weight: 600;">
                        ${statue.isChecked ? '✓' : '→'}
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// 打开石像详情
function openStatueDetail(id) {
    currentStatue = statuesData.find(s => s.id === id);
    
    document.getElementById('modalIcon').textContent = currentStatue.icon;
    document.getElementById('modalTitle').textContent = currentStatue.name;
    document.getElementById('modalDescription').textContent = currentStatue.introduction;
    document.getElementById('modalDistance').textContent = currentStatue.distance + 'km';
    document.getElementById('modalStatus').textContent = currentStatue.isChecked ? '已打卡' : '未打卡';
    document.getElementById('modalStatus').style.color = currentStatue.isChecked ? 'var(--success-color)' : 'var(--text-light)';
    
    document.getElementById('statueModal').classList.add('active');
}

// 关闭模态框
function closeModal() {
    document.getElementById('statueModal').classList.remove('active');
}

// 打卡功能
function checkIn() {
    if (!currentStatue) return;
    
    if (currentStatue.isChecked) {
        showToast('你已经打卡过这个景点了！');
        return;
    }
    
    // 模拟GPS定位
    showToast('正在定位...');
    
    setTimeout(() => {
        // 模拟距离检查（实际应该用GPS计算）
        const inRange = Math.random() > 0.3; // 70%概率成功
        
        if (inRange) {
            // 打卡成功
            currentStatue.isChecked = true;
            
            // 保存到本地存储
            checkInData.push({
                statueId: currentStatue.id,
                statueName: currentStatue.name,
                timestamp: new Date().toISOString(),
                location: {
                    lat: currentStatue.latitude,
                    lng: currentStatue.longitude
                }
            });
            localStorage.setItem('checkIns', JSON.stringify(checkInData));
            
            // 更新UI
            renderStatues();
            updateProgress();
            closeModal();
            
            // 显示成功提示
            showSuccessAnimation(currentStatue.name);
        } else {
            // 距离太远
            showToast(`你距离${currentStatue.name}还有${currentStatue.distance}km，请靠近后再打卡！`, 'warning');
        }
    }, 1000);
}

// 显示成功动画
function showSuccessAnimation(statueName) {
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease;
    `;
    
    overlay.innerHTML = `
        <div style="text-align: center; color: white; animation: slideUp 0.5s ease;">
            <div style="font-size: 5rem; margin-bottom: 1rem;">🎉</div>
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">打卡成功！</div>
            <div style="font-size: 1.125rem; opacity: 0.9;">恭喜你完成 ${statueName} 的打卡</div>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    setTimeout(() => {
        overlay.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(overlay);
        }, 300);
    }, 2000);
}

// ========== 甜品功能 ==========
function renderDesserts() {
    const list = document.getElementById('dessertList');
    list.innerHTML = dessertsData.map(dessert => `
        <div class="dessert-card">
            <div class="dessert-image">${dessert.icon}</div>
            <div class="dessert-info">
                <div class="dessert-header">
                    <div class="dessert-name">${dessert.name}</div>
                    <div class="dessert-price">¥${dessert.price}</div>
                </div>
                <div class="dessert-desc">${dessert.description}</div>
                <div class="dessert-footer">
                    <div class="dessert-stock">库存 ${dessert.stock}</div>
                    <div class="quantity-control">
                        <button class="qty-btn" onclick="updateDessertQuantity(${dessert.id}, -1)">−</button>
                        <div class="qty-value" id="qty-${dessert.id}">0</div>
                        <button class="qty-btn" onclick="updateDessertQuantity(${dessert.id}, 1)">+</button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// 更新甜品数量
function updateDessertQuantity(dessertId, change) {
    const dessert = dessertsData.find(d => d.id === dessertId);
    const qtyElement = document.getElementById(`qty-${dessertId}`);
    
    let currentQty = parseInt(qtyElement.textContent);
    let newQty = Math.max(0, Math.min(dessert.stock, currentQty + change));
    
    qtyElement.textContent = newQty;
    
    // 更新购物车数据
    updateCartData(dessertId, newQty);
    
    // 更新购物车徽章
    updateCartBadge();
}

// 更新购物车数据
function updateCartData(dessertId, quantity) {
    const index = cartData.findIndex(item => item.dessertId === dessertId);
    
    if (quantity > 0) {
        if (index >= 0) {
            cartData[index].quantity = quantity;
        } else {
            cartData.push({ dessertId, quantity });
        }
    } else {
        if (index >= 0) {
            cartData.splice(index, 1);
        }
    }
    
    // 保存到本地存储
    localStorage.setItem('cart', JSON.stringify(cartData));
}

// 加载购物车数据
function loadCartData() {
    const saved = localStorage.getItem('cart');
    if (saved) {
        cartData = JSON.parse(saved);
        
        // 恢复UI显示
        cartData.forEach(item => {
            const qtyElement = document.getElementById(`qty-${item.dessertId}`);
            if (qtyElement) {
                qtyElement.textContent = item.quantity;
            }
        });
        
        updateCartBadge();
    }
}

// 更新购物车徽章
function updateCartBadge() {
    const total = getTotalCartQuantity();
    const badge = document.getElementById('cartBadge');
    const cartFloat = document.getElementById('cartFloat');
    
    badge.textContent = total;
    
    if (total > 0 && currentPage === 'dessert') {
        cartFloat.classList.add('show');
    } else {
        cartFloat.classList.remove('show');
    }
}

// 获取购物车总数量
function getTotalCartQuantity() {
    return cartData.reduce((sum, item) => sum + item.quantity, 0);
}

// 获取购物车总价
function getTotalCartPrice() {
    return cartData.reduce((sum, item) => {
        const dessert = dessertsData.find(d => d.id === item.dessertId);
        return sum + (dessert.price * item.quantity);
    }, 0);
}

// 显示购物车
function showCart() {
    if (cartData.length === 0) {
        showToast('购物车是空的！');
        return;
    }
    
    const items = cartData.map(item => {
        const dessert = dessertsData.find(d => d.id === item.dessertId);
        return `${dessert.name} x${item.quantity} = ¥${dessert.price * item.quantity}`;
    }).join('\n');
    
    const total = getTotalCartPrice();
    const message = `🛒 购物车\n\n${items}\n\n总计：¥${total}\n\n点击确定进行结算`;
    
    if (confirm(message)) {
        handleCheckout();
    }
}

// 处理结算
function handleCheckout() {
    showToast('正在跳转到支付页面...');
    
    setTimeout(() => {
        showToast('🎉 订单提交成功！\n订单号：' + generateOrderNumber());
        
        // 清空购物车
        cartData = [];
        localStorage.removeItem('cart');
        
        // 重置UI
        dessertsData.forEach(dessert => {
            const qtyElement = document.getElementById(`qty-${dessert.id}`);
            if (qtyElement) {
                qtyElement.textContent = '0';
            }
        });
        
        updateCartBadge();
    }, 1500);
}

// 生成订单号
function generateOrderNumber() {
    return 'SZ' + Date.now() + Math.floor(Math.random() * 1000);
}

// ========== 人脸装饰功能 ==========
function capturePhoto() {
    showToast('📸 照片已保存！');
    
    setTimeout(() => {
        showToast('赛博装饰效果已添加！\n你可以在"我的照片"中查看', 'success');
    }, 1000);
}

// 切换装饰效果
function selectDecoration(index) {
    document.querySelectorAll('.decoration-item').forEach((item, i) => {
        if (i === index) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

// ========== 工具函数 ==========
function showToast(message, type = 'info') {
    const colors = {
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FF9800',
        error: '#F44336'
    };
    
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: ${colors[type]};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        max-width: 80%;
        text-align: center;
        white-space: pre-line;
        animation: slideUp 0.3s ease;
    `;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 2000);
}

// 退出登录
function handleLogout() {
    if (confirm('确定要退出登录吗？')) {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('userName');
        location.href = 'welcome.html';
    }
}

// 点击模态框背景关闭
document.getElementById('statueModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeModal();
    }
});

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
    }
`;
document.head.appendChild(style);

