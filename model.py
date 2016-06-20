#m_model
import sqlite3 as lite
import time
from datetime import datetime, date
import calendar
from collections import OrderedDict
import wx.grid as gridlib
from lib2to3.tests.support import proj_dir
import scanf as scanner
#import xlrd

#import xlsgrid
#import numpy


class LogInfo():
    def __init__(self):
        self.curProj = ''
        pass
    def set_current_project(self, proj):
        self.curProj = proj
        pass
        
    def get_mp_msg_title(self):
        if self.curProj == 'SSM_AOT':
            return self.get_ssm_aot_msg_title()
        else:
            pass
        pass
    def get_mp_msg_pattern(self):
        if self.curProj == 'SSM_AOT':
            return self.get_ssm_aot_msg_pattern()
        else:
            pass
        pass
    
    def get_ssm_aot_msg_title(self):
        msg_title = [
                'power_380', 'power_supply', 'auto_mode', 'btn_lock', 'mpc_error_code', #5
                'AO #1', 'AO #2', 'AO #3', 'AO #4', 'AO #5', 'AO #6',#6
                'AI #1', 'AI #2', 'AI #3', 'AI #4', 'AI #5', 'AI #6',#6
                
                'cylinder_lower_limit #1', 'cylinder_lower_limit #2', 'cylinder_lower_limit #3',
                'cylinder_lower_limit #4', 'cylinder_lower_limit #5', 'cylinder_lower_limit #6',#6
                
                'motor on output #1', 'motor on output #2', 'motor on output #3',
                'motor on output #4', 'motor on output #5', 'motor on output #6',#6
                
                'motor on input #1', 'motor on input #2', 'motor on input #3',
                'motor on input #4', 'motor on input #5', 'motor on input #6',#6
                
                'brake release output #1', 'brake release output #2', 'brake release output #3',
                'brake release output #4', 'brake release output #5', 'brake release output #6',#6
                
                'brake detect input #1', 'brake detect input #2', 'brake detect input #3',
                'brake detect input #4', 'brake detect input #5', 'brake detect input #6',#6
                
                'servo ai enable #1', 'servo ai enable #2', 'servo ai enable #3',
                'servo ai enable #4', 'servo ai enable #5', 'servo ai enable #6',#6
                
                'servo alarm #1', 'servo alarm #2', 'servo alarm #3',
                'servo alarm #4', 'servo alarm #5', 'servo alarm #6',#6
                
                'servo reset #1', 'servo reset #2', 'servo reset #3',
                'servo reset #4', 'servo reset #5', 'servo reset #6',#6
                
                'servo status #1', 'servo status #2', 'servo status #3',
                'servo status #4', 'servo status #5', 'servo status #6',#6
                
                'servo_alarm_code #1', 'servo_alarm_code #2', 'servo_alarm_code #3',
                'servo_alarm_code #4', 'servo_alarm_code #5', 'servo_alarm_code #6',#6
                
                'servo_alarm_minor_code #1', 'servo_alarm_minor_code #2',
                'servo_alarm_minor_code #3', 'servo_alarm_minor_code #4',
                'servo_alarm_minor_code #5', 'servo_alarm_minor_code #6',#6
                
                'servo_current #1', 'servo_current #2', 'servo_current #3',
                'servo_current #4', 'servo_current #5', 'servo_current #6',#6
                
                'servo_busvoltage #1', 'servo_busvoltage #2', 'servo_busvoltage #3',
                'servo_busvoltage #4', 'servo_busvoltage #5', 'servo_busvoltage #6',#6
                
                'servo_ai #1', 'servo_ai #2', 'servo_ai #3',
                'servo_ai #4', 'servo_ai #5', 'servo_ai #6',#6
                
                'servo_speed #1', 'servo_speed #2', 'servo_speed #3',
                'servo_speed #4', 'servo_speed #5', 'servo_speed #6',#6
                
                'servo_hour #1', 'servo_hour #2', 'servo_hour #3',
                'servo_hour #4', 'servo_hour #5', 'servo_hour #6',#6
                
                'is_carrier_remoteio_conn',
                'i_carrier_auto_control',
                'i_carrier_interlock', 
                'i_carrier_vfd_error',
                'o_carrier_moving_forward',
                'o_carrier_moving_backward',
                'i_carrier_front',
                'i_carrier_back', 
                'i_carrier_over', 
                'i_carrier_high_speed',
                
                'i_carrier_pressure', 
                'o_carrier_up_lock', 'o_carrier_up_unlock',  
                'i_carrier_up_lock #1', 'i_carrier_up_lock #2',
                'i_carrier_up_unlock #1', 'i_carrier_up_unlock #2',
                'o_carrier_down_lock #1', 'o_carrier_down_unlock #2',
                'i_carrier_down_lock #1', 'i_carrier_down_lock #2', 
                'i_carrier_down_unlock #1', 'i_carrier_down_unlock #2',
                
                'is_sb_remoteio_conn', 
                'o_seatbelt_buckle_unlock', 
                'o_seatbelt_roller_unlock', 
                
                'i_seatbelt #1', 'i_seatbelt #2', 'i_seatbelt #3', 'i_seatbelt #4', 'i_seatbelt #5',
                'i_seatbelt #6', 'i_seatbelt #7', 'i_seatbelt #8', 'i_seatbelt #9', 'i_seatbelt #10',#10
                
                'o_seatbelt_led_enable', 'i_all_sb_lock',
                
                'i_canopy_auto_control', 
                'o_canopy_up', 'o_canopy_down', 
                'i_canopy_up', 'i_canopy_down' 'i_canopy_up_over', 'i_canopy_down_over',
                
                'is_gt_remoteio_conn', 'i_gate_auto_control', 'i_gate_interlock', 'i_gate_vfd_error', 
                'o_gate_close', 'o_gate_open', 
                'i_gate_close', 'i_gate_close_over_limit', 'i_gate_open', 'i_gate_open_over_limit',
                
                'o_door_close #1', 'o_door_close #2', 'i_door_close #1', 'i_door_close #2',#DR
                
                'is_es_remoteio_conn', 'o_pwm_orentation_led', 'o_pwm_wind', 'o_spray_enable', 
                
                'o_scent_release #1', 'o_scent_release #2', 'o_scent_release #3',
                
                'play_last_ms', 'play_sync_ms', 'play_time_ms'#MS
            ]
        return msg_title
        pass
    def get_ssm_aot_msg_pattern(self):
        msg_pattern = "ST=%c%c%c%c;ERR=%3c;AO=%3c,%3c,%3c,%3c,%3c,%3c;AI=%3c,%3c,%3c,%3c,%3c,%3c;\
                LL=%c%c%c%c%c%c;RUN=%c%c%c%c%c%c,%c%c%c%c%c%c;BKR=%c%c%c%c%c%c,%c%c%c%c%c%c;\
                EN=%c%c%c%c%c%c;ALM=%c%c%c%c%c%c;RST=%c%c%c%c%c%c;SVO=%4c,%4c,%4c,%4c,%4c,%4c;\
                ALMC=%4c,%4c,%4c,%4c,%4c,%4c;MINC=%16c,%16c,%16c,%16c,%16c,%16c;A=%f,%f,%f,%f,%f,%f;\
                V=%f,%f,%f,%f,%f,%f;AI%%=%f,%f,%f,%f,%f,%f;SPD=%f,%f,%f,%f,%f,%f;\
                HR=%4c,%4c,%4c,%4c,%4c,%4c;CA=%c%c%c%c,%c%c,%c%c%c%c;CL=%c,%c%c,%c%c%c%c,%c%c,%c%c%c%c;\
                SB=%c,%c%c,%c%c%c%c%c%c%c%c%c%c,%c,%c;CN=%c,%c%c,%c%c%c%c;GT=%c%c%c%c,%c%c,%c%c%c%c;\
                DR=%c%c,%c%c;ES=%c,%2c,%2c,%c,%c%c%c;MS=%6c,%6c,%6c;"
        return msg_pattern
        pass





