import socket
import struct

header_size = 6
UDP_PORT = 31503

sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

sock.bind( ('', UDP_PORT) )

while True:
    data, addr = sock.recvfrom( 1024 )

    header_marker = int.from_bytes( data[ 0:1 ], byteorder='big', signed=False )
    header_meg_ID = int.from_bytes( data[ 1:2 ], byteorder='big', signed=False )
    header_major_ver = int.from_bytes( data[ 2:3 ], byteorder='big', signed=False )
    header_minor_ver = int.from_bytes( data[ 3:4 ], byteorder='big', signed=False )
    header_platform = int.from_bytes( data[ 4:5 ], byteorder='big', signed=False )
    header_type = int.from_bytes( data[ 5:6 ], byteorder='big', signed=False )

    if header_marker != ord( '$' ):
        print( "Invalid header {} {}".format( header_marker ) )

    if header_meg_ID != ord( 'N' ):
        print( "Invalid msg ID" )

    if header_major_ver != 1 or header_minor_ver != 0:
        print( "Invalid Version" )

    print( "Valid header DVR platform:{}, type:{}".format( header_platform, header_type ) )

    # HeartBeat Content
    msg_data = int.from_bytes( data[ header_size + 0:header_size + 2 ], byteorder='big', signed=False )
    print( "    message_data:{}".format( hex( msg_data ) ) )

    ip1 = int.from_bytes( data[ header_size + 2:header_size + 3 ], byteorder='big', signed=False )
    ip2 = int.from_bytes( data[ header_size + 3:header_size + 4 ], byteorder='big', signed=False )
    ip3 = int.from_bytes( data[ header_size + 4:header_size + 5 ], byteorder='big', signed=False )
    ip4 = int.from_bytes( data[ header_size + 5:header_size + 6 ], byteorder='big', signed=False )
    print( "    IP: {}.{}.{}.{}".format( ip1, ip2, ip3, ip4 ) )

    mac1 = int.from_bytes( data[ header_size + 6:header_size + 7 ], byteorder='big', signed=False )
    mac2 = int.from_bytes( data[ header_size + 7:header_size + 8 ], byteorder='big', signed=False )
    mac3 = int.from_bytes( data[ header_size + 8:header_size + 9 ], byteorder='big', signed=False )
    mac4 = int.from_bytes( data[ header_size + 9:header_size + 10 ], byteorder='big', signed=False )
    mac5 = int.from_bytes( data[ header_size + 10:header_size + 11 ], byteorder='big', signed=False )
    mac6 = int.from_bytes( data[ header_size + 11:header_size + 12 ], byteorder='big', signed=False )
    mac_str = '%x:%x:%x:%x:%x:%x' % (mac1, mac2, mac3, mac4, mac5, mac6)
    print( "    IP: {}.{}.{}.{} MAC: {}".format( ip1, ip2, ip3, ip4, mac_str ) )

    fw_ver = int.from_bytes( data[ header_size + 12:header_size + 16 ], byteorder='big', signed=False )

    title = data[ header_size + 16:header_size + 48 ]
    #print( "    {}".format( title ) )

    vloss = int.from_bytes( data[ header_size + 48:header_size + 52 ], byteorder='big', signed=False )
    hdd_status = int.from_bytes( data[ header_size + 52:header_size + 56 ], byteorder='big', signed=False )
    dvr_temp = int.from_bytes( data[ header_size + 56:header_size + 57 ], byteorder='big', signed=True )

    print( "    vloss:{}, hdd_status:{}, dvr_temp:{}".format( hex( vloss ), hex( hdd_status ), dvr_temp ) )

    print( addr )
