import mysql.connector
import requests

# 连接到mysql本地的数据库 需要提前先建好'company_management'这个数据库并存入info的表，完成本地的导入
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root123',
    database='company_management'
)
cursor = conn.cursor()

# 查询数据库中的地址数据
cursor.execute("SELECT id, address FROM address_info ")
addresses = cursor.fetchall()

# 遍历从数据库中检索到的地址数据
for address in addresses:
    address_id = address[0]
    address_text = address[1]
    # 使用高德 API 查询经纬度信息
    response = requests.get('https://restapi.amap.com/v3/geocode/geo',
                            params={'address': address_text, 'key': '9cca460539bced397af0a75597571ead'})
    data = response.json()
    if data['status'] == '1' and int(data['count']) > 0: # 确保从 API 获取到有效的地理信息
        location = data['geocodes'][0]['location'] # 从 API 返回的数据中提取 geocodes 列表的第一个元素的 location 字段
        latitude, longitude = location.split(',') # 将经度与纬度分别存储
        # 将地理信息更新到数据库表格中
        cursor.execute("UPDATE address_info SET latitude = %s, longitude = %s WHERE id = %s",
                       (latitude, longitude, address_id))
        conn.commit()

# 关闭数据库连接
cursor.close()
conn.close()

# 先查询包含地址和 ID 的数据，然后使用高德 API 查询每个地址的经纬度信息，并将其更新到数据库表格中，测试了239行代码是有效的（丐版api），好像是请求量受到限制
