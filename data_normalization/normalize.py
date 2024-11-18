from typing import Dict

def normalize_qualys_host(raw_host: Dict) -> Dict:
    """Normalize a Qualys host to a unified format."""
    return {
        "host_id": raw_host.get("_id"),
        "address": raw_host.get("address"),
        "os": raw_host.get("os", "").split("Build")[0].strip(),  # Extract primary OS info
        "last_seen": raw_host.get("agentInfo", {}).get("lastCheckedIn", {}).get("$date"),
        "cloud_provider": raw_host.get("cloudProvider"),
        "platform": raw_host.get("agentInfo", {}).get("platform"),
        "vulnerabilities": [
            vuln["HostAssetVuln"]["qid"]
            for vuln in raw_host.get("vuln", {}).get("list", [])
        ],
        "tags": [
            tag["TagSimple"]["name"]
            for tag in raw_host.get("tags", {}).get("list", [])
        ],
    }

def normalize_crowdstrike_host(raw_host: Dict) -> Dict:
    """Normalize a CrowdStrike host to a unified format."""
    return {
        "host_id": raw_host.get("device_id"),
        "address": raw_host.get("local_ip"),
        "external_ip": raw_host.get("external_ip"),
        "os": raw_host.get("os_version"),
        "last_seen": raw_host.get("last_seen"),
        "platform": raw_host.get("platform_name"),
        "cloud_provider": raw_host.get("cloud_provider", None),
        "hostname": raw_host.get("hostname"),
        "policies": raw_host.get("policies", []),
        "tags": raw_host.get("tags", []),
        "vulnerabilities": raw_host.get("vulnerabilities", []),  # If available
    }