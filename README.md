# 동일 Morning Call — 개발 코드

부문별 오늘의 법률·규제 리스크 브리핑. AI가 매일 아침 부문별 이슈를 정리하고, 법무팀이 검수한 이슈만 전 직원에게 공개합니다.

- 공개 페이지: https://essaycozy-byte.github.io/daily-briefing
- 저장소: https://github.com/essaycozy-byte/daily-briefing

## 폴더 구성

| 경로 | 내용 |
| --- | --- |
| `review-site/index.html` | 법무팀 검수 화면. claude.ai 아티팩트로 게시되며, 내장 DB(`briefings/날짜` 문서)를 읽고 검수 완료·취소를 기록합니다. 편집 권한자만 검수 버튼이 보입니다. |
| `index.html` | 전 직원용 공개 페이지(읽기 전용). `data/briefings.json`을 읽어 표시합니다. GitHub Pages로 게시. |
| `data/briefings.json` | 공개 데이터. 검수 완료(approved) 이슈만, 최근 60일. |
| `tools/build.py` | 검수 화면 DB에서 읽은 브리핑 중 검수 완료 이슈만 골라 `briefings.json`을 갱신하는 스크립트. |
| `prompts/01_briefing_generate.md` | 브리핑 생성 AI 프롬프트(평일 07:14 예약 실행). |
| `prompts/02_public_sync.md` | 공개 페이지 동기화 AI 프롬프트(평일 08:03, 11:47 예약 실행). |

## 하루 흐름

1. 07:14 — AI가 6개 부문(안전, 마케팅, 공사·현장, 사업, 재무, 경영지원)을 검색·요약해 검수 화면 DB에 '검수 대기'로 저장
2. 법무팀 검수 — 검수 화면에서 카드별 또는 일괄로 '검수 완료'
3. 08:03, 11:47 — AI가 검수 완료본만 골라 `build.py`로 공개 데이터를 갱신하고 GitHub에 반영
4. 전 직원 — 공개 페이지에서 로그인 없이 열람

## 데이터 형식 (briefings/YYYY-MM-DD)

```json
{
  "date": "2026-11-20",
  "generatedAt": "2026-11-20T07:14:00+09:00",
  "generator": "Claude 예약 작업",
  "items": [
    {
      "id": "s1", "dept": "safety", "level": "high", "status": "pending",
      "title": "…", "summary": "…", "check": "…",
      "source": "고용노동부 보도자료", "url": "https://…", "published": "2026-11-12"
    }
  ]
}
```

- `dept`: safety · marketing · construction · business · finance · admin
- `level`: high(주의) · mid(확인) · low(참고)
- `status`: pending(검수 대기) · approved(검수 완료)

## 로컬에서 공개 페이지 확인

```bash
python3 -m http.server 8000   # http://localhost:8000 접속
```

## 유의사항

- 기사 문장을 옮기지 않고 직접 요약하며, 원문은 링크로만 연결합니다(저작권법 제7조 제5호, 대법원 2004도5350 참고).
- 사내 정보는 AI에 입력하지 않고 공개 자료만 다룹니다.
- 이 브리핑은 법률 자문이 아니며, 구체적 사안은 법무팀과 협의합니다.
