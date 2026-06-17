# 기여 가이드

[English](./CONTRIBUTING.md) | 한국어

`service-ontology-lite`는 서비스 맵, 릴리스 감사, AI 에이전트 수정 위험 점검을 위한 작은 정적 검사 도구다.

## 범위

기여는 공개 가능한 core 안에 머물러야 한다.

```text
schema
CLI
MCP stdio server
generic scanner
generic audit rules
sample Next.js/Vercel app
report format
documentation
```

프로젝트별 운영 데이터, 실제 토큰, 비공개 장애 대응 문서, 고객 데이터, 도메인별 상업 점수 규칙은 추가하지 않는다.

## 개발 환경

```bash
python3 -m pip install -e .
python3 -m pip install pytest ruff build
```

## 릴리스 게이트

Pull request 전 실행:

```bash
python3 -m compileall -q src tests
python3 -m pytest -q
python3 -m ruff check .
python3 -m build --sdist --wheel
```

## 문서 변경

README를 바꿀 때는 영문과 한국어 페이지를 함께 맞춘다.

```text
README.md
README-ko_kr.md
```

명령, 출력 필드, 제한 사항이 한 언어에서 바뀌면 같은 pull request에서 다른 언어도 업데이트한다.

## 보안 경계

스캐너는 기본적으로 정적 검사로 유지한다.

```text
application code 실행 없음
target app 대상 network access 없음
.env 읽기 없음
secret 수집 없음
production-only schema/runbook 포함 없음
```

runtime inspection이나 network access가 필요한 변경은 구현 전에 별도 opt-in 기능으로 문서화한다.
