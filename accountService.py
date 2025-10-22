import re
import pymysql
import hashlib
import os
from pymysql import cursors

# ========== 数据库配置 ==========
DB_CONFIG = {
    'host': '10.147.18.11',
    'user': 'root',          # 替换为你的 MySQL 用户名
    'password': 'Vesoft!@#890',  # 替换为你的 MySQL 密码
    'database': 'classicrealmd',
    'charset': 'utf8mb3',
    'cursorclass': cursors.DictCursor
}

CHARACTERS_DB_CONFIG = {
    'host': '10.147.18.11',
    'user': 'root',
    'password': 'Vesoft!@#890',
    'database': 'classiccharacters',  # 角色数据库
    'charset': 'utf8mb3',
    'cursorclass': cursors.DictCursor
}

# ========== 邮箱正则验证函数 ==========
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ========== 注册逻辑函数 ==========
def register_user(username, password, gm_level, email):
    # 输入校验
    if not username:
        return "错误：账号不能为空！"
    if len(password) < 6:
        return "错误：密码至少6位！"
    if not is_valid_email(email):
        return "错误：邮箱格式不正确！"
    
    # 通常 salt 是 32 字节的随机数
    salt = os.urandom(32)  # 生成 16 字节随机 salt
    # salt = bytes.fromhex("F93C9470822E53F3E6AD8F3A55E4EA4F5CE85F37D4896F4C3B3642FDCE3BD869") #用于验证的salt， 账号：subin 密码：123456

    verifier = calculate_srp6_verifier(username, password, salt)

    # 注意: 在 CMaNGOS 数据库中，sha_pass_hash 字段是 salt 和 verifier 的组合
    # 格式通常是: <SALT_IN_HEX>:<VERIFIER_IN_HEX>
    # 其中 SALT_IN_HEX 和 VERIFIER_IN_HEX 都是大写十六进制字符串
    salt_hex = salt.hex().upper()
    verifier_hex = verifier.hex().upper()  # 或 verifier_wotlk.hex().upper()

    connection = None
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            # 检查用户名是否已存在
            sql_check_user = "SELECT * FROM account WHERE username = %s"
            cursor.execute(sql_check_user, (username,))
            if cursor.fetchone():
                return f"错误：用户 '{username}' 已存在！"

            # 检查邮箱是否已存在
            sql_check_email = "SELECT * FROM account WHERE email = %s"
            cursor.execute(sql_check_email, (email,))
            if cursor.fetchone():
                return f"错误：邮箱 '{email}' 已被注册！"

            # 插入新用户
            sql_insert = "INSERT INTO account (username, v, s, gmlevel, email) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_insert, (username.upper(), verifier_hex, salt_hex, int(gm_level), email))

        connection.commit()

        successMsg = f"✅ 注册成功！用户：{username.upper()}，GM等级：{gm_level}，邮箱：{email}"
        print(successMsg)
        return successMsg

    except Exception as e:
        faildMsg = f"❌ 数据库错误：{str(e)}"
        print(faildMsg)
        return faildMsg

    finally:
        if connection:
            connection.close()

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

            
"""
计算 SRP6 验证器 (verifier) v = g^x mod N, 其中 x = H(salt | H(I:P))。
此实现兼容 CMaNGOS 不同核心的变体。

Args:
    username (str): 用户名
    password (str): 密码
    salt (bytes): 随机 salt (通常 16 或 32 字节)

Returns:
    bytes: 32 字节长的验证器 (verifier) 字节串
"""
def calculate_srp6_verifier(username: str, password: str, salt: bytes) -> bytes:
    # --- SRP6 参数 ---
    # 生成元 g
    g = 7
    # 大素数模数 N (1024-bit, CMaNGOS 标准值)
    N_hex = "894B645E89E1535BBDAD5B8B290650530801B18EBFBF5E8FAB3C82872A3E9BB7"
    N = int(N_hex, 16)

    # --- 1. 计算第一个哈希 H(I:P) = H(username:password) ---
    # 将用户名和密码用冒号连接并转为大写
    identity_credential = f"{username}:{password}".upper().encode('utf-8')
    # 计算 SHA1 哈希 (返回原始二进制数据)
    h1 = hashlib.sha1(identity_credential).digest()  # 20 字节

    # --- 2. 计算第二个哈希 x = H(salt | h1) ---
    salt_for_hash = salt[::-1]  # 反转 salt 字节串

    # 拼接 salt_for_hash 和 h1
    x_input = salt_for_hash + h1
    # 计算 SHA1 哈希 (x 的原始二进制形式)
    h2 = hashlib.sha1(x_input).digest()  # 20 字节

    # --- 3. 将 h2 (x) 从字节串转换为大整数 (小端序) ---
    # Python 的 int.from_bytes 默认是 little-endian 当 byteorder='little'
    x = int.from_bytes(h2, byteorder='little')

    # --- 4. 计算验证器 v = g^x mod N ---
    # 使用内置的 pow 进行高效的模幂运算
    verifier_int = pow(g, x, N)  # v = g^x mod N

    # --- 5. 将验证器大整数转换回字节串 (小端序) ---
    # 计算需要的字节数 (至少 32 字节, 因为我们要填充到 32)
    byte_length = max(32, (verifier_int.bit_length() + 7) // 8)
    verifier_bytes = verifier_int.to_bytes(byte_length, byteorder='little')
    # 此时 verifier_bytes 可能 >= 32 字节

    # --- 6. 填充到恰好 32 字节 (小端序: 在末尾/高位补零) ---
    # 由于是小端序，高位在后，所以用右填充 (右侧加零)
    # 如果长度超过 32，我们取前 32 字节？但通常不会超过。
    # 更安全的做法是确保正好 32 字节，不足则右补零，超过则截断（但理论上 g^x mod N 不应超过 N 的字节长度，而 N 是 1024位=128字节）
    # 但 CMaNGOS 期望 32 字节，所以我们只取前 32 字节或填充到 32。
    # 实际上，CMaNGOS 的 verifier 存储为 32 字节，所以我们需要截断或确保。
    # 根据常见实现，我们取小端序表示并填充/截断到 32 字节。
    # 这里我们先确保至少 32 字节，然后取前 32 字节。
    # 但上面的 to_bytes 已经用 0 填充到 byte_length，而 byte_length >=32。
    # 所以我们直接取前 32 字节。
    verifier_padded = verifier_bytes[:32]  # 取前 32 字节

    # WotLK 及以上核心: 返回 verifier 的反转
    return verifier_padded[::-1]  # 反转字节串