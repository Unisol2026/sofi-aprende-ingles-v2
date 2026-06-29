from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower().replace("'", "")).strip("-") or "expression"


def main():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    blocks = re.findall(r"(hello|unit\d): \{(.*?)\n  \}", html, flags=re.S)
    missing = []
    summary = []

    for unit, block in blocks:
        words = re.findall(r'wordItem\("([^"]+)","([^"]+)","([^"]*)", "([^"]+)"\)', block)
        expr_match = re.search(r"expressions:\[(.*?)\]\.map\(expressionItem\)", block, flags=re.S)
        exprs = re.findall(r'"([^"]+)"', expr_match.group(1)) if expr_match else []

        for _word, img, _phrase, _u in words:
            path = ROOT / "Imagens" / ("words" if unit == "unit5" else unit) / img
            if not path.exists():
                missing.append(str(path.relative_to(ROOT)))

        for expr in exprs:
            path = ROOT / "Imagens" / "expressions" / unit / f"{slug(expr)}.png"
            if not path.exists():
                missing.append(str(path.relative_to(ROOT)))

        summary.append((unit, len(words), len(exprs)))

    print("summary=" + repr(summary))
    print("missing=" + repr(missing))
    raise SystemExit(1 if missing else 0)


if __name__ == "__main__":
    main()
