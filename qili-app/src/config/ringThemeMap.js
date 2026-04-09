// src/config/ringThemeMap.js

const FIXED_SURFACE = {
  panelBg: 'rgba(255, 250, 241, 0.98)',   // 奶油白
  panelBg2: 'rgba(252, 246, 235, 0.98)',  // 奶油白第二层
  tabBg: 'rgba(252, 248, 240, 0.98)',     // 米白 tab
  tabText: '#7b8274',
}

export const DEFAULT_RING_THEME = {
  ...FIXED_SURFACE,

  panelBorder: 'rgba(214, 194, 150, 0.34)',
  softLine: 'rgba(214, 194, 150, 0.24)',
  mainText: '#4d5a67',
  subText: '#8a8d84',
  softChip: 'rgba(214, 194, 150, 0.10)',
  shadow: 'rgba(120, 110, 90, 0.05)',

  primaryBg: '#6f97c8',
  primaryDark: '#40688f',
  primaryMid: '#85add6',
  primaryLight: '#7aa2cf',
  primaryBtn: '#6f97c8',
  primaryBtnText: '#ffffff',

  headerBorder: 'rgba(214, 194, 150, 0.58)',

  cardBackTop: '#7fa6d0',
  cardBackBot: '#7098c4',
  cardBackBorder: 'rgba(120, 158, 200, 0.38)',
  cardBackText: 'rgba(255, 255, 255, 0.82)',
  storyWrapBg: 'rgba(192, 216, 234, 0.92)'
}

export const RING_THEME_MAP = {
  // 白公狸：黄绿书卷系
  baigong: {
    ...FIXED_SURFACE,

    panelBorder: 'rgba(233, 238, 136, 0.87)',
    softLine: 'rgba(196, 200, 126, 0.8)',
    mainText: '#74805f',
    subText: '#908d76',
    softChip: 'rgba(218, 192, 95, 0.10)',
    shadow: 'rgba(150, 150, 90, 0.06)',

    primaryBg: '#b9d06c',
    primaryDark: '#aec46c',
    primaryMid: '#bccb8d',
    primaryLight: '#b6d360',
    primaryBtn: '#b8d557',
    primaryBtnText: '#ffffff',

    headerBorder: 'rgba(190, 183, 104, 0.52)',

    cardBackTop: '#a3ba62',
    cardBackBot: '#94ab56',
    cardBackBorder: 'rgba(176, 180, 104, 0.40)',
    cardBackText: 'rgba(255, 250, 236, 0.90)',
    storyWrapBg: 'rgba(229, 237, 200, 0.92)',
  },

  // 彩云狸：珊瑚暖红系
  caiyun: {
    ...FIXED_SURFACE,

    panelBorder: 'rgba(233, 148, 122, 0.84)',
    softLine: 'rgba(231, 192, 178, 0.4)',
    mainText: '#64594d',
    subText: '#9a897d',
    softChip: 'rgba(225, 188, 167, 0.12)',
    shadow: 'rgba(190, 120, 108, 0.06)',

    primaryBg: '#f38e80',
    primaryDark: '#ef9380',
    primaryMid: '#e79f8f',
    primaryLight: '#dc8c7d',
    primaryBtn: '#e68b79',
    primaryBtnText: '#ffffff',

    headerBorder: 'rgba(222, 149, 133, 0.52)',

    cardBackTop: '#ec8a77',
    cardBackBot: '#dc9081',
    cardBackBorder: 'rgba(222, 149, 133, 0.40)',
    cardBackText: 'rgba(255, 247, 243, 0.90)',
    storyWrapBg: 'rgba(255, 133, 133, 0.3)',
  },

  // 分水狸：雾感丹宁蓝系
  fenshui: {
    ...FIXED_SURFACE,
   panelBorder: 'rgba(150, 180, 215, 0.49)',
softLine: 'rgba(195, 214, 236, 0.54)',
mainText: '#5a6a7e',
subText: '#92a0ae',
softChip: 'rgba(202, 225, 248, 0.18)',
shadow: 'rgba(120, 145, 178, 0.08)',

primaryBg: '#7ea6d1',
primaryDark: '#5d82ae',
primaryMid: '#92b6dd',
primaryLight: '#87add8',
primaryBtn: '#7ea6d1',
primaryBtnText: '#ffffff',

headerBorder: 'rgba(150, 180, 215, 0.58)',

cardBackTop: '#5d82ae',
cardBackBot: '#86a9d3',
cardBackBorder: 'rgba(183, 202, 228, 0.44)',
cardBackText: 'rgba(248, 252, 255, 0.92)',
storyWrapBg: 'rgba(207, 224, 243, 0.92)',
    
  },

  // 海涌狸：樱粉海盐系
  haiyong: {
    ...FIXED_SURFACE,

    panelBorder: 'rgba(244, 150, 169, 0.89)',
    softLine: 'rgba(236, 197, 205, 0.85)',
    mainText: '#625857',
    subText: '#9b8c8f',
    softChip: 'rgba(210, 232, 244, 0.12)',
    shadow: 'rgba(210, 150, 166, 0.06)',

    primaryBg: '#fb8ca7',
    primaryDark: '#e97d9a',
    primaryMid: '#e5a2b2',
    primaryLight: '#f097ad',
    primaryBtn: '#e7869e',
    primaryBtnText: '#ffffff',

    headerBorder: 'rgba(233, 174, 186, 0.54)',

    cardBackTop: '#eb7a96',
    cardBackBot: '#db758e',
    cardBackBorder: 'rgba(233, 174, 186, 0.42)',
    cardBackText: 'rgba(255, 246, 249, 0.90)',
    storyWrapBg: 'rgb(255, 218, 226)',
  },

  // 通贵狸：鎏金富贵系
  tonggui: {
    ...FIXED_SURFACE,

    panelBorder: 'rgba(210, 184, 115, 0.34)',
    softLine: 'rgba(226, 206, 153, 0.24)',
    mainText: '#655840',
    subText: '#9b8a63',
    softChip: 'rgba(238, 220, 168, 0.12)',
    shadow: 'rgba(176, 146, 74, 0.06)',

    primaryBg: '#e1b753',
    primaryDark: '#ddb65d',
    primaryMid: '#d4b15d',
    primaryLight: '#cda952',
    primaryBtn: '#dcb251',
    primaryBtnText: '#ffffff',

    headerBorder: 'rgba(210, 184, 115, 0.56)',

    cardBackTop: '#d4b25f',
    cardBackBot: '#caa650',
    cardBackBorder: 'rgba(210, 184, 115, 0.42)',
    cardBackText: 'rgba(255, 250, 236, 0.90)',
    storyWrapBg: 'rgba(242, 232, 201, 0.92)',
  },

  // 文昌狸：青玉文气系
  wenchang: {
    ...FIXED_SURFACE,

    panelBorder: 'rgba(121, 186, 180, 0.34)',
    softLine: 'rgba(182, 226, 213, 0.24)',
    mainText: '#4f605c',
    subText: '#869690',
    softChip: 'rgba(217, 186, 209, 0.10)',
    shadow: 'rgba(100, 160, 150, 0.06)',

    primaryBg: '#4a8f6f',
    primaryDark: '#478f72',
    primaryMid: '#79b8b2',
    primaryLight: '#70b1ab',
    primaryBtn: '#66a9a3',
    primaryBtnText: '#ffffff',

    headerBorder: 'rgba(121, 186, 180, 0.54)',

    cardBackTop: '#7ab8b3',
    cardBackBot: '#6cabA6',
    cardBackBorder: 'rgba(121, 186, 180, 0.42)',
    cardBackText: 'rgba(244, 252, 250, 0.90)',
    storyWrapBg: 'rgba(209, 239, 233, 0.92)',
  },

  // 美仁狸：冰蓝珠光系
  meiren: {
    ...FIXED_SURFACE,

    panelBorder: 'rgba(159, 193, 228, 0.53)',
    softLine: 'rgba(215, 221, 240, 0.56)',
    mainText: '#6a819a',
    subText: '#8d99a8',
    softChip: 'rgba(210, 212, 238, 0.12)',
    shadow: 'rgba(130, 165, 200, 0.06)',

    primaryBg: '#7fb2e0',
    primaryDark: '#7fb2e0',
    primaryMid: '#7fb2e0',
    primaryLight: '#7fb2e0',
    primaryBtn: '#95c7f4',
    primaryBtnText: '#ffffff',

    headerBorder: 'rgba(159, 194, 228, 0.56)',

    cardBackTop: '#9cc8eb',
    cardBackBot: '#8ebde3',
    cardBackBorder: 'rgba(159, 194, 228, 0.42)',
    cardBackText: 'rgba(246, 250, 255, 0.90)',
    storyWrapBg: 'rgba(220, 237, 253, 0.92)',
  },
}

