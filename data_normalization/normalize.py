from typing import Dict

def normalize_qualys_host(raw_host: Dict) -> Dict:
    """Normalize a Qualys host to a unified format."""
    return {
        "host_id": raw_host.get("_id"),
        "address": raw_host.get("address"),
        "os": raw_host.get("os", "").split("Build")[0].strip() if raw_host.get("os") else None,  # Handle missing `os`
        "last_seen": raw_host.get("agentInfo", {}).get("lastCheckedIn", {}).get("$date"),
        "cloud_provider": raw_host.get("cloudProvider"),
        "platform": raw_host.get("agentInfo", {}).get("platform"),
        "dns_host_name": raw_host.get("dnsHostName"),  # Example additional field
        "fqdn": raw_host.get("fqdn"),
        "location": raw_host.get("agentInfo", {}).get("location"),
        "vulnerabilities": [
            vuln.get("HostAssetVuln", {}).get("qid")
            for vuln in raw_host.get("vuln", {}).get("list", [])
        ],
        "tags": [
            tag.get("TagSimple", {}).get("name")
            for tag in raw_host.get("tags", {}).get("list", [])
        ],
        "open_ports": [
            port.get("HostAssetOpenPort", {}).get("port")
            for port in raw_host.get("openPort", {}).get("list", [])
        ],
        "software": [
            software.get("HostAssetSoftware", {}).get("name")
            for software in raw_host.get("software", {}).get("list", [])
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
    }