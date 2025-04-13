import os
import sys
from kurotik import KuroTik, KuroTikRedis, KuroTools
from dotenv import load_dotenv

load_dotenv()

# Check for required Redis environment variables
required_env_vars = [
    "MKT_HOST",
    "MKT_USER",
    "MTK_PASSWORD",
    "MTK_PORT",
    "REDIS_HOST",
    "REDIS_PORT",
]

if not all(os.getenv(var) for var in required_env_vars):
    print("Required environment variables not found.")
    sys.exit(1)

WHITELIST_NAME = "Whitelist for Blocking"
BLACKLIST_RULES_COMMENT_NAME = "Block Rumah"

mkt_core = KuroTik()
mkt_redis = KuroTikRedis()
kuro_tools = KuroTools()
mkt_core.connect(
    host=os.getenv("MKT_HOST"),
    username=os.getenv("MKT_USER"),
    password=os.getenv("MTK_PASSWORD"),
    port=int(os.getenv("MTK_PORT")),
    plaintext_login=bool(os.getenv("MTK_PLAINTEXT_LOGIN")),
)
mkt_redis.connect(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    username=os.getenv("REDIS_USER") or '',
    password=os.getenv("REDIS_PASS") or ''
)

a = mkt_core.execute(x="/ip/firewall/address-list").get(list=WHITELIST_NAME)
b = (
    mkt_redis.setDataR(
        "ip_binding_data", mkt_core.execute(x="/ip/hotspot/ip-binding").get()
    )
    if mkt_redis.getDataR("ip_binding_data") is None
    else mkt_redis.getDataR("ip_binding_data")
)
blacklist_status = (
    mkt_core.execute(x="/ip/firewall/filter").get(comment=BLACKLIST_RULES_COMMENT_NAME)[
        0
    ]["disabled"]
    == "false"
)

whitelist = kuro_tools.filter2List(a, b, "comment")