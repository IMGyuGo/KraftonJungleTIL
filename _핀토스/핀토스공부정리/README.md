### 1. 아래 파일에서 제일 아랫 줄 source ./pintos/activate로 변경

```bash
sudo vi ~/bashrc
```

### 2. pintos 테스트시 /usr/bin/env: ‘python3\r’: No such file or directory 에러 발생

- .gitattributes 파일 변경

```
# 기본
* text=auto eol=lf

# 절대 깨지면 안되는 것들
*.sh text eol=lf
Makefile text eol=lf
*.mk text eol=lf

# Pintos utils
utils/* text eol=lf

# Python
*.py text eol=lf

# C 파일도 통일 (선택)
*.c text eol=lf
*.h text eol=lf
```

- 변경 내역 반영 후 확인

```bash
git add --renormalize .
git commit -m "Normalize line endings to LF"

git status

git rm --cached -r .
git reset --hard

git ls-files --eol | grep crlf
git ls-files --eol
```

### 빌드하기

```bash
cd ./pintos/threads
make
```

-> build 폴더 생성

```
# Makefile : 사본
# kernel.o : 전체 커널에 대한 오브젝트 파일
    - 각 소스 파일에서 컴파일된 오브젝트 파일들을 하나의 오브젝트 파일로 링크한 결과
    - 디버그 정보가 포함되어 있으므로 GDB 또는 backtrace를 실행 가능
# kernel.bin : 커널의 메모리 이미지, 핀토스 커널을 실행하기 위해 메모리에 로드된 정확한 바이트
    - kernel.o 디버그 정보는 제거되어 공간을 크게 절약할 수 있으며, 결과적으로 커널 로더 설계에서 부과하는 512kB 크기 제한에 커널이 걸리지 않도록 함
# loader.bin : 커널 로더용 메모리 이미지, 어셈블리 언어로 작성된 작은 코드 덩어리로, 디스크에서 커널을 읽어 메모리로 불러와 실행하는 역할 (크기는 정확히 512Byte, PC BIOS에서 고정된 크기. 하위 디렉터리에는 컴파일러가 생성하는 build 오브젝트 파일(.o)과 종속성 파일(.d)가 포함됨. 종속성 파일은 다른 소스 파일이나 헤더파일이 변경될 때 어떤 소스 파일을 다시 컴파일 해야 하는지 make에 알려줌)
```

### 시작 테스트

- build 디렉토리로 이동

```bash
pintos -- run alarm-multiple
```

- 파일로 출력

```bash
pintos -- run alarm-multiple > logfilepintos run
```

### 3. pintos 명령어가 무엇?

`QEMU(에뮬레이터) 위에서 Pintos OS를 실행하고, 테스트 프로그램을 같이 돌려주는 명령어`

```bash
pintos --fs-disk=10 -p tests/userprog/args-single:args-single -- -q -f run 'args-single onearg'
```

- 1. 디스크 이미지 생성 (--fs-disk=10)
- 2. 실행할 테스트 파일 복사 (-p)
- 3. QEMU 실행
- 4. Pintos 커널 부팅
- 5. user program 실행 (run 'args-single onearg')

> 즉, 부팅 + 파일 복사 + 실행 까지 한 번에 처리

### 4. pintos-mkdisk 명령어?

`Pintos용 가짜 디스크 이미지 파일을 만드는 명령어`

- filesys.dsk라는 이름의 10MB짜리 디스크 이미지 생성
- pintos는 실제 하드디스크에 직접 쓰는게 아니라, QEMU 안에서 사용할 가상 디스크 파일을 만들어서 그곳에 파일시스템을 올림

```bash
pintos-mkdisk filesys.dsk 10
```

### 5. backtrace 명령어는 무엇?

`프로그램이 죽었을 때 또는 커널 패닉이 났을 때`
`어떤 함수들이 차례대로 호출되다가 여기까지 왔는지를 보여주는 함수 호출 기록`

