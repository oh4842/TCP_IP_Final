from socket import *
from threading import Thread


# 클라이언트마다 스레드 실행을 위한 정보들인 소캣, ip, port를 받는다
def client_info(client_sock, client_ip, client_port):
    # 배열을 사용하기 위한 global 선언
    global connections
    # 소캣 내용을 저장하는 배열에 들어오는 소캣의 정보를 넣는다.
    connections.append(client_sock)
    
    # 메시지를 계속 처리하기 위해
    while True:
        # 메시지 수신
        msg = client_sock.recv(buf_size)
        # 서버에 메시지 출력
        print(msg.decode())
        # 메시지로 /out 이라는 것을 받았을 때
        if msg.decode() in '/out':
            print('[%s] 클라이언트 종료합니다...' % client_port)
            # 해당 클라이언트 소캣을 배열에서 지워주고
            connections.remove(client_sock)
            # 해당 클라이언트를 닫는다.
            client_sock.close()
        
        # 받은 메시지 중 'connectnickname|' 존재 여부를 찾는다
        tempmsgnick = msg.decode().find('connectnickname|')
        # 받은 메시지 중 'kill|' 존재 여부를 찾는다
        tempkill = msg.decode().find('kill|')

        # kill|이 있다면 실행
        if tempkill != -1:
            # 2개의 변수로 나누어 받는다. kill|유저이름 형식
            tempkill1, tempkill2 = msg.decode().split('|')
            # 보내서 담아줄 변수 실행
            temp: object = tempkill2 + '가 사망했습니다'
            # 모두에게 메시지를 보내준다.
            for conn in connections:
                conn.sendall(str(temp).encode())
            # 해당하는 소캣을 닫아버린다.
            socket_list[tempkill2].close()
            # connections에서 해당 값 삭제
            connections.remove(client_sock)
            # socket_list에서 해당 값 삭제
            del socket_list[tempkill2]
            continue
        # connectnickname|이 있다면 실행
        if tempmsgnick != -1:
            # connectnickname|유저이름 형식으로 받아서 나눈다.
            tempmsgnick1, tempmsgnick2 = msg.decode().split('|')
            # socket_list에 추가한다.
            socket_list.setdefault(tempmsgnick2, client_sock)

        # 소캣 정보 배열에 있는 소캣들 마다 전부 보내준다.
        for conn in connections:
            # 자신이라면 보내지 않는다
            if conn == client_sock:
                continue
            conn.send(msg)

        # 메시지가 없을 경우 반복문 탈출
        if not msg:
            break

# 서버 Ip
host = '127.0.0.1'
# 서버 port
port = 2700
# bind시 한 번에 하기 위한 변수
ADDR = (host, port)
# 버퍼의 크기
buf_size = 1024
# 최대 클라이언트 접속 수
max_client = 32
# 소캣 내용 저장
connections = []
# 닉네임별 소캣으로 저장할 딕셔너리 생성 # 구현 실패
socket_list = {}

if __name__ == '__main__':
    print('--------Server Ready--------')
    print('----------------------------')
    print('---------Createing.---------')
    # 소캣 생성
    sock = socket(AF_INET, SOCK_STREAM)
    # 소켓에 IP, PORT 할당
    sock.bind(ADDR)
    # 소켓 연결 요청 max_client만큼 대기 총 32개의 클라이언트를 받을 수 있음
    sock.listen(max_client)
    print('----------------------------')
    print('--------Server Start--------')
    while True:
        # 소캣, (ip, port)로 클라이언트 접속 허용
        clinet_sock, (clinet_ip, client_port) = sock.accept()
        # 확인을 위한 포트 출력
        print('서버에 연결되었습니다.....', client_port)
        # 클라이언트가 들어올 때 마다 스레드 처리
        client_thread = Thread(target=client_info, args=(clinet_sock, clinet_ip, client_port))
        client_thread.daemon = True
        client_thread.start()
