class PacketHandler():

    def __init__(self, loginpacketsuccess):
        p = loginpacketsuccess.split(" ")
        self.header =   p[0]
        self.null =     p[1]
        self.language = int(p[2])
        self.username = p[3]
        self.always_two = int(p[4])
        self.session_id =int(p[5])

        self.channels = []
        for n in range(6, len(p)-1, 1):
            self.channels.append( ChannelInfo(p[n]) )

class ChannelInfo():
    def __init__(self, packet):
        p = packet.split(":")
        self.ip =   p[0]
        self.port = int(p[1])
        self.channelcolor = int(p[2])

        k = p[3].split(".")
        self.worldCount =   int(k[0])
        self.channel_id =   int(k[1])
        self.name =         k[2]


#packet = "NsTeST  4 PL_szymongorl 2 12345 79.110.84.87:4016:0:6.7.Belial(New) 79.110.84.87:4015:0:6.6.Belial(New) 79.110.84.87:4014:0:6.5.Belial(New) 79.110.84.87:4013:0:6.4.Belial(New) 79.110.84.87:4011:0:6.2.Belial(New) 79.110.84.87:4012:0:6.3.Belial(New) 79.110.84.87:4010:0:6.1.Belial(New) 79.110.84.132:4016:0:1.7.Feniks 79.110.84.132:4015:0:1.6.Feniks 79.110.84.132:4014:1:1.5.Feniks 79.110.84.132:4013:0:1.4.Feniks 79.110.84.132:4012:0:1.3.Feniks 79.110.84.132:4011:6:1.2.Feniks 79.110.84.132:4010:1:1.1.Feniks -1:-1:-1:10000.10000.1"
#p = PacketHandler(packet)
#print(p)