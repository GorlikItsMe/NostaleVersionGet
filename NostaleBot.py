import socket
from hashlib import md5
import PacketHandler
from noscrypto.Client import LoginDecrypt, LoginEncrypt
from nosauth import api as nosauth_api


class Bot:
    session_id = 0
    pid = 53535  # packet id (increment every send packet) can be random
    GF_LOGIN = None
    sock = None

    def __init__(self, base):
        self.LOGIN_SERVER_IP = base["LOGIN_SERVER_IP"]
        self.LOGIN_SERVER_PORT = base["LOGIN_SERVER_PORT"]
        self.LOGIN = base["LOGIN"]
        self.PASSWORD = base["PASSWORD"]
        self.GF_ACC_ID = base["GF_ACC_ID"]
        self.INSTALLATION_GUID = base["INSTALLATION_GUID"]

        nt = base["nostale_version_json"]
        print(" version:", nt["version"])
        self.HASH_NOSTALE_CLIENTX = nt["hashNostaleClientX"].upper()
        self.HASH_NOSTALE_CLIENT = nt["hashNostaleClient"].upper()
        self.NOSTALE_VERSION = nt["version"]
        self.GAME_HASH = (
            md5(self.HASH_NOSTALE_CLIENTX.encode() + self.HASH_NOSTALE_CLIENT.encode())
            .hexdigest()
            .upper()
        )
        pass

    def Connect(self, ip, port) -> bool:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((ip, port))
        except Exception as e:
            print("Cannot connect to {0}:{1} the server:".format(ip, port), e)
            return False
        print("Connected to {0}:{1}".format(ip, port))
        return True

    def ConnectToLoginServer(self):
        if self.Connect(self.LOGIN_SERVER_IP, self.LOGIN_SERVER_PORT) is False:
            print("[ConnectToLoginServer] FAIL")
            return False

        self.sock.send(LoginEncrypt(self.CreateLoginPacket().encode("ascii")))

        rawdata = self.sock.recv(1024)
        loginpacketsuccess = LoginDecrypt(rawdata).decode("ascii")

        # obsługa pakietu Failc
        if loginpacketsuccess.startswith("failc"):
            PacketHandler.failc.PacketHandler(loginpacketsuccess)
            print(loginpacketsuccess.replace("\n", "\\n"))
            return False

        p = PacketHandler.NsTeST.PacketHandler(loginpacketsuccess)
        # print(" Channels: ")
        # for c in p.channels:
        #    print("   {0.ip}:{0.port}\t{0.name} \tchannel: {0.channel_id}".format(c))
        self.session_id = p.session_id
        return True

    def LoginToGameforge(self):
        """
        return False / token
        """
        api = nosauth_api.NtLauncher(locale="pl_PL", gfLang="pl")
        if not api.auth(username=self.LOGIN, password=self.PASSWORD):
            print(
                "[LoginToGameforge] Couldn't auth to gameforge (check login and password)!"
            )
            return False

        accounts = api.getAccounts()
        if len(accounts) == 0:
            print("[LoginToGameforge] You don't have any any account")
            return False

        gf_acc_id_n = 0
        for uid, displayName in accounts:
            print(
                "[LoginToGameforge] GF_ACC_ID:",
                gf_acc_id_n,
                "Account name:",
                displayName,
            )
            gf_acc_id_n += 1

        uid, displayName = accounts[self.GF_ACC_ID]
        token = api.getToken(uid)
        self.GF_LOGIN = displayName

        if token:
            print("[LoginToGameforge] Get token")
            self.SESSION_TOKEN = token
            return True
        else:
            print("[LoginToGameforge] Couldn't obtain token!")
            return False
        return False

    def CreateLoginPacket(self):
        REGION_CODE = "4"
        return "".join(
            [
                "NoS0577 ",
                self.SESSION_TOKEN,
                " ",
                self.INSTALLATION_GUID,
                " 003662BF",
                " ",
                REGION_CODE,
                "\v",
                self.NOSTALE_VERSION,
                " 0 ",
                self.GAME_HASH,
            ]
        )
