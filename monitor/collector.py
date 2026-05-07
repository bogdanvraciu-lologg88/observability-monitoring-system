import requests
import time
from datetime import datetime


def check_service(service):
    url = service["url"]

    start_time = time.time()

    try:
        response = requests.get(url, timeout=5)

        response_time = round(time.time() - start_time, 3)

        return {
            "service": service["name"],
            "url": url,
            "status_code": response.status_code,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }

    except Exception as e:
        return {
            "service": service["name"],
            "url": url,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "success": False
        }