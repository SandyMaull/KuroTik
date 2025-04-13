import os
import sys
from kurotik import KuroTik
from dotenv import load_dotenv

load_dotenv()

# Check for required Redis environment variables
required_env_vars = [
    "HOST",
    "USER",
    "PASSWORD",
    "PORT"
]

if not all(os.getenv(var) for var in required_env_vars):
    print("Required environment variables not found.")
    sys.exit(1)


test = KuroTik()
test.connect(
    host = os.getenv('HOST'),
    username = os.getenv('USER'),
    password = os.getenv('PASSWORD'),
    port = int(os.getenv('PORT')),
    plaintext_login = True
)
a = test.execute(x='/ip/firewall/address-list')
b = test.execute(x='/ip/hotspot/ip-binding')
a_comment = {item['comment'] for item in a.get(list="Whitelist for Blocking")}
filtered = [item for item in b.get() if item.get('comment') in a_comment]
# print(a.get(list="Whitelist for Blocking")[0]['comment'])
print(len(filtered))