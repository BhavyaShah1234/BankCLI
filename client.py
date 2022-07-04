import socket

SERVER_IP = '192.168.29.20'
SERVER_PORT = 24091
ENCODING = 'utf-8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

acc_number = input('ENTER ACCOUNT NUMBER: ')
password = input('ENTER PASSWORD: ')
client.send(bytes(acc_number, ENCODING))
client.send(bytes(password, ENCODING))

response = client.recv(1024).decode(ENCODING)
if response == 'PASS':
    connected = True
    print(f'CONNECTION SUCCESSFUL.')
    while connected:
        balance = float(client.recv(1024).decode(ENCODING))
        print(f'\n\nBALANCE: {balance}')

        choice = input('1) DEPOSIT MONEY\n2) WITHDRAW MONEY\n3) EXIT\nENTER CHOICE: ')
        client.send(bytes(choice, ENCODING))
        if choice == '1':
            amount = input('ENTER AMOUNT: ')
            client.send(bytes(amount, ENCODING))
        elif choice == '2':
            amount = input('ENTER AMOUNT: ')
            client.send(bytes(amount, ENCODING))
            response = client.recv(1024).decode(ENCODING)
            if response == 'INSUFFICIENT BALANCE':
                print('INSUFFICIENT BALANCE')
        elif choice == '3':
            exit(0)
        else:
            print('INVALID CHOICE.')
else:
    print('CONNECTION UNSUCCESSFUL.')
    client.close()
