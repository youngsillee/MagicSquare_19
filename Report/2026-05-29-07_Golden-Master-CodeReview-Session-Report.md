# Golden Master · Code Review · REFACTOR 준비 세션 — 작업 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_xx |
| **보고 일자** | 2026-05-29 |
| **작업 범위** | GM-1~GM-10 회귀 안전장치 · README GM-3 · GitHub 푸시 · 코드리뷰 · REFACTOR 대상 분석 |
| **TDD phase** | Solve 트랙: GM GREEN(스냅샷) / Judge 트랙: AC-FR-01-01 GREEN 유지 |
| **브랜치** | `feature/dual-track-tdd` |
| **커밋** | `ec59867` — `feat(test): add Golden Master GM-1 regression and solver stack` |

---

## 1. 요약

Dual-Track 스냅샷(`f171f29`)에서 Solver 스택과 Golden Master(GM-1) 인프라를 **루트 ECB**(`control/`, `boundary/`)로 이식하였다. UIBoundary 실제 DTO 출력을 `tests/golden_master_expected.txt`에 고정하고 approve 패턴·생성 스크립트·설계 문서를 추가하였다. 이후 코드리뷰에서 **Solve 트랙은 REFACTOR 전 추가 GREEN이 필요**함을 확인하였다.

| 성과 | 내용 |
|------|------|
| GM-1 | 5 시나리오 baseline · `test_gm_01_*` · `scripts/generate_golden_master.py` |
| GM-3 | README §Golden Master 회귀 안전장치 |
| Solver | `UIBoundary`, `InputValidator`, `SolvePartialMagicSquare`, Entity services |
| 테스트 | 57 passed (`pytest tests/`) |
| GitHub | `origin/feature/dual-track-tdd` (`8e3cf3c` → `ec59867`) |
| 코드리뷰 | C-1~C-3 Critical, I-1~I-7 Important |

---

## 2. 요청 이력

| 순서 | 요청 | 결과 |
|------|------|------|
| 1 | GM-1 기준 파일·approve·생성 스크립트·설계 문서 | GREEN · baseline 5 시나리오 |
| 2 | README GM-3 섹션 | RED To-Do 하위 삽입 |
| 3 | GM 수행 방법 | 실행 명령 문서화 |
| 4 | `tests` import 오류 수정 | `tests/__init__.py`, `pytest.ini` `pythonpath = .` |
| 5 | feature 브랜치 GitHub 업로드 | `ec59867` 푸시 |
| 6 | `/code-reviewer` 전체 리뷰 | Critical 3건·Important 7건 |
| 7 | `control/`·`boundary/` REFACTOR 대상 분석 | 테스트 매핑·RED→GREEN 목록 |
| 8 | Report·Prompt Export | 본 문서 |

---

## 3. Golden Master (GM-1~GM-10)

### 3.1 산출 파일

| 파일 | GM ID |
|------|-------|
| `tests/golden_master_expected.txt` | GM-01, GM-03 |
| `tests/golden_master_scenarios.py` | GM-02 |
| `tests/golden_master_support.py` | GM-05 |
| `tests/golden_master_conftest.py` | GM-05 |
| `tests/test_gm_01_magic_square_golden_master.py` | GM-04, GM-06 |
| `scripts/generate_golden_master.py` | GM-01 |
| `docs/golden_master_design.md` | 설계 SSOT |

### 3.2 시나리오 baseline

| Section | 기대 |
|---------|------|
| `normal_success` | `[3,3,1,4,4,6]` |
| `reverse_success` | `[2,2,7,3,3,10]` |
| `invalid_blank_count` | `E002` |
| `duplicate_number` | `E005` |
| `no_valid_solution` | `E006` (캡처 레이어; Boundary 미매핑) |

### 3.3 실행

```powershell
pytest tests/test_gm_01_magic_square_golden_master.py -v
python scripts/generate_golden_master.py --check
pytest tests/test_gm_01_magic_square_golden_master.py --approve-golden -v
```

---

## 4. 코드리뷰 핵심 (Critical)

| ID | 이슈 | 위치 |
|----|------|------|
| C-1 | `resolve()`가 `TwoCellSolver.solve()` 결과 무시 | `control/solve_partial_magic_square.py` |
| C-2 | `UnsolvableDomainError` → E006 미매핑 | `boundary/ui_boundary.py` |
| C-3 | GM이 현재 UIBoundary 스냅샷을 고정 — 수정 후 재approve 필요 | `tests/golden_master_*` |

---

## 5. REFACTOR 준비 — `control/` · `boundary/`

> 참고: `src/control`, `src/boundary` 없음 — 루트 `control/`, `boundary/` 기준.

### 5.1 테스트 대응

| 프로덕션 | 전용 `test_*.py` |
|----------|------------------|
| `control/services/judge_use_case.py` | `tests/control/test_judge_use_case.py` ✅ |
| `control/solve_partial_magic_square.py` | ❌ → `test_solve_partial_magic_square.py` 필요 |
| `boundary/cli/judge_handler.py` | `tests/boundary/test_judge_handler.py` ✅ |
| `boundary/input_validator.py` | ❌ → `test_input_validator.py` (U-IN-*) |
| `boundary/ui_boundary.py` | ❌ → `test_ui_boundary.py` (U-OUT, E006) |
| `boundary/screen/*` | `test_screen_app.py` 부분 ✅ |

### 5.2 REFACTOR 전 GREEN (`.cursorrules` refactor_phase)

- D-SOL-01~04, U-IN-01~05, U-OUT-01~02, U-FLOW-02
- C-1/C-2 수정 후 GM `--approve-golden`

**한 줄:** GREEN 없이 REFACTOR하면 *“구조만 개선·동작 불변”* 계약을 지킬 수 없다.

---

## 6. pytest 환경

| 조치 | 파일 |
|------|------|
| `tests` 패키지 | `tests/__init__.py` |
| import 경로 | `pytest.ini` → `pythonpath = .` |
| IDE cwd | `.vscode/settings.json` (로컬, gitignore) |

---

## 7. 미포함·후속

| 항목 | 상태 |
|------|------|
| GUI 세션 Report/Prompt (06) | 로컬 untracked 가능 |
| Solve 단위 테스트 RED 파일 | 미작성 |
| U-OUT-03 E006 Boundary 구현 | 미구현 |

---

## 8. Traceability

| 커밋 | 설명 |
|------|------|
| `8e3cf3c` | GUI Screen |
| `ec59867` | GM-1 + Solver 스택 |

---

## 9. 문서 이력

| 일자 | 내용 |
|------|------|
| 2026-05-29 | GM·코드리뷰·REFACTOR 분석 세션 보고서 최초 작성 |
