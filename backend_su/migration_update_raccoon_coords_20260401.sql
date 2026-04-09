-- 2026-04-01
-- 七狸点位矫正（按最新实测值）
-- 说明：
-- 1) 白公狸坐标按需求保持不变
-- 2) 其余 6 点更新为最新坐标
-- 3) 其余 6 点的半径更新为 1000 米

UPDATE statues
SET latitude = 31.316192,
    longitude = 120.603497,
    radius = 1000
WHERE icon = 'meiren';

UPDATE statues
SET latitude = 31.318288,
    longitude = 120.599361,
    radius = 1000
WHERE icon = 'tonggui';

UPDATE statues
SET latitude = 31.322563,
    longitude = 120.594519,
    radius = 1000
WHERE icon = 'wenchang';

UPDATE statues
SET latitude = 31.327672,
    longitude = 120.586627,
    radius = 1000
WHERE icon = 'caiyun';

UPDATE statues
SET latitude = 31.334761,
    longitude = 120.575063,
    radius = 1000
WHERE icon = 'haiyong';

UPDATE statues
SET latitude = 31.335581,
    longitude = 120.573329,
    radius = 1000
WHERE icon = 'fenshui';
