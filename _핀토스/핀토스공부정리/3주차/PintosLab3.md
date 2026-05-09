# Pintos lab 3

- 사용자 프로그램 실행
- 해야 할 일
```
- Supplemental page table
- Physical frame management
- Lazy Loading(demand paging)을 위한 page fault handler 수정
    - Stack growth, file-mapped 등
- mmap, munmap
- Swap in / out
```

- 용어
```
- page : 가상 메모리의 연속된 영역 [가상 주소 공간의 PGSIZE 단위 블록]
- frame : 물리 메모리의 연속된 영역 [물리 주소 공간의 PGSIZE 단위 블록]
- page table : 가상주소를 물리주소로 변환하는 자료구조 (page를 frame으로 매핑) (가상주소 -> 물리주소 매핑 구조 전체) [page를 frame에 매핑하는 계층적 자료구조, Pintos x86-64에서는 pml4가 최상위 테이블]
- Eviction : page를 frame에서 제거하고, 필요하면 swap table 또는 파일 시스템에 기록하는 것 (frame에서 어떤 page를 내보내는 전체 과정) [frame을 비우기 위해 page를 메모리에서 제거하는 과정, 필요하면 file 또는 swap disk에 기록함]
    - (page out : 메모리에 있던 page를 backing store로 내보내는 것)
    - (swap out : page를 swap disk로 내보내는 것)
만약 clean file-backed page라면 swap에 쓰지 않고 그냥 frame만 비워도 됨
나중에 필요하면 원래 파일에서 다시 읽으면 됨.
반면 anonymous page나 dirty page는 swap disk나 파일에 기록해야 할 수 있음
- Swap Table : eviction된 page가 swap partition에 기록되는 위치 [swap disk의 slot 사용 상태와 위치를 추적하는 커널 메모리 자료구조]
    - 메모리에 있는 커널 자료구조, 실제 page 내용이 저장되는 곳은 디스크의 swap partition / swap disk
    - 비교
        - swap disk : 실제 데이터가 저장되는 디스크 영역
        - swap table : swap disk의 어느 slot이 사용 중인지 추적하는 메모리 자료구조
            - bitmap이나 배열 같은 형태로 메모리에 있고, "이 page는 swap slot N번에 있다" 같은 정보를 supplemental page table entry 등에 기록
```

- 설계해야 할 자료구조
```
1. Supplemental page table : 프로세스별 자료구조로, 각 page의 보조 정보를 추적
    - ex : 데이터 위치(frame/disk/swap), 대응되는 kernel virtual address 포인터, active/inactive 등
2. Frame table
    - 할당되었거나 비어 있는 물리 frame을 추적하는 전역 자료구조
3. Swap table
4. File mapping table
    - 어떤 memory-mapped file이 어떤 page에 매핑되어 있는지 추적
```