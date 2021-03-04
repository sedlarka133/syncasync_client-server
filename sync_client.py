import socket
import time


def connect_send(HOST, PORT, data):

    # Vytvorenie socketu

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        # Pripojenie na server a odosielanie dat

        sock.connect((HOST, PORT))

        for i in range(1000):#Posle 100 000 paketov

            sock.send(data.encode('utf-8'))

        # Receive data from the server and shut down

        sock.close()
def run():

    with open('Data.bin','w') as file: #Pre vytvorenie suboru Data.bin / jeho vycistenie

        file.close()

    HOST, PORT = "localhost", 8888

    number_of_clients = 10

    message_to_be_sent = '\x08'

    previous_percent = 0

    connection_begin_time = time.perf_counter()

    for i in range(number_of_clients):

        actual_percent = round(i/number_of_clients*100)#Vypocet percent pripojenych klientov

        if previous_percent != actual_percent:#Printne percenta len pri ich zmene

            previous_percent = actual_percent

            print(f'Sent: {actual_percent}%')

        connect_send(HOST,PORT,message_to_be_sent)#Vytvorenie spojenia

    print(f'All clients time taken: {time.perf_counter()-connection_begin_time}')#Printnutie casu ktory zabralo pripojenie a odpojenie vsetkych klientov
    time.sleep(2)
    try:
        with open('sync_time.bin','r') as file:
            times = [float(item.replace('\n','')) for item in file.readlines()]
            print(f'Time to finish all connections {sum(times)}')
    finally:
        file.close()
    open('sync_time.bin','w').close()

if __name__ == '__main__':

    run()

