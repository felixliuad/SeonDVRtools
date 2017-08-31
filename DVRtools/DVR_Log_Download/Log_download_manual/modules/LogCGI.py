from requests.auth import HTTPDigestAuth
#from tkinter.filedialog import askdirectory
import requests
import re
import calendar, time
import datetime
import configparser
import os

def download_log( dvrip, st, et, st_dt, et_dt):
    print( "DVR IP:{} Log TT[{} - {}]".format( dvrip, st, et ) )

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
        return False
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("Too Many Redirects")
        return False
    except requests.exceptions.RequestException as err:
        # catastrophic error. bail.
        print(err)
        return False
    except requests.exceptions.HTTPError as err:
        # HTTP error.
        print(err)
        return False


    # Compose the file name
    filename = "C:\\Users\\fliu\\PycharmProjects\\DVRtools\\DVR_Log_Download\\Log_download_manual\\Download\\" + st_dt.strftime( "%Y%m%d%H%M" ) + "-" + et_dt.strftime( "%Y%m%d%H%M" ) + "-DVR(" + dvrip + ").log"
    print( filename )


    #folder = askdirectory()
    #print(folder)

    # Write to the file
    with open( filename, 'wb' ) as fout:
        fout.write( response.content )

    log_str = str( response.content )

    # print(response.content)
    '''
    Strip the signal and write to another log file
    '''
    str_list = log_str.split( '\\r\\n' )

    # Compose the file name

    signal_cnt = 0
    for x in str_list:
        text_str = x.replace( "\\t", " " )
        match = re.findall( "calibrate", text_str )
        if match:
            signal_cnt = signal_cnt + 1
            # print( text_str )
    print("Signal count:{}".format(signal_cnt))

            # Filter
            # match2 = re.findall( "calibrate", text_str)
            # if match2:
            #    print( text_str )


    return True

