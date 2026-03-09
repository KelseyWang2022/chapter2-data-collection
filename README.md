# SUMO-based Traffic Trajectory Simulation with Data-driven Vehicle Injection

## Project Overview

This project generates high-resolution vehicle trajectory data using the SUMO (Simulation of Urban Mobility) traffic simulation platform. The simulation integrates real-world traffic information to dynamically control traffic demand during the simulation.

Traffic congestion levels derived from real traffic data are used to dynamically adjust vehicle injection rates in the SUMO simulation. This approach allows the simulation to reproduce realistic traffic dynamics and generate detailed vehicle trajectory data for further traffic analysis.

The generated trajectory data can be used for tasks such as traffic flow analysis, congestion modeling, and turning-conflict detection.

---

# Methodology

The simulation framework consists of four main components:

1. Real traffic data collection
2. Congestion estimation
3. Dynamic vehicle injection
4. SUMO trajectory simulation

The overall pipeline is illustrated below:

Real traffic data → Congestion estimation → Dynamic vehicle generation → SUMO simulation → Vehicle trajectory output

---

# 1 Real Traffic Data Collection

Real-world traffic information is collected using the TomTom Traffic API.

Script:

```
1.data_collection_TOMTOM.py
```

The collected data include:

* current travel time
* free-flow travel time
* timestamped traffic measurements

These data are used to estimate traffic congestion levels.

---

# 2 Congestion Estimation

Traffic congestion is quantified using the ratio between the current travel time and the free-flow travel time:

```
congestion = current_travel_time / free_flow_travel_time
```

Where:

* **current_travel_time** represents the real-time travel time measured from traffic data.
* **free_flow_travel_time** represents the travel time under free-flow conditions.

A congestion value greater than 1 indicates increased traffic density.

---

# 3 Dynamic Vehicle Injection

Vehicle generation during the simulation is dynamically controlled based on the congestion level.

For each minute of traffic data, the vehicle injection rate is computed as:

```
rate = base_rate * exp(-(congestion - 1))
```

Where:

* **base_rate** is the maximum vehicle injection rate per minute.
* **congestion** is the congestion index derived from traffic data.

This formulation ensures that higher congestion levels reduce the number of newly injected vehicles, mimicking realistic traffic demand dynamics.

The dynamic simulation is implemented using the TraCI interface.

Main script:

```
config/4.dynamic_simulation.py
```

Key features of the simulation:

* The SUMO simulation runs with a time step of **1 second**.
* Traffic data are updated every **60 seconds**.
* At each update interval, the vehicle injection rate is recalculated.
* Vehicles are inserted dynamically into the network using TraCI.

---

# 4 SUMO Simulation Environment

The SUMO simulation uses the following components.

### Road Network

```
config/111.net.xml
```

This file represents the road network of the study area.

The network is derived from OpenStreetMap data:

```
map.osm
```

---

### Vehicle Routes

Vehicle routes are defined in:

```
config/route_multitype.rou.xml
config/dynamic_route_multitype.rou.xml
```

These files define vehicle types and route structures used during the simulation.

---

### Simulation Configuration

The main SUMO configuration file is:

```
config/final_config.sumocfg
```

This file specifies:

* the road network
* route configuration files
* simulation parameters
* output configuration

---

# 5 Running the Simulation

To run the simulation, navigate to the configuration directory:

```
cd config
```

Then run the dynamic simulation script:

```
python 4.dynamic_simulation.py
```

The script will start SUMO and control the simulation using TraCI.

Alternatively, the simulation can be launched manually:

```
sumo -c final_config.sumocfg
```

or

```
sumo-gui -c final_config.sumocfg
```

---

# 6 Trajectory Data Output

The simulation records vehicle trajectories using the SUMO Floating Car Data (FCD) output.

```
--fcd-output vehicle_trajectories.xml
```

The trajectory data include:

* vehicle ID
* simulation time
* vehicle position (x, y)
* vehicle speed
* heading angle

These data enable detailed analysis of vehicle movement patterns.

---

# Project Structure

```
chapter2-data-collection

config/
    111.net.xml
    final_config.sumocfg
    route_multitype.rou.xml
    dynamic_route_multitype.rou.xml
    4.dynamic_simulation.py
    vehicle_trajectories.xml

data/
    traffic data files

networks/
    network files

outputs/
    simulation outputs

1.data_collection_TOMTOM.py
map.osm
```

---

# Requirements

The simulation environment requires:

* SUMO
* Python 3
* TraCI (included in SUMO)
* pandas
* numpy

Install required Python packages:

```
pip install pandas numpy
```

---

# Notes

* All trajectory data are generated using SUMO simulation.
* Real-world traffic information is incorporated through TomTom traffic data.
* Vehicle injection rates dynamically adapt to traffic congestion levels.

This framework enables the generation of realistic traffic trajectories suitable for traffic safety analysis and traffic flow studies.
