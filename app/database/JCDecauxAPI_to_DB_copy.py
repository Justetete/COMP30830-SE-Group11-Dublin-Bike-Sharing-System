import requests
import traceback
import json
import sqlalchemy  
from sqlalchemy import create_engine, text as sql_text  
import JCD_DB_local
import JCD_API_Info
import time
from datetime import datetime  

def stations_to_db(text_data, engine): 
    """解析 JSON 数据，打印 station 数量，
       并将站点信息插入到数据库中，同时避免重复插入，并为每个 station 插入 availability 信息。
       如果没有传入 engine，则将数据写入到本地 JSON 文件。
    """
    try:
        stations = json.loads(text_data)
        print(f"Loaded {len(stations)} stations\n")

        # 如果没有提供数据库连接，则写入本地文件
        if engine is None:
            with open("stations_output.json", "w", encoding="utf-8") as f:
                json.dump(stations, f, indent=2)
            print("Saved station data to stations_output.json")
            return

        # 使用 engine.begin() 管理事务，自动提交或在异常时回滚
        with engine.begin() as conn:
            for station in stations:
                station_number = station.get('number')
                # 解析并转换字段，同时提供默认值
                try:
                    vals = {
                        "number": station_number,
                        "address": station.get('address', 'N/A'),
                        "banking": int(station.get('banking', 0)) if station.get('banking') is not None else 0,
                        "bike_stands": int(station.get('bike_stands', 0)) if station.get('bike_stands') is not None else 0,
                        "name": station.get('name', 'Unknown'),
                        "status": station.get('status', 'Unknown'),
                        "position_lat": float(station.get('position', {}).get('lat', 0.0)),
                        "position_lng": float(station.get('position', {}).get('lng', 0.0))
                    }
                except Exception as conv_e:
                    print(f"❌ 数据转换错误，跳过站点 {station_number}：{conv_e}")
                    continue

                # 检查该站点是否已经存在
                check_query = "SELECT COUNT(*) FROM station WHERE number = :number"
                query_result = conn.execute(sql_text(check_query), {"number": station_number}).scalar()

                if query_result == 0:
                    insert_query = """
                        INSERT INTO station (number, address, banking, bike_stands, name, status, position_lat, position_lng)
                        VALUES (:number, :address, :banking, :bike_stands, :name, :status, :position_lat, :position_lng)
                    """
                    conn.execute(sql_text(insert_query), vals)
                    print(f"Inserted new station: {vals['name']}")
                else:
                    print(f"Skipped (already exists): {vals['name']}")

                # 始终插入新的 availability 记录
                insert_availability(conn, station)
                
            # 事务在 with 块结束后自动提交
        
        print("\nData insertion completed!\n")
    except Exception as e:
        print("Error processing data:", e)
        print(traceback.format_exc())

def insert_availability(conn, station):
    """将 availability 数据插入到数据库中，若为重复记录则跳过。"""
    try:
        number = int(station.get('number', 0))
        available_bikes = int(station.get('available_bikes', 0)) if station.get('available_bikes') is not None else 0
        available_bike_stands = int(station.get('available_bike_stands', 0)) if station.get('available_bike_stands') is not None else 0
        status = station.get('status', 'Unknown')
        
        # 将时间戳从毫秒转换为 MySQL DATETIME 格式；若 last_update 为空则使用 0
        last_update_val = station.get('last_update', 0)
        last_update = int(station.get('last_update', 0))  # 保持为毫秒时间戳


        # MySQL 的 INSERT IGNORE 用于重复记录时忽略错误（如果未来更换数据库，请注意相应语法）
        insert_query = """
            INSERT IGNORE INTO availability (number, available_bikes, available_bike_stands, last_update, status)
            VALUES (:number, :available_bikes, :available_bike_stands, :last_update, :status)
        """

        result = conn.execute(sql_text(insert_query), {
            "number": number,
            "available_bikes": available_bikes,
            "available_bike_stands": available_bike_stands,
            "last_update": last_update,
            "status": status
        })

        # 根据 rowcount 判断是否插入成功
        if result.rowcount == 1:
            print(f"✅ Inserted availability for station {number} at {last_update}")
        else:
            print(f"⏩ Skipped duplicate for station {number} at {last_update}")

    except Exception as e:
        print(f"❌ Error inserting availability for station {station.get('number')}: {e}")
        print(traceback.format_exc())

def main():
    """获取 JCDecaux 站点数据，并插入到数据库中。"""
    USER = JCD_DB_local.USER
    PASSWORD = JCD_DB_local.PASSWORD
    PORT = JCD_DB_local.PORT
    DB = JCD_DB_local.DB
    URI = JCD_DB_local.URI

    connection_string = f"mysql+pymysql://{USER}:{PASSWORD}@{URI}:{PORT}/{DB}"
    engine = create_engine(connection_string, echo=True)

    try:
        response = requests.get(
            JCD_API_Info.STATIONS_URI, 
            params={"apiKey": JCD_API_Info.JCKEY, "contract": JCD_API_Info.NAME}
        )
        response.raise_for_status()
        stations_to_db(response.text, engine)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    while True:
        print("Fetching and writing data...")
        main()
        print("Sleeping for 5 minutes...\n")
        time.sleep(300)  # 5分钟 = 300秒
