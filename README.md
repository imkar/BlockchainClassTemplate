# BlockChain Class Implementation

Implementation of a Blockchain class, operations can be called remotely using Remote Procedure Call (RPC) obviously with centralized architecture. Each Blockchain created by this class runs on own server, and the operations between them called remotely using proxies by clients. 

Python 3 and PYRO4 used during the implementation.

Operations clients can make on the Blockchain class:
- CreateAccount: Client can create an Account, which does not exist and put value in it.
- Transfer: Client can transfer money to someone in the same blockchain, or transfer money to its account. In both scenarios, there must exist an Account, which is already created.
- Exchange: Clients can convert their currency by charging with exchange rate.
- calculateBalance: Service provided to client, in order to check its balance.
- printChain: Prints the Blockchain. 

Installing requirements:

$ pip install Pyro4

Run above command after installing Python3 and pip.

## Run the below command below before running Blockchain Servers:

$ python -m Pyro4.naming 

After starting the naming service, run following:

$ python BTCServer.py
$ python ETHServer.py

Then, start the clients.

Thanks,
