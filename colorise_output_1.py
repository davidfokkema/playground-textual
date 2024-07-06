from rich import print


def scan(ip_addr: str):
    return [22, 80, 443]


def open_ports(ip_addr: str):
    open_ports = scan(ip_addr)  # abbreviated
    for port in open_ports:
        print(f"The port: [green]{port}[/] is open")


open_ports("1.2.3.4")
