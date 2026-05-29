# Report

4×4 Magic Square (`MagicSquare_xx`) 프로젝트 작업 보고서 보관 폴더입니다.

---

## 보고서 목록

| 보고서 | 설명 |
|--------|------|
| [2026-05-28-01_Problem-Definition-Report.md](./2026-05-28-01_Problem-Definition-Report.md) | 문제 정의 세션(STEP 1~5) 및 Prompting Export 종합 보고서 |
| [2026-05-29-01_PRD-Reference-Document-Analysis-Report.md](./2026-05-29-01_PRD-Reference-Document-Analysis-Report.md) | PRD 작성 전 참고 문서 분석 및 섹션 매핑 종합 보고서 |
| [2026-05-29-01_Prompt-Execution-Report.md](./2026-05-29-01_Prompt-Execution-Report.md) | PRD 분석 세션 작업 실행 요약 |
| [2026-05-29-02_GitHub-Upload-Session-Report.md](./2026-05-29-02_GitHub-Upload-Session-Report.md) | GitHub 업로드 세션 종합 보고서 (커밋·브랜치·푸시 결과) |
| [2026-05-29-02_Prompt-Execution-Report.md](./2026-05-29-02_Prompt-Execution-Report.md) | GitHub 업로드·Export 세션 작업 실행 요약 |
| [2026-05-29-03_AC-FR-01-01-TDD-Session-Report.md](./2026-05-29-03_AC-FR-01-01-TDD-Session-Report.md) | AC-FR-01-01 TDD 세션 종합 (테스트 계획·RED·GREEN·결함) |
| [2026-05-29-03_Prompt-Execution-Report.md](./2026-05-29-03_Prompt-Execution-Report.md) | AC-FR-01-01 세션 Export 작업 실행 요약 |
| [02.MagicSquare_DualTrack_TDD_Design_Report.md](./02.MagicSquare_DualTrack_TDD_Design_Report.md) | FR-01~FR-05 Dual-Track RED 설계표 (Track A/B, G0~G3) |
| [2026-05-29-04_DualTrack-RED-Design-Session-Report.md](./2026-05-29-04_DualTrack-RED-Design-Session-Report.md) | Dual-Track RED 설계 세션 종합 |
| [2026-05-29-04_Prompt-Execution-Report.md](./2026-05-29-04_Prompt-Execution-Report.md) | Dual-Track RED Export 작업 실행 요약 |
| [2026-05-29-05_GREEN-BV-GitHub-Session-Report.md](./2026-05-29-05_GREEN-BV-GitHub-Session-Report.md) | GitHub develop 업로드·GREEN 앵커·BV To-Do 세션 종합 |
| [2026-05-29-05_Prompt-Execution-Report.md](./2026-05-29-05_Prompt-Execution-Report.md) | GREEN·BV·GitHub·Export 세션 작업 실행 요약 |

---

## AC-FR-01-01 GREEN 진행 가이드

> SSOT: [docs/test_plan.md](../docs/test_plan.md) · 루트 [README.md](../README.md) RED/GREEN 체크리스트  
> 대표 계약: `grid = None` → `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }` · Domain `resolve()` **0회**

### 테스트 규모

| 구분 | 건수 | GREEN |
|------|------|-------|
| Entity / Control / Boundary (`-m ac_fr_01_01`) | 40 | 최소 구현 필요 |
| Scope 가드 (`test_ac_fr_01_01_scope.py`) | 10 | **불필요** (RED·메타 검증만) |
| **합계** | **50** | |

### BV 교차 레이어 커밋 순서 (건수 오름차순)

동일 입력(BV)으로 Entity → Control → Boundary를 한 커밋에 묶어 GREEN 진행.

| 순서 | BV | 입력 | 테스트 수 | 레이어 |
|------|-----|------|-----------|--------|
| 1 | BV-05 | 4×3 | 1 | Entity |
| 2 | BV-08 | 5×5 | 1 | Entity |
| 3 | BV-03 | `[[]] * 4` | 4 | Entity + Control + Boundary |
| 4 | BV-02 | `[]` | 7 | Entity + Control + Boundary |
| 5 | BV-04 | 3×4 | 7 | Entity + Control + Boundary |
| 6 | BV-01 | `None` | 20 | Entity + Control + Boundary (AC 앵커) |

### GREEN To-Do — BV-05 · 4×3 (1건)

- [ ] Entity `test_4x3_grid_returns_invalid_size_code` — `INVALID_SIZE` code
- [ ] GREEN: `validate_grid_shape` 열 개수 ≠ 4 분기

### GREEN To-Do — BV-08 · 5×5 (1건)

- [ ] Entity `test_5x5_grid_returns_invalid_size_code` — `INVALID_SIZE` code
- [ ] GREEN: 행·열 모두 4 초과 분기

### GREEN To-Do — BV-03 · `[[]] * 4` (4건)

