class PingValues():

    def __init__(self, packets_transmitted, packets_received, max_time, time_observed):
        self.packets_transmitted = int(packets_transmitted)
        self.packets_received = int(packets_received)
        self.max_time = float(max_time)
        self.time_observed = time_observed
    
    def __str__(self):
        return str(self.max_time) + ',' + \
        str(self.packets_transmitted) + ',' + \
        str(self.packets_received) + ',' + \
        str(self.time_observed)