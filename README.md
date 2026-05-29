# MagicSquare_xx

4×4 마방진(Magic Square)을 다루는 프로그램 프로젝트입니다.  
값 **1~16**을 격자에 한 번씩 배치하고, **합의된 규칙**에 따라 배치를 판정·반복·비교할 수 있게 하는 것이 목표입니다.

**AC-FR-01-01**(격자 형식 선행 검증) RED·GREEN 완료. ECB(entity / control / boundary) 최소 구현 및 pytest 50건 통과.

---

## 프로젝트가 다루는 문제

### 표면 정의 (피해야 할 표현)

> 4×4 칸에 1~16을 넣어 행·열·대각 합이 같은 마방진을 **완성하는 프로그램**

### 진짜 문제 (본 프로젝트의 기준)

> **4×4 격자 배치**가 사전에 합의한 마방진 규칙(값 집합·선 집합·마방 상수)을 **모두** 만족하는지 **판정**하고, 필요 시 같은 규칙으로 **반복·확보·비교**할 수 있도록, 판정 기준을 **명시적·재현 가능**하게 다루는 문제.

| 요소 | 내용 |
|------|------|
| 격자 | 4×4 |
| 값 | 1~16, 각각 정확히 한 번 |
| 마방 상수 | 34 |
| 핵심 활동 | 판정 → (선택) 반복 적용 → (선택) 확보·비교 |

난이도의 중심은 “16칸 채우기”가 아니라 **“무엇을 마방진이라 부를지”** 를 명확히 하는 것입니다.

---

## 현재 상태

| 항목 | 상태 |
|------|------|
| 문제 정의 (STEP 1~5) | 완료 |
| Why 체인 (완성 · 프로그램 · TDD) | 정리 완료 |
| AC-FR-01-01 (INVALID_SIZE) | RED·GREEN 완료 (50 tests) |
| 구현 / 테스트 (전체) | 진행 중 |
| 미결정 (STEP 6) | 선 집합, 활동 범위, 동치 정책, 성공 증거 |

---

## 핵심 불변 조건 (Invariant)

판정·비교 시 깨지면 “마방진”이라 말할 수 없는 조건입니다.

**구조**

- **I-Shape** — 4×4 격자  
- **I-Cell** — 칸마다 값 하나  
- **I-Range** — 모든 값 ∈ [1, 16]  
- **I-Set** — {1, …, 16}과 정확히 일치 (중복·누락 없음)

**수치** (선 집합은 STEP 6에서 확정)

- **I-Constant** — 공통 합 = 34  
- **I-Line-Row / Col / Diag** — 명세된 각 선의 합 = 34  

**운용**

- **I-Judge-Complete** — 수용 = 위 불변을 **동시에** 만족  
- **I-Judge-Repeat** — 동일 배치·규칙 → 동일 판정  
- **I-Separation** — 판정 통과 ≠ 새 배치를 만든 것  
- **I-Equivalence** — 동치 해 처리 방식 고정 (해 비교 시)

---

## 훈련·설계 원칙

이 프로젝트에서 우선하는 사고 방식입니다.

1. **규칙 층위화** — 집합 / 선 / 수용 규칙 분리  
2. **판정 우선** — 만들기보다 “옳다고 부를 조건” 먼저  
3. **명세적 사고** — 모호한 “완성·맞다”를 검사 가능 조건으로  
4. **불변식·경계·재현** — 책임 분리, 같은 입력 → 같은 판정  

