// 苏州石像打卡网站 - 数据文件

// 七座石像数据
const statuesData = [
    {
        id: 1,
        name: "虎丘塔",
        icon: "🗼",
        latitude: 31.3297,
        longitude: 120.5962,
        radius: 100,
        introduction: "虎丘塔是中国现存时代最久、规模最大的斜塔，有"中国第一斜塔"之称。始建于隋文帝仁寿九年（公元601年），已有一千多年历史。塔身向西北倾斜约2.48米，斜度2.48°，被誉为"东方比萨斜塔"。",
        history: "虎丘塔原名云岩寺塔，是一座八角形七层楼阁式砖塔，高47.5米。南宋绍兴年间曾因塔身倾斜进行过修缮，明清两代又有多次维修。",
        culturalValue: "虎丘塔不仅是苏州的标志性建筑，更承载着深厚的历史文化底蕴，是研究中国古代建筑史的重要实物资料。",
        isChecked: true,
        distance: 0.5
    },
    {
        id: 2,
        name: "狮子林",
        icon: "🦁",
        latitude: 31.3258,
        longitude: 120.6248,
        radius: 100,
        introduction: "狮子林以假山群闻名于世，素有"假山王国"之美誉。园内假山众多，形似狮子，故名"狮子林"。假山迷宫般的结构，让游客流连忘返。",
        history: "始建于元代至正二年（1342年），为禅宗高僧天如禅师为纪念其师中峰明本禅师而创建。园林几经兴衰，现为世界文化遗产。",
        culturalValue: "狮子林的假山被誉为"园林之最"，乾隆皇帝六下江南，曾五次游览狮子林，足见其魅力。",
        isChecked: false,
        distance: 1.2
    },
    {
        id: 3,
        name: "拙政园",
        icon: "🏞️",
        latitude: 31.3255,
        longitude: 120.6305,
        radius: 100,
        introduction: "拙政园是江南古典园林的代表作品，被誉为"中国园林之母"。园林占地面积5.2公顷，是苏州现存最大的古典园林，也是中国四大名园之一。",
        history: "始建于明正德初年（1506年），由御史王献臣归隐后兴建。取晋代潘岳《闲居赋》中"灌园鬻蔬，以供朝夕之膳……此亦拙者之为政也"之意，故名拙政园。",
        culturalValue: "1997年被联合国教科文组织列为世界文化遗产，是中国园林艺术的巅峰之作。",
        isChecked: true,
        distance: 0.8
    },
    {
        id: 4,
        name: "寒山寺",
        icon: "🔔",
        latitude: 31.3147,
        longitude: 120.5627,
        radius: 100,
        introduction: "寒山寺因唐代诗人张继的《枫桥夜泊》而闻名天下："姑苏城外寒山寺，夜半钟声到客船。"每年除夕，寒山寺都会举行敲钟仪式，钟声悠扬，传递着祝福与希望。",
        history: "始建于南朝萧梁代天监年间（502-519年），初名"妙利普明塔院"。唐代贞观年间，名僧寒山、希迁两位高僧创建寺院，遂更名"寒山寺"。",
        culturalValue: "寒山寺在日本等东亚国家享有盛誉，每年吸引大量海外游客前来朝拜。",
        isChecked: false,
        distance: 3.5
    },
    {
        id: 5,
        name: "平江路",
        icon: "🚣",
        latitude: 31.3289,
        longitude: 120.6311,
        radius: 100,
        introduction: "平江路是苏州一条历史悠久的古街，沿河而建，至今已有2500多年历史，是苏州古城保存最完整的一条古街。白墙黛瓦、小桥流水，展现了原汁原味的江南水乡风情。",
        history: "平江路是苏州的一条历史老街，南起干将东路，北至白塔东路。街道沿河而建，河街相邻，人家枕河而居。",
        culturalValue: "2009年被联合国教科文组织评为"世界遗产保护优秀范例"，成为了解苏州历史文化的重要窗口。",
        isChecked: false,
        distance: 2.1
    },
    {
        id: 6,
        name: "留园",
        icon: "🌸",
        latitude: 31.3271,
        longitude: 120.5924,
        radius: 100,
        introduction: "留园以园内建筑布置精巧、奇石众多而知名，与苏州拙政园、北京颐和园、承德避暑山庄并称中国四大名园。园内建筑精美，厅堂宏敞华丽，庭院富有变化。",
        history: "始建于明代嘉靖年间（1522-1566年），原为太仆寺少卿徐泰时的东园。清代时屡经易主，乾隆末年为刘恕所得，更名"寒碧山庄"，又称"刘园"。",
        culturalValue: "留园以其独特的造园艺术闻名中外，园内的冠云峰为宋代花石纲遗物，被誉为"江南园林三大名石"之首。",
        isChecked: false,
        distance: 4.2
    },
    {
        id: 7,
        name: "苏州博物馆",
        icon: "🏛️",
        latitude: 31.3261,
        longitude: 120.6298,
        radius: 100,
        introduction: "苏州博物馆是中国地方历史艺术性博物馆，由世界著名建筑大师贝聿铭设计，将现代建筑与苏州园林完美融合。馆藏文物丰富，展现了苏州深厚的历史文化底蕴。",
        history: "新馆于2006年10月建成开放，建筑面积26500平方米，是贝聿铭封笔之作。博物馆本身就是一件艺术品，采用"中而新，苏而新"的设计理念。",
        culturalValue: "博物馆收藏文物4万余件，其中一级文物865件/套，以历代书画、工艺品为主，尤以明清时期的苏州地方文物最具特色。",
        isChecked: false,
        distance: 1.5
    }
];

