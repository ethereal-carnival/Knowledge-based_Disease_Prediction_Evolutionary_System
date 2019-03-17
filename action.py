import json, os
from pymongo import MongoClient


class MongoDBManagement:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['openConnect']
        self.collection_student = self.db['dataFromDevice']

    def insert_one(self, s):
        self.collection_student.insert_one(s)


# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

port = 22

client = MongoClient('localhost', 27017)
db = client['openConnect']
collection = db["users"]


def do(path, username):
    user = collection.find_one({'username': username})
    host = user['ip']
    ssh_username = user['ssh_username']
    """
    try:
        ssh.connect(host, port=port, username=ssh_username)
        stdin, stdout, stderr = ssh.exec_command('python ' + path + 'capture.py')
    except paramiko.ssh_exception.NoValidConnectionsError:
        return 'Device is not connected to the internet or IP for the device has changed. Please update the IP. If the problem persits, please check if ssh is snabled on your RaspberryPi Device'
    except paramiko.ssh_exception.SSHException:
        return 'Either the registered user has been deleted or SSH access has been revoked. Please register the user and IP again to continue.'
    else:
        output = stdout.read()
        ssh.close()
        mongoDB = MongoDBManagement()
        mongoDB.insert_one(json.loads(output))
        return 'Executed'
    """
    return "Hello"
