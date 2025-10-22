import pymysql
import config
from pymysql import cursors

CHARACTERS_DB_CONFIG = {
    'host': config.host_characters,
    'user': config.user_characters,
    'password': config.password_characters,
    'database': config.database_characters, 
    'charset': 'utf8mb3',
    'cursorclass': cursors.DictCursor
}

# ========== 角色查询函数 ==========
def get_all_characters(character_name="", online_status="all"):
    connection = None
    try:
        connection = pymysql.connect(**CHARACTERS_DB_CONFIG)
        with connection.cursor() as cursor:
            # 查询所有角色信息
            sql = """
                SELECT a.name,
                CASE WHEN race = 1 THEN '人类' 
                WHEN race = 2 THEN '兽人' 
                WHEN race = 3 THEN '矮人' 
                WHEN race = 4 THEN '暗夜精灵' 
                WHEN race = 5 THEN '亡灵' 
                WHEN race = 6 THEN '牛头人' 
                WHEN race = 7 THEN '侏儒' 
                WHEN race = 8 THEN '巨魔' 
                END AS race,
                CASE WHEN class = 1 THEN '战士' 
                WHEN class = 2 THEN '圣骑士' 
                WHEN class = 3 THEN '猎人' 
                WHEN class = 4 THEN '盗贼' 
                WHEN class = 5 THEN '牧师' 
                WHEN class = 7 THEN '萨满' 
                WHEN class = 8 THEN '法师' 
                WHEN class = 9 THEN '术士' 
                WHEN class = 11 THEN '德鲁伊' 
                END AS class,
                CASE WHEN gender = 0 THEN '男' ELSE '女' END AS gender,
                level,xp,
                CONCAT(
                    FLOOR(money / 10000), '金',
                    FLOOR(MOD(money, 10000) / 100), '银',
                    MOD(money, 100), '铜'
                ) AS money,
                CASE WHEN online = 0 THEN '离线' ELSE '在线' END AS online,
                CONCAT(
                    FLOOR(totaltime / 86400), '天',
                    FLOOR(MOD(totaltime,86400) / 3600), '小时',
                    FLOOR(MOD(totaltime,3600) / 60), '分钟'
                ) AS totaltime,
                CONCAT(FROM_UNIXTIME(logout_time)) AS logout_time,
                b.field15 AS locationName 
                FROM characters AS a
                LEFT JOIN ja_areatable AS b ON a.zone = b.ID 
                WHERE 1=1 
                """

            # 添加角色名过滤条件
            params = []
            if character_name:
                sql += " AND a.name LIKE %s "
                params.append(f"%{character_name}%")

            # 添加在线状态过滤条件
            if online_status == "online":
                sql += " AND a.online = %s"
                params.append(1)
            elif online_status == "offline":
                sql += " AND a.online = %s"
                params.append(0)
            
            # 添加排序
            sql += " ORDER BY a.guid ASC"
            # 限制最多返回100条记录
            sql += " limit 100"  

            # 如果有参数则使用参数化查询，否则直接执行
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            characters = cursor.fetchall()
            
            # 格式化数据为表格
            data = []
            if characters:
                for char in characters:
                    data.append([
                        char['name'],
                        char['level'],
                        char['race'],
                        char['class'],
                        char['gender'],
                        char['xp'],
                        char['money'],
                        char['online'],
                        char['totaltime'],
                        char['logout_time'],
                        char['locationName'],
                    ])
            else:
                data.append(["暂无角色数据", "", "", "", "", "", "", "", "", "", ""])
                
            return data
                
    except Exception as e:
        return [[f"数据库查询错误: {str(e)}", "", "", "", "", "", "", "", "", "", ""]]
    
    finally:
        if connection:
            connection.close()