class HugeTable(gridlib.PyGridTableBase):
    
    def __init__(self, title, data, rows, cols):
        gridlib.PyGridTableBase.__init__(self)
        self.title = title
        
        self.data_souce = data
        self.row_count_source = rows
        
        #remve first row
        self.data = self.data_souce[1:]
        self.row_count = self.row_count_source-1
        
        
        
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
    def set_table_name(self, tablename):
        self.tableName = tablename
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
                cmd_t += ' LIMIT 1'
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
    def __init__(self):
        #Sqlite Database
        self.sqlite = Sqlite()
        #self.tableName = 'mp_log_all'
        self.tableName = 'log_raw'
        self.sqlite.tableName = self.tableName
        self.timezone = 0
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
        self.filename = ''
        
        #proj
        if self.filename == None:
            self.curProj = 'unknow'#current project
        
      
    def set_filename(self, filename):
        self.filename = filename
        self.curProj = self.find_current_project()
        
    def set_timezone(self, timezone):
        self.timezone = timezone
        pass    
    
    def find_total_row_number(self, cmd):
        return self.sqlite.get_total_row_number(self.filename, cmd)[0][0]
    
    def find_table_col_name(self, cmd):
        return self.sqlite.get_col_name(self.filename, cmd)
        pass
    def find_current_project_daytime(self):
        cmd = 'SELECT ts FROM %s LIMIT 1'%self.tableName
        timestamp = self.sqlite.execute_command(self.filename, cmd)[0][0]
        return time.strftime('%Y-%m-%d', time.gmtime(timestamp/1000000))
        
        
    def find_current_project(self):
        
        cmd = 'SELECT %s FROM %s LIMIT 1'%(self.id_token, self.tableName)
        data = self.sqlite.execute_command(self.filename, cmd)[0]
        
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
        msg = str(msg)
        if self.curProj == 'unknow':
            return False
        
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
    
    def mp_message_parsing(self, mp_message):
        if isinstance(mp_message, str):
            pass
        else:
            mp_message = ''.join(str(x) for x in mp_message)
            pass
        result_mp_message = OrderedDict()
        _info = LogInfo()
        if self.curProj == '':
            return
        _info.set_current_project(self.curProj)
        mpc_log_message = mp_message.partition('MPLOG=')[2]
        log_message = mp_message.partition('MPLOG')[0]
        
        _title = _info.get_mp_msg_title()
        _pattern = _info.get_mp_msg_pattern()
        
        
        
        _data = scanner.sscanf(log_message, _pattern)
        
        
        
        for index, key in enumerate(_title):
            
            result_mp_message[key] = _data[index]
            pass
        
        result_mp_message['MPLOG'] = mpc_log_message
        
        return result_mp_message
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
                if y == '':
                    continue 
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
            result_data = result_data.replace('LOG', 'MPLOG')
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
            
            result_data = result_data.replace('LOG', 'MPLOG')
            
            pass
        return result_data
        pass
    
    def get_title(self):
        pass
    
    def timestamp_convert(self, ts):
        _t = dict()
        _t['day'] = time.strftime('%Y-%m-%d', time.gmtime(ts/1000000))
        _t['time'] = time.strftime('%H:%M:%S', time.gmtime(ts/1000000))
        
        day_offset = 0
        hr_offset = 0
        
        hr_offset = (int(_t['time'][:2]) + int(self.timezone))
        if hr_offset > 24:
            day_offset = int(_t['day'][-2:])+1
            hr_offset = int(hr_offset %24)
        else:
            pass
        
        _t['day'] = _t['day'].replace(_t['day'][-2:], str(day_offset))
        
        _t['time'] = _t['time'].replace(_t['time'][:2], '{:02d}'.format(hr_offset))
        
        
        
        
        
        _t['ms'] = int(ts%1000000)
        
        
        
        return _t
        pass
    
    def unixtime_covert(self, year, mon, day, hr, mm, ss):
        _d = datetime(year, mon, day, hr, mm, ss)
        return calendar.timegm(_d.timetuple())
        pass
    
