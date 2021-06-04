#!/usr/bin/env python3

import asyncio
from mavsdk import System
import random

async def connect(self):
    self.conn = System(port=random.randint(1000, 65535))

    print(f"{self.name}: connecting")
    await self.conn.connect(system_address=self.address)

    print(f"{self.name}: waiting for connection")
    async for state in self.conn.core.connection_state():
        print(f"{self.name}: {state}")
        if state.is_connected:
            print(f"{self.name}: connected!")
            break

async def run():

    drone = System(port=50041)
    await drone.connect(system_address="udp://:14540")
    drone1 = System(port=50042)
    await drone1.connect(system_address="udp://:14541")

    print("Waiting for drone to connect...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered with UUID: {state.uuid}")
            break

    # async for state1 in drone1.core.connection_state():
    #     if state1.is_connected:
    #         print(f"Drone1 discovered with UUID: {state1.uuid}")
    #         break
    print("Waiting for drone to have a global position estimate...")
    # async for health in drone.telemetry.health():
    #     if health.is_global_position_ok:
    #         print("Global position estimate ok")
    #         break

    print("-- Arming 1")
    await drone.action.arm()
    print("-- Arming 2")
    await drone1.action.arm()
    print("-- Taking off 1")
    await drone.action.takeoff()
    print("-- Taking off 2")
    await drone1.action.takeoff()

    await asyncio.sleep(5)

    print("-- Landing")
    await drone.action.land()
    await drone1.action.land()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
