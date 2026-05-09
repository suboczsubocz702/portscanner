import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):
    open_ports = []

    # validate IP or hostname
    try:
        ip_address = socket.gethostbyname(target)
    except socket.gaierror:
        if any(char.isalpha() for char in target):
            return "Error: Invalid hostname"
        return "Error: Invalid IP address"

    start_port = port_range[0]
    end_port = port_range[1]

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((ip_address, port))

        if result == 0:
            open_ports.append(port)

        sock.close()

    if not verbose:
        return open_ports

    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        header = f"Open ports for {hostname} ({ip_address})"
    except socket.herror:
        header = f"Open ports for {target} ({ip_address})"

    output = header + "\n"
    output += "PORT     SERVICE\n"

    for port in open_ports:
        service = ports_and_services.get(port, "")
        output += f"{port:<9}{service}\n"

    return output.rstrip()