구현 단계에서는 **검증 → 집합 → 선 합 → 생성/탐색** 순으로 진행하는 것을 권장합니다(TDD·Why #3 정리).

---

## 저장소 구조

```text
MagicSquare_xx/
├── README.md
├── docs/test_plan.md         ← AC-FR-01-01 테스트 계획서
├── entity/                   ← Domain (models, rules)
├── control/                  ← Use-case orchestration
├── boundary/                 ← I/O adapters (CLI, PyQt screen)
│   ├── cli/
│   └── screen/               ← GUI (PyQt6)
├── tests/                    ← pytest (entity / control / boundary)
├── Report/
└── Prompt/
```

### Report

종합 보고서와 세션 요약.

| 문서 | 설명 |
|------|------|
| [Report/2026-05-28-01_Problem-Definition-Report.md](./Report/2026-05-28-01_Problem-Definition-Report.md) | STEP 1~5, Why 체인, Invariant, 미결정, 리스크 |
| [Report/README.md](./Report/README.md) | Report 폴더 안내 |

### Prompting

AI 세션 재현·이어하기용 프롬프트·트랜스크립트.

| 문서 | 설명 |
|------|------|
| [Prompting/2026-05-28-01_Problem-Definition-Prompt.md](./Prompting/2026-05-28-01_Problem-Definition-Prompt.md) | Cursor Export 전체 대화 (STEP 1~5) |
| [Prompting/4x4-magic-square-session-summary.md](./Prompting/4x4-magic-square-session-summary.md) | 짧은 요약 (새 채팅 컨텍스트용) |
| [Prompting/4x4-magic-square-prompts-chain.md](./Prompting/4x4-magic-square-prompts-chain.md) | User 프롬프트만 (STEP별 복사) |
| [Prompting/4x4-magic-square-problem-definition-interactive.md](./Prompting/4x4-magic-square-problem-definition-interactive.md) | 대화형 트랜스크립트 + STEP 6 템플릿 |
| [Prompting/README.md](./Prompting/README.md) | Prompting 폴더 안내 |

---

## 문제 정의 진행 (STEP 요약)

| STEP | 주제 | 결과 한 줄 |
|------|------|------------|
| 1 | Observation | 제약 만족 4×4 배치를 다루는 상황 |
| 2 | Why #1 | 올바른 배치가 있어야 검증·비교 가능 — “완성” 정의는 열림 |
| 3 | Why #2 | 반복·자동 판정·규칙 명시를 위해 절차(프로그램) 사용 |
| 4 | Why #3 | TDD로 판정·불변·입출력 계약을 먼저 고정 |
| 5 | 진짜 문제 정의 | 판정·재현·불변 중심 정의 확정 |
| **6** | *(예정)* | 선 집합·활동 범위·동치·성공 증거 **결정** |

STEP 6을 이어가려면 `Prompting/4x4-magic-square-problem-definition-interactive.md` 하단 **Continuation** 블록을 사용하거나, `session-summary`를 컨텍스트로 붙인 뒤 STEP 6 프롬프트를 실행하세요.

---

## 다음 단계 (구현 전)

1. **선 집합** — 행·열만 / 주대각 / 부대각 포함 여부  
2. **활동 범위** — 판정만 / 해 확보 / 해 비교·개수  
3. **동치 정책** — 회전·반사 등 동치 해 처리  
4. **성공 증거** — 어떤 Invariant 통과를 “완료”로 볼지  

위 네 가지를 닫은 뒤 테스트 명세·구현 범위를 정하는 것을 권장합니다.

---

## GUI 실행 (AC-FR-01-01 GREEN 확인)

PyQt6 화면은 루트 ECB의 `JudgeHandler`에 연결되어 있습니다.

```powershell
cd c:\DEV\MagicSquare_xx

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-gui.txt

# 창 띄우기 (4×4 격자 + 「판정」 버튼)
python -m boundary.screen.app

# CLI로 grid=None 앵커 검증 (AC-FR-01-01)
python -m boundary.screen.app --verify
```

`--verify` 예상 출력:

```text
code=INVALID_SIZE
message=Grid must be 4x4.
```

> **참고:** 현재 GREEN 범위는 격자 **형식 검증**(INVALID_SIZE)까지입니다. 유효한 4×4 격자에서 「판정」을 누르면 값·선 판정 미구현 안내가 표시됩니다 (AC-FR-01-02 이후).

---

## RED 단계 To-Do 리스트

> 이 체크리스트는 [docs/test_plan.md](./docs/test_plan.md) 기반으로 생성되었습니다.
> RED(실패 테스트 작성) 및 GREEN(최소 구현) 완료 시 체크합니다.

### Golden Master 회귀 안전장치

Refactoring 시작 전 구축. GREEN 완료 후 즉시 적용.

**기준 파일 생성**

- [x] GM-01: `golden_master_expected.txt` 생성
- [x] GM-02: 정상/역순/오류 시나리오 추가
- [x] GM-03: `git add tests/golden_master_expected.txt`

**테스트 코드**

- [x] GM-04: `test_golden_master_magic_square` 작성 (`tests/test_gm_01_magic_square_golden_master.py`)
- [x] GM-05: approve 패턴 적용
- [x] GM-06: Golden Master 테스트 PASS 확인

**회귀 보호**

- [x] GM-07: row-major 규칙 보호
- [x] GM-08: 1-index 출력 보호
- [x] GM-09: reverse 조합 fallback 보호
- [x] GM-10: Error Contract 보호

실행 참조: [docs/golden_master_design.md](./docs/golden_master_design.md)

```powershell
pytest tests/test_gm_01_magic_square_golden_master.py -v
python scripts/generate_golden_master.py --check
```

### Track A — UI / Boundary 테스트
- [x] TC-A-01: grid=None 입력 → 실패 결과 반환 (Happy Path of Failure)
- [x] TC-A-02: code가 정확히 "INVALID_SIZE" 문자열인지 검증
- [x] TC-A-03: message가 "Grid must be 4x4." 와 문자 단위 동일한지 검증
- [x] TC-A-04: grid=None 시 Domain 진입점 0회 호출 (mock/spy 검증)
- [x] TC-A-05: grid=[] 빈 리스트 → 실패 결과 반환
- [x] TC-A-06: grid=3×4 크기 불일치 → 실패 결과 반환
- [x] TC-A-07: 반환 객체 타입이 지정 실패 결과 구조체인지 검증

### Track B — Domain / Logic 테스트
- [x] TC-B-01: resolve()가 None grid를 직접 받지 않음을 격리 검증
- [x] TC-B-02: Boundary가 None 분기를 처리 후 resolve() 미호출 확인
- [x] TC-B-03: resolve() mock이 호출됐을 경우 테스트 실패 처리
- [x] TC-B-04: AC-FR-01-02~05 범위의 케이스는 이 커밋에 포함하지 않음 확인

### 커버리지 목표
- [ ] Domain Logic (`entity/rules/`): 95%+ — 현재 ~82% (`resolve()`·유효 4×4 분기 미실행)
- [x] Boundary Layer: 85%+ — 현재 100%
- [ ] 전체 TOTAL: 90%+ — 현재 89% (전체 tests/ 기준)

### 결함 목록 연결
- [x] [defect_list.md](./defect_list.md) 생성 및 발견 결함 기록
- [x] Critical 결함 수정 후 회귀 테스트 통과 확인 (`pytest tests/` 53 passed)
- [ ] DEF-004~006 품질·범위 결함 해소 (커버리지 95%/90%, `resolve()` 구현)

---

## 라이선스 / 기여

*(미정 — 필요 시 추가)*

---

## 문서 이력

| 일자 | 내용 |
|------|------|
| 2026-05-28 | 문제 정의 STEP 1~5, `Prompting/`·`Report/` 작성 |
| 2026-05-28 | 루트 `README.md` 추가 |
| 2026-05-29 | AC-FR-01-01 RED·GREEN, `docs/test_plan.md`, ECB 최소 구현 |
| 2026-05-29 | GM-1~GM-10 Golden Master 회귀 안전장치, `docs/golden_master_design.md` |
