# 테스트 계획서 — AC-FR-01-01 (격자 형식 선행 검증)

| 항목 | 내용 |
|------|------|
| **AC ID** | `AC-FR-01-01` |
| **PRD 요구사항** | `FR-01` (4×4 격자 마방진 판정), `§9.1` (Input/Output Contract — 격자 형식 선행 검증) |
| **대표 입력** | `grid = None` |
| **대표 기대 출력** | `{ "code": "INVALID_SIZE", "message": "Grid must be 4x4." }` |
| **작성 기준일** | 2026-05-29 |
| **대상 스택** | Python 3.11+, pytest, pydantic, unittest.mock |
| **아키텍처** | ECB (Boundary → Control → Entity) |

---

## 1. 목적 및 범위

### 1.1 목적

FR-01 판정 흐름에서 **I-Shape(4×4 격자) 선행 검증**이 올바르게 동작하는지 확인한다. 형식이 유효하지 않은 입력은 Domain 해·판정 진입점에 **도달하기 전** `INVALID_SIZE`로 조기 종료되어야 한다.

### 1.2 In-Scope (AC-FR-01-01)

- 격자 형식(존재 여부, 행·열 개수) 검증 로직
- `INVALID_SIZE` 응답 코드·메시지 계약
- Boundary / Control / Entity 계층별 단위 테스트
- Domain 해 결정 진입점 **미호출** 검증 (mock/spy)

### 1.3 Out-of-Scope (본 계획서에서 제외)

| 항목 | 사유 |
|------|------|
| `grid = 4×4` 정상 입력 | AC-FR-01-01 범위 외 (후속 AC에서 다룸) |
| 값 집합 검증 (I-Set, 중복·누락) | L1 이후 불변식 |
| 선 합 검증 (I-Line-*) | L2 이후 불변식 |
| CLI/API 통합 E2E | 본 단계는 단위 테스트 우선 |
| 성능·부하 테스트 | 비기능, FR-01 형식 검증과 무관 |

---

## 2. pytest 단위 테스트 범위 및 우선순위

### 2.1 테스트 디렉터리 구조 (ECB 대칭)

```text
tests/
├── entity/
│   └── test_grid_shape_validator.py      # P1 — Domain 형식 검증
├── control/
│   └── test_judge_use_case.py            # P2 — Use-case 조기 종료
└── boundary/
    └── test_judge_handler.py             # P3 — I/O 직렬화·위임
```

> **모듈 경로 가정** (구현 시): `entity/rules/grid_shape_validator.py`, `entity/rules/magic_square_judge.py`, `control/services/judge_use_case.py`, `boundary/cli/judge_handler.py`

### 2.2 우선순위 매트릭스

| 우선순위 | 계층 | 테스트 대상 | 검증 초점 | AC 연관 |
|----------|------|-------------|-----------|---------|
| **P1** | Entity (Domain) | `validate_grid_shape(grid)` | None·빈·비정형·크기 불일치 → `INVALID_SIZE` | 직접 |
| **P2** | Control | `JudgeUseCase.execute(grid)` | 형식 실패 시 Domain judge **0회** 호출, 동일 응답 반환 | 간접 + 격리 |
| **P3** | Boundary | `JudgeHandler.handle(raw_input)` | raw → grid 변환 후 Control 위임, 실패 응답 직렬화 | I/O 계약 |

### 2.3 실행 순서 (TDD Red → Green)

1. **P1 Entity** — `test_grid_shape_validator.py` (형식 검증 최소 구현)
2. **P2 Control** — `test_judge_use_case.py` (조기 종료 + spy)
3. **P3 Boundary** — `test_judge_handler.py` (응답 포맷·위임)

### 2.4 pytest 관례

- 패턴: **AAA** (Arrange – Act – Assert)
- 함수명: `test_<동작>_<조건>_<기대결과>`
- docstring: 실패 시 의미(어떤 AC·불변식 위반인지) 기록
- fixture scope: `function` (상태 누수 방지)
- pydantic: Boundary/Control 응답 DTO(`JudgeResult`, `ErrorCode`) 스키마 검증에 사용

---

## 3. 경계값 케이스 목록

