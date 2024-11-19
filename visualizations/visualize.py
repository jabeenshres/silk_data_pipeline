import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

# Ensure the 'images/' directory exists
os.makedirs("images", exist_ok=True)

def plot_os_distribution(hosts, filename, title="Distribution of Hosts by OS"):
    """
    Plot the distribution of hosts by operating system.

    :param hosts: List of hosts.
    :param filename: Name of the output image file.
    :param title: Title of the plot.
    """
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
    full_path = os.path.join("images", filename)  # Save in 'images/' directory
    plt.savefig(full_path)
    plt.close()  # Close the plot to free memory
    print(f"Saved OS distribution plot to {full_path}")


def plot_host_age(hosts, filename, title="Old vs. New Hosts"):
    """
    Plot a comparison of old vs. new hosts based on `last_seen`.

    :param hosts: List of hosts.
    :param filename: Name of the output image file.
    :param title: Title of the plot.
    """
    old_hosts = 0
    new_hosts = 0
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=30)

    for host in hosts:
        last_seen = datetime.fromisoformat(host["last_seen"].replace("Z", "+00:00"))
        if last_seen < cutoff_date:
            old_hosts += 1
        else:
            new_hosts += 1

    labels = ["Old Hosts", "New Hosts"]
    counts = [old_hosts, new_hosts]

    plt.bar(labels, counts, color=["#FF5733", "#33B5E5"], alpha=0.8)
    plt.title(title)
    plt.ylabel("Number of Hosts")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    full_path = os.path.join("images", filename)  # Save in 'images/' directory
    plt.savefig(full_path)
    plt.close()  # Close the plot to free memory
    print(f"Saved host age plot to {full_path}")


def plot_open_ports_distribution(hosts, filename="open_ports_distribution.png"):
    """
    Plot the distribution of open ports across all hosts.

    :param hosts: List of hosts.
    :param filename: Name of the output image file.
    """
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
    full_path = os.path.join("images", filename)  # Save in 'images/' directory
    plt.savefig(full_path)
    plt.close()  # Close the plot to free memory
    print(f"Saved open ports distribution plot to {full_path}")
