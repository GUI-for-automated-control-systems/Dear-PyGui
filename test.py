import paramiko


def send_file_to_server(local_file_path, remote_file_path, server_address, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=server_address, username=username, password=password)

        scp = ssh_client.open_sftp()

        scp.put(local_file_path, remote_file_path)

        scp.close()
        ssh_client.close()
        print("Файл успешно передан на сервер.")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    local_file_path = "/home/egor/python-app/test.py"  # Путь к вашему локальному файлу
    remote_file_path = "/root/file/test.py"  # Путь куда вы хотите сохранить файл на удаленном сервере
    server_address = "192.168.40.17"
    username = "root"
    password = ""

    send_file_to_server(local_file_path, remote_file_path, server_address, username, password)
