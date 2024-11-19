from typing import List, Dict


def merge_host_data(latest_host: Dict, duplicate_host: Dict) -> Dict:
    """
    Merge additional information from duplicate_host into latest_host.

    :param latest_host: The host with the latest 'last_seen' timestamp.
    :param duplicate_host: The duplicate host to be merged.
    :return: The updated latest_host with merged information.
    """
    # Merge tags
    latest_host["tags"] = list(set(latest_host.get("tags", []) + duplicate_host.get("tags", [])))

    # Merge vulnerabilities
    latest_host["vulnerabilities"] = list(
        set(latest_host.get("vulnerabilities", []) + duplicate_host.get("vulnerabilities", []))
    )

    # Merge open ports
    latest_host["open_ports"] = list(
        set(latest_host.get("open_ports", []) + duplicate_host.get("open_ports", []))
    )

    # Merge software
    latest_host["software"] = list(
        set(latest_host.get("software", []) + duplicate_host.get("software", []))
    )

    return latest_host


def deduplicate_hosts(hosts: List[Dict]) -> List[Dict]:
    """
    Deduplicate host data based on 'host_id', merging data from duplicates.

    :param hosts: List of host dictionaries.
    :return: Deduplicated list of hosts with merged data.
    """
    unique_hosts = {}
    for host in hosts:
        host_id = host["host_id"]
        if host_id not in unique_hosts:
            unique_hosts[host_id] = host
        else:
            # Merge data if duplicate exists
            existing_host = unique_hosts[host_id]
            if host["last_seen"] > existing_host["last_seen"]:
                # Update with the latest host and merge data
                unique_hosts[host_id] = merge_host_data(host, existing_host)
            else:
                # Merge data into the existing host
                unique_hosts[host_id] = merge_host_data(existing_host, host)

    return list(unique_hosts.values())