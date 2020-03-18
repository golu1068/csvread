from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename 
import threading
import time

master = Tk()
w, h = master.winfo_screenwidth(), master.winfo_screenheight()
#master.overrideredirect(1)
master.geometry("%dx%d+%d+%d" % (w/4, h/5, w/2.5, h/2.5))
master.title('TWSTFT GUI')

#master.iconbitmap(r'E:\spyder_code\New_folder\multipath_test\favicon.ico')
#master.geometry('300x200+460+320')
master.resizable(0, 0)
#master.maxsize(500,200)

import socket
from bitstring import Bits
import csv
row = ['Header1', 'Header2', 'Header3','checksum','messege length','weekno','towc','year','month','day','hour','min','sec',\
      'MOS','Time_REF','OSC_lock','clk_src','Time_init_stat','sync_stat','stat_pos_mod','optical_port_o/p','Tx_sig_on/off','LS_st_ID',\
      'LS_lat','LS_lon','LS_alt','SA_lat','SA_lon','SA_alt','Tx_freq','Rx_freq', 'Tx_pow','Time_off','freq_off','Osc_con_vol','TSPO',\
      'NMEA_bd_rate','RS422_PPS_del','RS422_10MHz_delay','Off_wrt_master','Fault_ID','PRN_chan','CH_track_stat','doppler','lock_count',\
        'C/No','Decr_stat','Auth_stat','LS_time_off','RS_time_off','time_off','freq_off','RS_TX_pow','RS_C/No','lst_year','lst_mon','lst_day','lst_hour',\
        'lst_min','lst_sec','RS_lat','RS_lon','RS_alt','PRN_chan2','CH_track_stat2','doppler2','lock_count2',\
      'C/No2','Decr_stat2','Auth_stat2','LS_time_off2','RS_time_off2','time_off2','freq_off2','RS_TX_pow2','RS_C/No2','lst_year2','lst_mon2','lst_day2','lst_hour2',
   'lst_min2','lst_sec2','RS_lat2','RS_lon2','RS_alt2' ]
      
      
      
      
#      'Tx_pow','Time_off','freq_off','Osc_con_vol','TSPO',\
#      'NMEA_bd_rate','RS422_PPS_del','RS422_10MHz_delay','Off_wrt_master','Fault_ID','PRN_chan','CH_track_stat','doppler','lock_count',\
#      'C/No','Decr_stat','Auth_stat','one_way_off','RS_time_off','freq_off','RS_TX_pow','RS_C/No','lst_year','lst_mon','lst_day','lst_hour',
#      'lst_min','lst_sec','RS_lat','RS_lon','RS_alt','PRN_chan2','CH_track_stat2','doppler2','lock_count2',\
#      'C/No2','Decr_stat2','Auth_stat2','one_way_off2','RS_time_off2','freq_off2','RS_TX_pow2','RS_C/No2','lst_year2','lst_mon2','lst_day2','lst_hour2',
#      'lst_min2','lst_sec2','RS_lat2','RS_lon2','RS_alt2']


clo=1;

def extract_val(data, strt_ind, no_by):
    stri='';
    for i in range(strt_ind, strt_ind+no_by):
        stri = str(format(data[i],'08b')) + stri
    return int(stri,2)

def SinglePrecision2Float(data):
    bias = 127
    sign = int(data[0])
    exp = data[1:9]
    frac = data[9:]
    exp_dec = int(exp,2)
    fr=0.0;
    for i in range(len(frac)):
        fr = fr + int(frac[i])*(2.0**-(i+1))
    if (sign == 0):
        re = (1+fr)*(2**(exp_dec-bias))
    else:
        re = -(1+fr)*(2**(exp_dec-bias))
    return round(re, 7)

def DoublePrecision2Float(data):
    sign=int(data[0])
    arr=data[1:12]
    #print(arr)
    e=(int(arr,2))
    #print(e)
    arr2=data[12:]
   #print(arr2)
    total=0
    for i in range(len(arr2)):
        total=total+(int(arr2[i])*(2**-(i+1)))
    
    
    total=total+1
    total=total*(2**(e-1023))
    if(sign==0):
       total=total
    else:
        total=-(total)
    return round(total, 7)




