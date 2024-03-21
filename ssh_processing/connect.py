import paramiko


def init_session():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return ssh


def ssh_connect(hostname: str, port: int, username: str, password: str, ssh: paramiko.SSHClient):
    try:
        ssh.connect(hostname, port, username, password)
        print("Успешное подключение по SSH")
        return True
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return False
    finally:
        ssh.close()


def execute_command(command: str, ssh: paramiko.SSHClient):
    stdin, stdout, stderr = ssh.exec_command(command)
    data = stdout.read() + stderr.read()
    return data.decode('utf-8')

# host = '192.168.40.16'
# port = 22
# username = 'root'
# password = ''
