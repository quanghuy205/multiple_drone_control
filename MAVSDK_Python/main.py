from mavsdk import System, telemetry
import asyncio
from asyncqt import QEventLoop, asyncSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
from gui import *
import sys


#create gui
class MainWindow(QMainWindow):

    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionConnect.triggered.connect(self.connect_drone)

        self.ui.mode_arm.clicked.connect(self.arm)
        self.ui.mode_disarm.clicked.connect(self.disarm)
        self.ui.mode_to.clicked.connect(self.takeoff)
        self.ui.mode_land.clicked.connect(self.land)
        self.ui.mode_rtl.clicked.connect(self.rtl)

    # Connect to vehicles
    @asyncSlot()
    async def connect_drone(self):

        print("Connecting")
        global drone
        drone = System()
        await drone.connect()
        print("Drone connected")

        self.ui.connect_label.setText("Connected")

        await asyncio.gather(self.get_mode(), self.get_bat(), self.get_arm(), self.get_gps(), self.get_pos())

        return None

    @asyncSlot()
    async def get_pos(self):
        async for pos in drone.telemetry.position():
            lat = round(pos.latitude_deg, 8)
            self.ui.lat_label.setText(str(lat))
            long = round(pos.longitude_deg,8)
            self.ui.long_label.setText(str(long))
            alt_rel = round(pos.relative_altitude_m, 1)
            self.ui.alt_rel_label.setText(str(alt_rel) + "m")
            alt_msl = round(pos.absolute_altitude_m, 1)
            self.ui.alt_msl_label.setText(str(alt_msl) + "m")
        return None


    @asyncSlot()
    async def get_mode(self):

        async for mode in telemetry.Telemetry.flight_mode(drone.telemetry):

            if str(mode) == "RETURN_TO_LAUNCH":
                mod = "RTL"
            else:
                mod = str(mode)
            self.ui.mode_label.setText(mod)

        return None

    @asyncSlot()
    async def get_bat(self):

        async for bat in telemetry.Telemetry.battery(drone.telemetry):
            v = round(bat.voltage_v, 1)
            rem = round(100 * bat.remaining_percent, 1)

            self.ui.bat_v_label.setText(str(v) + "v")
            self.ui.bat_rem_label.setText(str(rem) + "v")
        return None

    @asyncSlot()
    async def get_arm(self):

        async for arm in telemetry.Telemetry.armed(drone.telemetry):
            arm = "Armed" if arm else "Disarmed"
            self.ui.arm_label.setText(arm)
        return None

    @asyncSlot()
    async def disarm(self):
        print("Disarming Drone...")
        await drone.action.disarm()

    @asyncSlot()
    async def arm(self):
        print("Arming Drone...")
        await drone.action.arm()

    @asyncSlot()
    async def takeoff(self):
        print("Taking off...")
        await drone.action.takeoff()

    @asyncSlot()
    async def get_gps(self):

        async for gps in telemetry.Telemetry.gps_info(drone.telemetry):
            sat = gps.num_satellites
            fix = gps.fix_type

            self.ui.gps_sat_label.setText(str(sat))
            self.ui.gps_fix_label.setText(str(fix))

    @asyncSlot()
    async def rtl(self):

        print("Returning to Launch location...")
        await drone.action.return_to_launch()

    @asyncSlot()
    async def land(self):

        print("Landing...")
        await drone.action.land()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    MainWindow = MainWindow()
    MainWindow.show()

    with loop:
        sys.exit(loop.run_forever())












