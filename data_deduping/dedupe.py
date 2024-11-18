# data_deduping/dedupe.py
def deduplicate_hosts(hosts: list) -> list:
    unique_hosts = {}
    for host in hosts:
        unique_key = host["host_id"]
        if unique_key not in unique_hosts:
            unique_hosts[unique_key] = host
        else:
            # Merging logic - choose the latest `last_seen`
            existing = unique_hosts[unique_key]
            if host["last_seen"] > existing["last_seen"]:
                unique_hosts[unique_key] = host
    return list(unique_hosts.values())
