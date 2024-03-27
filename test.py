import paramiko


def get_top_output(server_address, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server_address, port=22, username=username, password=password)

    stdin, stdout, stderr = ssh.exec_command("top -b -n1")
    top_output = stdout.readlines()
    ssh.close()
    return top_output


address = "192.168.40.17"
user = "root"
pwd = ""

while True:
    output = get_top_output(address, user, pwd)
    if output:
        for line in output[7:28]:
            print(line.strip())
    else:
        print("Failed to get top output. Retrying...")

