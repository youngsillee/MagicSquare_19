# 결함 목록 (Defect List)

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_xx |
| **기준 AC** | AC-FR-01-01 (FR-01, PRD §8.1 `INVALID_SIZE`) |
| **작성일** | 2026-05-29 |
| **최종 회귀** | `pytest tests/` — **81 passed** (2026-05-29) |
| **관련 문서** | [docs/test_plan.md](./docs/test_plan.md) |

---

## 요약

| 구분 | 건수 |
|------|------|
| **Critical (기능)** | 3건 — **수정 완료** |
| **Medium / Low (품질·범위)** | 3건 — **미해결 (후속 AC·REFACTOR)** |
| **합계** | 6건 |

RED 단계에서 pytest 수집 시 **구현 모듈 부재**로 3건의 Critical 결함이 확인되었고, GREEN 최소 구현 후 **기능 결함은 모두 해소**되었습니다. 커버리지·`resolve()` 스텁 관련 항목은 AC-FR-01-01 범위 밖 동작으로 **열린 결함**으로 관리합니다.

---

## 결함 상세

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-------|-----------|--------|--------|-----------|-----------|
| DEF-001 | Critical | AC-FR-01-01 | 가상환경에서 `python -m pytest tests/entity/test_grid_shape_validator.py` 실행 | 테스트 수집·실행 성공; `grid=None` 시 `code="INVALID_SIZE"` | `ModuleNotFoundError: No module named 'entity.models.judge_result'` (수집 단계 ERROR) | Entity DTO·형식 검증 모듈 미구현 | `entity/models/judge_result.py`, `entity/rules/grid_shape_validator.py` 추가 — **해결됨** |
| DEF-002 | Critical | AC-FR-01-01 | `python -m pytest tests/control/test_judge_use_case.py` 실행 | `grid=None` 시 `INVALID_SIZE` 반환; `resolve()` 0회 호출 | `ModuleNotFoundError: No module named 'control.services'` (수집 단계 ERROR) | Control Use-case 레이어 미구현 | `control/services/judge_use_case.py` 추가; 형식 실패 시 `resolve()` 미호출 — **해결됨** |
| DEF-003 | Critical | AC-FR-01-01 | `python -m pytest tests/boundary/test_judge_handler.py` 실행 | Boundary가 `INVALID_SIZE` 구조화 응답 반환 | `ModuleNotFoundError: No module named 'boundary.cli'` (수집 단계 ERROR) | Boundary I/O 레이어 미구현 | `boundary/cli/judge_handler.py` 추가; Control 위임 — **해결됨** |
| DEF-004 | Medium | AC-FR-01-01 | `python -m pytest tests/ -m ac_fr_01_01 --cov=entity/rules --cov-report=term-missing` | Domain Logic(`entity/rules/`) 커버리지 **≥ 95%** | **~91%** (`grid_shape_validator` 유효 격자 분기 추가; `magic_square_judge.resolve` 본문 미실행) | `resolve()`는 AC-FR-01-02+ 범위 | AC-FR-01-02+에서 `resolve()` 구현 시 커버리지 충족 예정 — **부분 개선** |
| DEF-005 | Low | AC-FR-01-01 | 형식 검증 통과 4×4 격자로 `JudgeUseCase.execute(grid)` 호출 | `JudgeResult` 판정 결과 반환 | `NotImplementedError` (`MagicSquareJudge.resolve`) | `resolve()`는 AC-FR-01-01 범위 밖(값·선 합 검증) 의도적 스텁 | AC-FR-01-02+에서 `resolve()` 구현 — **미해결 (예정)** |
| DEF-006 | Low | AC-FR-01-01 | `python -m pytest tests/ --cov=entity --cov=control --cov=boundary` | 전체 TOTAL 커버리지 **≥ 90%** | **~78%** (81 passed; Solve·Entity 서비스 테스트 추가) | `user.py`·GUI·`magic_square_judge.resolve` 스텁 등 | Solve 트랙 GREEN 후 점진 확대 — **부분 개선** |

---

## 재현 로그 참고 (DEF-001~003, RED 단계)

```text
ERROR collecting tests/entity/test_grid_shape_validator.py
  ModuleNotFoundError: No module named 'entity.models.judge_result'

ERROR collecting tests/control/test_judge_use_case.py
  ModuleNotFoundError: No module named 'control.services'

ERROR collecting tests/boundary/test_judge_handler.py
  ModuleNotFoundError: No module named 'boundary.cli'

!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!
```

GREEN 구현 후 동일 명령: **50 passed** (`-m ac_fr_01_01`), 전체 **53 passed**.

---

## 회귀 테스트

| 명령 | 결과 |
|------|------|
| `python -m pytest tests/ -m ac_fr_01_01` | 50 passed |
| `python -m pytest tests/` | 81 passed |

**Critical 결함(DEF-001~003)** 에 대한 회귀는 통과합니다. **DEF-004~006** 은 품질·범위 이슈로 별도 마일스톤에서 해소합니다.

---

## 문서 이력

| 버전 | 일자 | 내용 |
|------|------|------|
| 1.0 | 2026-05-29 | AC-FR-01-01 RED/GREEN 세션 결함 최초 등록 |