- 실행

```bash
backtrace kernel.o 0x80042113 0x80043210 0x80044555
```

- 결과

```
0x80042113: thread_current (threads/thread.c:120)
0x80043210: schedule (threads/thread.c:300)
0x80044555: thread_yield (threads/thread.c:400)
```

# 전체 큰 흐름

```
Pintos
"동시에 여러 thread가 실행된다"는 개념은 Pintos에서는 없음
대신 "여러 thread가 번갈아 실행되는 time slicing"

왜 여러 개가 동시에 실행 안되나?
Pintos는 기본적으로
단일 CPU (single-core) 환경으로 동작

실제
동시에 "존재"하는 thread는 여러 개 이지만 CPU는 하나라서
A 실행 -> 잠깐 멈춤
B 실행 -> 잠깐 멈춤
C 실행 -> 잠깐 멈춤
이걸 엄청 빠르게 반복
-> 그래서 동시에 실행되는 것처럼 보이는 것 (concurrency)

Concurrency -> 번갈아 실행 (pintos)
Parallelism -> 진짜 동시에 실행 (multi-core)
```

```
- interrupt 때문에 context switching이 "항상" 일어나는 건 아님
- 특정 조건에서만 스케줄러가 개입하면서 발생

Interrupt 발생
-> 커널 진입
-> interrupt handler 실행
-> (필요하면) thread_yield / schedule
-? context switching
```

# 함수 분석

> threads/init.c

```
int main(void);
    ↓
bss_init()
    ↓


```

# 테스트 케이스 분석 (개념적으로)

```
> 공통적으로 보는 것
timer_sleep(ticks)가 현재 스레드를 정확한 시점까지 재웠다가 깨우는지, 그리고 ticks <= 0 같은 예외 입력도 안전하게 처리하는지 확인
```

## alarm-single

- alarm-wait.c

```
5개 스레드를 만들고, 각 스레드가 한 번만 잠
스레드 0은 10 ticks, 1은 20 ticks, ... 이런 식으로 서로 다른 시간 동안 잠듬
기대하는 건 "짧게 잔 스레드가 먼저, 길게 잔 스레드가 나중"
즉, 기본적인 wake-up 시점과 순서가 맞는지 보느 기초 테스트
```

## alarm-multiple

- alarm-wait.c

```
구조는 같고, 각 스레드가 한 번이 아니라 여러 번 잠
한 번은 맞는데 반복하면 꼬이는 구현을 잡아냄
sleep list에서 제거를 제대로 안 하거나, 깬 뒤 다시 재울 때 상태가 꼬이거나, 횟수가 누락되는 버그를 잘 잡음
테스트는 각 스레드의 iteration * duration 값이 nondecreasing 인지, 그리고 정확히 정해진 횟수만큼 깼는지 확인
```

## alarm-simultaneous

- alarm-simultaneous.c

```
여러 스레드가 같은 길이인 10 ticks씩 잠들고, 이걸 여러 번 반복
핵심은 같은 iteration 안에서는 모든 스레드가 "같은 tick"에 깨어나야 한다는 점
이 테스트는 "현재 tick에 깨워야 할 스레드가 여러 개일 때 하나만 깨우고 나머지는 다음 tick으로 미루는 버그"를 잡음
즉, timer interrupt 때 wake_tick <= now 인 스레드를 전부 깨우는지가 중요
```

## alarm-zero

- alarm-zero.c

```
timer_sleep(0)을 호출하고 바로 pass()함.
의미는 단순. 0 tick이면 재우지 말고 즉시 리턴
여기서 block 되거나 이상한 상태가 되면 실패
```

## alarm-negative

- alarm-negative.c

```
timer_sleep(-100) 을 호출하고 바로 pass()함
의미는 "음수 입력이 와도 커널이 멈추거나 crash나면 안 된다."
보통 ticks <= 0 이면 그냥 return 하도록 구현하면 됨.
```

