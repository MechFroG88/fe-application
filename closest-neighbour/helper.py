def recv_until(sock, end_marker):
    """Receive data from the socket until we find the end marker."""
    data = b''
    while True:
        chunk = sock.recv(1)
        if not chunk:
            raise RuntimeError("Socket connection broken")
        data += chunk
        if end_marker == data[-4:]:
            break
    return data[:-len(end_marker)]
