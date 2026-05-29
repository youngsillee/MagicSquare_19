# 2026-05-29 Interactive Prompt Transcript

> 형식: User/Assistant 대화형 프롬프트 기록  
> 프로젝트: MagicSquare_xx  
> 주제: FR-01~FR-05 Dual-Track RED 설계 (Boundary + Logic)

---

## Turn 1

**User**

당신은 Dual-Track UI + Logic TDD 전문가입니다.

**TDD phase: RED** — 오직 RED 테스트 설계표만 작성하십시오.

## 금지 (엄격)

- 구현 코드, 테스트 코드, 스켈레톤 코드 작성 금지
- 클래스/파일 구조 확정 금지
- GREEN / REFACTOR 단계 진입 금지
- pytest 실행·코드 생성·파일 저장 금지 (설계표 텍스트 출력만)

## SSOT (반드시 참조)

- `docs/PRD_MagicSquare.md` v0.2
- `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md`
- `.cursorrules` (ECB, Dual-Track, Test ID 규칙)

## 프로젝트 계약

**입력:** 4×4 `int[][]`, `0`=빈칸(정확히 2개), 값은 `0` 또는 `1~16`, `0` 제외 중복 금지  
**출력:** `int[6]` = `[r1,c1,n1,r2,c2,n2]`, 좌표 **1-index**  
**마방진 상수:** 4×4 → M=34 (`MagicConstant` SSOT)  
**검증 순서 (short-circuit):** null → size → empty count → value range → duplicate

**Boundary invalid 입력:** Failure envelope 반환 (Python 예외 아님)  
- E003 null, E001 size, E002 empty count, E004 range, E005 duplicate  
- invalid 시 `SolvePartialMagicSquare.execute` **0회** (U-FLOW-02)

**Domain Logic:** Entity/Control 단위, **Domain Mock 금지**

## 범위

[전체 FR-01~FR-05 Dual-Track RED 설계표]

### TRACK A — Boundary / UI Contract RED

입력 검증 U-IN-* (1~5), 출력 계약 U-OUT-* (6~7), 흐름 격리 U-FLOW-02 (8)

### TRACK B — Domain / Logic RED

`find_blank_coords`, `find_not_exist_nums`, `is_magic_square`, `solution` — G0~G3, D-LOC/MIS/VAL/SOL-*

출력 형식: UI RED Tests 표, Logic RED Tests 표, RED 설계 검수 체크리스트

**Assistant**

- SSOT 파일 `PRD_MagicSquare.md`, `Report/02...` 워크스페이스 미존재 확인
- G0·G1 표준 4×4 마방진에서 유도; G2·G3 placeholder
- Track A 9행 (U-IN-01~05, U-OUT-01~02, U-FLOW-02)
- Track B 12행 (D-LOC-01, D-MIS-01, D-VAL-01~06, D-SOL-01~04)
- 검수 체크리스트 6항 통과 명시

산출: 채팅 내 RED 설계표 (코드·파일 저장 없음)

---

## Turn 2

**User**

Report에보내고 Prompt 저장해줘

**Assistant**

- `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md` — RED 설계 SSOT
- `Report/2026-05-29-04_DualTrack-RED-Design-Session-Report.md`
- `Report/2026-05-29-04_Prompt-Execution-Report.md`
- `Prompt/2026-05-29-04_Interactive-Prompt-Transcript.md` (본 문서)
- `Report/README.md` 인덱스 갱신

---

## 재사용 가이드

- **RED pytest 이어하기**: `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md`를 컨텍스트로 제공 후 Track A Boundary 테스트부터 작성
- **G2/G3 확정 후**: §7 Open 항목 치환 → D-SOL-02·03 RED Then 갱신
- **PRD v0.2 작성 후**: E00x message exact를 U-IN-* Then에 반영

---

## 주요 산출물 경로

| 유형 | 경로 |
|------|------|
| RED 설계 SSOT | `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md` |
| 세션 보고서 | `Report/2026-05-29-04_DualTrack-RED-Design-Session-Report.md` |
| Transcript | `Prompt/2026-05-29-04_Interactive-Prompt-Transcript.md` |
