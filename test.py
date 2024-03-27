import time
import paramiko
import socket


def get_top_output(server_address, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_address, port=22, username=username, password=password)

        stdin, stdout, stderr = ssh.exec_command("top -b -n1")
        top_output = stdout.readlines()
        ssh.close()
        return top_output
    except socket.error as e:
        print("Socket error:", e)
        return None
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
        return None
    except paramiko.SSHException as e:
        print("SSH connection failed:", e)
        return None


address = "192.168.40.17"
user = "root"
pwd = ""

while True:
    output = get_top_output(address, user, pwd)
    if output:
        for line in output:
            print(line.strip())
    else:
        print("Failed to get top output. Retrying...")
    time.sleep(0.5)

