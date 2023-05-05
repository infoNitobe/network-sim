import socket
import struct
import time

class sntp:
    def __init__(self):
        self.SNTP_SERVER = "time.aws.com" # SNTPサーバーはtime.aws.comである
        self.TIME1970 = 2208988800 # 1970年1月1日からの秒数

    def sntp_client(self):
        # Make a socket.
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INETはIPv4、SOCK_DGRAMはUDPを表す
        client.settimeout(1) # Set to make socket.timeout detectable

        # Send SNTP request.
        data = b'\x1b' + 47 * b'\x00'
        client.sendto(data, (self.SNTP_SERVER, 123)) # send message to port 123 of SNTP server.

        # Receive SNTP response.
        self.__recv_sntp_resp(client)
    
    def __recv_sntp_resp(self, client):
        try:
            data, address = client.recvfrom(1024)
            t = struct.unpack('!12I', data)[10] # レスポンスから時刻情報を取り出す
            t -= self.TIME1970 # 1900年1月1日からの秒数から1970年1月1日からの秒数に変換
            t = time.ctime(t) # 時刻を人間が読める形式に変換する。
            print('Time: {}'.format(t)) # 時刻を人間が読める形式に変換して表示
        except socket.timeout:
            print("No SNTP response.")