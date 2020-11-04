

class PacketHandler():

    def __init__(self, loginpacketsuccess):
        if loginpacketsuccess.startswith("failc 1"):
            print(">> Client not update")
        if loginpacketsuccess.startswith("failc 2"):
            print(">> an error occurred while connecting (GF dont like you)")
        if loginpacketsuccess.startswith("failc 3"):
            print(">> Serwer Maintrence")
        if loginpacketsuccess.startswith("failc 4"):
            print(">> Someone is loged in on this account")
        if loginpacketsuccess.startswith("failc 5"):
            print(">> Wrong login or password")
        if loginpacketsuccess.startswith("failc 6"):
            print(">> That client cant connect (GF dont like you)")
        if loginpacketsuccess.startswith("failc 7"):
            print(">> BAN")
        if loginpacketsuccess.startswith("failc 8"):
            print(">> This country is baned on this server (user proxy or something)")
        if loginpacketsuccess.startswith("failc 9"):
            print(">> Check big and small letters in your password or nickname")
        if loginpacketsuccess.startswith("failc 404"):
            print(">> WorldServer dont started!")
        pass


    