import subprocess
from time import strftime, localtime, sleep
from pingvalues import PingValues
from report import Report

# Parameters --------------------------------------------------------

"""The ping target. Suggested default: 8.8.8.8, Google DNS server."""
ping_destination = '8.8.8.8'

"""Argument to -c flag."""
ping_count = 10

"""The time, in seconds, defining the rate at which ping is called.
In between ping calls, the program sleeps."""
sleep_interval = 1

"""The time, in milliseconds, which serves as an upper bound for
acceptable performance. If the average RTT of a run of ping exceeds
this, it will be added to the report."""
max_acceptable_time = 200

"""The ratio, expressed between zero and one inclusive, which serves
as a lower bound for the acceptable rate of packet loss. If packet
loss for a run of ping fails to meet this value, it will be added to 
the report."""
min_acceptable_success_rate = 0.95

# -------------------------------------------------------------------

ping_command = ['ping', '-c ' + str(ping_count), ping_destination]
time_format = '%Y%m%d.%H%M%S'
stamp_format = '%Y%m%d.%H:%M:%S'

def get_ping_values_from_result(s):
    time_start = s.find('mdev = ') + 7
    max_time = s[time_start:].split('/')[2]

    transmit_start = s.find('---\n') + 4
    transmit_end = s.find(' packets transmitted')
    packets_transmitted = s[transmit_start:transmit_end]

    receive_start = s.find('ted, ') + 5
    receive_end = s.find(' received,')
    packets_received = s[receive_start:receive_end]

    now = strftime(stamp_format, localtime())

    return PingValues(packets_transmitted, packets_received, max_time, now)

def get_current_ping():
    result = subprocess.run(ping_command, capture_output=True)
    try:
        return get_ping_values_from_result(result.stdout.decode('UTF8'))
    except:
        print("Bad values: " + result.stdout.decode('UTF8'))
        return None

def is_acceptable_ping(ping_values):
    if not ping_values:
        return True
    acceptable_time = ping_values.max_time <= max_acceptable_time
    acceptable_success_rate = (ping_values.packets_received/ping_values.packets_transmitted) >= min_acceptable_success_rate
    return acceptable_time and acceptable_success_rate

def main_loop():
    report = Report('pingreport.' + strftime(time_format, localtime()) + '.csv')
    print('Started with file ' + report.filename)
    i = 0
    while(True):
        print('--- Iteration {} ---'.format(i))
        sleep(sleep_interval)
        ping_values = get_current_ping()
        if not is_acceptable_ping(ping_values):
            print('Bad ping values: ' + str(ping_values))
            report.write(str(ping_values))
        i += 1

main_loop()
