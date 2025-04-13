# ==============================================================================
#  ©2025 Kuronekosan. All Rights Reserved.
# 
#  Packages:    kurotik
#  Author:      Kuronekosan
#  Created:     2025
# 
#  Description:
#      A Custom Mikrotik Packages for automatic enabled/disabled block script
# ==============================================================================

import redis
import json

class KuroTikTools:
    def __init__(self, host = 'localhost', port = 6379, db = 0):
        self.rConn = redis.Redis(host=host, port=port, db=db)
        
    def getData(self, key):
        cached = self.rConn.get(key)
        return json.loads(cached)
    
    def setData(self, key, data):
        self.rConn.set(key, json.dumps(data), ex=300)
        return self.getData(key)
    
    def filter2List(self, list1, data_list, keys):
        """
            List1 : Expected filter list
            List2 : All data list
            keys : keys for comparement filtering (if list1[keys] == list2[keys])
        """
        list1 = {item[keys] for item in list1}
        return [item for item in data_list if item.get(keys) in list1]