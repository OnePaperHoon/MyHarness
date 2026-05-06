# MyHarness

Claude Code 하네스를 어떤 프로젝트에도 빠르게 세팅할 수 있는 TUI 도구입니다.

## 요구사항

- Python 3.8+
- [Claude Code CLI](https://claude.ai/code) 설치 및 로그인 완료

## 설치

```powershell
git clone https://github.com/your-username/MyHarness.git
cd MyHarness
pip install -r requirements.txt
```

## 사용법

### 현재 디렉토리에 하네스 초기화

```powershell
.\run.ps1
```

### 특정 프로젝트 경로 지정

```powershell
.\run.ps1 -TargetDir "C:\path\to\your\project"
```

### Python으로 직접 실행

```powershell
python init-harness.py
python init-harness.py "C:\path\to\your\project"
```

## TUI 화면

```
┌─────────────────────┬──────────────────────────────────┐
│  프로젝트 이름       │  실행 로그                        │
│  프로젝트 유형  ▼   │                                   │
│  기술 스택           │  ▶ Claude Code 실행 중...         │
│  프로젝트 설명       │  [실시간 출력]                    │
│  특별 요구사항       │                                   │
│  [하네스 생성] [종료]│  ✓ 하네스 생성 완료!             │
└─────────────────────┴──────────────────────────────────┘
```

| 단축키 | 동작 |
|--------|------|
| `Ctrl+G` | 하네스 생성 |
| `Ctrl+C` | 종료 |

## 생성되는 파일

```
your-project/
├── CLAUDE.md                      # 프로젝트 진입점 (프로젝트 맞게 자동 작성)
└── .claude/
    ├── settings.json              # 권한 및 훅 설정
    ├── rules/
    │   ├── system.md              # 기본 행동 원칙
    │   ├── coding.md              # 기술 스택 맞춤 코딩 규칙
    │   └── security.md            # 보안 가드레일
    ├── tools/
    │   └── check-lint.sh          # 프로젝트 유형 자동 감지 린터
    └── docs/
        └── architecture.md        # 아키텍처 문서
```

## 동작 방식

1. TUI 폼에 프로젝트 정보 입력
2. 입력값을 바탕으로 프롬프트 자동 조합
3. `claude -p "..."` 백그라운드 실행
4. Claude가 하네스 파일들을 프로젝트에 맞게 직접 편집
5. 실행 로그를 우측 패널에 실시간 스트리밍
