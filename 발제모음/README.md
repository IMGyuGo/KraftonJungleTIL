# CSAPP 공부법

## How study?

- 색깔에 따라 파트가 다르다.

- 1 ~ 6 ( 시스템 구조 )

- 7 ~ 9 ( 알아야 하는 내용 )

- 10 ~ 12 ( 알아야 하는 내용 )

- 1, 3, 4, 6, 7, 8, 9, 10, 11 ( 다 읽어야 함 )

- 실질적으로 1장읽고 3장 -> 9장 -> 11장

- 핀토스 가더라도 별 내용은 없고 7장,8장이 알면 약간 도움 됨

## 3장- Machine-Level Representation of Programs

- C 언어를 기계어로 변경

- C언어를 기계어로 바꾼다는건 실행가능한 파일을 만든다느 것

- Compiler가 하는 역할

### 어셈블리 생성 과정

```
main.c -> translator(cpp, cc1, as) -> main.o
sum.c -> translator(cpp, cc1, as) -> sum.o
합쳐서
-> Linker(Id) -> 실행파일

목적파일은 시스템마다 다르다. ★

Windows: Portal Executable(PE)
Linux: Executable and Linkable Format(ELF)
Mac OS-X: Mach-0

-> 운영체제마다 컴파일러가 다르고, 만들어지는 결과도 다르다. (바이너리로 바꿔주는데 규칙이 다 다르다)
```

### 어셈블리 명령어 종류

```
어셈블리 멸영어 세트는 CPU마다 다르다.

데이터 이동, 함수 호출,
산술 연산, 스택 관련,
논리/비트 연산, 제어 흐름,
비교 및 조건 설정, 인터럽트/시스템
```

### 어셈블리 실행 환경

```
어셈블리 실행 환경

- 메모리

스택
힙 (malloc/free)
코드 (assembly code)
```

- 구체적인 어셈블리 명령어가 아닌 변환 규칙을 아는 게 목표다.

- 3장 서브섹션
  - assignment
  - calculate
  - if
  - for
  - function
  - array
  - class (이기종 자료 구조) struct
  - 부동소수점 float

- ## 할당문

- 학습 방법

```
1. 노트북 LM을 사용한다.

2. 남한테 설명했을 때 이해가 될 수 있도록 설명할 줄 알아야 한다.
-> 남한테 설명하지 못하면 정리한 게 아니다!
```
