import paramiko


class SSHProcessing:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, host, port, username, password):
        try:
            self.ssh.connect(hostname=host, port=port, username=username, password=password)
            return True
        except Exception as e:
            print("Connection error:", str(e))
            return False

    def execute_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdout.read().decode('utf-8')
        except Exception as e:
            print("Command execution error:", str(e))
            return None

# host = '192.168.40.16'
# port = 22
# username = 'root'
# password = ''
