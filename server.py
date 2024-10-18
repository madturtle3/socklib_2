import selectors
import socket
import socklib
import chatlib
import blessed
from dataclasses import dataclass

# rich imports
import rich
import rich.box
import rich.panel
import rich.console
import rich.panel


@dataclass
class Connection:
    initted: bool
    username: str
    sockobj: socket.socket
    fileno: int
    addr: tuple


console = rich.console.Console()
term = blessed.Terminal()


def main():

    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        console.clear()
        run_server()


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", chatlib.PORT))
    server.listen(5)
    # polling setup
    poller = selectors.DefaultSelector()
    poller.register(server, selectors.EVENT_READ, "server")
    running = True
    fileno_list = []
    conn_list: list[Connection] = []
    while running:
        for key, events in poller.select(1.5):
            # if it is a read selector
            if events & selectors.EVENT_READ:
                if key.data == "server":
                    newconn, addr = server.accept()
                    print("new connection from", addr)
                    fileno_list.append(newconn.fileno())
                    conn_list.append(
                        Connection(False, "", newconn, newconn.fileno(), addr)
                    )
                    poller.register(newconn, selectors.EVENT_READ)
                else:
                    # req from server
                    # or the socket closed maybe perhaps
                    msg = socklib.recv_msg(key.fileobj)
                    if msg == socklib.ERR_EOF:
                        # remove the socket from the list of connections
                        index, conn = [
                            (index, conn)
                            for index, connection in enumerate(conn_list)
                            if connection.fileno == key.fd
                        ][0]
                        print(f"{conn.username} ({conn.addr[0]}) has disconnected")
                        poller.unregister(key.fd)
                        key.fileobj.close()

                    else:
                        match msg:
                            case chatlib.ChatMsg():
                                msg.src = [x for x in conn_list if x.fileno == key.fd][
                                    0
                                ].username
                                print(f"Message from {msg.src}: {msg.msg}")
                                match msg.dest:
                                    # none meaning no specific destination;
                                    # send it to everyone!
                                    case None:
                                        for conn in conn_list:
                                            conn.sockobj.send(socklib.encode_msg(msg))
                                    case str():
                                        destlist = [
                                            x
                                            for x in conn_list
                                            if x.username == msg.dest
                                        ]
                                        for dest in destlist:
                                            dest.sockobj.send(socklib.encode_msg(msg))
                            case chatlib.InitMsg():
                                initted_conn = [
                                    index
                                    for index, conn in enumerate(conn_list)
                                    if conn.fileno == key.fd
                                ][0]
                                conn_list[initted_conn].username = msg.username


if __name__ == "__main__":
    main()