export function applyThemeToRoot(ringId) {
  const theme = RING_THEME_MAP[ringId] || DEFAULT_RING_THEME;
  const root = document.documentElement;
  
  root.style.setProperty('--skin-panel-bg', theme.panelBg);
  root.style.setProperty('--skin-panel-bg-2', theme.panelBg2);
  root.style.setProperty('--skin-panel-border', theme.panelBorder);
  root.style.setProperty('--skin-soft-line', theme.softLine);
  root.style.setProperty('--skin-main-text', theme.mainText);
  root.style.setProperty('--skin-sub-text', theme.subText);
  root.style.setProperty('--skin-soft-chip', theme.softChip);
  root.style.setProperty('--skin-shadow', theme.shadow);
  root.style.setProperty('--skin-primary', theme.primaryBg);
  root.style.setProperty('--skin-primary-dark', theme.primaryDark);
  root.style.setProperty('--skin-primary-mid', theme.primaryMid);
  root.style.setProperty('--skin-primary-light', theme.primaryLight);
  root.style.setProperty('--skin-primary-btn', theme.primaryBtn);
  root.style.setProperty('--skin-primary-btn-text', theme.primaryBtnText);
  root.style.setProperty('--skin-tab-bg', theme.tabBg);
  root.style.setProperty('--skin-tab-text', theme.tabText);
  root.style.setProperty('--skin-header-border', theme.headerBorder);
  root.style.setProperty('--skin-card-back-top', theme.cardBackTop);
  root.style.setProperty('--skin-card-back-bot', theme.cardBackBot);
  root.style.setProperty('--skin-card-back-border', theme.cardBackBorder);
  root.style.setProperty('--skin-card-back-text', theme.cardBackText);
  root.style.setProperty('--skin-storywrap', theme.storyWrapBg);
  localStorage.setItem('selected-ring', ringId);
}

export function initGlobalTheme() {
  let ringId = 'wenchang';
  const userInfoStr = localStorage.getItem('user-info');
  if (userInfoStr) {
    try {
      const userInfo = JSON.parse(userInfoStr);
      if (userInfo.theme) ringId = userInfo.theme;
    } catch(e) {}
  }
  // Fallback to local storage if not logged in or backend hasn't synced
  const savedRing = localStorage.getItem('selected-ring');
  if (savedRing && (!userInfoStr || !JSON.parse(userInfoStr).theme)) {
    ringId = savedRing;
  }
  applyThemeToRoot(ringId);
}