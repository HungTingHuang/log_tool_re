#m_model
import sqlite3 as lite
import time
from datetime import datetime, date
import calendar
from collections import OrderedDict
import wx.grid as gridlib
import xlrd
from matplotlib.cbook import Null
#import xlsgrid
#import numpy

class HugeTable(gridlib.PyGridTableBase):
    
    def __init__(self, title, data, rows, cols):
        gridlib.PyGridTableBase.__init__(self)
        self.title = title
        self.data = data
        
        self.row_count = rows
        self.col_count = cols
        
      
        
        self.ReadyOnly = gridlib.GridCellAttr()
        self.ReadyOnly.SetReadOnly(True)
        
        pass
    def UpdateData(self, title, data, rows, cols):
        self.title = title
        self.data = data
        
        #self.row_count = rows
        self.col_count = cols
        self.row_count = rows
        
        pass
    
    def GetAttr(self, row, col, kind):
        attr = None
        attr = self.ReadyOnly
        attr.IncRef()
        return attr
    
    '''
    def GetRowLabelValue(self, row):
        return 'fuck'
    #'''
    def GetColLabelValue(self, col):
        return self.title[col]
    
    def GetNumberRows(self):
        return self.row_count
    
    def GetNumberCols(self):
        return self.col_count
    
    
    def IsEmptyCell(self, row, col):
        return False
    
    def GetValue(self, row, col):
        
        
        if col >= len(self.data[row]) or row > self.row_count:
            return ''
        else:
            return self.data[row][col]
            pass
    
    def SetValue(self, row, col, value):
        self.data.write('SetValue(%d, %d, "%s") ignored.\n' % (row, col, value))
    
    
class Sqlite():
    def __init__(self):
        self.tableName = ''
        
        #repeat parameter
        self.count = 0
        self.data_len = 0
        pass
    
    
    def reset(self):
        self.count = 0
        self.data_len = 0
        pass
    
    def is_sqlite_file(self, filename):
        if filename == filename.split('.')[0]:
            return False
        else:
            if 'db' == filename.split('.')[1]:
                return True
            else:
                return False
        pass
     
    
    #@staticmethod
    def execute_command(self, filename, cmd):
        data = list()
        
        if not filename and not cmd:
            return data
        
        try:
            con = lite.connect(filename)
            cur = con.cursor()
            cur.execute(cmd)
            data = cur.fetchall()
            
        except lite.Error, e:
            print 'Error %s:' % e.args[0]
            data = []
        finally:
            if con:
                con.close()
            return data
        
    #@staticmethod
    def get_col_name(self, filename, cmd):
        data = list()
        cmd_t = cmd
        
        if not filename:
            pass
        else:
            if not cmd:
                cmd_t = 'SELECT * FROM %s LIMIT 1'%self.tableName
                pass
            else:
                pass  
        
        try:
            con = lite.connect(filename)
            
            cur = con.cursor()
            cur.execute(cmd_t)
            data = [f[0] for f in cur.description]
            
        except lite.Error, e:
            print 'Error %s:' % e.args[0]
            data = []
        finally:
            if con:
                con.close()
            return data
        
    def get_total_row_number(self, filename, cmd):
        count = 0
        temp = "SELECT COUNT(1) FROM "
        cmd_t = cmd.partition('FROM')
        cmd = temp + cmd_t[2] 
        if not filename:
            return count
        
        try:
            con = lite.connect(filename)
            cur = con.cursor()
            cur.execute(cmd)
            count = cur.fetchall()
        except lite.Error, e:
            print 'Error %s:' % e.args[0]
            count = 0
        finally:
            if con:
                con.close()
            return count
        pass
    
    #@staticmethod
    '''
    def get_data_repeat(self, filename, row_limit):
        data = list()
        if self.count == 0:#first call
            print type(self.get_total_row_number(filename)[0][0])
            self.data_len = self.get_total_row_number(filename)[0][0]
        offset = self.count * row_limit
        if (self.data_len - offset) < row_limit:
            row_limit = self.data_len - offset
            cmd = "SELECT * FROM %s LIMIT %s OFFSET %s"%(self.tableName, row_limit, offset)
            data = self.execute_command(filename, cmd)
            self.count = 0
            self.data_len = 0
        else:
            cmd = "SELECT * FROM %s LIMIT %s OFFSET %s"%(self.tableName, row_limit, offset)
            data = self.execute_command(filename, cmd)
        self.count += 1
        return data 
        pass
    '''
    
