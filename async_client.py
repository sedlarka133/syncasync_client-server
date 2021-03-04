import asyncio, socket
import time

#Klient pripojenie na server a odoslanie 100 000 paketov

clients = {}
async def tcp_echo_client(message):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.connect(('localhost',8888))

    for i in range(0,1000): #Loop posiela 100 000 krat spravu (simuluje posielanie spravy o dlzke 100 000 po paketoch)

        server.send(str(message).encode('utf8')) #Posle spravu
    server.close() #Po odoslani daneho poctu paketov ukonci spojenie

#Funkcia ktora pripoji 10 klientov z ktorych kazdy posle 100 000 paketov

def make_connection(host, port):

    task = asyncio.Task(tcp_echo_client('\x08')) #Vytvorenie tasku

    clients[task] = (host, port) #Pridanie do dictionary clientov

    def client_done(task): #Funkcia pre ukoncenie spojenia

        del clients[task] #Odstrani z dictionary

        if len(clients) == 0: #Ak niesu ziadny pripojeni klienti zrusi loop

            loop = asyncio.get_event_loop()

            loop.stop()

            get_results()


    task.add_done_callback(client_done)

def run(): #Funkcia pre spustenie klienta

    connection_begin_time = time.perf_counter() # Ulozi cas zaciatku spojenia

    number_of_clients = 10 # Pocet klientov ktori sa pripoja

    previous_percent = 0 #Premenna ktora porovnava percenta aby neprintovalo tie iste percenta stale dookola ale az ked sa zmenia

    loop = asyncio.get_event_loop() # Vytvorenie asyncio loopky (pre pripojenie vsetkych naraz)

    for client in range(number_of_clients): #Loopka vytvara klientov/spojenia

        actual_percent = client/10*100#Pre printovanie kolko % pripojeni bolo vytvorenych

        if previous_percent != actual_percent:# Printuje len pri zmene %

            previous_percent=actual_percent

            print(f'{previous_percent}%')

        make_connection('localhost', 8888) #Funkcia ktora prida task do loop

    loop.run_forever() #Spustenie loop


    print(f'Time taken to establish all {number_of_clients} connections: {time.perf_counter()-connection_begin_time}')#Vytlaci cas ktory zabralo vytvorenie a ukoncenie vsetkych klientov dokopy.


def get_results():
    File = 'NaN'
    while len(File) != 10:
        try:
            with open('times.bin','r') as file:
                File = file.readlines()
        finally:
            file.close()
    try:
        with open('times.bin','r') as file:
            times = [float(item.replace('\n','')) for item in file.readlines()]
            print(f'Time taken to send & recieve & write all packets {sum(times)}')
    finally:
        file.close()
        try:
            file = open('times.bin','w')
        finally:
            file.close()
if __name__ == '__main__': #Ak je importovany (import async_client.py)  tak sa nasledujuci kod nevykona a treba si pustit manualne

    run()  #Spusti funkciu na spustenie spojeni
