# 2025 04 12

main에는 최대한 gui관련만 넣어놓고
deck_tracker랑 game_logic, utills에서
함수 끌어다 쓰는거

ico파일은 아이콘이고
main.exe는 실행파일이라서
이거만 다운받아서 사용하면 됨.

spec파일은 아직 잘 모르겠음.

cmd창에 cd 파일위치 한다음에
pyinstaller --noconsole --onefile --icon=poker_chip_hd.ico main.py
이거 넣으면 exe 만들어짐.

위치 제대로 들어왔나 확인하려면 dir 입력해보기

그리고 뭔 .bat 이라는 형식이 있다는데
나중에 해보자.