- [ ] Entity `test_zero_column_rows_returns_invalid_size_code`
- [ ] Entity `test_message_and_code_pair_consistency`
- [ ] Control `test_zero_column_grid_resolve_zero_calls`
- [ ] Boundary `test_zero_cols_resolve_zero_calls_boundary`

### GREEN To-Do — BV-02 · `[]` (7건)

- [ ] Entity `test_empty_list_returns_invalid_size_code` · `test_empty_list_message_exact_match_prd_8_1`
- [ ] Control `test_empty_list_resolve_zero_calls` · `test_empty_list_returns_invalid_size_control`
- [ ] Boundary `test_empty_list_returns_invalid_size_boundary` · `test_empty_list_resolve_zero_calls_boundary` · `test_empty_message_exact_match_boundary`

### GREEN To-Do — BV-04 · 3×4 (7건)

- [ ] Entity `test_3x4_grid_returns_invalid_size_code` · `test_3x4_grid_message_exact_match_prd_8_1`
- [ ] Control `test_3x4_grid_resolve_zero_calls` · `test_3x4_grid_returns_invalid_size_control`
- [ ] Boundary `test_3x4_grid_returns_invalid_size_boundary` · `test_3x4_resolve_zero_calls_boundary` · `test_3x4_message_exact_match_boundary`

### GREEN To-Do — BV-01 · `None` (20건)

- [ ] Entity 7건 — `TestNormalFailureReturn` + None 메시지 2건
- [ ] Control 5건 — resolve 격리 2건 + 정상 실패 3건
- [ ] Boundary 8건 — 정상 실패 3 · 격리 2 · 메시지/타입 3
- [ ] GREEN: `grid is None` → `JudgeResult(INVALID_SIZE)` · Control 조기 종료 · Boundary 위임

### Scope · BV 무관 (10건, GREEN 불필요)

- [ ] `TestScopeRestriction` 5건 — AC-FR-01-02~05 / FR-02~05 미포함
- [ ] `TestScopeAstGuards` 5건 — AST·마커·fixture 범위

### BV별 pytest 확인 명령

```powershell
python -m pytest tests/entity/test_grid_shape_validator.py -k "4x3" -v          # BV-05
python -m pytest tests/entity/test_grid_shape_validator.py -k "5x5" -v          # BV-08
python -m pytest tests/ -k "zero_col" -m ac_fr_01_01 -v                        # BV-03
python -m pytest tests/ -k "empty" -m ac_fr_01_01 -v                           # BV-02
python -m pytest tests/ -k "3x4" -m ac_fr_01_01 -v                             # BV-04
python -m pytest tests/ -k "none" -m ac_fr_01_01 -v                            # BV-01
```

---

## ECB 구현 경로 (AC-FR-01-01)

| 경로 | 역할 | 상태 |
|------|------|------|
| `entity/rules/grid_shape_validator.py` | P1 — 형식 검증 (`validate_grid_shape`) | GREEN |
| `control/services/judge_use_case.py` | P2 — 조기 종료·resolve 격리 | GREEN |
| `boundary/cli/judge_handler.py` | P3 — I/O 위임 | GREEN |

> ECB 소스는 저장소 루트의 `entity/` · `control/` · `boundary/`에 둡니다. (잘못 추가되었던 루트 `src/` 폴더는 제거됨)

---

## GitHub / 원격 저장소

| 항목 | 내용 |
|------|------|
| **저장소** | [MagicSquare_19](https://github.com/youngsillee/MagicSquare_19) |
| **브랜치** | `develop` · `feature/dual-track-tdd` — AC-FR-01-01 ECB + Dual-Track RED 문서 |

자세한 푸시 이력: [2026-05-29-02_GitHub-Upload-Session-Report.md](./2026-05-29-02_GitHub-Upload-Session-Report.md)

---

## 관련 산출물

| 경로 | 설명 |
|------|------|
| [../Prompt/](../Prompt/) | 대화형 프롬프트·트랜스크립트 Export |
| [../docs/test_plan.md](../docs/test_plan.md) | AC-FR-01-01 테스트 계획서 (BV-01~08 정의) |
| [../defect_list.md](../defect_list.md) | TDD 세션 결함 목록 |
| [../README.md](../README.md) | 프로젝트 개요·Track A/B RED 체크리스트 |

---

## 문서 이력

| 일자 | 내용 |
|------|------|
| 2026-05-28 | Report 폴더·문제 정의 보고서 |
| 2026-05-29 | PRD 분석·GitHub 업로드·AC-FR-01-01 TDD·Dual-Track RED 보고서 |
| 2026-05-29 | `2026-05-29-05` 세션 Report·Prompt Export (GREEN·BV·GitHub) |
| 2026-05-29 | 루트 `src/` 폴더 제거 (잘못 생성된 스냅샷·중복 boundary) |
