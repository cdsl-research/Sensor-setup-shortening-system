from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel
import pymysql.cursors

# JSONデータのスキーマ定義
class SensorInfo(BaseModel):
    I2C_addr: int
    register_num: list
    readable_register_num: int

class FileRequest(BaseModel):
    filename: str


app = FastAPI()

@app.post("/api/sensor-info")
async def receive_sensor_info(info: SensorInfo):
    # データを確認・処理

    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='*****',
                             database='sensors',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Read a single record
            sql="SELECT name, file_dir FROM sensor_info WHERE I2C=%s AND id_register_addr=%s AND id=%s AND readable_register_num=%s AND id_bit_shift=%s"
            for i in range(0x101):
                for j in range(4):
                    cursor.execute(sql, (info.I2C_addr, i, info.register_num[i] >> j, info.readable_register_num, j))
                    search_result = cursor.fetchone()
                    if(search_result != None):
                        files = os.listdir(search_result["file_dir"])
                        print({"name": search_result["name"]})
                        return {"files": files, "name": search_result["name"]}
    return {"message": "Sensor not found"}


@app.get("/scripts/{dirname}/{filename}")
async def download_file(dirname: str, filename: str):
    
    file_path = os.path.join(os.getcwd(), f"/home/c0a22016/scripts/{dirname}/{filename}")
    # ファイルをレスポンスとして送信
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
