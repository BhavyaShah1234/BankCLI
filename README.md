# BankCLI
This is a simple banking CLI. One can perform concurrent transactions of withdrawing and depositing money without letting race condition to occur.
The <code>server.py</code> file runs the script for central banking server and <code>client.py</code> file runs the script for client machines at various branches. One can see his or her account balance after every transaction. Insufficient balance messages are also displayed when one tries to withdraw a larger amount than the account's balance.
