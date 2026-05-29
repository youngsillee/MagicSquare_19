# MagicSquare_xx

4×4 마방진(Magic Square)을 다루는 프로그램 프로젝트입니다.  
값 **1~16**을 격자에 한 번씩 배치하고, **합의된 규칙**에 따라 배치를 판정·반복·비교할 수 있게 하는 것이 목표입니다.

**Dual-Track TDD** — Judge 트랙(AC-FR-01-01 `INVALID_SIZE`)과 Solve 트랙(부분 격자 채우기·E002~E006)을 분리합니다.  
회귀: `pytest tests/` **81 passed** (Golden Master GM-1 matched 포함).

| 트랙 | 범위 | 상태 |
|------|------|------|
| **Judge** | `grid_shape_validator` → `JudgeUseCase` → `JudgeHandler` / GUI 판정 | AC-FR-01-01 GREEN |
| **Solve** | `InputValidator` → `UIBoundary` → `SolvePartialMagicSquare` → `TwoCellSolver` | GREEN + GM baseline |
| **REFACTOR** | 구조·DRY·SSOT (기능·출력 계약 불변) | Wave 1 일부 선행 완료, 프로그램 진행 예정 |

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
| AC-FR-01-01 (INVALID_SIZE) | RED·GREEN 완료 (`-m ac_fr_01_01` 50건 + scope 10건) |
| Solve 트랙 (U-IN·U-OUT·U-FLOW·D-SOL) | GREEN + GM-1 matched |
| Golden Master (GM-1~GM-10) | baseline 고정 · approve 패턴 |
| REFACTOR 프로그램 | G-01·G-02 충족 · G-03~G-05·커버리지 80%는 후속 |
| AC-FR-01-02+ (`MagicSquareJudge.resolve`) | 의도적 `NotImplementedError` 스텁 |
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

## Solve 트랙 계약 (요약)

입력·출력·오류는 [Report/02 Dual-Track RED 설계](./Report/02.MagicSquare_DualTrack_TDD_Design_Report.md) 및 [docs/golden_master_design.md](./docs/golden_master_design.md)와 정합합니다.

| 항목 | 규칙 |
|------|------|
| 입력 | 4×4 `int[][]`, `0`=빈칸(정확히 2개), 값 `0` 또는 `1~16`, 0 제외 중복 금지 |
| 출력 | `int[6]` = `[r1,c1,n1,r2,c2,n2]`, 좌표 **1-index**, row-major 첫 빈칸 기준 |
| 솔버 | Step A: 작은 누락 수→첫 빈칸 · 큰 수→둘째 빈칸; 실패 시 Step B(reverse) |
| 오류 | `FailureResponse` envelope — `INVALID_SIZE`, `E002`~`E005`, `E006`(해 없음) |
| SSOT | 성공 벡터는 `SolutionResult.values` (`TwoCellSolver` 배치 결과) |

격자 fixture SSOT: `tests/solve_grids.py` (G0~G3). Golden Master 기대값:

| 시나리오 | 기대 |
|----------|------|
| `reverse_success` (G1) | `[2,2,10,3,3,7]` |
| `normal_success` (G2) | `[3,3,6,4,4,1]` |
| `invalid_blank_count` | `E002` |
| `duplicate_number` | `E005` |
| `no_valid_solution` | `E006` |

> 이전 GM 스냅샷(`[2,2,7,3,3,10]` 등)은 Control이 솔버 결과를 무시하던 시기의 값입니다. 수정 후 `python scripts/generate_golden_master.py --approve`로 갱신되었습니다.

---

## 저장소 구조

```text
MagicSquare_xx/
├── README.md
├── docs/test_plan.md              ← AC-FR-01-01 테스트 계획서
├── docs/golden_master_design.md   ← GM-1 설계 SSOT
├── entity/                        ← Domain (models, rules, services)
├── control/                       ← Judge + Solve use cases
├── boundary/                      ← Validator, UIBoundary, CLI, PyQt
│   ├── validation_result.py       ← ValidationOk / FailureResponse
│   ├── input_validator.py
│   ├── ui_boundary.py
│   ├── cli/
│   └── screen/
├── tests/                         ← pytest (markers: ac_fr_01_01, solve_track)
├── scripts/generate_golden_master.py
├── Report/
└── Prompt/
```

### Report

종합 보고서와 세션 요약.

| 문서 | 설명 |
|------|------|
| [Report/2026-05-28-01_Problem-Definition-Report.md](./Report/2026-05-28-01_Problem-Definition-Report.md) | STEP 1~5, Why 체인, Invariant, 미결정, 리스크 |
| [Report/02.MagicSquare_DualTrack_TDD_Design_Report.md](./Report/02.MagicSquare_DualTrack_TDD_Design_Report.md) | Dual-Track RED 설계 (U-IN / U-OUT / D-SOL) |
| [Report/2026-05-29-07_Golden-Master-CodeReview-Session-Report.md](./Report/2026-05-29-07_Golden-Master-CodeReview-Session-Report.md) | GM-1 · 코드리뷰 · REFACTOR 준비 |
| [Report/README.md](./Report/README.md) | Report 폴더 안내 · AC-FR-01-01 GREEN 가이드 |

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

