from typing import Callable, Awaitable, List
import threading
import functools
import queue
import asyncio
import random

from mavsdk import System
from mavsdk.offboard import Attitude, PositionNedYaw, OffboardError
from mavsdk.telemetry import PositionNed
import numpy as np


class Drone(threading.Thread):
    def __init__(
        self,
        name: str,
        connection_address: str,
        action: Callable[["Craft"], Awaitable[None]] = None,
    ):
        super().__init__()
        self.name: str = name
        self.conn: System = None
        self.address: str = connection_address
        self.action: Callable[["Drone"], Awaitable[None]] = action
        # self.loop = None
        self.loop = asyncio.new_event_loop()
        self.tasking = queue.Queue()
        self.current_task = None
        self.current_task_lock = threading.Lock()
        self.sensors = []


