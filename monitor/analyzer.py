def analyze_result(result, service_config):
    alerts = []

    if not result["success"]:
        alerts.append({
            "severity": "critical",
            "message": f"{result['service']} is DOWN",
            "recommendation": "Check network connectivity or service availability"
        })

        return alerts

    response_time = result["response_time"]
    max_response = service_config["max_response_time"]

    if response_time > max_response:
        alerts.append({
            "severity": "warning",
            "message": f"{result['service']} response time is high ({response_time}s)",
            "recommendation": "Investigate possible latency or backend performance issues"
        })

    return alerts