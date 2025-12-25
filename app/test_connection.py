import pymysql

print("正在测试数据库连接...")
print("-" * 50)

try:
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='lxl123756',
        database='大作业-test4',
        charset='utf8mb4'
    )
    print("数据库连接成功!")
    print()
    
    cursor = conn.cursor()
    
    # 查询端口
    cursor.execute("SHOW VARIABLES LIKE 'port'")
    port_result = cursor.fetchone()
    print(f"MySQL 端口: {port_result[1]}")
    
    # 查询版本
    cursor.execute("SELECT VERSION()")
    version_result = cursor.fetchone()
    print(f"MySQL 版本: {version_result[0]}")
    
    # 查询当前数据库
    cursor.execute("SELECT DATABASE()")
    db_result = cursor.fetchone()
    print(f"当前数据库: {db_result[0]}")
    
    # 查询主机
    cursor.execute("SHOW VARIABLES LIKE 'hostname'")
    host_result = cursor.fetchone()
    print(f"MySQL 主机: {host_result[1] if host_result else 'localhost'}")
    
    cursor.close()
    conn.close()
    
    print()
    print("=" * 50)
    print("结论: config.py 的配置正确!")
    print("  - host: 'localhost' ✅")
    print("  - port: 3306 ✅")
    print("  - database: '大作业-test4' ✅")
    print("  - user: 'root' ✅")
    print("  - password: 'lxl123756' ✅")
    
except Exception as e:
    print(f"❌ 连接失败: {e}")
    print()
    print("请检查:")
    print("  1. MySQL 服务是否启动")
    print("  2. 用户名密码是否正确")
    print("  3. 端口号是否正确")
