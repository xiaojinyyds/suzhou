"""
更新数据库中的石像数据为七狸山塘（保留白公狸不变）。
"""
import pymysql
from dotenv import load_dotenv
import os


def main():
    # Load .env
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))
    
    username = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = int(os.environ.get("MYSQL_PORT", 3306))
    database = os.environ.get("MYSQL_DATABASE")

    conn = pymysql.connect(
        host=host,
        user=username,
        password=password,
        database=database,
        port=port,
        cursorclass=pymysql.cursors.DictCursor
    )

    # 仅更新实测已确认的 6 个点位，白公狸按需求保持原数据不动
    # 坐标顺序：纬度(lat), 经度(lng)
    raccoons_data = [
        ("meiren", "美仁狸", 31.316192, 120.603497, 1000, "位于山塘桥畔，是七狸之首，象征美丽与仁慈。", "明代初年刘伯温所设七狸之一。", "镇水瑞兽", 7),
        ("tonggui", "通贵狸", 31.318288, 120.599361, 1000, "位于通贵桥畔。", "明代初年刘伯温所设七狸之一。", "寓意官运亨通、富贵双全。", 6),
        ("wenchang", "文昌狸", 31.322563, 120.594519, 1000, "位于星桥畔。", "明代初年刘伯温所设七狸之一。", "保佑文运昌盛，学子高中。", 5),
        ("caiyun", "彩云狸", 31.327672, 120.586627, 1000, "位于彩云桥畔。", "明代初年刘伯温所设七狸之一。", "象征平步青云，吉祥如意。", 4),
        ("haiyong", "海涌狸", 31.334761, 120.575063, 1000, "位于望山桥畔。", "明代初年刘伯温所设七狸之一。", "镇海纳川，气吞山河。", 2),
        ("fenshui", "分水狸", 31.335581, 120.573329, 1000, "位于西山庙桥畔。", "明代初年刘伯温所设七狸之一。", "分水镇江，保境安民。", 1),
    ]

    try:
        with conn.cursor() as cursor:
            # 按 icon 更新已有点位；若不存在则新增。保留白公狸不变。
            update_sql = """
                UPDATE statues
                SET name = %s,
                    latitude = %s,
                    longitude = %s,
                    radius = %s,
                    introduction = %s,
                    history = %s,
                    cultural_value = %s,
                    images = %s,
                    order_index = %s,
                    is_active = 1
                WHERE icon = %s
            """
            insert_sql = """
                INSERT INTO statues
                (name, icon, latitude, longitude, radius, introduction, history, cultural_value, images, order_index, is_active)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            """

            for icon, name, lat, lng, radius, intro, history, cultural, order_index in raccoons_data:
                update_payload = (name, lat, lng, radius, intro, history, cultural, "[]", order_index, icon)
                cursor.execute(update_sql, update_payload)

                if cursor.rowcount == 0:
                    insert_payload = (name, icon, lat, lng, radius, intro, history, cultural, "[]", order_index)
                    cursor.execute(insert_sql, insert_payload)
        
        conn.commit()
        print(f"✅ 成功更新 {len(raccoons_data)} 个点位（白公狸未改动）")
    except Exception as e:
        conn.rollback()
        import traceback
        traceback.print_exc()
        print(f"❌ 更新七狸数据失败: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