### alarm 구현에서의 핵심

```
ticks <= 0 이면 즉시 반환
ticks > 0 이면 현재 스레드를 block
timer interrupt 때 깰 시각이 된 스레드를 모두 unblock
busy waiting 대신 sleep queue + block/unblock 방식 사용
```

# 공부하는 내용 아래에 정리

## 동기화 (asynchronize)

### 인터럽트 비활성화 (interrupt disable)

```
동기화를 위한 가장 기본적인 방법
1. 인터럽트를 비활성화
즉, CPU가 인터럽트에 응답하지 못하도록 일시적으로 막는 것
인터럽트가 꺼져 있으면 다른 스레드가 실행 중인 스레드를 선점할 수 없음
스레드 선점은 타임 인터럽트에 의해 이루어짐
인터럽트가 켜져 있는 경우(일반적으로) 실행 중인 스레드는 두 C 명령문 사이 또는 명령문 실행 중에도 언제든 다른 스레드에 의해 선점될 수 있음
(핀토스는 "선점형 커널". 즉, 커널 스레드는 언제든지 선점될 수 있음 - 기존 유닉스는 "비선점형")
선점형 커널은 더 명시적인 동기화를 필요로 함
인터럽트 상태를 직접 설정할 필요는 거의 없고 대부분의 경우 다른 동기화 기본 요소를 사용해야 함.
인터럽트를 비활성화하는 주된 이유는 커널 스레드를 외부 인터럽트 핸들러와 동기화하기 위함
외부 interrupt handler는 sleep 기능을 사용할 수 없으므로 대부분의 다른 동기화 방식을 사용할 수 없음
일부 외부 interrupt는 인터럽트를 비활성화하더라도 연기할 수 없음. 이러한 인터럽트를 "마스크 불가능 인터럽트(NMI)"라고 하며, 컴퓨터에 화재가 발생한 경우와 같은 비상 상황에서만 사용하도록 되어 있음.
```

- 마스크 불가능 인터럽트(NMI - Non-Maskable Interrupt)
  - "CPU가 절대 무시(마스크)할 수 없는 인터럽트"
  ```
    1. 하드웨어 오류
    2. 전원 이상
    3. 시스템 치명적 실패
    4. 디버깅/프로파일링 (특수 용도)
  ```

### 신호기 (Semaphore)

```
Semaphore는 음수가 아닌 정수와 이를 원자적으로 조작하는 두 개의 연산자로 구성됨.
그 연산자는 다음과 같음
- "Down" or "P" : 값이 양수가 될 때까지 기다린 후 값을 1/2로 줄임
- "Up" or "V" : 값을 증가시키고 (대기 중인 쓰레드가 있으면 하나를 깨움)

0으로 초기화된 세마포어는 정확히 한 번만 발생하는 이벤트르 기다리는 데 사용할 수 있음
예를 들어, 스레드 A가 다른 스레드 B를 시작하고 B가 어떤 작업을 완료했다는 신호를 보낼 때 까지 기다리고 싶다고 가정해 봄.
A는 0으로 초기화된 세마포어를 생성하여 B가 시작될 때 전달하고, B가 작업을 완료하면 세마포어를 "Down"함.
B가 작업을 완료하면 세마포어를 "Up"함.
이 방법은 A가 먼저 세마포어를 "Down"하든 B가 먼저 "Up"하든 상관없이 작동
```

### Locks

```
"up" eq "release"
"down" eq "acquire"
```

# 코어타임 문제들

timer_sleep()를 올바르게 구현한 방식으로 가장 적절한 것은?
A. while 루프에서 계속 thread_yield()를 호출한다.
B. 현재 스레드를 sleep_list에 넣고 thread_block() 한 뒤, timer interrupt에서 깨운다.
C. 현재 스레드를 ready_list에 다시 넣고 기다린다.
D. busy_wait()를 사용해 tick 수를 직접 센다.
정답: B
해설: alarm clock 과제의 핵심은 busy waiting을 없애고 block/unblock 기반으로 재우고 깨우는 것입니다.

