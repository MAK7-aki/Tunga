from pymavlink import mavutil

# Start a connection listening to a UDP port
master = mavutil.mavlink_connection("/dev/ttyUSB1", baud=115200)

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (master.target_system, master.target_component))
# #master.reboot_autopilot()