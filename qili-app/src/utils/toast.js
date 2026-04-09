export const showToast = (message, type = 'info', duration = 3000) => {
  // 防止重复快速点击出现堆叠，保留基础体验
  const existing = document.querySelector('.custom-toast-message');
  if (existing) {
    existing.remove();
  }

  const toast = document.createElement('div');
  toast.className = 'custom-toast-message';
  toast.textContent = message;
  
  // 设计现代化、具有游戏和古典结合风味的提示框样式
  // 适配 qili-app 的现有的颜色 --font-body
  Object.assign(toast.style, {
    position: 'fixed',
    top: '40px',
    left: '50%',
    transform: 'translateX(-50%) translateY(-20px)',
    background: type === 'error' ? 'rgba(255, 240, 240, 0.95)' : type === 'success' ? 'rgba(238, 253, 244, 0.95)' : 'rgba(255, 250, 240, 0.95)',
    color: type === 'error' ? '#d93025' : type === 'success' ? '#188038' : '#4f9674',
    border: `1.5px solid ${type === 'error' ? 'rgba(244, 199, 195, 0.6)' : type === 'success' ? 'rgba(183, 225, 205, 0.6)' : 'rgba(120, 150, 130, 0.45)'}`,
    padding: '14px 28px',
    borderRadius: '24px',
    boxShadow: '0 10px 30px rgba(79, 150, 116, 0.15)',
    fontSize: '15px',
    fontWeight: '600',
    fontFamily: '"ZCOOL XiaoWei", "Ma Shan Zheng", cursive, sans-serif',
    zIndex: '9999',
    opacity: '0',
    backdropFilter: 'blur(8px)',
    transition: 'all 0.35s cubic-bezier(0.18, 0.89, 0.32, 1.28)',
    pointerEvents: 'none',
    whiteSpace: 'nowrap',
  });

  document.body.appendChild(toast);

  // 触发弹簧出场动画
  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';
  });

  // 定时移除
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(-50%) translateY(-20px)';
    setTimeout(() => {
      if (document.body.contains(toast)) {
        document.body.removeChild(toast);
      }
    }, 350); // 等待淡出动画结束再移除DOM
  }, duration);
};
