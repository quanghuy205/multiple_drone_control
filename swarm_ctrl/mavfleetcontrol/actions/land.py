from mavfleetcontrol.craft import Craft
from mavsdk import System
import numpy as np
import asyncio

# from mavsdk.offboard import (OffboardError,Attitude, PositionNedYaw)

class land:

	# def __init__(self, point: np.array, tolerance: float = 1.0):
	# 	self.target = point
	# 	self.tolerance = tolerance


	async def __call__(self, drone):
		# print(drone.conn.telemetry.armed)
		#print(f"{self.name}: Landing")
		print("Landing----")
		await drone.land()
		print("-- Land")
		# await drone.start_offboard()
		# await drone.register_sensor("imu", drone.conn.telemetry.imu())
		# await drone.register_sensor("ned", drone.conn.telemetry.position_velocity_ned())
		# while drone.imu is None or drone.ned is None:
		# 	await asyncio.sleep(0)
		# while True:
		# 	await drone.conn.offboard.set_velocity_ned(VelocityNedYaw(xvelocity,yvelocity,0.0,0.0)) 