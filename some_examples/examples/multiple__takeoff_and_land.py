#!/usr/bin/env python3

import asyncio
from mavsdk import System
import threading
import functools
import queue
import random
from mavsdk.offboard import Attitude, PositionNedYaw, OffboardError
from mavsdk.telemetry import PositionNed
class Craft(threading.Thread):
    def __init__(
        self,
        name: str,
        connection_address: str,
    ):
        super().__init__()
        self.name: str = name
        self.conn: System = None
        self.address: str = connection_address

    async def run():
        drone = System()

        await drone.connect(system_address="udp://:14541")

        print("Waiting for drone to connect...")
        async for state in drone.core.connection_state():
            if state.is_connected:
                print(f"Drone discovered with UUID: {state.uuid}")
                break

        print("Waiting for drone to have a global position estimate...")
        async for health in drone.telemetry.health():
            if health.is_global_position_ok:
                print("Global position estimate ok")
                break

        print("-- Arming")
        await drone.action.arm()

        print("-- Taking off")
        await drone.action.takeoff()

        await asyncio.sleep(5)

        print("-- Landing")
        await drone.action.land()

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

    async def arm(self, coordinate: List[float] = None, attitude: List[float] = None):
        async for arm in self.conn.telemetry.armed():
            if arm is False:
                try:
                    print(f"{self.name}: arming")
                    await self.conn.action.arm()
                    print(f"{self.name}: Setting initial setpoint")
                    if coordinate is not None:
                        await self.conn.offboard.set_position_ned(
                            PositionNedYaw(*coordinate, 0.0)
                        )
                    if attitude is not None:
                        await self.conn.offboard.set_attitude(Attitude(*attitude, 0.0))

                except Exception as bla:  # add exception later
                    print(bla)
                break
            else:
                break

    async def land(self):
        await self.conn.action.land()

    async def disarm(self):
        async for arm in self.conn.telemetry.armed():
            if arm is True:
                try:
                    print(f"{self.name}: Disarming")
                    await self.conn.action.disarm()

                except Exception as bla:  # add exception later
                    print(bla)
                break
            else:
                break


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
