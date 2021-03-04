import asyncio, socket, time

def write_to_file(packet):
    try:
        with open('Data_async.bin','a') as file:
            file.write(packet)
    except:
        print('Saving packet was unsuccessful')
    finally:
        file.close()
def write_time(time):
    try:
        with open('times.bin','a') as file:
            file.write(str(time)+'\n')
    except:
        print('saving connecton time unsuccessful')
    finally:
        file.close()



async def handle_client(client):
    print(f'[CONNECTION] {client.getpeername()} connected')
    prev_time = time.perf_counter()
    request = None
    while request != '':

        request = (await loop.sock_recv(client, 1)).decode('utf8').strip()
        if request:
            write_to_file(str(request)+'\n')
    print(f'[CONNECTION] {client.getpeername()} disconnected')
    client.close()
    write_time(time.perf_counter()-prev_time)

async def run_server():
        while True:
            client, _ = await loop.sock_accept(server)
            loop.create_task(handle_client(client))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8888))

server.listen(8)
server.setblocking(False)

loop = asyncio.get_event_loop()
loop.run_until_complete(run_server())
