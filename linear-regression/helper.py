def recv_until(sock, end_marker, buffer_size=4096):
    """Receive data from the socket until we find the end marker."""
    data = b''
    while True:
        chunk = sock.recv(buffer_size)
        if not chunk:
            raise RuntimeError("Socket connection broken")
        data += chunk
        if end_marker in data:
            break
    return data[:-len(end_marker)]
