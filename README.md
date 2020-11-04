# NostaleVersionGet

Get Nostale hashes used to auth to servers

# Install
```
python3 -m pip install -r .\requirements.txt
```

# Example
```
from NostaleVersionGet import NostaleVersionGet

print(NostaleVersionGet())
# {'hashNostaleClientX': 'bdf34914ef5140e5cbaca5b029e7fa08', 'hashNostaleClient': 'b1c1923340a71cc6f1ef9fa6b4b01114', 'version': '0.9.3.3130'}

```

# You can also use API
https://nostale-version.herokuapp.com/


# Extra
If you want checking login server connection set this variables in env
```
LOGIN_SERVER_IP: 79.110.84.75
LOGIN_SERVER_PORT: 4004
LOGIN: "email@gmail.com"
PASSWORD: "yourpassword"
GF_ACC_ID: 0
INSTALLATION_GUID: "e2ba7765-68d9-4694-8f9b-64ec44788349"
```