class LogParse():
    def __init__(self, filename):
        #Sqlite Database
        self.sqlite = Sqlite()
        self.tableName = 'log_raw'
        self.sqlite.tableName = self.tableName
        
        #identification_token
        self.id_token = 'msg'
        self.dev = 'Start New CCS Run.'
        
        self.ssm_aot = 'Load ccs.ini'
        self.ssm_balloon = 'Enter init state'
        self.ssm_odyssey = 'PROG-START:'
        self.ssm_trex = 'Initialize  VRide T-Rex'
        self.ssm_xride = 'PROG-START : Release Mode'
        self.ssm_freefall = 'Init State:connect btns done'
        self.ssm_mecha = 'Get hight score'
        
        self.emmem = 'HASP KEY CHECK : SUCCESS'
        
        #proj
        if filename == None:
            self.curProj = 'unknow'#current project
        else:
            self.find_current_project(filename)
        
    def find_total_row_number(self, filename, cmd):
        return self.sqlite.get_total_row_number(filename, cmd)[0][0]
    
    def find_table_col_name(self, filename, cmd):
        return self.sqlite.get_col_name(filename, cmd)
        pass
    def find_current_project_daytime(self, filename):
        cmd = 'SELECT ts FROM %s LIMIT 1'%self.tableName
        timestamp = self.sqlite.execute_command(filename, cmd)[0][0]
        return time.strftime('%Y-%m-%d', time.gmtime(timestamp/1000000))
        
        
    def find_current_project(self, filename):
        
        cmd = 'SELECT %s FROM %s LIMIT 1'%(self.id_token, self.tableName)
        data = self.sqlite.execute_command(filename, cmd)[0]
        
        if self.dev in data[0]:
            self.curProj = 'DEV_iRide'
        elif self.emmem in data[0]:
            self.curProj = 'Zoo_Emmem'
        elif self.ssm_aot in data[0]:
            self.curProj = 'SSM_AOT'
        elif self.ssm_freefall in data[0]:
            self.curProj = 'SSM_FreeFall'
        elif self.ssm_mecha in data[0]:
            self.curProj = 'SSM_Mecha'
        elif self.ssm_odyssey in data[0]:
            self.curProj = 'SSM_Odyssey'
        elif self.ssm_trex in data[0]:
            self.curProj = 'SSM_Trex'
        elif self.ssm_xride in data[0]:
            self.curProj = 'SSM_xRide'
        elif self.ssm_balloon in data[0]:
            self.curProj = 'SSM_Balloon'
        else:
            self.curProj = 'unknow'

        return self.curProj
    '''
    def find_mp_message(self, src, level):
        proj = self.curProj
        pass
    '''
    def find_mp_message(self, msg):
        if self.curProj == 'SSM_Balloon':
            if len(msg) > 294:
                return True
            else:
                return False
        else:
            if len(msg) > 320:
                return True
            else:
                return False
        pass
    
    
    
    def mp_message_parse(self, mp_message):
        if isinstance(mp_message, str):
            pass
        else:
            mp_message = ''.join(str(x) for x in mp_message)
            pass
        result_mp_message = OrderedDict()
        count = 0
        for x in mp_message.split(';'):
            item = x.partition('=')
            title = item[0]
            for y in item[2].split(','):
                
                if len(item[2].split(',')) == 1:
                    result_mp_message[title] = y
                else:
                    result_mp_message[title+(str(count+1))] = y
                count +=1
            count =0
            #'''
        return result_mp_message
        
        pass 
    
    def mp_message_standardize(self, mp_message):
        if isinstance(mp_message, str):
            pass
        else:
            mp_message = ''.join(str(x) for x in mp_message)
            pass
        
        raw_data = mp_message
        result_data = ''
        sep = 'LOG'
        if self.curProj == '':
            pass
        elif self.curProj == 'SSM_Trex':
            result_data = mp_message.partition(sep)
            result_data =  result_data[0].replace(':', ';').replace("'", ';').replace(' ','')+'LOG'+result_data[2].replace(',', ' ')
            result_data =  result_data.partition('SVOST')
            result_data = result_data[0]+";"+"SVOST"+result_data[2]
            result_data = result_data + ';'
            pass
        else:
            result_data = mp_message.partition(sep)
            if result_data[1] == '':
                sep = 'MPLOG'
                result_data = mp_message.partition(sep)
            else:
                pass
            result_data = result_data[0].replace(':', ';').replace("'", ';').replace(" ","")+sep+result_data[2].replace(',', ' ')
            result_data = result_data + ';'
            pass
        return result_data
        pass
    
    def get_title(self):
        pass
    
    def timestamp_convert(self, ts):
        _t = dict()
        _t['day'] = time.strftime('%Y-%m-%d', time.gmtime(ts/1000000))
        _t['time'] = time.strftime('%H:%M:%S', time.gmtime(ts/1000000))
        _t['ms'] = int(ts%1000000)
        return _t
        pass
    
    def unixtime_covert(self, year, mon, day, hr, mm, ss):
        _d = datetime(year, mon, day, hr, mm, ss)
        return calendar.timegm(_d.timetuple())
        pass
    
