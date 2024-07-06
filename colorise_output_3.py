from rich import print


def fprint(text, *args):
    new_text = text.replace("{}", "[green]{}[/]")
    print(new_text.format(*args))


def scan(ip_addr: str):
    return [22, 80, 443]


def open_ports(ip_addr: str):
    open_ports = scan(ip_addr)  # abbreviated
    for port in open_ports:
        fprint("The port: {} is open", port)
    fprint("I've scanned {} ports: {}", len(open_ports), open_ports)


open_ports("1.2.3.4")