def extract_float(data, strt_ind, no_by,s_d):
    stri='';
    for i in range(strt_ind, strt_ind+no_by):
        stri = str(format(data[i],'08b'))+ stri

   
    if(s_d==1):
        return SinglePrecision2Float(stri)
    elif(s_d==2):
        return DoublePrecision2Float(stri)

arr=[];
ptr=0
header_dict={};
strt=0;
UDP_IP_ADDRESS=''
UDP_PORT_NO=2000
file_path = ''


def go_to_while():
    global UDP_IP_ADDRESS, UDP_PORT_NO, strt, clo, file_path
    if (strt == 1):
        try:
            serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))
        except:
            print('The requested address is not valid in its context')
            print(str(UDP_IP_ADDRESS) +  ' or ' + str(UDP_PORT_NO) + ' is not valid')
            print('Please try again.....')
            master.destroy()
            return
        one_t=0
        csv_data=[]
        
        while True:
        
            if (clo == 0):
                break
            
            data_m, addr = serverSock.recvfrom(UDP_PORT_NO)    #port no configured in webpage
            for i in range(len(data_m)):
                re = data_m[i]
                arr.append(re)
                
            header=(arr[0:3])
            print((header[0:3]))
            csv_data.append(header[0])
            csv_data.append(header[1])
            csv_data.append(header[2])
            checksum=extract_val(arr,3,2)
            header_dict['checksum']=checksum
            print('checksum:',checksum)
            csv_data.append(checksum)
            msg_len=extract_val(arr,5,2)
            print("messege length:",msg_len)
            csv_data.append(msg_len)
            week_no=extract_val(arr,7,2)
            print("week no:",week_no)
            csv_data.append(week_no)
            towc=extract_val(arr,9,4)
            print("towc:",towc)
            csv_data.append(towc)
            year=extract_val(arr,13,2)
            print("year:",year)
            csv_data.append(year)
            month=extract_val(arr,15,1)
            print("month:",month)
            csv_data.append(month)
            day=extract_val(arr,16,1)
            print("day:",day)
            csv_data.append(day)
            hour=extract_val(arr,17,1)
            print("hour:",hour)
            csv_data.append(hour)    
            minn=extract_val(arr,18,1)
            print("minn:",minn)
            csv_data.append(minn)
            sec=extract_val(arr,19,1)
            print("sec:",sec)
            csv_data.append(sec)
            mode_of_sys=extract_val(arr,20,1)
            print("mode_of_sys:",mode_of_sys)
            csv_data.append(mode_of_sys)
            if((arr[21]&0x07)==0):
                print("Time reference:internal GNSS rx")
            elif((arr[21]&0x07)==1):
                print("Time reference:External GNSS rx")
            elif((arr[21]&0x07)==2):
                print("Time reference:NTP server")
            elif((arr[21]&0x07)==3):    
                print("Time reference:manual")
            elif((arr[21]&0x07)==4):
              print("Time reference:TWSTFT master")
            time_ref=(arr[21]&0x07)
            csv_data.append(time_ref) 
            osc_lock=(arr[21]>>3 & 0x01)
            if(osc_lock==0):
                print("osc_lock:not locked")
            elif(osc_lock==1):
                print("osc_lock:locked")
            csv_data.append(osc_lock)  
            clk_src=(arr[21]>>4 & 0x01)
            if(clk_src==0):
                print("clk_src:internal")
            elif(osc_lock==1):
                print("clk_src:external")
            csv_data.append(clk_src)    
            Time_init_status=(arr[21]>>5 & 0x01)
            if(Time_init_status==0):
                print("Time_init_status:not initialized")
            elif(Time_init_status==1):
                print("Time_init_status:initialized")
            csv_data.append(Time_init_status)    
            sync_status=(arr[21]>>6 & 0x03)
            if(sync_status==0):
                print("sync_status:sync")
            elif(sync_status==1):
                print("sync_status:no sync")
            elif(sync_status==2):
                print("sync_status:holdover")
            csv_data.append(sync_status)     
            station_pos_mode=(arr[22] & 0x01)
            if(station_pos_mode==0):
                print("station_pos_mode:Manual")
            elif(station_pos_mode==1):
                print("station_pos_mode:External GNSS RX")
            csv_data.append(station_pos_mode)     
            optical_port_output=(arr[22]>>1 & 0x03)
            if(optical_port_output==0):
                print("optical_port_output:1PPS")
            elif(optical_port_output==1):
                print("optical_port_output:10 MHz")
            elif(optical_port_output==2):
                print("optical_port_output:TOD(Time Of Day)")
            csv_data.append(optical_port_output)    
            TX_signal_pow=(arr[22]>>3 & 0x01)
            if(TX_signal_pow==0):
                print("TX_signal_pow:OFF")
            elif(optical_port_output==1):
                print("TX_signal_pow:ON")
            csv_data.append(TX_signal_pow)     
            Local_station_ID=extract_val(arr,25,1)
            print("Local_station_ID:",Local_station_ID)
            csv_data.append(Local_station_ID)
            LS_latitude= extract_float(arr,26,4,1)
            print("LS_latitude:",LS_latitude)
            csv_data.append(LS_latitude)
            LS_longitude= extract_float(arr,30,4,1)
            print("LS_longitude:",LS_longitude)
            csv_data.append(LS_longitude)
            LS_altitude= extract_float(arr,34,4,1)
            print("LS_altitude:",LS_altitude)
            csv_data.append(LS_altitude)
            SA_latitude= extract_float(arr,38,4,1)
            print("SA_latitude:",SA_latitude)
            csv_data.append(SA_latitude)
            SA_longitude= extract_float(arr,42,4,1)
            print("SA_longitude:",SA_longitude)
            csv_data.append(SA_longitude)
            SA_altitude= extract_float(arr,46,4,1)
            print("SA_altitude:",SA_altitude)
            csv_data.append(SA_altitude)
            Tx_frequency=extract_float(arr,50,4,1)
            print("Tx_frequency:",(Tx_frequency))
            csv_data.append(Tx_frequency) 
            
            ########################################################################
            Rx_frequency=extract_float(arr,54,4,1)
            print("Rx_frequency:",(Rx_frequency))
            csv_data.append(Rx_frequency) 
            
            TX_power=extract_val(arr,58,4)  #signed
            binary = bin(TX_power)
            bits = Bits(bin=binary)
            TX_power = bits.int
            print("TX_power:",(TX_power))
            csv_data.append(TX_power)
            
            Time_offset=extract_float(arr,62,8,2)
            print("Time_offset:",Time_offset)
            csv_data.append(Time_offset)  
            
            Freq_offset=extract_float(arr,70,8,2)
            print("Freq_offset:",Freq_offset)
            csv_data.append(Freq_offset)
            
            Osc_control_voltage=extract_val(arr,78,4)
            print("Osc_control_voltage:",Osc_control_voltage)
            csv_data.append(Osc_control_voltage)  
            
            TSPO=extract_val(arr,82,4)
            print("TSPO:",TSPO)
            csv_data.append(TSPO) 
            
            NMEA_baud_rate=extract_val(arr,86,4)
            print("NMEA_baud_rate:",NMEA_baud_rate)
            csv_data.append(NMEA_baud_rate) 
            
            RS422_1PPS_delay=extract_val(arr,90,2)
            print("RS422_1PPS_delay:",RS422_1PPS_delay)
            csv_data.append(RS422_1PPS_delay) 
            
            RS422_10MHz_delay=extract_val(arr,92,2)
            print("RS422_10MHz_delay:",RS422_10MHz_delay)
            csv_data.append(RS422_10MHz_delay)
            
            Offset_wrt_master=extract_val(arr,94,4)
            binary = bin(Offset_wrt_master)
            bits = Bits(bin=binary)
            Offset_wrt_master = bits.int
            print("Offset_wrt_master:",(Offset_wrt_master))
            csv_data.append(Offset_wrt_master)
            
            Fault_id=extract_val(arr,98,4)
            print("Fault_id:",Fault_id)
            csv_data.append(Fault_id)
            
        
            
            
            
            
        #    TX_power=extract_val(arr,54,4)  #signed
        #    binary = bin(TX_power)
        #    bits = Bits(bin=binary)
        #    TX_power = bits.int
        #    print("TX_power:",(TX_power))
        #    csv_data.append(TX_power)    
        #    Time_offset=extract_float(arr,58,8,2)
        #    print("Time_offset:",Time_offset)
        #    csv_data.append(Time_offset)  
        #    Freq_offset=extract_float(arr,66,8,2)
        #    print("Freq_offset:",Freq_offset)
        #    csv_data.append(Freq_offset)   
        #    Osc_control_voltage=extract_val(arr,74,4)
        #    print("Osc_control_voltage:",Osc_control_voltage)
        #    csv_data.append(Osc_control_voltage)   
        #    TSPO=extract_val(arr,78,4)
        #    print("TSPO:",TSPO)
        #    csv_data.append(TSPO)  
        #    NMEA_baud_rate=extract_val(arr,82,4)
        #    print("NMEA_baud_rate:",NMEA_baud_rate)
        #    csv_data.append(NMEA_baud_rate)  
        #    RS422_1PPS_delay=extract_val(arr,86,2)
        #    print("RS422_1PPS_delay:",RS422_1PPS_delay)
        #    csv_data.append(RS422_1PPS_delay) 
        #    RS422_10MHz_delay=extract_val(arr,88,2)
        #    print("RS422_10MHz_delay:",RS422_10MHz_delay)
        #    csv_data.append(RS422_10MHz_delay)
        #    Offset_wrt_master=extract_val(arr,90,4)
        #    binary = bin(Offset_wrt_master)
        #    bits = Bits(bin=binary)
        #    Offset_wrt_master = bits.int
        #    print("Offset_wrt_master:",(Offset_wrt_master))
        #    csv_data.append(Offset_wrt_master)
        #    Fault_id=extract_val(arr,94,4)
        #    print("Fault_id:",Fault_id)
        #    csv_data.append(Fault_id)
        #    
            ####################################channel data 1#####################################
             ##channel 1 data
            PRN_channel1=extract_val(arr,126,1)
            print("PRN_channel1:",PRN_channel1)
            csv_data.append(PRN_channel1)
            
            Channel_Track_Status=extract_val(arr,127,1)
            if(Channel_Track_Status==0):
                print("Channel_Track_Status:IDLE")
            elif(Channel_Track_Status==1):
                print("Channel_Track_Status:Acquisition")        
            elif(Channel_Track_Status==2):
                print("Channel_Track_Status:FLL")  
            elif(Channel_Track_Status==3):
                print("Channel_Track_Status:PLL")       
            elif(Channel_Track_Status==4):
                print("Channel_Track_Status:Reacquisition")  
            csv_data.append(Channel_Track_Status) 
            
            Doppler=extract_float(arr,128,4,1)
            print("Doppler:",Doppler)    
            csv_data.append(Doppler)
            
            Lock_Count= extract_val(arr,132,4)
            print("Lock_Count:",Lock_Count) 
            csv_data.append(Lock_Count)
            
            C_N0=extract_float(arr,136,4,1)
            print("C_N0:",(C_N0)) 
            csv_data.append(C_N0)
            
            Decryption_status=extract_val(arr,140,1)
            print("Decryption_status:",Decryption_status)
            csv_data.append(Decryption_status)
            Authentication_status=extract_val(arr,141,1)
            print("Authentication_status:",Authentication_status)
            csv_data.append(Authentication_status)
            
            LS_time_offset=extract_float(arr,142,8,2)  #it was One_way_offset before
            print("One_way_offset:",LS_time_offset)
            csv_data.append(LS_time_offset)
            RS_time_offset=extract_float(arr,150,8,2)
            print("RS_time_offset:",RS_time_offset)  
            csv_data.append(RS_time_offset)
            
            time_offset=extract_float(arr,158,8,2)
            print("time_offset:",time_offset)  
            csv_data.append(time_offset)
            
            Freq_offset=extract_float(arr,166,8,2)
            print("Freq_offset:",Freq_offset)  
            csv_data.append(Freq_offset)
            
            RS_tx_power=extract_float(arr,174,4,1)
            print("RS_tx_power:",RS_tx_power) 
            csv_data.append(RS_tx_power) 
            
            RS_C_N0=extract_float(arr,178,4,1)
            print("RS_C_N0:",RS_C_N0) 
            csv_data.append(RS_C_N0)
            
            Year1=extract_val(arr,182,2)
            Month1=extract_val(arr,184,1)
            Day1=extract_val(arr,185,1)
            Hour1=extract_val(arr,186,1)
            Min1=extract_val(arr,187,1)
            Sec1=extract_val(arr,188,1)
            print("Last_sync_time:%s.%s.%s.%s/%s/%s"%(Hour1,Min1,Sec1,Day1,Month1,Year1))
            csv_data.append(Year1)
            csv_data.append(Month1)
            csv_data.append(Day1)
            csv_data.append(Hour1) 
            csv_data.append(Min1)
            csv_data.append(Sec1) 
            
            RS_latitude1=extract_float(arr,189,4,1)
            print("RS_latitude1:",RS_latitude1)    
            csv_data.append(RS_latitude1)
            RS_longitude1=extract_float(arr,193,4,1)
            print("RS_longitude1:",RS_longitude1) 
            csv_data.append(RS_longitude1)
            RS_altitude1=extract_float(arr,197,4,1)
            print("RS_altitude1:",RS_altitude1) 
            csv_data.append(RS_altitude1)
        ####################################channel data 1#####################################
            
            
            
            
            
        #    ##channel 1 data
        #    PRN_channel1=extract_val(arr,122,1)
        #    print("PRN_channel1:",PRN_channel1)
        #    csv_data.append(PRN_channel1)
        #    Channel_Track_Status=extract_val(arr,123,1)
        #    if(Channel_Track_Status==0):
        #        print("Channel_Track_Status:IDLE")
        #    elif(Channel_Track_Status==1):
        #        print("Channel_Track_Status:Acquisition")        
        #    elif(Channel_Track_Status==2):
        #        print("Channel_Track_Status:FLL")  
        #    elif(Channel_Track_Status==3):
        #        print("Channel_Track_Status:PLL")       
        #    elif(Channel_Track_Status==4):
        #        print("Channel_Track_Status:Reacquisition")  
        #    csv_data.append(Channel_Track_Status)     
        #    Doppler=extract_float(arr,124,4,1)
        #    print("Doppler:",Doppler)    
        #    csv_data.append(Doppler)
        #    Lock_Count= extract_val(arr,128,4)
        #    print("Lock_Count:",Lock_Count) 
        #    csv_data.append(Lock_Count)
        #    C_N0=extract_float(arr,132,4,1)
        #    print("C_N0:",(C_N0)) 
        #    csv_data.append(C_N0)
        #    Decryption_status=extract_val(arr,136,1)
        #    print("Decryption_status:",Decryption_status)
        #    csv_data.append(Decryption_status)
        #    Authentication_status=extract_val(arr,137,1)
        #    print("Authentication_status:",Authentication_status)
        #    csv_data.append(Authentication_status)
        #    One_way_offset=extract_float(arr,138,8,2)
        #    print("One_way_offset:",One_way_offset)
        #    csv_data.append(One_way_offset)
        #    RS_time_offset=extract_float(arr,146,8,2)
        #    print("RS_time_offset:",RS_time_offset)  
        #    csv_data.append(RS_time_offset)
        #    Freq_offset=extract_float(arr,154,8,2)
        #    print("Freq_offset:",Freq_offset)  
        #    csv_data.append(Freq_offset)
        #    RS_tx_power=extract_float(arr,162,4,1)
        #    print("RS_tx_power:",RS_tx_power) 
        #    csv_data.append(RS_tx_power) 
        #    RS_C_N0=extract_float(arr,166,4,1)
        #    print("RS_C_N0:",RS_C_N0) 
        #    csv_data.append(RS_C_N0)
        #    Year1=extract_val(arr,170,2)
        #    Month1=extract_val(arr,172,1)
        #    Day1=extract_val(arr,173,1)
        #    Hour1=extract_val(arr,174,1)
        #    Min1=extract_val(arr,175,1)
        #    Sec1=extract_val(arr,176,1)
        #    print("Last_sync_time:%s.%s.%s.%s/%s/%s"%(Hour1,Min1,Sec1,Day1,Month1,Year1))
        #    csv_data.append(Year1)
        #    csv_data.append(Month1)
        #    csv_data.append(Day1)
        #    csv_data.append(Hour1) 
        #    csv_data.append(Min1)
        #    csv_data.append(Sec1)  
        #    RS_latitude1=extract_float(arr,177,4,1)
        #    print("RS_latitude1:",RS_latitude1)    
        #    csv_data.append(RS_latitude1)
        #    RS_longitude1=extract_float(arr,181,4,1)
        #    print("RS_longitude1:",RS_longitude1) 
        #    csv_data.append(RS_longitude1)
        #    RS_altitude1=extract_float(arr,185,4,1)
        #    print("RS_altitude1:",RS_altitude1) 
        #    csv_data.append(RS_altitude1)
          
         ###############################channel 2 data######################################
            
            PRN_channel2=extract_val(arr,201,1)
            print("PRN_channel2:",PRN_channel2)
            csv_data.append(PRN_channel2)   
            Channel_Track_Status2=extract_val(arr,202,1)
            if(Channel_Track_Status2==0):
                print("Channel_Track_Status:IDLE")
            elif(Channel_Track_Status2==1):
                print("Channel_Track_Status:Acquisition")        
            elif(Channel_Track_Status2==2):
                print("Channel_Track_Status:FLL")  
            elif(Channel_Track_Status2==3):
                print("Channel_Track_Status:PLL")       
            elif(Channel_Track_Status2==4):
                print("Channel_Track_Status:Reacquisition") 
            csv_data.append(Channel_Track_Status2)     
            Doppler2=extract_float(arr,203,4,1)
            print("Doppler2:",Doppler2) 
            csv_data.append(Doppler2)
            Lock_Count2= extract_val(arr,207,4)
            print("Lock_Count2:",Lock_Count2) 
            csv_data.append(Lock_Count2)
            C_N02=extract_float(arr,211,4,1)
            print("C_N02:",C_N02) 
            csv_data.append(C_N02)  
            Decryption_status2=extract_val(arr,215,1)
            print("Decryption_status2:",Decryption_status2)
            csv_data.append(Decryption_status2)   
            Authentication_status2=extract_val(arr,216,1)
            print("Authentication_status2:",Authentication_status2)
            csv_data.append(Authentication_status2)  
         
            LS_time_offset2=extract_float(arr,217,8,2)
            print("LS_time_offset2:",LS_time_offset2)
            csv_data.append(LS_time_offset2)
            
            RS_time_offset2=extract_float(arr,225,8,2)
            print("RS_time_offset2:",RS_time_offset2)  
            csv_data.append(RS_time_offset2)
             
            time_offset2=extract_float(arr,233,8,2)
            print("time_offset2:",time_offset2)  
            csv_data.append(time_offset2)
         
            Freq_offset2=extract_float(arr,241,8,2)
            print("Freq_offset2:",Freq_offset2)  
            csv_data.append(Freq_offset2)
            RS_tx_power2=extract_float(arr,249,4,1)
            print("RS_tx_power2:",RS_tx_power2) 
            csv_data.append(RS_tx_power2)
            
            RS_C_N02=extract_float(arr,253,4,1)
            print("RS_C_N02:",RS_C_N02) 
            csv_data.append(RS_C_N02)
            Year2=extract_val(arr,257,2)
            Month2=extract_val(arr,259,1)
            Day2=extract_val(arr,260,1)
            Hour2=extract_val(arr,261,1)
            Min2=extract_val(arr,262,1)
            Sec2=extract_val(arr,263,1)
            print("Last_sync_time:%s.%s.%s.%s/%s/%s"%(Hour2,Min2,Sec2,Day2,Month2,Year2))
            csv_data.append(Year2)   
            csv_data.append(Month2) 
            csv_data.append(Day2) 
            csv_data.append(Hour2) 
            csv_data.append(Min2) 
            csv_data.append(Sec2) 
          
            RS_latitude2=extract_float(arr,264,4,1)
            print("RS_latitude2:",RS_latitude2)    
            csv_data.append(RS_latitude2)  
            RS_longitude2=extract_float(arr,268,4,1)
            print("RS_longitude2:",RS_longitude2) 
            csv_data.append(RS_longitude2)  
            RS_altitude2=extract_float(arr,272,4,1)
            print("RS_altitude2:",RS_altitude2) 
            csv_data.append(RS_altitude2)   
            print("\n")
            
            
            
        #    PRN_channel2=extract_val(arr,189,1)
        #    print("PRN_channel2:",PRN_channel2)
        #    csv_data.append(PRN_channel2)   
        #    Channel_Track_Status2=extract_val(arr,190,1)
        #    if(Channel_Track_Status2==0):
        #        print("Channel_Track_Status:IDLE")
        #    elif(Channel_Track_Status2==1):
        #        print("Channel_Track_Status:Acquisition")        
        #    elif(Channel_Track_Status2==2):
        #        print("Channel_Track_Status:FLL")  
        #    elif(Channel_Track_Status2==3):
        #        print("Channel_Track_Status:PLL")       
        #    elif(Channel_Track_Status2==4):
        #        print("Channel_Track_Status:Reacquisition") 
        #    csv_data.append(Channel_Track_Status2)     
        #    Doppler2=extract_float(arr,191,4,1)
        #    print("Doppler:",Doppler2) 
        #    csv_data.append(Doppler2)
        #    Lock_Count2= extract_val(arr,195,4)
        #    print("Lock_Count:",Lock_Count2) 
        #    csv_data.append(Lock_Count2)
        #    C_N02=extract_float(arr,199,4,1)
        #    print("C_N0:",C_N02) 
        #    csv_data.append(C_N02)  
        #    Decryption_status2=extract_val(arr,203,1)
        #    print("Decryption_status:",Decryption_status2)
        #    csv_data.append(Decryption_status2)   
        #    Authentication_status2=extract_val(arr,204,1)
        #    print("Authentication_status:",Authentication_status2)
        #    csv_data.append(Authentication_status2)  
        #    
        #    One_way_offset2=extract_float(arr,205,8,2)
        #    print("One_way_offset:",One_way_offset2)
        #    csv_data.append(One_way_offset2)
        #    
        #    RS_time_offset2=extract_float(arr,213,8,2)
        #    print("RS_time_offset:",RS_time_offset2)  
        #    csv_data.append(RS_time_offset2)
        #    Freq_offset2=extract_float(arr,221,8,2)
        #    print("Freq_offset:",Freq_offset2)  
        #    csv_data.append(Freq_offset2)
        #    RS_tx_power2=extract_float(arr,229,4,1)
        #    print("RS_tx_power:",RS_tx_power2) 
        #    csv_data.append(RS_tx_power2)
        #    RS_C_N02=extract_float(arr,233,4,1)
        #    print("RS_C_N0:",RS_C_N02) 
        #    csv_data.append(RS_C_N02)
        #    Year2=extract_val(arr,237,2)
        #    Month2=extract_val(arr,239,1)
        #    Day2=extract_val(arr,240,1)
        #    Hour2=extract_val(arr,241,1)
        #    Min2=extract_val(arr,242,1)
        #    Sec2=extract_val(arr,243,1)
        #    print("Last_sync_time:%s.%s.%s.%s/%s/%s"%(Hour2,Min2,Sec2,Day2,Month2,Year2))
        #    csv_data.append(Year2)   
        #    csv_data.append(Month2) 
        #    csv_data.append(Day2) 
        #    csv_data.append(Hour2) 
        #    csv_data.append(Min2) 
        #    csv_data.append(Sec2) 
        #  
        #    RS_latitude2=extract_float(arr,244,4,1)
        #    print("RS_latitude2:",RS_latitude2)    
        #    csv_data.append(RS_latitude2)  
        #    RS_longitude2=extract_float(arr,248,4,1)
        #    print("RS_longitude2:",RS_longitude2) 
        #    csv_data.append(RS_longitude2)  
        #    RS_altitude2=extract_float(arr,252,4,1)
        #    print("RS_altitude2:",RS_altitude2) 
        #    csv_data.append(RS_altitude2)   
        #    print("\n")
             ###############################channel 2 data######################################
            time_sec = time.time()
            result = time.localtime(time_sec)
            hhh = result.tm_hour
            mmm = result.tm_min
            sss = result.tm_sec
            final_time = hhh*60*60 + mmm*60 + sss
            #################################CSV File handling############################################
