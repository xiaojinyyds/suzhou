"""
初始化数据库数据脚本
"""
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.models.statue import Statue
from app.models.dessert import Dessert


def init_statues():
    """初始化七个石像景点数据"""
    statues_data = [
        {
            "name": "虎丘塔",
            "icon": "🗼",
            "latitude": 31.3297,
            "longitude": 120.5962,
            "radius": 100,
            "introduction": "虎丘塔是中国现存时代最久、规模最大的斜塔",
            "history": "始建于隋文帝仁寿九年（公元601年）",
            "cultural_value": "被誉为'东方比萨斜塔'",
            "images": "[]",
            "order_index": 1
        },
        {
            "name": "狮子林",
            "icon": "🦁",
            "latitude": 31.3258,
            "longitude": 120.6248,
            "radius": 100,
            "introduction": "狮子林以假山群闻名于世，素有'假山王国'之美誉",
            "history": "建于元代至正二年（1342年）",
            "cultural_value": "中国四大名园之一",
            "images": "[]",
            "order_index": 2
        },
        {
            "name": "拙政园",
            "icon": "🏞️",
            "latitude": 31.3236,
            "longitude": 120.6297,
            "radius": 100,
            "introduction": "江南园林的代表，中国四大名园之一",
            "history": "始建于明正德初年（16世纪初）",
            "cultural_value": "世界文化遗产，中国园林艺术的巅峰之作",
            "images": "[]",
            "order_index": 3
        },
        {
            "name": "寒山寺",
            "icon": "🔔",
            "latitude": 31.3043,
            "longitude": 120.5626,
            "radius": 100,
            "introduction": "因唐代诗人张继的《枫桥夜泊》而闻名天下",
            "history": "始建于南朝梁代天监年间（502-519年）",
            "cultural_value": "中国十大名寺之一",
            "images": "[]",
            "order_index": 4
        },
        {
            "name": "平江路",
            "icon": "🚣",
            "latitude": 31.3247,
            "longitude": 120.6213,
            "radius": 100,
            "introduction": "苏州保存最完整的古街区，展现水乡风貌",
            "history": "建于南宋时期，至今已有800多年历史",
            "cultural_value": "中国历史文化名街",
            "images": "[]",
            "order_index": 5
        },
        {
            "name": "留园",
            "icon": "🌸",
            "latitude": 31.3156,
            "longitude": 120.6004,
            "radius": 100,
            "introduction": "中国四大名园之一，以建筑精美著称",
            "history": "始建于明代嘉靖年间（1593年）",
            "cultural_value": "世界文化遗产，园林建筑艺术的精华",
            "images": "[]",
            "order_index": 6
        },
        {
            "name": "苏州博物馆",
            "icon": "🏛️",
            "latitude": 31.3261,
            "longitude": 120.6285,
            "radius": 100,
            "introduction": "由建筑大师贝聿铭设计的现代博物馆",
            "history": "2006年10月6日正式开馆",
            "cultural_value": "融合传统与现代的建筑艺术典范",
            "images": "[]",
            "order_index": 7
        }
    ]
    
    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_count = db.query(Statue).count()
        if existing_count > 0:
            print(f"⚠️  石像数据已存在（{existing_count}条），跳过初始化")
            return
        
        # 插入数据
        for data in statues_data:
            statue = Statue(**data)
            db.add(statue)
        
        db.commit()
        print(f"✅ 成功初始化 {len(statues_data)} 个石像景点数据")
    except Exception as e:
        db.rollback()
        print(f"❌ 初始化石像数据失败: {str(e)}")
    finally:
        db.close()


def init_desserts():
    """初始化七种苏式甜品数据"""
    desserts_data = [
        {
            "name": "苏式月饼",
            "icon": "🥮",
            "price": 18.0,
            "description": "传统苏式月饼，酥皮松软，馅料香甜",
            "ingredients": '["小麦粉", "猪油", "豆沙", "白糖"]',
            "calories": 320,
            "stock": 50,
            "order_index": 1
        },
        {
            "name": "桂花糖藕",
            "icon": "🍡",
            "price": 15.0,
            "description": "香甜软糯，桂花飘香，江南特色甜品",
            "ingredients": '["莲藕", "糯米", "桂花", "冰糖"]',
            "calories": 180,
            "stock": 30,
            "order_index": 2
        },
        {
            "name": "松子糕",
            "icon": "🍰",
            "price": 12.0,
            "description": "松软香甜，松子香气浓郁",
            "ingredients": '["糯米粉", "松子", "白糖"]',
            "calories": 250,
            "stock": 40,
            "order_index": 3
        },
        {
            "name": "青团",
            "icon": "🥟",
            "price": 10.0,
            "description": "清明时节必备，软糯可口",
            "ingredients": '["糯米", "艾草", "豆沙"]',
            "calories": 200,
            "stock": 60,
            "order_index": 4
        },
        {
            "name": "定胜糕",
            "icon": "🍮",
            "price": 8.0,
            "description": "软糯香甜，寓意美好",
            "ingredients": '["粳米粉", "豆沙", "红曲"]',
            "calories": 150,
            "stock": 45,
            "order_index": 5
        },
        {
            "name": "海棠糕",
            "icon": "🍪",
            "price": 6.0,
            "description": "外脆内软，豆沙香甜",
            "ingredients": '["面粉", "豆沙", "红糖"]',
            "calories": 180,
            "stock": 55,
            "order_index": 6
        },
        {
            "name": "梅花糕",
            "icon": "🧁",
            "price": 9.0,
            "description": "造型精美，香甜可口",
            "ingredients": '["糯米粉", "豆沙", "果仁"]',
            "calories": 220,
            "stock": 35,
            "order_index": 7
        }
    ]
    
    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing_count = db.query(Dessert).count()
        if existing_count > 0:
            print(f"⚠️  甜品数据已存在（{existing_count}条），跳过初始化")
            return
        
        # 插入数据
        for data in desserts_data:
            dessert = Dessert(**data)
            db.add(dessert)
        
        db.commit()
        print(f"✅ 成功初始化 {len(desserts_data)} 种甜品数据")
    except Exception as e:
        db.rollback()
        print(f"❌ 初始化甜品数据失败: {str(e)}")
    finally:
        db.close()


def main():
    """主函数"""
    print("=" * 50)
    print("开始初始化数据库数据...")
    print("=" * 50)
    
    # 创建所有表
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建/更新成功")
    except Exception as e:
        print(f"❌ 数据库表创建失败: {str(e)}")
        return
    
    # 初始化数据
    init_statues()
    init_desserts()
    
    print("=" * 50)
    print("数据初始化完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
