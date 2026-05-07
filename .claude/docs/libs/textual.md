# textual

Python 풀 TUI 프레임워크. CSS로 레이아웃을 잡고 위젯 기반으로 복잡한 터미널 앱을 만들 수 있음.
이 프로젝트(`init-harness.py`)에서 사용 중.

## 설치

```bash
pip install textual
```

## 기본 구조

```python
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Label
from textual.containers import Vertical, Horizontal
from textual.binding import Binding
from textual import on

class MyApp(App):
    CSS = """
    #container {
        padding: 1 2;
    }
    Button {
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "종료"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="container"):
            yield Label("이름을 입력하세요")
            yield Input(placeholder="홍길동", id="name")
            yield Button("확인", variant="primary", id="submit")
        yield Footer()

    @on(Button.Pressed, "#submit")
    def handle_submit(self) -> None:
        name = self.query_one("#name", Input).value
        self.notify(f"안녕하세요, {name}!")

MyApp().run()
```

## 주요 위젯

| 위젯 | 설명 |
|------|------|
| `Input` | 텍스트 입력 |
| `TextArea` | 멀티라인 텍스트 편집기 |
| `Select` | 드롭다운 선택 |
| `Button` | 버튼 (`variant`: primary / error / warning / default) |
| `Label` | 텍스트 출력 |
| `RichLog` | Rich 마크업 지원 로그 패널 |
| `DataTable` | 테이블 |
| `ProgressBar` | 진행률 바 |
| `Markdown` | 마크다운 렌더링 |
| `ListView` | 스크롤 가능한 목록 |

## 컨테이너

| 컨테이너 | 설명 |
|----------|------|
| `Vertical` | 세로 배치 |
| `Horizontal` | 가로 배치 |
| `ScrollableContainer` | 스크롤 가능한 영역 |
| `Grid` | 그리드 레이아웃 |

## CSS 주요 속성

```css
/* 크기 */
width: 1fr;        /* 비율 분할 */
height: auto;      /* 콘텐츠 크기 */
min-width: 20;

/* 여백 */
padding: 1 2;      /* 상하 1, 좌우 2 */
margin-top: 1;

/* 테두리 */
border: solid $primary;
border-right: solid $primary-darken-2;

/* 색상 변수 */
$primary / $primary-darken-2
$surface / $text / $text-muted
$success / $error / $warning
```

## 비동기 처리 (subprocess 스트리밍)

```python
async def run_background(self) -> None:
    process = await asyncio.create_subprocess_exec(
        "some-command", "arg",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    log = self.query_one("#log", RichLog)
    async for line in process.stdout:
        log.write(line.decode("utf-8", errors="replace").rstrip())
    await process.wait()
```

## 특징

- CSS 기반 레이아웃 (웹 개발 감각으로 접근 가능)
- 비동기(asyncio) 기반 → subprocess 스트리밍에 자연스럽게 통합
- 패널 분할, 탭, 모달 등 복잡한 UI 구성 가능
- `textual devtools`로 실시간 CSS 수정 가능

## 언제 쓰면 좋은가

- 좌우/상하 패널 분할이 필요한 앱
- 실시간 로그 스트리밍을 보여줘야 할 때
- 폼 + 결과를 동시에 보여주는 대시보드형 CLI

## 링크

- [공식 문서](https://textual.textualize.io)
- [GitHub](https://github.com/Textualize/textual)
- [위젯 갤러리](https://textual.textualize.io/widget_gallery/)
