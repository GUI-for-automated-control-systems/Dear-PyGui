import paramiko
import dearpygui.dearpygui as dpg


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

    def close(self):
        self.ssh.close()

    def execute_command(self, command):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdout.read().decode('utf-8')
        except Exception as e:
            print("Command execution error:", str(e))
            return None

    def get_vm_info(self):
        distributive_info = self.execute_command('lsb_release -a')
        memory_info = self.execute_command('df -h')
        cpu_info = self.execute_command('lscpu -e')
        uptime_info = self.execute_command('uptime')
        return distributive_info, memory_info, cpu_info, uptime_info

    def send_file_to_server(self, local_file_path, remote_file_path):
        try:
            with open(local_file_path, 'rb') as local_file:
                ftp_client = self.ssh.open_sftp()
                ftp_client.putfo(local_file, remote_file_path)
                ftp_client.close()
            dpg.set_value('transfer_message', 'The file is successfully transferred to the server.')
        except Exception as e:
            dpg.set_value('transfer_message', f'{e}')

    def get_top_output(self):
        try:
            stdin, stdout, stderr = self.ssh.exec_command("top -o %CPU -b -n1")
            top_output = stdout.readlines()
            return top_output
        except Exception as e:
            print("Error getting top output:", str(e))
            return None

