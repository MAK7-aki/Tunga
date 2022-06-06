from pymavlink import mavutil

# Start a connection listening to a UDP port
master = mavutil.mavlink_connection("/dev/ttyUSB0", baud=115200)

# Wait for the first heartbeat
#   This sets the system and component ID of remote system for the link
master.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" %
      (master.target_system, master.target_component))

master.mav.command_long_send(master.target_system, master.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

msg = master.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)


master.mav.command_long_send(master.target_system, master.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)

msg = master.recv_match(type='COMMAND_ACK', blocking=True)
print(msg)