// 七种苏式甜品数据
const dessertsData = [
    {
        id: 1,
        name: "苏式月饼",
        icon: "🥮",
        price: 18,
        description: "传统苏式月饼，酥皮松软，馅料香甜。层层起酥，入口即化。",
        ingredients: ["小麦粉", "猪油", "豆沙", "白糖"],
        calories: 320,
        stock: 50
    },
    {
        id: 2,
        name: "桂花糖藕",
        icon: "🍡",
        price: 15,
        description: "香甜软糯，桂花飘香，江南特色甜品。清凉爽口，甜而不腻。",
        ingredients: ["莲藕", "糯米", "桂花", "冰糖"],
        calories: 180,
        stock: 30
    },
    {
        id: 3,
        name: "松子糕",
        icon: "🍰",
        price: 12,
        description: "松软香甜，松子香气浓郁。色泽金黄，口感细腻。",
        ingredients: ["糯米粉", "松子", "白糖"],
        calories: 250,
        stock: 40
    },
    {
        id: 4,
        name: "青团",
        icon: "🥟",
        price: 10,
        description: "清明时节必备，软糯可口。艾草清香，豆沙香甜。",
        ingredients: ["糯米", "艾草", "豆沙"],
        calories: 200,
        stock: 60
    },
    {
        id: 5,
        name: "定胜糕",
        icon: "🍮",
        price: 8,
        description: "软糯香甜，寓意美好。色泽粉红，造型精致。",
        ingredients: ["粳米粉", "豆沙", "红曲"],
        calories: 150,
        stock: 45
    },
    {
        id: 6,
        name: "海棠糕",
        icon: "🍪",
        price: 6,
        description: "外脆内软，豆沙香甜。形似海棠花，美观诱人。",
        ingredients: ["面粉", "豆沙", "红糖"],
        calories: 180,
        stock: 55
    },
    {
        id: 7,
        name: "梅花糕",
        icon: "🧁",
        price: 9,
        description: "造型精美，香甜可口。梅花造型，层次分明。",
        ingredients: ["糯米粉", "豆沙", "果仁"],
        calories: 220,
        stock: 35
    }
];

// 装饰效果数据
const decorationsData = [
    { id: 1, name: "赛博光环", icon: "✨", effect: "halo" },
    { id: 2, name: "彩虹特效", icon: "🌈", effect: "rainbow" },
    { id: 3, name: "电路纹理", icon: "⚡", effect: "circuit" },
    { id: 4, name: "星光粒子", icon: "💫", effect: "particles" },
    { id: 5, name: "魔法光球", icon: "🔮", effect: "orb" },
    { id: 6, name: "烟花效果", icon: "🎆", effect: "fireworks" }
];

// 成就数据
const achievementsData = [
    { id: 1, name: "初来乍到", icon: "🎯", condition: "完成第一次打卡", unlocked: true },
    { id: 2, name: "探索者", icon: "🧭", condition: "打卡3个景点", unlocked: false },
    { id: 3, name: "收藏家", icon: "📸", condition: "拍摄5张照片", unlocked: true },
    { id: 4, name: "美食家", icon: "🍰", condition: "品尝全部7种甜品", unlocked: false },
    { id: 5, name: "完美主义", icon: "🏆", condition: "打卡全部7个景点", unlocked: false },
    { id: 6, name: "社交达人", icon: "👥", condition: "分享10次", unlocked: false },
    { id: 7, name: "苏州通", icon: "📚", condition: "阅读全部景点介绍", unlocked: false },
    { id: 8, name: "连续打卡", icon: "🔥", condition: "连续7天打卡", unlocked: false }
];