모든 케이스의 공통 기대 결과:

```json
{ "code": "INVALID_SIZE", "message": "Grid must be 4x4." }
```

Domain 해 결정 진입점(`MagicSquareJudge.judge`) 호출 횟수: **0**

| ID | 입력 | 설명 | 테스트 파일 |
|----|------|------|-------------|
| **BV-01** | `grid = None` | 명시적 None — AC-FR-01-01 대표 케이스 | entity, control, boundary |
| **BV-02** | `grid = []` | 빈 리스트 — 행 0개 | entity, control |
| **BV-03** | `grid = [[]] * 4` | 행 4개 존재, 열 0개 (각 행 길이 0) | entity, control |
| **BV-04** | `grid = [[1]*4]*3` | 3×4 — 행 부족 | entity |
| **BV-05** | `grid = [[1]*3]*4` | 4×3 — 열 부족 | entity |
| **BV-06** | `grid = [[1]*4]*4 + [[1]*4]` | 5×4 — 행 초과 | entity |
| **BV-07** | `grid = [[1]*5]*4` | 4×5 — 열 초과 | entity |
| **BV-08** | `grid = [[1]*4]*5` | 5×5 — 행·열 모두 초과 | entity |

> **포함 금지**: 4×4 정상 격자(값이 올바른/잘못된 경우 모두) — 후속 AC(FR-01-02 이후)에서 다룸.

### 3.1 Entity 계층 테스트 ID 매핑

| 테스트 ID | 케이스 | Given | When | Then |
|-----------|--------|-------|------|------|
| `UT-ENT-01` | BV-01 | `grid is None` | `validate_grid_shape(grid)` | `INVALID_SIZE`, message 일치 |
| `UT-ENT-02` | BV-02 | `grid == []` | 동일 | 동일 |
| `UT-ENT-03` | BV-03 | `grid == [[]]*4` | 동일 | 동일 |
| `UT-ENT-04` | BV-04 | 3×4 격자 | 동일 | 동일 |
| `UT-ENT-05` | BV-05 | 4×3 격자 | 동일 | 동일 |
| `UT-ENT-06` | BV-06~08 | 5×4, 4×5, 5×5 | 동일 | 동일 |

---

## 4. 예외 / 특이 케이스 목록

형식 검증 단계에서 **예외를 raise하지 않고** 구조화된 `INVALID_SIZE` 응답을 반환해야 한다 (Boundary I/O 계약).

| ID | 입력 | 특이점 | 기대 동작 |
|----|------|--------|-----------|
| **EX-01** | `grid = "not a grid"` | `str` 타입 | `INVALID_SIZE` (예외 미전파) |
| **EX-02** | `grid = 42` | 스칼라 `int` | `INVALID_SIZE` |
| **EX-03** | `grid = {"rows": 4}` | `dict` 타입 | `INVALID_SIZE` |
| **EX-04** | `grid = [[1,2,3,4], None, [5,6,7,8], [9,10,11,12]]` | 행 원소가 `None` | `INVALID_SIZE` |
| **EX-05** | `grid = [[1,2,3,4], [5,6,7], [8,9,10,11], [12,13,14,15]]` | ragged row (열 길이 불균일) | `INVALID_SIZE` |
| **EX-06** | `grid = [[[1]]*4]*4` | 3차원 중첩 | `INVALID_SIZE` |
| **EX-07** | Boundary: `raw_input = ""` (빈 문자열) | 파싱 전 I/O | `INVALID_SIZE` 또는 파싱 오류 → `INVALID_SIZE` 매핑 |
| **EX-08** | Boundary: `raw_input = "null"` (JSON null) | 역직렬화 후 `None` | BV-01과 동일 결과 |

### 4.1 pydantic 검증 케이스 (Boundary DTO)

| ID | 검증 대상 | 입력 | 기대 |
|----|-----------|------|------|
| **PD-01** | `JudgeResult` 스키마 | `{"code": "INVALID_SIZE", "message": "Grid must be 4x4."}` | 유효 |
| **PD-02** | `JudgeResult` 스키마 | `{"code": "INVALID_SIZE"}` (message 누락) | `ValidationError` |
| **PD-03** | `JudgeResult` 스키마 | `{"code": "UNKNOWN", "message": "..."}` | `ValidationError` (허용 code enum 외) |

