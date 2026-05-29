# GUI Screen 세션 — 작업 보고서

| 항목 | 내용 |
|------|------|
| **프로젝트** | MagicSquare_xx |
| **보고 일자** | 2026-05-29 |
| **작업 범위** | 루트 ECB PyQt GUI 추가 · AC-FR-01-01 `--verify` · GitHub 푸시 |
| **TDD phase** | GREEN 유지 (Screen Boundary 어댑터 + 테스트 3건) |

---

## 1. 요약

`src/` 삭제 이후 사라진 PyQt GUI를 **루트 ECB**에 `boundary/screen/`으로 재구현하였다. 기존 스냅샷의 `UIBoundary`·`SolvePartialMagicSquare` 대신 현재 GREEN 범위의 `JudgeHandler` / `JudgeUseCase`에 연결하였다.

| 성과 | 내용 |
|------|------|
| GUI | `boundary/screen/` — PyQt6 4×4 격자 + 「판정」 버튼 |
| CLI 검증 | `python -m boundary.screen.app --verify` → `grid=None` → `INVALID_SIZE` |
| 테스트 | `tests/boundary/test_screen_app.py` 3건 추가 (**53 passed** `-m ac_fr_01_01`) |
| GitHub | `feature/dual-track-tdd` 커밋 `8e3cf3c` 푸시 완료 |
| 문서 | 루트 `README.md` GUI 실행 섹션 추가 |

---

## 2. 요청 이력

| 순서 | 요청 | 결과 |
|------|------|------|
| 1 | GREEN 완료 프로그램 GUI 실행 방법 | `src/` 삭제로 GUI 없음 안내 · 복구 vs 신규 구현 제안 |
| 2 | GUI 구현 진행 (`네`) | Git `f171f29`에서 구 UI 참고 · 루트 ECB에 `boundary/screen/` 신규 작성 |
| 3 | `feature` 커밋·푸시 | `8e3cf3c` — `feat(gui): add boundary/screen PyQt app wired to JudgeHandler` |
| 4 | Report보내기 + Prompt 저장 | 본 보고서·transcript Export |

---

## 3. 배경 — `src/` 제거

| 항목 | 값 |
|------|-----|
| **커밋** | `05c35b7` — `chore: remove mistakenly added root src folder.` |
| **영향** | `src/4.MagicSquare_1004_完/boundary/screen/` 포함 161 tracked files 삭제 |
| **잔존 ECB** | 루트 `entity/` · `control/` · `boundary/cli/` |

GUI는 삭제된 스냅샷에만 존재했으므로, 루트 구조에 맞게 **재작성**이 필요했다.

---

## 4. 구현 — `boundary/screen/`

| 파일 | 역할 |
|------|------|
| `boundary/screen/app.py` | 진입점 · `--verify` CLI · PyQt lazy import |
| `boundary/screen/main_window.py` | 4×4 `QSpinBox` · 「판정」 → `JudgeHandler.handle()` |
| `boundary/screen/presentation.py` | `format_judge_result()` — `[code] message` 표시 |
| `requirements-gui.txt` | `PyQt6>=6.6` (+ `requirements.txt`) |

### 아키텍처

```text
MagicSquareMainWindow
    → JudgeHandler (boundary/cli)
        → JudgeUseCase (control)
            → validate_grid_shape (entity)  ← AC-FR-01-01 GREEN
            → MagicSquareJudge.resolve      ← AC-FR-01-02+ (미구현)
```

### AC-FR-01-01 계약 (`--verify`)

```text
grid = None
→ code=INVALID_SIZE
→ message=Grid must be 4x4.
```

### GUI 「판정」 동작

- 스핀박스는 항상 4×4 정수 행렬 → 형식은 유효
- `MagicSquareJudge.resolve()`는 `NotImplementedError` → 화면에 AC-FR-01-02 이후 안내 문구 표시

---

## 5. 실행 방법

```powershell
cd c:\DEV\MagicSquare_xx
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-gui.txt

python -m boundary.screen.app              # GUI
python -m boundary.screen.app --verify       # CLI 앵커
```

> Windows: Microsoft Store Python에서 PyQt6 설치 실패 시 **프로젝트 `.venv`** 사용 권장 (Long Path 이슈).

---

## 6. 테스트

| 명령 | 결과 |
|------|------|
| `python -m pytest tests/ -m ac_fr_01_01 -q` | 53 passed |
| `python -m boundary.screen.app --verify` | `INVALID_SIZE` 출력 확인 |

신규 테스트 (`tests/boundary/test_screen_app.py`):

- `run_verify_none_grid()` — code·message 반환 및 stdout
- `format_judge_result()` — 표시 포맷

---

## 7. GitHub

| 항목 | 값 |
|------|-----|
| **원격** | `https://github.com/youngsillee/MagicSquare_19.git` |
| **브랜치** | `feature/dual-track-tdd` |
| **커밋** | `8e3cf3c` — feat(gui): add boundary/screen PyQt app wired to JudgeHandler |
| **변경** | 7 files, +241 lines |

---

## 8. 산출물

| 경로 | 설명 |
|------|------|
| [2026-05-29-06_Prompt-Execution-Report.md](./2026-05-29-06_Prompt-Execution-Report.md) | Export 실행 요약 |
| [../Prompt/2026-05-29-06_Interactive-Prompt-Transcript.md](../Prompt/2026-05-29-06_Interactive-Prompt-Transcript.md) | 대화형 transcript |
| [../README.md](../README.md) | GUI 실행 섹션 |
| `boundary/screen/` | PyQt GUI 어댑터 |

---

## 9. 미완 / 다음 단계

| 항목 | 상태 |
|------|------|
| AC-FR-01-02+ 값·선 판정 | `MagicSquareJudge.resolve()` 미구현 — GUI는 안내 문구만 |
| BV별 GREEN 커밋 분리 | `Report/README.md` To-Do 대부분 `[ ]` |
| GUI E2E (pytest-qt) | 미도입 — `--verify` 경로만 단위 테스트 |

---

## 10. 문서 이력

| 일자 | 내용 |
|------|------|
| 2026-05-29 | GUI Screen 세션 보고서 작성 (`2026-05-29-06`) |