> **참고:** GUI 「판정」 버튼은 **Judge 트랙 앵커**입니다 — `grid=None` 등 형식 검증(INVALID_SIZE)만 확인합니다. 유효한 4×4 격자에서 「판정」을 누르면 값·선 판정 미구현 안내가 표시됩니다 (AC-FR-01-02 이후). Solve(채우기) 계약은 Golden Master·`UIBoundary.solve`·`-m solve_track` 테스트로 검증합니다.

---

## 테스트 실행

```powershell
cd c:\DEV\MagicSquare_xx
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 전체 회귀 (81건)
python -m pytest tests/ -v

# Judge 트랙만 (AC-FR-01-01)
python -m pytest tests/ -m ac_fr_01_01 -v

# Solve 트랙만 (U-IN, U-OUT, U-FLOW, D-SOL, domain services)
python -m pytest tests/ -m solve_track -v

# Golden Master
python -m pytest tests/test_gm_01_magic_square_golden_master.py -v
python scripts/generate_golden_master.py --check

# baseline 갱신 (의도적 출력 변경 시만)
python scripts/generate_golden_master.py --approve
# 또는
python -m pytest tests/test_gm_01_magic_square_golden_master.py --approve-golden -v

# 커버리지 (entity + control + boundary)
python -m pytest tests/ --cov=entity --cov=control --cov=boundary --cov-report=term-missing
```

| 마커 | 용도 |
|------|------|
| `ac_fr_01_01` | INVALID_SIZE 선행 검증 (Judge) |
| `solve_track` | Solve Boundary/Control/Entity 계약 |

---

## REFACTOR 프로그램 (진입 게이트)

구조 개선만 수행합니다. 기능 추가·계약 변경·GM 임의 수정은 금지합니다.

| 게이트 | 기준 | 현재 (`MagicSquare_xx`) |
|--------|------|-------------------------|
| G-01 | `pytest tests/` 전체 GREEN | **81 passed** |
| G-02 | GM-1 matched | **PASS** |
| G-03 | U-FLOW-02(6), U-OUT-02~03, U-IN-06~08 | U-OUT·U-IN-01~05·U-FLOW(2건) GREEN · 06~08·6케이스 **미작성** |
| G-04 | D-SOL-03, SC-CTL-002~004 | D-SOL-01~04 GREEN · SC-CTL ID **미도입** |
| G-05 | `tests/boundary/test_main_window.py` | **없음** (`test_screen_app.py` Judge 앵커만) |

**이미 반영된 Wave 1 항목 (재작업 불필요):** `ValidationOk`/`ValidationResult`(RF-01), `UIBoundary` E006 매핑(RF-02), `resolve()` → `SolutionResult.values`(RF-03), Control locate/find 중복 제거(RF-04).

**다음 REFACTOR 후보:** `ErrorMapper` 추출(C2), `_failure()` extract(C5), Screen `ResultPresenter`·`test_main_window`(C6~C8), Entity R-L*(Wave 3).

매 커밋 후 `pytest tests/` + GM `--check` 필수. diff 시 버그면 롤백, SSOT 통일이면 Report 근거 후 `--approve-golden`만 허용.

---

## RED / GREEN To-Do 리스트

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

### Solve 트랙 — Boundary / Control / Entity

- [x] U-IN-01~05: `tests/boundary/test_input_validator.py`
- [x] U-OUT-01~03: `tests/boundary/test_ui_boundary.py` (E006 envelope)
- [x] U-FLOW-02: `tests/boundary/test_ui_boundary_flow.py` (None, `[]` — 2건)
- [x] D-SOL-01~04: `tests/control/test_solve_partial_magic_square.py`
- [x] D-LOC-01, D-MIS-01: `tests/entity/test_domain_services.py`
- [ ] U-FLOW-02 확장 (6케이스) · U-IN-06~08 (1004 SSOT 이식 시)
- [ ] `tests/boundary/test_main_window.py` (Screen REFACTOR 선행)

### Track A — Judge / Boundary (AC-FR-01-01)
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

`python -m pytest tests/ --cov=entity --cov=control --cov=boundary`

| 범위 | 목표 | 현재 (참고) |
|------|------|-------------|
| `entity/rules/` | 95%+ | ~91% (`magic_square_judge.resolve` 스텁 미실행) |
| Boundary | 85%+ | Judge 경로 높음 · Solve 모듈 포함 시 변동 |
| entity+control+boundary TOTAL | 90%+ | ~78% (Solve·domain services 테스트 반영) |
| `.cursorrules` 최소 | 80%+ | REFACTOR Wave 완료 시 재측정 |

### 결함 목록 연결

- [x] [defect_list.md](./defect_list.md) — DEF-001~003 Critical 해결
- [x] 회귀 `pytest tests/` **81 passed**
- [ ] DEF-004~006 — Judge `resolve()`·커버리지 게이트 (AC-FR-01-02+)

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
| 2026-05-29 | Solve 트랙 GREEN, C-1/C-2 수정, `solve_track` 마커, REFACTOR 게이트·실행 가이드 |