class Model():
    def __init__(self):
        self.sqlite = Sqlite()
        self.sqlite.tableName = 'log_raw'
    
    
    
   
    def GetFullDataCmd(self, filename):
        if not filename:
            return
        log = LogParse(filename)
        cmd = "SELECT * FROM %s"%log.tableName
        return cmd
        pass
    
    def GetTimeRangeCmd(self,filename, hl, ll):
        if not filename:
            return
        log = LogParse(filename)
        hl = str(hl)
        hl = hl[::-1].replace(hl[len(hl)-1][::-1], '%'[::-1], 1)[::-1]
        
        ll = str(ll)
        ll = ll[::-1].replace(ll[len(ll)-1][::-1], '%'[::-1], 1)[::-1]
        
        cmd_hl = "SELECT * FROM %s WHERE ts LIKE '%s' ORDER BY ts DESC LIMIT 1"%(log.tableName, hl)
        cmd_ll = "SELECT * FROM %s WHERE ts LIKE '%s' ORDER BY ts ASC LIMIT 1"%(log.tableName, ll)
        
        data_hl = self.sqlite.execute_command(filename, cmd_hl)
        data_ll = self.sqlite.execute_command(filename, cmd_ll)
        

        if len(data_hl) == 1 and len(data_ll) == 1:
            ts_hl = self.sqlite.execute_command(filename, cmd_hl)[0][0]
            ts_ll = self.sqlite.execute_command(filename, cmd_ll)[0][0]

            cmd_range = "SELECT * FROM %s WHERE ts BETWEEN %s AND %s ORDER BY ts ASC"%(log.tableName, ts_ll, ts_hl)
            #raw_data = self.sqlite.execute_command(filename, cmd_range)
            #data = self.SetDataToGrid(filename, raw_data)    
            return cmd_range
        else:
            return None
            pass
        pass
    
    def GetRowRangeData(self, filename, cmd, limit, offset):
        range = " LIMIT %s OFFSET %s"%(limit, offset)
        if not filename:
            return
        else:
            log = LogParse(filename)
            cmd += range
            #print 'start'
            raw_data = self.sqlite.execute_command(filename, cmd)            
            #print 'get raw data'
            data = self.SetDataToGrid(filename, raw_data)
            #print 'parsing data'
            return data
        pass
    '''
    def GetRowRangeData(self, filename, limit, offset):
        
        if not filename:
            return
        else:
            log = LogParse(filename)
            cmd = "SELECT * FROM %s LIMIT %s OFFSET %s"%(log.tableName, limit, offset)
           
            raw_data = self.sqlite.execute_command(filename, cmd)
            
            data = self.SetDataToGrid(filename, raw_data)
            return data
        pass
    ''' 
    '''
    def GetTimeRangeData(self, filename, hl, ll):
        if not filename:
            return
        log = LogParse(filename)
        hl = str(hl)
        hl = hl[::-1].replace(hl[len(hl)-1][::-1], '%'[::-1], 1)[::-1]
        
        ll = str(ll)
        ll = ll[::-1].replace(ll[len(ll)-1][::-1], '%'[::-1], 1)[::-1]
        
        cmd_hl = "SELECT * FROM %s WHERE ts LIKE '%s' ORDER BY ts DESC LIMIT 1"%(log.tableName, hl)
        cmd_ll = "SELECT * FROM %s WHERE ts LIKE '%s' ORDER BY ts ASC LIMIT 1"%(log.tableName, ll)
        
        data_hl = self.sqlite.execute_command(filename, cmd_hl)
        data_ll = self.sqlite.execute_command(filename, cmd_ll)
        

        if len(data_hl) == 1 and len(data_ll) == 1:
            ts_hl = self.sqlite.execute_command(filename, cmd_hl)[0][0]
            ts_ll = self.sqlite.execute_command(filename, cmd_ll)[0][0]

            cmd_range = "SELECT * FROM %s WHERE ts BETWEEN %s AND %s ORDER BY ts ASC"%(log.tableName, ts_ll, ts_hl)
            raw_data = self.sqlite.execute_command(filename, cmd_range)
            data = self.SetDataToGrid(filename, raw_data)    
            return data
        else:
            return None
            pass
        pass    
    '''
    def SetDataToGrid(self, filename, raw_data):
        if not len(raw_data) >= 1:
            return
        else:
            pass
        
        
        log = LogParse(filename)
        first_append_title = True
        data = [[] for _ in range(len(raw_data)+1)]
        title = self.sqlite.get_col_name(filename, '')
        
        mp_message = ''
        for item in title:
            data[0].append(item)
        
        iter = data[0].index('ts')
        data[0][iter] = 'timestamp'
        iter +=1
        #data[0].insert(iter, 'day')
        #iter +=1
        data[0].insert(iter, 'time')
        iter +=1
        data[0].insert(iter, 'ms')
        data[0][data[0].index('msg')] = 'mc_log'
        #print 'title processed'
        row_count = 1
        for row in raw_data:
            data[row_count].append(row[0])
            #data[row_count].append(self.log.timestamp_convert(row[0])['day'])
            data[row_count].append(log.timestamp_convert(row[0])['time'])
            data[row_count].append(log.timestamp_convert(row[0])['ms'])
            data[row_count].append(row[1])
            data[row_count].append(row[2])
            data[row_count].append(row[3])
            data[row_count].append(row[4])
            if log.find_mp_message(row[5]):
                mp_message = log.mp_message_standardize(row[5])
                mp_message = log.mp_message_parse(mp_message)#return OrderedDict()
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
                data[row_count].append(row[5])
                pass    
            row_count += 1
        #print 'write to array'
        return data
        pass

    """
    def GetDataOnItemActivated(self, filename, row_limit):
        log = LogParse(filename)
        if row_limit == 0:
            cmd = "SELECT * FROM %s"%log.tableName
        else:    
            cmd = "SELECT * FROM %s LIMIT %s"%(log.tableName, row_limit)
        #cmd = "SELECT * FROM %s"%self.log.tableName
        row_data = self.sqlite.execute_command(filename, cmd)
        data = self.SetDataToGrid(filename, row_data)
        
        if len(row_data) < 1:
            return None
        else:
            data = self.SetDataToGrid(filename, row_data)
            return data
            
        '''
        first_append_title = True
        data = [[] for _ in range(row_limit+1)]
        title = self.sqlite.get_col_name(filename, '')
        mp_message = ''
        
        for item in title:
            data[0].append(item)
        
        iter = data[0].index('ts')
        data[0][iter] = 'timestamp'
        iter +=1
        #data[0].insert(iter, 'day')
        #iter +=1
        data[0].insert(iter, 'time')
        iter +=1
        data[0].insert(iter, 'ms')
        data[0][data[0].index('msg')] = 'mc_log' 
        
        cmd = "SELECT * FROM %s LIMIT %s"%(self.log.tableName, row_limit)
        #cmd = "SELECT * FROM %s"%self.log.tableName
        temp = self.sqlite.execute_command(filename, cmd)
        
        row_count = 1
        for row in temp:
            data[row_count].append(row[0])
            #data[row_count].append(self.log.timestamp_convert(row[0])['day'])
            data[row_count].append(self.log.timestamp_convert(row[0])['time'])
            data[row_count].append(self.log.timestamp_convert(row[0])['ms'])
            data[row_count].append(row[1])
            data[row_count].append(row[2])
            data[row_count].append(row[3])
            data[row_count].append(row[4])
            if self.log.find_mp_message(row[5]):
                mp_message = self.log.mp_message_standardize(row[5])
                mp_message = self.log.mp_message_parse(mp_message)#return OrderedDict()
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
                data[row_count].append(row[5])
                pass    
            row_count += 1
        '''
        
        pass
    """

        #self, sql_name, col_limit, 
   

     