#            file_name = file_path + 'TWSTFT_' + str(final_time) + '_' + str(UDP_PORT_NO)  + '.csv'
            if(one_t==0):
                file_name = file_path + 'TWSTFT_log_' + str(final_time) + '_' + str(UDP_PORT_NO)  + '.csv'
                with open(file_name, 'w+',newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)  
                    writer.writerow(csv_data)
                    one_t=1
                     
            else:
                 with open(file_name, 'a+',newline='') as csvFile:
                     writer = csv.writer(csvFile)
                     writer.writerow(csv_data) 
            
            #############################################################################
            csv_data.clear()
        
            arr.clear()
    else:
        pass
    
    
def go_to_start(fd):
    go_to_while()
    
def quit_btn(fd):
    global clo
    clo = 0
    master.destroy()
    
def go_to_browse():
    #    master.withdraw()
    e3.delete(0,END)    # To delete the content in the search bar
    dirname = askdirectory(initialdir='', title='Please select a directory')
    e3.insert(10,dirname+r"/")
    return dirname

def go_to_t1():
    global UDP_IP_ADDRESS, UDP_PORT_NO, strt,file_path
    UDP_IP_ADDRESS = e1.get()
    UDP_PORT_NO = int(e2.get())
    file_path = e3.get()
    strt = 1
    e1.config(state='disabled')
    e2.config(state='disabled')
    e3.config(state='disabled')
    start_btn.config(state='disabled')
    browse_btn.config(state='disabled')
    t1.start()
    
    
