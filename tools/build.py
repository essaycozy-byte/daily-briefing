"""검수 완료 이슈만 골라 공개용 data/briefings.json 을 만든다.

사용법: python3 tools/build.py <사이트DB에서 읽은 브리핑 문서들.json>
입력: [{"date": "YYYY-MM-DD", "items": [...]}, ...]  (사이트 DB briefings/<날짜> 문서들의 data)
기존 data/briefings.json 과 날짜 기준으로 합치고, 최근 60일만 남긴다.
"""
import json, sys, datetime, pathlib

KEEP = ("id", "dept", "level", "title", "summary", "check", "source", "url", "published")
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "briefings.json"

def clean(doc):
    items = [{k: i.get(k, "") for k in KEEP} for i in doc.get("items", [])
             if isinstance(i, dict) and i.get("status") == "approved"]
    return {"date": doc.get("date"), "items": items}

def main(src):
    new = json.load(open(src, encoding="utf-8"))
    old = json.load(open(OUT, encoding="utf-8")).get("briefings", []) if OUT.exists() else []
    by_date = {b["date"]: b for b in old if b.get("date")}
    for d in new:
        if d.get("date"):
            by_date[d["date"]] = clean(d)
    keep = sorted((b for b in by_date.values() if b["items"]), key=lambda b: b["date"], reverse=True)[:60]
    kst = datetime.timezone(datetime.timedelta(hours=9))
    out = {"updatedAt": datetime.datetime.now(kst).isoformat(timespec="minutes"), "briefings": keep}
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(keep)} dates, {sum(len(b['items']) for b in keep)} approved items")

if __name__ == "__main__":
    main(sys.argv[1])
