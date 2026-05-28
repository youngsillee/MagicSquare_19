# Prompting — 4×4 Magic Square 문제 정의 세션

이 폴더는 **문제 인식·Why 체인·진짜 문제 정의**(STEP 1~5) 대화를 재사용할 수 있도록보낸 프롬프트입니다.

| 파일 | 용도 |
|------|------|
| [2026-05-28-01_Problem-Definition-Prompt.md](./2026-05-28-01_Problem-Definition-Prompt.md) | Cursor Export 전체 대화 (STEP 1~5, 원문) |
| [4x4-magic-square-problem-definition-interactive.md](./4x4-magic-square-problem-definition-interactive.md) | 전체 대화형 트랜스크립트(시스템 역할 + 턴별 User/Assistant) |
| [4x4-magic-square-prompts-chain.md](./4x4-magic-square-prompts-chain.md) | User 프롬프트만 연속 복사용 |
| [4x4-magic-square-session-summary.md](./4x4-magic-square-session-summary.md) | STEP 1~5 결론 요약(짧은 컨텍스트 주입용) |
| [4x4-magic-square-step5-full-response.md](./4x4-magic-square-step5-full-response.md) | STEP 5 Assistant 응답 원문(압축 없음) |

## 재사용 방법

1. **이어서 진행**: `interactive` 파일의 **Continuation** 섹션을 새 채팅에 붙여넣기.
2. **처음부터 반복**: `prompts-chain`의 STEP 블록을 순서대로 실행.
3. **요약만 주입**: `session-summary`를 시스템/컨텍스트로 넣고 STEP 6부터 시작.

## 제약 (세션 공통)

- 문제 정의 단계: **설계·구현·코드·알고리즘 설명 금지**(STEP별 추가 제약은 각 턴 참고).
- 프로젝트: `MagicSquare_xx` — 4×4, 값 1~16, 마방진 규칙·판정·불변 중심.

## Export 메타

- **보낸 일자**: 2026-05-28
- **범위**: STEP 1 (Observation) ~ STEP 5 (진짜 문제 정의)
- **다음 예정**: STEP 6 — 선 집합·활동 범위·동치·성공 증거 결정