sleep_list를 전역 변수로 선언했더라도 list_init(&sleep_list)가 필요한 이유는?
A. 전역 변수는 자동으로 1로 초기화되기 때문이다.
B. struct list는 단순 0 초기화만으로는 유효한 빈 리스트 상태가 아니기 때문이다.
C. sleep_list는 heap에만 존재할 수 있기 때문이다.
D. list_insert_ordered()가 내부에서 malloc()을 호출하기 때문이다.
정답: B
해설: Pintos 리스트는 head.next = &tail, tail.prev = &head 같은 sentinel 연결이 필요합니다.

struct thread에 wakeup_tick 필드를 추가하는 가장 직접적인 이유는?
A. 스레드의 우선순위를 저장하기 위해
B. 스레드의 이름 길이를 저장하기 위해
C. 잠든 스레드를 언제 깨워야 하는지 기록하기 위해
D. 인터럽트 횟수를 저장하기 위해
정답: C
해설: timer_sleep(ticks) 호출 시 현재 tick + ticks 값을 저장해 두어야 interrupt 시점에 깨울 수 있습니다.

timer_interrupt()에서 반드시 해야 하는 동작으로 가장 적절한 것은?
A. ticks를 감소시키고 모든 스레드를 block한다.
B. ticks를 증가시키고, 깨어날 시간이 된 sleeping thread들을 thread_unblock() 한다.
C. 현재 실행 중인 스레드를 무조건 종료한다.
D. sleep_list를 매 tick마다 비운다.
정답: B
해설: tick 증가와 wakeup 처리가 alarm 테스트의 핵심입니다.

semaphore와 lock의 차이로 가장 올바른 것은?
A. lock은 owner가 없고, semaphore만 owner가 있다.
B. semaphore는 항상 값이 0 또는 1이다.
C. lock은 owner가 있으며, 보통 획득한 스레드만 release할 수 있다.
D. 둘은 완전히 동일한 자료구조라 의미 차이가 없다.
정답: C
해설: lock은 ownership이 있는 binary semaphore라고 보면 됩니다.

Pintos에서 timer tick 처리 흐름으로 가장 적절한 것은?
A. timer_sleep() -> thread_exit() -> timer_interrupt()
B. timer_init() -> intr_register_ext() -> 하드웨어 tick -> intr_handler() -> timer_interrupt()
C. lock_acquire() -> sema_up() -> timer_interrupt()
D. thread_block() -> malloc() -> timer_interrupt()
정답: B
해설: PIT가 interrupt를 발생시키고, 공통 interrupt 경로를 거쳐 timer_interrupt()가 실행됩니다.

기존 timer_sleep()의 while (timer_elapsed(start) < ticks) thread_yield(); 방식이 문제인 이유는?
A. interrupt를 절대 발생시키지 못해서
B. 스레드를 실제로 block하지 않고 반복적으로 깨어나 CPU를 낭비하기 때문에
C. thread_yield()가 항상 panic을 일으키기 때문에
D. tick 값을 음수로 만들기 때문에
정답: B
해설: yield는 양보일 뿐이고, 과제가 요구하는 sleep queue 기반 수면이 아닙니다.

alarm-single 테스트가 timeout으로 끝났다면 가장 먼저 의심할 부분은?
A. timer_sleep()에서 스레드를 재우는 코드가 없는 경우
B. timer_interrupt()에서 sleeping thread를 깨우는 코드가 없는 경우
C. thread_name()이 잘못된 경우
D. malloc()이 0을 반환한 경우
정답: B
해설: 재우기만 하고 깨우지 않으면 테스트는 보통 TIMEOUT으로 끝납니다.
