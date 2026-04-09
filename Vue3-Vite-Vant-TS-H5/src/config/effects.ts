/**
 * 拍照特效配置
 */

export interface Effect {
  id: string
  name: string
  icon: string
  decorations: string[]
}

export const effects: Effect[] = [
  {
    id: 'none',
    name: '无特效',
    icon: '📷',
    decorations: []
  },
  {
    id: 'icecream',
    name: '冰激凌',
    icon: '🍦',
    decorations: ['🍦', '🍨', '🍧', '🧁', '🍭', '🍫', '🥤', '🍩', '🍪']
  },
  {
    id: 'stars',
    name: '星星',
    icon: '⭐',
    decorations: ['⭐', '✨', '💫', '🌟', '🌠', '🌌', '🔆', '💥']
  },
  {
    id: 'hearts',
    name: '爱心',
    icon: '💖',
    decorations: ['💖', '💕', '💗', '💝', '❤️', '💘', '💓', '💞']
  },
  {
    id: 'rainbow',
    name: '彩虹',
    icon: '🌈',
    decorations: ['🌈', '🦄', '🎨', '🎪', '🎭', '🎨', '🌺', '🌸']
  }
]

export const getEffectById = (id: string): Effect | undefined => {
  return effects.find(effect => effect.id === id)
}
