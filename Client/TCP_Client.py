from socket import *
from threading import Thread


# 메시지를 받는 함수
def receive_handler():
    while True:
        # 메시지 수신
        try:
            receiveMsg = sock.recv(buf_size)
            # 아무것도 없을 시 반복문 종료
            if not receiveMsg:
                break
            # 깔끔하게 보이게 하기위한 콘솔창 전 줄 삭제
            print('', end='\r', flush=True)
            # 받는 메시지중 ':'이 있나 확인한다.
            flag = receiveMsg.decode().find(':')
            # ':'이 있다면 실행
            if flag != -1:
                # 메시지 출력
                print(receiveMsg.decode())
                # split으로 나눈 내용들을 따로 저장한다.
                nick, nick_answer = receiveMsg.decode().split(':')
                # 나눈 후 정답 부분의 문자열을 해당 클라이언트에 저장한 것과 비교한다.
                if nick_answer == answer:
                    # 정답이 맞을 시 죽었다는 걸 알리기 위해 보낸다.
                    sock.send(str('kill|' + user_name).encode())
                    print('당신은 죽었습니다.')
                    # 프로그램 종료
                    exit()
            else:
                # 메시지 출력
                print(receiveMsg.decode())
                continue
        except:
            pass

# 메시지를 보내는 함수
def send_handler():
    while True:
        # 보낼 메시지 입력
        msg = input(user_name + ":")
        # 메시지가 /out 일시에 소캣 닫음
        if msg == '/out':
            # /out을 서버에 알리기 위해 보낸다
            sock.send(msg.encode())
            print('채팅을 종료합니다...')
            return

        # 이 외의 메시지일 경우 유저이름:메시지
        msg = user_name + ":" + msg
        # 만든 소캣으로 인코딩하여 보냄
        sock.send(msg.encode())


# 서버 ip
ip = '127.0.0.1'
# 서버 port
port = 2700
# 버퍼 사이즈
buf_size = 1024
# 연걸 시 필요한 변수 서버 ip, port
ADDR = (ip, port)
# 유저 닉네임
user_name = ''
answer = ''

if __name__ == '__main__':
    # IPv4, TCP 방식 서버 소켓 생성
    sock = socket(AF_INET, SOCK_STREAM)
    # 서버ip, port로 접속
    sock.connect(ADDR)
    print('서버에 연결 되었습니다.')

    # 이름이 제대로 입력 될 때 까지
    while True:
        # 유저 이름 입력
        user_name = input('닉네임 입력 : ')

        # 유저 이름 빈칸 입력 시
        if user_name == '':
            print('닉네임을 입력해 주세요......')
            # 반복문 다시 실행
            continue
        else:
            # 닉네임 전송
            username = 'connectnickname|' + user_name
            sock.send(username.encode())
            break

    while True:
        # 금지어 입력
        answer = input('금지어를 입력하세요 : ')

        # 금지어 빈칸 입력 시
        if answer == '':
            print('금지어를 다시 입력해 주세요......')
            continue
        else:
            break

    # 메시지 보내기, 받기 스레드 생성
    send_thread = Thread(target=send_handler, args=())
    receive_thread = Thread(target=receive_handler, args=())

    # 프로그램 종료 시 스레드도 종료
    send_thread.daemon = True
    receive_thread.daemon = True

    # 스레드 시작
    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()