def go_to_t2():
    t2.start()
#    t1.join()
#    t2.join()
t1 = threading.Thread(target=go_to_start, args=(10,)) 
t2 = threading.Thread(target=quit_btn, args=(10,)) 

Label(master, text="IP Address").grid(row=1, pady=5,padx=5)
Label(master, text="Port No.").grid(row=2, pady=5,padx=5)
Label(master, text="File Path").grid(row=3, pady=5,padx=5)

e1 = Entry(master, width=30)
e2 = Entry(master, width=30)
e3 = Entry(master, width=30)

e1.insert(10,"192.168.9.90")
e2.insert(10,"2000")


e1.grid(row=1, column=1,pady=5)
e2.grid(row=2, column=1,pady=5)
e3.grid(row=3, column=1,pady=5)

browse_btn =  Button(master, text="Browse", bg="light green", command=go_to_browse, disabledforeground='grey')          ##   browse button for offlien mode
browse_btn.grid(row=3, column=2, sticky=W, pady=0,padx=10)

start_btn =  Button(master, text="Start", bg="light blue", command=go_to_t1, disabledforeground='grey')          ##   browse button for offlien mode
start_btn.grid(row=6, column=2, sticky=W, pady=15,padx=10)  

quit_btn =  Button(master, text="Quit", bg="red", command=go_to_t2, disabledforeground='grey')          ##   browse button for offlien mode
quit_btn.grid(row=6, column=4, sticky=E, pady=15,padx=10)


master.mainloop()



