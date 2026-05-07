# @clack/prompts

Node.js CLI 인터랙티브 프롬프트 라이브러리. 심플하고 세련된 UI가 특징.

## 설치

```bash
npm install @clack/prompts
```

## 기본 사용법

```ts
import * as p from '@clack/prompts';

async function main() {
  p.intro('배포 설정');

  const config = await p.group({
    name: () => p.text({
      message: '프로젝트 이름',
      placeholder: 'my-app',
      validate: (v) => !v ? '필수 항목입니다.' : undefined,
    }),
    type: () => p.select({
      message: '프로젝트 유형',
      options: [
        { value: 'web', label: '웹 애플리케이션' },
        { value: 'api', label: 'REST API' },
        { value: 'cli', label: 'CLI 도구' },
      ],
    }),
    confirm: () => p.confirm({ message: '계속하시겠습니까?' }),
  }, {
    onCancel: () => {
      p.cancel('취소됨.');
      process.exit(0);
    },
  });

  const spinner = p.spinner();
  spinner.start('처리 중...');
  await doSomething();
  spinner.stop('완료!');

  p.outro('설정 완료');
}

main();
```

## 주요 위젯

| 위젯 | 설명 |
|------|------|
| `p.text()` | 텍스트 입력 |
| `p.password()` | 비밀번호 입력 (마스킹) |
| `p.select()` | 단일 선택 |
| `p.multiselect()` | 다중 선택 |
| `p.confirm()` | Y/N 확인 |
| `p.group()` | 여러 프롬프트 묶기 |
| `p.spinner()` | 로딩 스피너 |
| `p.intro()` / `p.outro()` | 시작/종료 메시지 |
| `p.note()` | 강조 박스 출력 |
| `p.cancel()` | 취소 메시지 출력 |

## 특징

- TypeScript 기본 지원
- 단순한 순차 흐름에 최적화 (폼 하나 → 실행)
- 의존성 없음, 매우 가벼움
- 풀 TUI보다 설치 스크립트/CLI 도구에 어울림

## 언제 쓰면 좋은가

- 설치/초기화 스크립트 (`create-app`, `init`)
- 배포 전 확인 단계
- 단계별 설정 수집이 필요한 CLI

## 링크

- [npm](https://www.npmjs.com/package/@clack/prompts)
- [GitHub](https://github.com/bombshell-dev/clack)
