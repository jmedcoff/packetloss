class Report():

    def __init__(self, filename):
        self.filename = filename
        self.write('max_time,packets_transmitted,packets_received,time_observed')
    
    def write(self, s):
        with open(self.filename, 'a') as file:
            file.writelines(s)
            file.write('\n')
    
