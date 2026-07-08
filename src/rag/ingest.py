from __future__ import annotations
from pathlib import Path


def build_corpus(data_dir: str = "src/rag/data") -> dict[str, str]:
    corpus = {}
    root = Path(data_dir)
    for file_path in root.glob("*.txt"):
        corpus[file_path.stem] = file_path.read_text(encoding="utf-8")
    return corpus


def main() -> None:
    corpus = build_corpus()
    for name, content in corpus.items():
        print(f"Loaded {name}: {len(content)} chars")


if __name__ == "__main__":
    main()
