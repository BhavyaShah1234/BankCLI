import socket
import threading

SERVER_IP = '192.168.29.20'
SERVER_PORT = 24091
ENCODING = 'utf-8'
ACCOUNT_PASSWORD_DICT = {'1': 'one', '2': 'two', '3': 'three'}
ACCOUNT_BALANCE_DICT = {'1': 100.0, '2': 150.0, '3': 75.0}


def handle_client(enc, conn, ip, port, acc_pass, acc_bal):
    acc_number = conn.recv(1024).decode(enc)
    password = conn.recv(1024).decode(enc)
    print(f'CREDENTIALS RECEIVED FROM ({ip}, {port}).')
    if acc_number in acc_pass and acc_pass[acc_number] == password:
        conn.send(bytes('PASS', enc))
        print(f'({ip}, {port}) CONNECTED.')
        connected = True
        while connected:
            balance = str(acc_bal[acc_number])
            conn.send(bytes(balance, enc))

            choice = conn.recv(1024).decode(enc)
            if choice == '1':
                action = 'DEPOSIT MONEY'
                print(f'({ip}, {port}) CHOSE TO {action}.')
                amount = float(conn.recv(1024).decode(enc))
                acc_bal[acc_number] = acc_bal[acc_number] + amount
            elif choice == '2':
                action = 'WITHDRAW MONEY'
                print(f'({ip}, {port}) CHOSE TO {action}.')
                amount = float(conn.recv(1024).decode(enc))
                if amount > acc_bal[acc_number]:
                    conn.send(bytes('INSUFFICIENT BALANCE', enc))
                else:
                    conn.send(bytes('SUFFICIENT BALANCE.', enc))
                    acc_bal[acc_number] = acc_bal[acc_number] - amount
            elif choice == '3':
                action = 'EXIT'
                print(f'({ip}, {port}) CHOSE TO {action}.')
                conn.close()
                print(f'({ip}, {port}) DISCONNECTED.')
                connected = False
    else:
        conn.send(bytes('FAIL', enc))
        conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
print(f'SERVER STARTED ON ({SERVER_IP}, {SERVER_PORT})')

server.listen(1)
print('WAITING FOR CONNECTIONS....')

running = True
while running:
    connection, (client_ip, client_port) = server.accept()
    print(f'({client_ip}, {client_port}) MADE CONTACT.')
    thread = threading.Thread(target=handle_client, args=[ENCODING, connection, client_ip, client_port, ACCOUNT_PASSWORD_DICT, ACCOUNT_BALANCE_DICT])
    thread.start()
