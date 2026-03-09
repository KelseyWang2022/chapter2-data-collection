
import traci
import pandas as pd
import numpy as np

# 加载交通数据，每行代表1分钟（60秒）
df = pd.read_csv(r"C:\Users\Kelsey\PycharmProjects\sumo_simulation\RD383_Villeurbanne(4_10).csv")
df["current_travel_time"] = pd.to_numeric(df["current_travel_time"], errors="coerce")
df["free_flow_travel_time"] = pd.to_numeric(df["free_flow_travel_time"], errors="coerce")
df.dropna(inplace=True)
df["congestion"] = df["current_travel_time"] / df["free_flow_travel_time"]

# 车辆计数器
veh_id_counter = 0

# 启动 TraCI 仿真，设置仿真步长为1秒
sumoBinary = "sumo"  # 或 "sumo-gui"
sumoConfig = "final_config.sumocfg"

traci.start([sumoBinary, "-c", sumoConfig, "--step-length", "1"])

step = 0
while step < 60 * len(df):  # 每行 = 60秒
    traci.simulationStep()

    if step % 60 == 0:
        row_idx = step // 60
        if row_idx < len(df):
            congestion = df.iloc[row_idx]["congestion"]
            base_rate = 30  # 每分钟最大注入车辆数
            rate = int(base_rate * np.exp(-(congestion - 1)))
            print(f"[step {step}] Injecting {rate} vehicles (congestion={congestion:.2f})")

            for i in range(rate):
                veh_id = f"veh_{veh_id_counter}"
                route_id = "dynamic_route"
                traci.vehicle.add(vehID=veh_id, routeID=route_id, typeID="car")
                veh_id_counter += 1

    step += 1

traci.close()
