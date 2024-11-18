from typing import List, Dict


def deduplicate_hosts(hosts: List[Dict]) -> List[Dict]:
    """
    Deduplicate host data based on `host_id`.

    :param hosts: List of host dictionaries.
    :return: Deduplicated list of hosts.
    """
    unique_hosts = {}
    for host in hosts:
        host_id = host["host_id"]
        if host_id not in unique_hosts:
            unique_hosts[host_id] = host
        else:
            # Update with the latest `last_seen` if duplicate is found
            existing = unique_hosts[host_id]
            if host["last_seen"] > existing["last_seen"]:
                unique_hosts[host_id] = host
    return list(unique_hosts.values())