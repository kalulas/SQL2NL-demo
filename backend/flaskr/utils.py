import base64
import time

def generate_request_id(remote_addr:str):
    identifier_raw = f"{time.strftime('%Y%m%d%H%M%S', time.localtime())}@{remote_addr}"
    # identifier_raw = f"{time.strftime('%Y%m%d%H%M%S', time.localtime())}@{remote_addr}".encode()
    # return str(base64.b64encode(identifier_raw))
    return identifier_raw