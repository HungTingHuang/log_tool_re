


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
from multiprocessing import Process as pro, Queue as que, Pool as pool, Manager
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

def add(data, res):
    #res.append(10)
    
    for index, rows in enumerate(data):
        temp = []
        for value in rows:
            temp.append(value + 100) 
        res.append(temp)
    
    
    '''
    for value in data:
        value = int(value) + 100
        res.append(value)
    #''' 

class DataParser():

    def __init__(self):
        self.data = None
        self.datalen = 0
        self.processor_count = 4 #mp.cpu_count()
        
        self.divData = []
        self.resData = []
        self.outputData = [] 
        
        
        
    def import_data(self, data):
        self.data = data
        self.datalen = len(self.data)
        
        self.divData = [[] for _ in range(self.processor_count)]
        
        self.resData = [mp.Manager().list() for _ in range(self.processor_count)]
        self.outputData = [[] for _ in range(self.datalen)]
    
    def divide_data(self):
        
        data = self.data
        for ind in range(self.datalen):
            self.divData[ind%self.processor_count].append(data[ind])
                
        pass
    
    
    
    def proc_data(self, func):
        
        po = pool(self.processor_count)#mp.cpu_count()
        multiple_results = [po.apply_async(func, (self.divData[i],self.resData[i])) for i in range(self.processor_count)]
        #[res.get(timeout=None) for res in multiple_results]
        for res in multiple_results:
            res.get(timeout=None)
        
        #p = pro(target=func, args=(self.divData[0], self.resultData[0]))
        #p.start()
        #p.join()
        
        pass
        
    
    def conquer_data(self, callback):
        
        for ind in range(self.datalen):
            for key, value in enumerate(self.resData[ind%self.processor_count]):
                index = key*self.processor_count + ind%self.processor_count
                #print index
                self.outputData[index] = value
            pass
        
        callback(self.outputData)
        
        pass


test = ['0','1','2','3','4','5','6','7','8','9']
test1 = [[1,2,3,4],[11,12,13,14],[21,22,23,24],[31,32,33,34],[41,42,43,44],[51,52,53,54]]


def hello(data):
    for rows in data:
        print rows


class main():
    def __init__(self):
        proc = DataParser()
        proc.import_data(test1)
        proc.divide_data()
        proc.proc_data(add)
        proc.conquer_data(callback=hello)
        
        
if __name__ == '__main__':
    
    main()