class Model():
    def __init__(self, filename):
        
        self.parse = LogParse()
        
        
        
        
        self.filename = filename
        if self.filename == '':
            return
        self.parse.set_filename(self.filename)
    
   
    def GetFullDataCmd(self):
        if not self.filename:
            return
        
        cmd = "SELECT * FROM %s"%self.parse.tableName
        return cmd
        pass
    
    def GetTimeRangeCmd(self, hl, ll):
        
        hl = str(hl)
        hl = hl[::-1].replace(hl[len(hl)-1][::-1], '%'[::-1], 1)[::-1]
        
        ll = str(ll)
        ll = ll[::-1].replace(ll[len(ll)-1][::-1], '%'[::-1], 1)[::-1]
        
        cmd_hl = "SELECT * FROM %s WHERE ts LIKE '%s' ORDER BY ts DESC LIMIT 1"%(self.parse.tableName, hl)
        cmd_ll = "SELECT * FROM %s WHERE ts LIKE '%s' ORDER BY ts ASC LIMIT 1"%(self.parse.tableName, ll)
        
        data_hl = self.parse.sqlite.execute_command(self.filename, cmd_hl)
        data_ll = self.parse.sqlite.execute_command(self.filename, cmd_ll)
        

        if len(data_hl) == 1 and len(data_ll) == 1:
            ts_hl = self.parse.sqlite.execute_command(self.filename, cmd_hl)[0][0]
            ts_ll = self.parse.sqlite.execute_command(self.filename, cmd_ll)[0][0]

            cmd_range = "SELECT * FROM %s WHERE ts BETWEEN %s AND %s ORDER BY ts ASC"%(self.parse.tableName, ts_ll, ts_hl)
            #raw_data = self.sqlite.execute_command(filename, cmd_range)
            #data = self.SetDataToGrid(filename, raw_data)    
            return cmd_range
        else:
            return None
            pass
        pass
    
    def GetRowRangeData(self, cmd, limit, offset):
        range = " LIMIT %s OFFSET %s"%(limit, offset)
        order = ' ORDER BY ts ASC'
        temp = str(cmd)
        if not self.filename:
            return
        else:
            
            
            cmd = cmd + order + range
            
            #print 'start'
            raw_data = self.parse.sqlite.execute_command(self.filename, cmd)            
            #print 'get raw data'
           
            data = self.SetDataToGrid(raw_data, temp)
            
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
    def SetDataToGrid(self, raw_data, cmd):
        

        if not len(raw_data) >= 1:
            return
        else:
            pass
        
        
        
        first_append_title = True
        data = [[] for _ in range(len(raw_data)+1)]
        title = self.parse.find_table_col_name(cmd)
        
        
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
        
        if 'msg' in data[0]:
            data[0][data[0].index('msg')] = 'mc_log'
        #print 'title processed'
        
        
        
        row_count = 1
        for index, row in enumerate(raw_data):
            
            for ind, value in enumerate(row):
                
                if ind == 0:
                    data[row_count].append(row[ind])
                    #data[row_count].append(self.log.timestamp_convert(row[0])['day'])
                    data[row_count].append(self.parse.timestamp_convert(row[ind])['time'])
                    data[row_count].append(self.parse.timestamp_convert(row[ind])['ms'])
                elif ind == 5:
                    if  self.parse.find_mp_message(row[ind]):
                        
                        mp_message = self.parse.mp_message_standardize(row[ind])
                        mp_message = self.parse.mp_message_parsing(mp_message)#return OrderedDict()
                        
                        if first_append_title:
                            for keys in mp_message:
                                data[0].append(keys)
                                first_append_title = False
                                pass
                        data[row_count].append('')
                        for key in mp_message:
                            data[row_count].append(mp_message[key])
                        else:
                            pass
                    else:
                        data[row_count].append(row[ind])
                        pass
                else:
                    data[row_count].append(row[ind])
                    pass
                
                    
                        
                #data[row_count].append(row[ind])
            row_count += 1
            
            
            
            
            '''
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
            '''
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
   

     