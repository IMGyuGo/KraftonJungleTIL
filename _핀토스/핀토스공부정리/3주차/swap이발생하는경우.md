# Swap in, out 과 Page in, out
```
Page in/out ⊃ Swap in/out
즉, 모든 Page in/out은 Swap in/out이 될 수 없지만
모든 Swap in/out 은 Page in/out이 될 수 있다.

Page In / Page Out
[
    페이지를 RAM 에 넣거나
    RAM에서 빼는 행위 전체
]
backing store
[
    executable file
    mmap file
    swap disk
    file system
    전부 포함 가능
]
Swap In / Swap Out
[
    anonymous page를
    swap 영역으로 내보내거나 가져오는 것

    backing store가 specifically : swap disk 인 경우
]
```

# 왜 이런 구분이 중요할까?
1. 코드 영역 (.text)
```
프로그램 코드
ELF executable 에서 읽어온 페이지 (원본 파일이 존재)
그래서 page out 시 그냥 버려도 됨 (나중에 executable file에서 다시 읽으면 되니까)

(page out 발생 swap out은 아님)
```
2. mmap file
```
mmap("data.txt") 로 매핑된 파일
dirty 아니면 그냥 제거
dirty 면 원본 file에 write back

(page out 발생 swap out은 아님)
```
- dirty 파일이란
```
메모리로 매핑된 파일의 내용이 RAM에서 수정되었지만 아직 디스크 파일에는 반영되지 않은 상태를 의미
파일 -> mmap -> 메모리 페이지
```

# 이유

1. RAM이 꽉 찼을 때 (메모리 부족)
```
RAM:
[ A ][ B ][ C ][ D ]  ← 꽉 참

새 페이지 E 필요

운영체제가 victim 페이지 하나(C)를 골라
C -> swap disk로 저장 (page out)
E -> RAM으로 로딩 (page in)
```

2. Lazy Loading (Demand Paging)
```
프로그램 실행 시 ELF 전체를 RAM에 다 안올림

main()
foo()
bar()
실제로는 main()만 먼저 실행될 수 있기 때문에
처음엔 "가상주소만 등록하고 실제 frame은 없음" 상태로 둠

page fault 발생 -> 그때 ELF에서 읽어서 RAM에 올림 (이게 page in)
즉, RAM이 부족하지 않아도 발생 가능 (처음 접근) 자체가 원인

- 궁금증 1
    - 이 예시말고 다른 예시도 있는지 궁금 (Lazy Loading에서의)
```

3. mmap() 파일 접근
```
메모리 매핑 파일
mmap(file) 하면 파일 전체를 RAM에 즉시 안 읽음 -> 접근 시점에만 파일 일부 page in 발생
그리고 dirty 상태면 나갈 때 RAM -> 파일로 write back (page out 유사)
```

4. Stack Growth
- 스택도 처음부터 엄청 크게 잡지 않음
```
ex. RSP가 아래로 커지면서 아직 존재하지 않는 페이지를 접근하면 page fault -> 새 stack page 생성
```

5. Accessed Bit / Working Set 최적화
- 실제 Linux는 단순히 "RAM 꽉 참"만 보는 게 아님
```
운영체제가 최근 안 쓰는 페이지를 미리 page out하기도 함

왜냐하면
- 미래에 메모리 부족 가능성 대비
- 캐시 효율 최적화
- file cache 확보 등 때문
```
- 꼬리 질문 : Accessed Bit / Working Set 최적화가 아래 내용, 메모리 부족 가능성 대비, 캐시 효율 최적화, file cache 확보 등과 어떤 상관관계가 있지?
    - Linux가 RAM을 단순히 "비어 있는 공간"으로 보는 게 아니라 "최대한 활용해야 하는 자원"으로 본다는 것
    - Linux 철학은 빈 RAM = 낭비
    - Accessed Bit
    ```
    CPU는 페이지에 접근하면 PTE(Page Table Entry)에 Accessed bit = 1 을 자동으로 세팅 (최근 사용됨 이라는 표시)
    ```
| 페이지 | 최근 접근 여부 |
| --- | -------- |
| A   | 1        |
| B   | 1        |
| C   | 0        |
| D   | 0        |
그러면 운영체제는 C, D는 안쓰였네? 라고 판단

- 실제로 Working Set과 Accessed Bit을 통해 잘 안쓰인 페이지를 찾아서 미리 page-out
- 즉 자주 쓰는 페이지만을 메모리에 남기고 싶을 때 쓰는 전략

6. 파일 캐시 정리
- 리눅스는 남는 RAM을 file cache로 많이 사용함
```
디스크 파일 읽은 내용 -> RAM에 캐싱

메모리 필요해지면 (캐시 페이지 제거) 이런 식으로 page out 비슷한 reclaim 발생
```

# 실제로 RAM이 꽉 차 Swap이 발생할 때 어떤 것부터 page out이 되고, 어떤 것부터 page in이 될까?
```

```

# 개념

## ELF (Executable and Linkable Format)의 약자
```
운영체제에서 실행 파일, 오브젝트 파일(.o), 라이브러리(.so) 등을 저장하는 표준 파일 형식
Linux, Unix 계열에서 가장 많이 사용됨

Why ELF Used?
운영체제가 프로그램을 실행하려면 알아야 하는 정보가 많음
- 코드가 어디에 있는지
- 데이터 영역은 어디인지
- 시작 주소(entry point)는 어디인지
- 어떤 메모리에 올려야 하는지
- 어떤 라이브러리를 연결해야 하는지
이걸 전부 규칙화한 파일 형식이 ELF

즉, 운영체제가 프로그램을 실행하기 위한 설명서

+-------------------+
| ELF Header        |
+-------------------+
| Program Header    |
+-------------------+
| .text             |  <- 실행 코드
+-------------------+
| .data             |  <- 초기화된 전역 변수
+-------------------+
| .bss              |  <- 초기화 안 된 전역 변수
+-------------------+
| Symbol Table      |
+-------------------+

1. ELF Header
파일이 ELF인지 확인하는 정보가 들어있음
- 32bit / 64bit
- little endian
- entry point 주소
- program header 위치

2. .text
printf("hello");
같은 코드가 컴파일되면 여기에 들어감.
보통 읽기 전용(Read Only)

3. .data
초기화된 전역 변수

4. .bss
초기화 안 된 전역 변수

Pintos에서 ELF를 어떻게 사용하나?
- Pintos의 load() 함수가 ELF 파일을 읽음
ELF 파일 열기
    ↓
ELF Header 검사
    ↓
Program Header 읽기
    ↓
각 segment를 메모리에 매핑
    ↓
유저 스택 생성
    ↓
RIP(entry point) 설정
    ↓
iret로 유저 프로그램 실행

ELF에는 이 코드를 가상주소 0x400000에 올려라 라는 말이 있음

```