---

## 5. Domain 해 결정 진입점 호출 횟수 검증 전략 (mock/spy)

### 5.1 대상 심볼

| 계층 | Mock/Spy 대상 | 역할 |
|------|---------------|------|
| Entity | `MagicSquareJudge.judge` | I-Set·I-Line 등 **해·판정** Domain 진입점 |
| Control | `JudgeUseCase._judge` (또는 주입된 `MagicSquareJudge`) | Use-case가 Domain judge를 위임하는 지점 |

> **형식 검증 함수** `validate_grid_shape`는 mock 대상이 **아님** — 실제 로직을 실행해야 한다.

### 5.2 Control 계층 — `unittest.mock.patch` + `Autospec`

```python
# 개념 예시 (계획서 — 구현 시 tests/control/test_judge_use_case.py)
with patch(
    "control.services.judge_use_case.MagicSquareJudge.judge",
    autospec=True,
) as mock_judge:
    result = use_case.execute(grid=None)
    mock_judge.assert_not_called()
    assert result.code == "INVALID_SIZE"
```

**검증 규칙**

| 조건 | `MagicSquareJudge.judge` 호출 횟수 |
|------|--------------------------------------|
| BV-01 ~ BV-08, EX-01 ~ EX-06 | **0** |
| 4×4 정상 격자 (Out-of-Scope) | ≥ 1 (본 계획서에서 테스트 작성 금지) |

### 5.3 Boundary 계층 — spy on Control

Boundary 테스트에서는 Domain judge가 아닌 **Control Use-case**를 spy한다.

```python
with patch.object(handler, "_use_case") as mock_use_case:
    mock_use_case.execute.return_value = JudgeResult(
        code="INVALID_SIZE",
        message="Grid must be 4x4.",
    )
    response = handler.handle(None)
    mock_use_case.execute.assert_called_once_with(None)
```

- Boundary는 Domain judge를 **직접 import하지 않음** (ECB 의존 방향 준수).
- Boundary 테스트의 격리 목표: I/O 변환·응답 직렬화만 검증, Domain judge 미참조 확인 (`grep`/import lint).

### 5.4 Entity 계층 — judge 미호출 자명성

Entity 단위 테스트에서는 `validate_grid_shape`만 호출하므로 judge mock **불필요**.  
Control 통합 단위 테스트(P2)에서 **0회 호출** assertion이 Entity–Control 경계 격리의 근거가 된다.

### 5.5 실패 시 진단

| spy assertion 실패 | 의미 |
|--------------------|------|
| `assert_not_called()` 실패 | 형식 검증 우회 — Domain judge가 None/빈 격자에 도달 (버그) |
| `assert_called_once()` 실패 (Boundary) | I/O 핸들러가 Control을 중복·미호출 |

---

## 6. 커버리지 목표

| 계층 | 패키지 | 목표 | 근거 |
|------|--------|------|------|
| **Domain (Entity)** | `entity/rules/` | **≥ 95%** | 형식 검증은 분기 적으나 FR-01 핵심 불변(I-Shape) — 누락 시 전체 판정 오염 |
| **Boundary** | `boundary/` | **≥ 85%** | I/O 변형·직렬화 경로 다양; 일부 방어 코드는 통합 단계에서 보완 |
| **Control** | `control/` | **≥ 90%** | 조기 종료 분기·spy 대상 경로 포함 (Entity–Boundary 간 조율) |
| **전체** | `src/` | **≥ 80%** | `.cursorrules` 프로젝트 최소 기준 |

> AC-FR-01-01 범위 구현 완료 시 Entity `grid_shape_validator` 모듈은 **100%** branch coverage를 목표로 한다.

---

## 7. pytest-cov 측정 전략

### 7.1 설치

```bash
pip install pytest-cov
```

### 7.2 AC-FR-01-01 범위 실행 (전체 리포트)

```bash
pytest --cov=src --cov-report=term-missing
```

### 7.3 계층별 측정 (권장)

