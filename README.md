# App Chat Zalo

## Running the code
### Starting the server
In the commandline, start the server with ```python3 server.py```. Change ```localhost``` in server.py to ```127.0.0.1``` to be able to accept connections from other computers.

### Starting the client app
In the commandline, start the server with ```python3 client.py```

### Logging to the server
- Hostname ```127.0.0.1```
- Port```8686```
- Enter "Username and Password" to enter the server
- Click the ```Login``` button.

- Create multiple instances of the client for messages to be sent and received by each client

### Register
- Enter Username, Password, Confirm Password and Name to register
- Click the ```Register``` button.

### Send Group Message
- Click the ```Group``` button to show people who are already online.
- Select the people you want to talk to and then click the ```Ok``` button to text
## Generating ```.py``` files from ```.ui``` files
Run ```pyuic5 test.ui -o test.py```

