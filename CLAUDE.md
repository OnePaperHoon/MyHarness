# MyHarness

## 프로젝트 개요
<!-- 프로젝트 목적과 핵심 기능을 여기에 작성하세요 -->

## 필수 규칙
모든 작업 전에 아래 규칙 파일을 반드시 읽어야 합니다:
- `.claude/rules/system.md` — 기본 행동 원칙
- `.claude/rules/coding.md` — 코딩 스타일
- `.claude/rules/security.md` — 보안 가드레일

## 프로젝트 구조
```
MyHarness/
├── .claude/
│   ├── commands/       # 슬래시 커맨드 (/review, /init, /commit)
│   ├── agents/         # 서브에이전트 정의 (code-reviewer, security-auditor, test-writer)
│   ├── skills/         # 재사용 작업 지침 (refactor, new-feature, debug, karpathy-guidelines)
│   ├── rules/          # AI 행동 지침 (system, coding, security)
│   ├── tools/          # 커스텀 스크립트
│   ├── docs/           # 프로젝트 기술 문서 및 라이브러리 레퍼런스
│   └── settings.json   # 권한 및 훅 설정
├── CLAUDE.md           # 이 파일
└── memory/             # 대화 간 메모리 저장소
```

## 작업 가이드라인

### 코드 수정 시
1. 관련 규칙 파일 확인
2. 기존 코드 스타일 파악 후 맞추기
3. 테스트 실행: `.claude/tools/check-lint.sh`
4. 커밋 전 변경사항 확인 요청

### 금지 사항
- 사용자 확인 없이 push, deploy
- `rm -rf`, `git push --force` 등 파괴적 명령어
- 소스 파일에 시크릿/API 키 하드코딩

## 아키텍처 문서
`.claude/docs/architecture.md` 참조