```bash
# Domain (Entity) — 95%+ 게이트
pytest tests/entity/ --cov=src/entity --cov-report=term-missing --cov-fail-under=95

# Boundary — 85%+ 게이트
pytest tests/boundary/ --cov=src/boundary --cov-report=term-missing --cov-fail-under=85

# Control — 90%+ 게이트
pytest tests/control/ --cov=src/control --cov-report=term-missing --cov-fail-under=90
```

### 7.4 AC-FR-01-01 전용 마커 실행

테스트에 `@pytest.mark.ac_fr_01_01` 마커를 부여한 경우:

```bash
pytest -m ac_fr_01_01 --cov=src --cov-report=term-missing
```

### 7.5 커버리지 해석 가이드

| `--cov-report=term-missing` 출력 | 조치 |
|----------------------------------|------|
| `grid_shape_validator.py` 미커버 분기 | BV/EX 케이스 추가 |
| `judge_use_case.py` judge 호출 경로 커버 | Out-of-Scope — 본 AC 테스트 추가 금지 |
| `boundary/` parser except 블록 미커버 | EX-07, EX-08 케이스 추가 |

### 7.6 CI 게이트 (권장)

```bash
pytest \
  --cov=src \
  --cov-report=term-missing \
  --cov-report=xml \
  --cov-fail-under=80
```

Entity·Boundary 계층별 `--cov-fail-under`는 별도 job 또는 `pyproject.toml` `[tool.coverage.report]` `fail_under`로 분리 설정한다.

---

## 8. 테스트 데이터 및 Fixture

| Fixture | 제공 값 | 사용 계층 |
|---------|---------|------------|
| `invalid_size_none` | `None` | 전 계층 |
| `invalid_size_empty` | `[]` | entity, control |
| `invalid_size_zero_cols` | `[[]] * 4` | entity, control |
| `invalid_size_3x4` | `[[0]*4]*3` | entity |
| `invalid_size_4x3` | `[[0]*3]*4` | entity |
| `invalid_size_5x5` | `[[0]*4]*5` | entity |
| `expected_invalid_size_result` | `JudgeResult(code="INVALID_SIZE", message="Grid must be 4x4.")` | assert 공통화 |

---

## 9. 완료 기준 (Definition of Done)

- [ ] BV-01 ~ BV-08 Entity 테스트 GREEN
- [ ] EX-01 ~ EX-08 예외/특이 케이스 GREEN (구조화 응답, 예외 미전파)
- [ ] Control 계층: 모든 In-Scope 케이스에서 `MagicSquareJudge.judge` **0회** spy 통과
- [ ] Boundary 계층: `INVALID_SIZE` JSON/DTO 직렬화 및 Control 위임 검증
- [ ] 4×4 정상 입력 테스트 **미포함** 확인 (코드 리뷰 체크리스트)
- [ ] Entity coverage ≥ 95%, Boundary coverage ≥ 85%
- [ ] `pytest --cov=src --cov-report=term-missing` 실행 결과 아카이브

---

## 10. 리스크 및 완화

| 리스크 | 영향 | 완화 |
|--------|------|------|
| `[[]]*4` 가변 행 공유 | BV-03 오판 | 테스트에서 `assert all(len(row)==0 for row in grid)` 선행 확인 |
| Boundary가 Domain judge 직접 호출 | ECB 위반, spy 무의미 | import lint + P3 테스트에서 Control만 patch |
| pydantic message 필드 누락 | API 계약 깨짐 | PD-01~03 스키마 테스트 |
| `src/` 패키지 미존재 | cov 0% | 구현 착수 시 ECB 디렉터리를 `src/` 하위로 배치 |

---

## 11. 참조 문서

- `Report/2026-05-28-01_Problem-Definition-Report.md` — L0 형식, I-Shape, 불변식 의존 관계
- `Report/2026-05-29-01_PRD-Reference-Document-Analysis-Report.md` — §9 I/O Contract, ECB 매핑
- `.cursorrules` — pytest AAA, coverage 80%, ECB 의존 방향

---

*본 문서는 AC-FR-01-01 범위의 테스트 계획서이며, 구현 코드·테스트 코드를 포함하지 않는다.*
