import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

def plot_os_distribution(hosts, filename, title="Distribution of Hosts by OS"):
    os_counts = {}
    for host in hosts:
        os = host["os"]
        os_counts[os] = os_counts.get(os, 0) + 1
    plt.bar(os_counts.keys(), os_counts.values())
    plt.xticks(rotation=45, ha="right")
    plt.title(title)
    plt.xlabel("Operating System")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

def plot_host_age(hosts, filename, title="Old vs. New Hosts"):
    old_hosts = 0
    new_hosts = 0
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)  # Aware datetime

    for host in hosts:
        # Convert last_seen to a timezone-aware datetime
        last_seen = datetime.fromisoformat(host["last_seen"].replace("Z", "+00:00"))
        if last_seen < cutoff_date:
            old_hosts += 1
        else:
            new_hosts += 1

    # Create a bar chart
    labels = ["Old Hosts", "New Hosts"]
    counts = [old_hosts, new_hosts]

    plt.bar(labels, counts, color=["#FF5733", "#33B5E5"], alpha=0.8)
    plt.title(title)
    plt.ylabel("Number of Hosts")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.savefig(filename)
    plt.show()


def plot_open_ports_distribution(hosts, filename="open_ports_distribution.png"):
    port_counts = {}
    for host in hosts:
        for port in host.get("open_ports", []):
            port_counts[port] = port_counts.get(port, 0) + 1

    plt.bar(port_counts.keys(), port_counts.values(), color="#ff9999")
    plt.xticks(rotation=45, ha="right")
    plt.title("Distribution of Open Ports")
    plt.xlabel("Port Number")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()