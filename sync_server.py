import socket, time

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 8888        # Port to listen on (non-privileged ports are > 1023)
def write_to_file(packet):
    try:
        with open('Data.bin','a') as file:
            file.write(packet)
    except:
        print('[SAVE] writing to file was unsuccessful')
    finally:
        file.close()

def write_time_to_file(time):
    try:
        with open('sync_time.bin','a') as file:
            file.write(str(time)+'\n')
    finally:
        file.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        prev_time = time.perf_counter()
        conn, addr = s.accept()
        with conn:
            print(f'[CONNECTION] {addr} connected')
            while True:
                data = conn.recv(1).decode('utf8')
                if data:
                    write_to_file(data+'\n')
                if not data:
                    print(f'[CONNECTION] {addr} disconnected')
                    conn.close()
                    write_time_to_file(time.perf_counter()-prev_time)
                    break
