import os

lte_address = [
    {'area': '1', 'id': 'user', 'ip': '10.154.58.2', 'num': '2'},
    {'area': '2', 'id': 'user', 'ip': '10.121.227.206', 'num': '2'},
    {'area': '3', 'id': 'user', 'ip': '10.77.128.77', 'num': '2'},
    {'area': '4', 'id': 'user', 'ip': '10.121.95.231', 'num': '2'},
    {'area': '5', 'id': 'user', 'ip': '10.82.83.92', 'num': '2'},
    {'area': '6', 'id': 'user', 'ip': '10.152.142.28', 'num': '2'},
    {'area': '7', 'id': 'user', 'ip': '10.64.160.80', 'num': '2'},
    {'area': '8', 'id': 'user', 'ip': '10.76.61.165', 'num': '1'},
    {'area': '9', 'id': 'user', 'ip': '10.228.186.199', 'num': '1'},
    {'area': '10', 'id': 'user', 'ip': '10.151.199.20', 'num': '2'},
    {'area': '11', 'id': 'user', 'ip': '10.144.217.202', 'num': '2'},
    {'area': '12', 'id': 'user', 'ip': '10.118.57.196', 'num': '2'},
    # {'area': '13', 'id': 'user', 'ip': '10.192.115.136', 'num': '2'},
    # {'area': '14', 'id': 'user', 'ip': '10.230.86.108', 'num': '2'},

]


def system_call(ip_address):

    area = lte_address[i]['area']
    id = lte_address[i]['id']
    ip_address = lte_address[i]['ip']
    num = lte_address[i]['num']

    for get_port in range(int(num)):
        port = f"{get_port + 1}022"  ## port : x022

        message_1 = f"sshpass -p 123 ssh -o StrictHostKeyChecking=no -p {port} {id}@{ip_address} \"echo '123' \| sudo -S rm /home/user/DetectNet-COCO-Chair -r\""
        message_2 = f"sshpass -p 123 ssh -o StrictHostKeyChecking=no -p {port} {id}@{ip_address} mkdir /home/user/DetectNet-COCO-Chair"
        message_3 = f"sshpass -p 123 scp -o StrictHostKeyChecking=no -P {port} /Users/feus/JetBrains/PyCharm/utility/model/* {id}@{ip_address}:/home/user/DetectNet-COCO-Chair/"

        os.system(message_1)
        os.system(message_2)
        os.system(message_3)

        print(f"Done: {area} -> {int(get_port) + 1} controller")


if __name__ == '__main__':

    # for i in range(len(lte_address)):
    #     system_call(i)

    for i in range(len(lte_address)):
        system_call(i)

