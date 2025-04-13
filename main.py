import os
import sys
from kurotik import KuroTik, KuroTikTools
from dotenv import load_dotenv
from ext import tools

load_dotenv()

# Check for required Redis environment variables
required_env_vars = ["HOST", "USER", "PASSWORD", "PORT"]

if not all(os.getenv(var) for var in required_env_vars):
    print("Required environment variables not found.")
    sys.exit(1)


tik = KuroTik()
tools = KuroTikTools()
tik.connect(
    host=os.getenv("HOST"),
    username=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    port=int(os.getenv("PORT")),
    plaintext_login=True,
)

a = tik.execute(x="/ip/firewall/address-list").get(list="Whitelist for Blocking")
b = (
    tools.setData("ip_binding_data", tik.execute(x="/ip/hotspot/ip-binding").get())
    if tools.getData("ip_binding_data") is None
    else tools.getData("ip_binding_data")
)
filtered = tools.filter2List(a, b, "comment")
print(filtered)
