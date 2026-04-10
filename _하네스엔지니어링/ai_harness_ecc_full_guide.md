# AI Harness & ECC 시스템 설계 완전 정리

## 1. 전체 목표
AI를 "도구"가 아니라 **조직의 규약을 따르는 시스템**으로 만들기

---

# 2. ECC vs Toss Harness 핵심 비교

## ECC (Agent 기반 시스템)
- 중심: Agent
- 구조:
  - Agent
  - Skill
  - Hook
  - Rule
  - Security (AgentShield)
- 특징:
  - AI가 자율적으로 판단 + 실행
  - 자동화 중심
  - 보안/검증 포함

👉 한마디:
> "AI를 하나의 개발자처럼 운영"

---

## Toss Harness (팀 생산성 시스템)
- 중심: Workflow / Process
- 구조:
  - Task 흐름
  - 규칙 기반 실행
  - 자동화된 반복 작업
- 특징:
  - 팀 전체 생산성 향상
  - 표준화된 개발 프로세스
  - 협업 중심

👉 한마디:
> "팀 전체를 자동화된 공장처럼 운영"

---

# 3. 공통 핵심 개념

둘 다 결국 같은 목표:

> "AI + 시스템을 통해 팀의 규칙을 강제한다"

공통 요소:

- 규칙 (Rule)
- 자동 실행 (Automation)
- 반복 작업 제거
- 일관성 유지
- 구조 기반 개발

---

# 4. 차이 핵심 정리

| 구분 | ECC | Toss Harness |
|------|-----|-------------|
| 중심 | Agent | Workflow |
| 방식 | 자율적 | 규칙 기반 |
| 단위 | 개별 AI | 팀 프로세스 |
| 목적 | 자동 개발 | 생산성 향상 |

---

# 5. 실무에서 필요한 구조

너가 헷갈리는 핵심 포인트:

👉 "그래서 실제로 어떻게 폴더를 만들고 시작하지?"

---

# 6. 실제 프로젝트 구조 예시

## 예시 프로젝트: SQL Processor

### 전체 구조

```
project/
│
├── agents/
│   ├── parser_agent.md
│   ├── execution_agent.md
│
├── skills/
│   ├── parse_sql.md
│   ├── execute_query.md
│
├── rules/
│   ├── coding_rules.md
│   ├── sql_rules.md
│
├── hooks/
│   ├── pre_commit.md
│   ├── post_generate.md
│
├── workflows/
│   ├── feature_flow.md
│
├── src/
│   ├── parser.c
│   ├── executor.c
│
├── tests/
│
└── README.md
```

---

# 7. 각 폴더 역할

## agents/
- 역할:
  - AI 역할 정의
- 예:
  - Parser Agent
  - Execution Agent

---

## skills/
- 역할:
  - AI가 수행 가능한 기능 정의
- 예:
  - SQL 파싱
  - 쿼리 실행

---

## rules/
- 역할:
  - 강제 규칙
- 예:
  - 코드 스타일
  - SQL 문법 제한

---

## hooks/
- 역할:
  - 특정 시점 자동 실행
- 예:
  - 코드 생성 후 검사
  - 커밋 전 검사

---

## workflows/
- 역할:
  - 작업 흐름 정의
- 예:
  - feature 개발 과정

---

# 8. 실제 동작 흐름

1. 사용자 요청
2. Agent 선택
3. Skill 실행
4. Rule 검사
5. Hook 실행
6. 결과 생성

---

# 9. 핵심 깨달음 (중요)

👉 너가 지금 막히는 이유:

"AI를 어떻게 쓸지"가 아니라  
"시스템을 어떻게 설계할지" 고민해야 하기 때문

---

# 10. 결론

- ECC → AI 중심
- Toss Harness → 팀 프로세스 중심

👉 실제 정답:

> 둘을 섞어야 한다

---

# 11. 다음 단계 추천

1. 작은 프로젝트 하나 선택
2. 위 구조 그대로 폴더 생성
3. Agent 2개만 먼저 만들기
4. Skill 2개만 구현
5. Rule 1개 적용

👉 이걸로 시작하면 된다
