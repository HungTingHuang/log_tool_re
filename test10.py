


'''
def SetDataToGrid(self, raw_data, cmd):
        
        
        if not len(raw_data) >= 1:
            print 'error'
            return
        else:
            pass
        
        
        
        first_append_title = True
        data = [[] for _ in range(len(raw_data)+1)]
        title = self.parse.find_table_col_name(cmd)
        
        
        mp_message_t = ''
        for item in title:
            data[0].append(item)
        
        iter = data[0].index('ts')
        data[0][iter] = 'timestamp'
        iter +=1
        data[0].insert(iter, 'time')
        iter +=1
        data[0].insert(iter, 'ms')
        
        if 'msg' in data[0]:
            data[0][data[0].index('msg')] = 'mc_log'
        
        self.parse.timezone = self.timezone
        
        mp_message = OrderedDict()
        row_count = 1
        for index, row in enumerate(raw_data):
            for ind, value in enumerate(row):
                
                if ind == 0:
                    data[row_count].append(row[ind])
                    data[row_count].append(self.parse.timestamp_convert(row[ind])['time'])
                    data[row_count].append(self.parse.timestamp_convert(row[ind])['ms'])
                elif ind == 5:
                    if  self.parse.find_mp_message(row[ind]) and self.IsParsing:
                        mp_message_t = self.parse.mp_message_standardize(row[ind])
                        mp_message = self.parse.mp_message_parsing(mp_message_t)#return OrderedDict()
                        
                        if first_append_title:
                            for keys in mp_message:
                                data[0].append(keys)
                                first_append_title = False
                                pass
                        data[row_count].append('')
                        for key in mp_message:
                            data[row_count].append(mp_message[key])
                        pass
                    else:
                        
                        if not row[ind] == None:
                            data[row_count].append(row[ind])
                        pass
                    
                else:
                    
                    if not row[ind] == None:
                        data[row_count].append(row[ind])
                    pass
            row_count += 1
        return data
        pass

#'''







'''

filepath = 'D:\workspace\ssm_log_example\AOT\log-20160623.db'
query = "SELECT * FROM log_raw"


mm = _m.Model(filepath)
lite = _m.Sqlite()

start_time = str(time.time())
#print start_time + ":start time" 
rawData = lite.execute_command(filepath, 'SELECT * FROM log_raw')
end_time = str(time.time())
#print end_time + ":end time"
total_time = float(end_time) - float(start_time)
#get rawdata
'''
import multiprocessing as mp
from multiprocessing import Process as pro, Queue as que, Pool as Po
import time,os,sys,math

def f(name):
    print   'hello ', name
    print   os.getpid()
    print   os.getpid()
    sys.stdout.flush()
    for i in xrange(10000000):
        math.sqrt(i**2)
    print   name,'ok'
    sys.stdout.flush()

def add(array, res):
    print res
    res.put('1', True, None)
        

class BigDataParser():

    def __init__(self):
        self.data = None
        self.datalen = 0
        self.procCount = 4
        self.divData = []
        self.resultData = [0]
        #self.resData = [0]
        
    def import_data(self, data):
        self.data = data
        self.datalen = len(self.data)
        #self.resultData = que.Queue(self.datalen)
    
    def divide_data(self):
        
        data = self.data
        self.divData = [[] for _ in range(self.datalen)]
        
        for ind in range(self.datalen):
            self.divData[ind%self.procCount].append(data[ind])        
        pass
    
    
    
    def proc_data(self, func):
        pool = Po(4)
        multiple_results = [pool.apply_async(func, (i,)).start() for i in range(4)]
        #print [res.get(timeout=None) for res in multiple_results]
        
        pass
        
    
    def conquer_data(self):
        
        
        
        pass


test = ['0','1','2','3','4','5','6','7','8','9']




class main():
    def __init__(self):
        proc = BigDataParser()
        proc.import_data(test)
        proc.divide_data()
        proc.proc_data(f)
        
        
if __name__ == '__main__':
    
    main()























