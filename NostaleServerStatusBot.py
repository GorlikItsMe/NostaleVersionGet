from NostaleBot import Bot
import os



def CanConnect(nostale_version_json):
    bot_config={
        "LOGIN_SERVER_IP":      os.environ.get("LOGIN_SERVER_IP",   default="79.110.84.75"),
        "LOGIN_SERVER_PORT":int(os.environ.get("LOGIN_SERVER_PORT", default=4004)),
        "LOGIN":            os.environ.get("LOGIN"),
        "PASSWORD":         os.environ.get("PASSWORD"),
        "GF_ACC_ID":    int(os.environ.get("GF_ACC_ID", default=0)),
        "INSTALLATION_GUID": os.environ.get("INSTALLATION_GUID", default="e2ba7765-68d9-4694-8f9b-64ec44788349"),
        "nostale_version_json": nostale_version_json
    }

    bot = Bot(bot_config)
    if bot.LoginToGameforge() == False:
        print("[LoginToGameforge] Cant get token. FAIL")
        bot.sock.close()
        return "Login to Gameforge Fail"

    if bot.ConnectToLoginServer() == False:
        print("[ConnectToLoginServer] FAIL")
        bot.sock.close()
        return "Fail connect to login server"

    return True