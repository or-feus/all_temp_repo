"""
Prod By. 정선교
화성시 일괄 소프트웨어 변경 프로그램
변경하거나 업데이트할 파일이나 시스템이 있을 때 사용할 것
"""

import os

lte_address = [
    {'id': 'user', 'ip_band': '20.2.10', 'num': '2', 'area': '오일2교차로'},
    {'id': 'user', 'ip_band': '20.2.11', 'num': '2', 'area': '여의교차로'},
    {'id': 'user', 'ip_band': '20.2.12', 'num': '2', 'area': '백리교차로'},
    {'id': 'user', 'ip_band': '20.2.13', 'num': '2', 'area': '문학3교차로'},
    {'id': 'user', 'ip_band': '20.2.14', 'num': '2', 'area': '문학2교차로'},
    {'id': 'user', 'ip_band': '20.2.15', 'num': '2', 'area': '문학1교차로'},
    {'id': 'user', 'ip_band': '20.2.16', 'num': '1', 'area': '가막교차로'},
    {'id': 'user', 'ip_band': '20.2.17', 'num': '1', 'area': '동오첨단산업단지입구교차로'},
    {'id': 'user', 'ip_band': '20.2.18', 'num': '2', 'area': '찬구화학사거리'},
    {'id': 'user', 'ip_band': '20.2.19', 'num': '1', 'area': '린스트라우스아파트삼거리'},
    {'id': 'user', 'ip_band': '20.2.20', 'num': '1', 'area': '우남퍼스트빌삼거리'},
    {'id': 'user', 'ip_band': '20.2.21', 'num': '1', 'area': '중흥S클래스삼거리'},

    {'id': 'user', 'ip_band': '20.3.10', 'num': '1', 'area': '점촌교차로'},
    {'id': 'user', 'ip_band': '20.3.11', 'num': '3', 'area': '발안바이오과학고사거리'},
    {'id': 'user', 'ip_band': '20.3.12', 'num': '1', 'area': '동오타운교차로'},
    {'id': 'user', 'ip_band': '20.3.13', 'num': '2', 'area': '동오리마을교차로'},
    {'id': 'user', 'ip_band': '20.3.14', 'num': '1', 'area': '쉴모텔삼거리'},
    {'id': 'user', 'ip_band': '20.3.15', 'num': '2', 'area': '남양우림필유사거리'},
    {'id': 'user', 'ip_band': '20.3.16', 'num': '2', 'area': '남양아이파크앞교차로'},
    {'id': 'user', 'ip_band': '20.3.17', 'num': '1', 'area': '롤링힐스삼거리'},
    {'id': 'user', 'ip_band': '20.3.18', 'num': '2', 'area': '송림교차로'},
    {'id': 'user', 'ip_band': '20.3.19', 'num': '2', 'area': '삼부실교차로'},
    {'id': 'user', 'ip_band': '20.3.20', 'num': '2', 'area': '문호교차로'},
    {'id': 'user', 'ip_band': '20.3.21', 'num': '2', 'area': '비봉1'},
    {'id': 'user', 'ip_band': '20.3.22', 'num': '2', 'area': '비봉2'},
    {'id': 'user', 'ip_band': '20.3.23', 'num': '2', 'area': '샘골앞삼거리'},

]


def system_call(ip_address):
    area = lte_address[i]['area']
    id = lte_address[i]['id']
    ip_band = lte_address[i]['ip_band']
    num = lte_address[i]['num']

    for get_address in range(int(num)):
        ip_address = f"{ip_band}.{((get_address + 1) * 2) + 1}"

        # message_1 = f"sshpass -p 123 ssh -o StrictHostKeyChecking=no {id}@{ip_address} mv /home/user/jetson-inference/dbict/python/uart.py /home/user/jetson-inference/dbict/python/uart_old.py"
        # message_3 = f"sshpass -p 123 scp -o StrictHostKeyChecking=no uart.py {id}@{ip_address}:/home/user/jetson-inference/dbict/python/"
        # message_2 = f"sshpass -p 123 ssh -o StrictHostKeyChecking=no {id}@{ip_address} \"echo '123' | sudo -S systemctl restart uart\""
        message_4 = f"sshpass -p 123 ssh -o StrictHostKeyChecking=no {id}@{ip_address} \"echo '123' | sudo -S reboot\""

        # os.system(message_1)
        # os.system(message_2)
        # os.system(message_3)

        os.system(message_4)

        # print(f"\"echo '123' | sudo -S systemctl restart uart\"")
        print(f"Done: {area} -> {int(get_address) + 1} controller  ip : {ip_address}")


if __name__ == '__main__':

    # for i in range(len(lte_address)):
    #     system_call(i)

    for i in range(len(lte_address)):
        system_call(i)
