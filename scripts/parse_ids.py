import re
from pathlib import Path

def main():
    pattern = re.compile(r'id="([^"]+)"')

    file_path = Path("board.svg")
    result = []
    with file_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = pattern.search(line)
            if m:
                group1 = m.group(1)
                result.append(str(group1))

    for r in sorted(result):
        # print(r)
        print(f"document.getElementById('{r}').color;")


if __name__ == "__main__":
    main()
