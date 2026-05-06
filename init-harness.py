#!/usr/bin/env python3
"""Claude Code 하네스 초기화 TUI"""

import asyncio
import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    RichLog,
    Select,
    TextArea,
)
from textual import on

PROJECT_TYPES = [
    ("웹 애플리케이션", "web"),
    ("REST API / 백엔드", "api"),
    ("CLI 도구", "cli"),
    ("라이브러리 / 패키지", "library"),
    ("모바일 앱", "mobile"),
    ("데이터 파이프라인 / ML", "data"),
    ("게임", "game"),
    ("기타", "other"),
]

PROMPT_TEMPLATE = """
Claude Code 하네스 템플릿 파일들을 아래 프로젝트에 맞게 커스터마이즈해주세요.

## 프로젝트 정보
- 이름: {name}
- 유형: {type}
- 기술 스택: {stack}
- 설명: {description}
- 특별 요구사항: {requirements}

## 수행 작업
다음 3개 파일을 프로젝트에 맞게 실제로 편집해주세요.

1. **CLAUDE.md**
   - 프로젝트 이름과 개요를 실제 정보로 채우기
   - 기술 스택에 맞는 로컬 개발 실행 명령어 추가
   - 프로젝트 구조에 맞는 디렉토리 설명 추가

2. **.claude/docs/architecture.md**
   - 기술 스택 정보로 채우기
   - 주요 컴포넌트 설명 추가
   - 환경변수 테이블 예시 채우기

3. **.claude/rules/coding.md**
   - {stack} 스택에 특화된 코딩 규칙 추가
   - 프레임워크별 베스트 프랙티스 반영
   - 프로젝트 유형({type})에 맞는 규칙 추가

특별 요구사항이 있으면 .claude/rules/security.md에도 반영해주세요.
""".strip()


class HarnessApp(App):
    CSS = """
    Screen {
        background: $surface;
    }

    #form-panel {
        width: 1fr;
        padding: 1 2;
        border-right: solid $primary-darken-2;
    }

    #log-panel {
        width: 2fr;
        padding: 1;
    }

    .field-label {
        color: $text-muted;
        margin-top: 1;
    }

    Input, Select, TextArea {
        margin-bottom: 0;
    }

    TextArea {
        height: 6;
    }

    #buttons {
        margin-top: 1;
        height: auto;
        align: center middle;
    }

    #buttons Button {
        margin-right: 1;
    }

    #log {
        height: 1fr;
        border: solid $primary;
    }

    #log-title {
        color: $text-muted;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "quit", "종료"),
        Binding("ctrl+g", "generate", "생성"),
    ]

    def __init__(self, target_dir: Path):
        super().__init__()
        self.target_dir = target_dir
        self._claude_process = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal():
            with Vertical(id="form-panel"):
                yield Label("프로젝트 이름", classes="field-label")
                yield Input(placeholder="예: my-awesome-app", id="project-name")

                yield Label("프로젝트 유형", classes="field-label")
                yield Select(
                    [(label, value) for label, value in PROJECT_TYPES],
                    id="project-type",
                    value="web",
                )

                yield Label("기술 스택", classes="field-label")
                yield Input(
                    placeholder="예: Python, FastAPI, PostgreSQL, Redis",
                    id="tech-stack",
                )

                yield Label("프로젝트 설명", classes="field-label")
                yield TextArea(id="description")

                yield Label("특별 요구사항 (선택)", classes="field-label")
                yield Input(
                    placeholder="예: 금융 앱 - 보안 강화 필요",
                    id="requirements",
                )

                with Horizontal(id="buttons"):
                    yield Button("하네스 생성 (Ctrl+G)", variant="primary", id="generate")
                    yield Button("종료", variant="default", id="cancel")

            with Vertical(id="log-panel"):
                yield Label("실행 로그", id="log-title")
                yield RichLog(id="log", highlight=True, markup=True, wrap=True)

        yield Footer()

    def on_mount(self) -> None:
        log = self.query_one("#log", RichLog)
        log.write("[bold]Claude Code 하네스 초기화 도구[/bold]")
        log.write(f"대상 디렉토리: [cyan]{self.target_dir}[/cyan]")
        log.write("─" * 50)
        log.write("프로젝트 정보를 입력하고 [bold green]하네스 생성[/bold green]을 누르세요.")

    @on(Button.Pressed, "#generate")
    async def on_generate(self) -> None:
        await self.action_generate()

    async def action_generate(self) -> None:
        name = self.query_one("#project-name", Input).value.strip()
        project_type = self.query_one("#project-type", Select).value
        stack = self.query_one("#tech-stack", Input).value.strip()
        description = self.query_one("#description", TextArea).text.strip()
        requirements = self.query_one("#requirements", Input).value.strip() or "없음"

        if not name:
            self.notify("프로젝트 이름을 입력해주세요.", severity="error")
            return
        if not stack:
            self.notify("기술 스택을 입력해주세요.", severity="error")
            return
        if not description:
            self.notify("프로젝트 설명을 입력해주세요.", severity="error")
            return

        # 유형 한글명 변환
        type_label = next(
            (label for label, val in PROJECT_TYPES if val == project_type),
            project_type,
        )

        prompt = PROMPT_TEMPLATE.format(
            name=name,
            type=type_label,
            stack=stack,
            description=description,
            requirements=requirements,
        )

        self.query_one("#generate", Button).disabled = True
        asyncio.create_task(self._run_claude(prompt))

    async def _run_claude(self, prompt: str) -> None:
        log = self.query_one("#log", RichLog)
        log.write("")
        log.write("[bold green]▶ Claude Code 실행 중...[/bold green]")
        log.write("─" * 50)

        try:
            self._claude_process = await asyncio.create_subprocess_exec(
                "claude",
                "-p",
                prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=str(self.target_dir),
            )

            async for raw_line in self._claude_process.stdout:
                line = raw_line.decode("utf-8", errors="replace").rstrip()
                if line:
                    log.write(line)

            await self._claude_process.wait()
            rc = self._claude_process.returncode

            log.write("─" * 50)
            if rc == 0:
                log.write("[bold green]✓ 하네스 생성 완료![/bold green]")
                self.notify("하네스 생성 완료!", severity="information")
            else:
                log.write(f"[bold red]✗ 오류 발생 (exit code: {rc})[/bold red]")
                self.notify("오류가 발생했습니다. 로그를 확인해주세요.", severity="error")

        except FileNotFoundError:
            log.write("[bold red]✗ 'claude' CLI를 찾을 수 없습니다.[/bold red]")
            log.write("Claude Code가 설치되어 있는지 확인해주세요: https://claude.ai/code")
        except Exception as e:
            log.write(f"[bold red]✗ 예외 발생: {e}[/bold red]")
        finally:
            btn = self.query_one("#generate", Button)
            btn.disabled = False

    @on(Button.Pressed, "#cancel")
    def on_cancel(self) -> None:
        if self._claude_process and self._claude_process.returncode is None:
            self._claude_process.terminate()
        self.exit()


def main() -> None:
    # 실행 위치를 대상 디렉토리로 사용 (인수로 지정 가능)
    if len(sys.argv) > 1:
        target = Path(sys.argv[1]).resolve()
    else:
        target = Path.cwd()

    if not target.exists():
        print(f"오류: 디렉토리가 존재하지 않습니다: {target}")
        sys.exit(1)

    app = HarnessApp(target_dir=target)
    app.run()


if __name__ == "__main__":
    main()
