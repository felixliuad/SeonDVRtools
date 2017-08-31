from flask import Flask, render_template, request, redirect
import datetime
import calendar
from modules import LogCGI

# 初始化 Flask 類別成為 instance
app = Flask( __name__ )


# 路由和處理函式配對
@app.route( '/' )
def index():
    return render_template( "log_download.html" )


@app.route( '/log_download' )
def log_download_method():
    return redirect( "log_download.html" )


@app.route( '/download', methods=[ 'GET', 'POST' ] )
def download_method():
    if request.method == 'POST':
        dvr_ip = request.form[ 'InputDvrIP' ]
        StartTime = request.form[ 'InputStartDateTime' ]
        EndTime = request.form[ 'InputEndDateTime' ]

        StartTime = StartTime.replace( "T", "-" )
        StartTime = StartTime.replace( ":", "-" )
        StartTime_arr = StartTime.split( '-' )

        EndTime = EndTime.replace( "T", "-" )
        EndTime = EndTime.replace( ":", "-" )
        EndTime_arr = EndTime.split( '-' )

        st_year = int( StartTime_arr[ 0 ] )
        st_mon = int( StartTime_arr[ 1 ] )
        st_day = int( StartTime_arr[ 2 ] )
        st_hour = int( StartTime_arr[ 3 ] )
        st_min = int( StartTime_arr[ 4 ] )

        et_year = int( EndTime_arr[ 0 ] )
        et_mon = int( EndTime_arr[ 1 ] )
        et_day = int( EndTime_arr[ 2 ] )
        et_hour = int( EndTime_arr[ 3 ] )
        et_min = int( EndTime_arr[ 4 ] )

        timezone = int( request.form[ 'InputTZ' ] )
        dst = int( request.form[ 'InputDST' ] )

        # Convert time to POSIX timestamp
        st_dt = datetime.datetime( st_year, st_mon, st_day, st_hour, st_min )
        et_dt = datetime.datetime( et_year, et_mon, et_day, et_hour, et_min )
        print( "Local Time: " + str( st_dt ) + " - " + str( et_dt ) + ", TZ:" + str( timezone ) + ", DST:" + str(
            dst ) )

        # Convert time to POSIX timestamp( UTC time )
        st = int( calendar.timegm( st_dt.timetuple() ) ) - timezone * 3600 - dst * 3600
        et = int( calendar.timegm( et_dt.timetuple() ) ) - timezone * 3600 - dst * 3600

        print( "DVR IP: {}, Time {}-{}-{} {}:{} to {}-{}-{} {}:{} TZ:{}, DST:{}".format( dvr_ip, st_year, st_mon,
                                                                                         st_day, st_hour, st_min,
                                                                                         et_year, et_mon, et_day,
                                                                                         et_hour, et_min, timezone,
                                                                                         dst ) )

        LogCGI.download_log( dvr_ip, st, et, st_dt, et_dt )

        return render_template( "download.html" )
    else:
        return render_template( "download.html" )

if __name__ == '__main__':
    app.run( port=5053 )
