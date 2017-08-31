from requests.auth import HTTPDigestAuth
import requests
import re
import calendar, time
import datetime
import configparser
import os


dvrIP_arr = []
dir_name =""

# dvrip = str(raw_input("Input DVR IP:"))
# st = str(input('Start Time:'))
# et = str(input('End Time:'))

# Load the ini file
config = configparser.ConfigParser()
config.read('config.ini')

timezone = int( config.get('TimeSetting', 'timezone') )
dst = int( config.get('TimeSetting', 'daylightsaving') )

Auto_DL_enable = config.get('Auto_Download', 'Enable')

if Auto_DL_enable == 'True' or Auto_DL_enable == 'true' :
    print( "Auto Download Start" )
    dvrIP_str = str( config.get( 'Auto_Download', 'IP' ) ).replace(",", " ")
    dvrIP_arr = dvrIP_str.split(  )

    # Get Current PC time
    cur_time = datetime.datetime.now()
    time_t = int( time.time() )
    # Get the End datetime
    end_datetime = datetime.date.fromtimestamp( time_t )
    # Roll back 24 hours
    time_t = time_t - 86400
    # Get the Start datetime
    start_datetime = datetime.date.fromtimestamp( time_t )

    et_year = end_datetime.year
    et_mon = end_datetime.month
    et_day = end_datetime.day
    et_hour = 7
    et_min = 0

    st_year = start_datetime.year
    st_mon = start_datetime.month
    st_day = start_datetime.day
    st_hour = 0
    st_min = 0

    dir_name = str(st_year) + str(st_mon) + str(st_day)

    if not os.path.exists( "DailyLog\\" + dir_name ):  # The folder isn't exist
        os.makedirs( "DailyLog\\" + dir_name )
else:
    print( "Manual Download Start" )
    dvrIP_str = str( config.get( 'Manual_Download', 'IP' ) )
    dvrIP_str = str( config.get( 'Auto_Download', 'IP' ) ).replace( ",", " " )
    dvrIP_arr = dvrIP_str.split()

    # Hard code start and end time
    st_year = int( config.get('Manual_Download', 'Start_Year') )
    st_mon  = int( config.get('Manual_Download', 'Start_Month') )
    st_day  = int( config.get('Manual_Download', 'Start_Day') )
    st_hour = int( config.get('Manual_Download', 'Start_Hour') )
    st_min  = int( config.get('Manual_Download', 'Start_Min') )

    et_year = int( config.get('Manual_Download', 'End_Year') )
    et_mon  = int( config.get('Manual_Download', 'End_Month') )
    et_day  = int( config.get('Manual_Download', 'End_Day') )
    et_hour = int( config.get('Manual_Download', 'End_Hour') )
    et_min  = int( config.get('Manual_Download', 'End_Min') )


# Convert time to POSIX timestamp
st_dt = datetime.datetime( st_year, st_mon, st_day, st_hour, st_min )
et_dt = datetime.datetime( et_year, et_mon, et_day, et_hour, et_min )
print( "Local Time: " + str( st_dt ) + " - " + str( et_dt ) + ", TZ:" + str( timezone ) + ", DST:" + str( dst ) )

# Convert time to POSIX timestamp( UTC time )
st = int( calendar.timegm( st_dt.timetuple() ) ) - timezone * 3600 - dst * 3600
et = int( calendar.timegm( et_dt.timetuple() ) ) - timezone * 3600 - dst * 3600


for dvrip in dvrIP_arr:
    # Construct the command with DVR ip and timestamp
    url = "http://" + dvrip + "/Log.log?cmd=export_log&start_time=" + str( st ) + "&end_time=" + str( et )
    response = None
    try:
        # Make a request to DVR
        print( url )
        response = requests.get( url, stream=True, verify=True, auth=HTTPDigestAuth( 'Admin', '11111111' ) )
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print("Timeout")
        continue
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("Too Many Redirects")
        continue
    except requests.exceptions.RequestException as err:
        # catastrophic error. bail.
        print(err)
        continue
    except requests.exceptions.HTTPError  as err:
        # HTTP error.
        print(err)
        continue

    # Compose the file name
    filename = "C:\\Users\\fliu\PycharmProjects\DVRtools\DVR_Log_Download\DailyLog\\" + dir_name + "\\" + st_dt.strftime( "%Y%m%d%H%M" ) + "-" + et_dt.strftime( "%Y%m%d%H%M" ) + "-DVR(" + dvrip + ").log"
    print( filename )

    # Write to the file
    with open( filename, 'wb' ) as fout:
        fout.write( response.content )

    log_str = str(response.content)

    # print(response.content)
    '''
    Strip the signal and write to another log file
    '''
    str_list = log_str.split('\\r\\n')

    # Compose the file name
    filename2 = "C:\\Users\\fliu\PycharmProjects\DVRtools\DVR_Log_Download\DailyLog\\" + dir_name + "\\"  + st_dt.strftime( "%Y%m%d%H%M" ) + "-" + et_dt.strftime( "%Y%m%d%H%M" ) + "-DVR(" + dvrip + ")_NoSignal.log"
    f = open( filename2, 'w' )
    for x in str_list:
        text_str = x.replace( "\\t", " " )
        match = re.findall( "Signal", text_str)
        if match:
            i = 1;
            #print( text_str )
        else:
            #print( text_str )
            f.write( text_str + '\n' )

        # Filter
        #match2 = re.findall( "calibrate", text_str)
        #if match2:
        #    print( text_str )

    f.close()


    # Filter the results
    #regep = re.compile( '\d\d-\d\d-\d\d\d\d.*\\t.*calibrate.*' )

    # Print all the results
    #for x in re.findall( regep, log_str ):
    #    print( x )

