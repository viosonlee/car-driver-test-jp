from __future__ import annotations

from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
import argparse
import json
import math
import re


HAN_OR_ALNUM = re.compile(r"[\u3400-\u9fffA-Za-z0-9]+")


def normalize(text: str) -> str:
    return "".join(HAN_OR_ALNUM.findall((text or "").lower()))


def ngrams(text: str, size: int = 2) -> set[str]:
    value = normalize(text)
    return {value[index:index + size] for index in range(max(0, len(value) - size + 1))}


def question_text(question: dict) -> str:
    parts = [question.get("question", ""), question.get("explanation", ""), question.get("scenario", "")]
    for sub_question in question.get("sub_questions") or []:
        parts.extend([sub_question.get("question", ""), sub_question.get("explanation", "")])
    return "\n".join(part for part in parts if part)


def build_page_matcher(pages: list[dict]):
    page_grams = [ngrams(page["text"]) for page in pages]
    document_frequency = Counter(gram for grams in page_grams for gram in grams)
    page_count = len(pages)

    def match(text: str) -> tuple[int, float]:
        query_grams = ngrams(text)
        if not query_grams:
            return 0, 0.0
        weights = {gram: math.log((page_count + 1) / (document_frequency[gram] + 1)) + 1 for gram in query_grams}
        denominator = sum(weights.values())
        scores = [sum(weights[gram] for gram in query_grams & grams) / denominator for grams in page_grams]
        best_index = max(range(page_count), key=scores.__getitem__)
        return pages[best_index]["page"], scores[best_index]

    return match


class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def duplicate_groups(questions: list[dict]) -> list[list[int]]:
    normalized = [normalize(question.get("question") or question.get("scenario") or "") for question in questions]
    buckets: dict[str, list[int]] = defaultdict(list)
    for index, text in enumerate(normalized):
        buckets[text[:8]].append(index)

    groups = UnionFind(len(questions))
    for candidates in buckets.values():
        for position, left in enumerate(candidates):
            for right in candidates[position + 1:]:
                left_text, right_text = normalized[left], normalized[right]
                if questions[left].get("answer") != questions[right].get("answer"):
                    continue
                if min(len(left_text), len(right_text)) < 12:
                    continue
                ratio = SequenceMatcher(None, left_text, right_text).ratio()
                if ratio >= 0.9:
                    groups.union(left, right)

    result: dict[int, list[int]] = defaultdict(list)
    for index in range(len(questions)):
        result[groups.find(index)].append(index)
    return [members for members in result.values() if len(members) > 1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", required=True)
    parser.add_argument("--ocr", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    questions = json.loads(Path(args.questions).read_text(encoding="utf-8"))
    pages = json.loads(Path(args.ocr).read_text(encoding="utf-8"))
    match_page = build_page_matcher(pages)
    matches = [match_page(question_text(question)) for question in questions]
    duplicates = duplicate_groups(questions)
    per_page = Counter(page for page, score in matches if score >= 0.12)
    verified_per_page = Counter()
    for question in questions:
        for tag in question.get("tags", []):
            if tag.startswith("source_page_"):
                verified_per_page[int(tag.removeprefix("source_page_"))] += 1
    low_matches = sorted(range(len(questions)), key=lambda index: matches[index][1])

    report = [
        "# 题库与《交通的教则》覆盖审计",
        "",
        f"- PDF 页数：{len(pages)}（第 1–3 页为封面/说明/目录，第 41 页为封底）",
        f"- 题目总数：{len(questions)}",
        f"- 近重复题组：{len(duplicates)} 组，涉及 {sum(len(group) for group in duplicates)} 道题",
        f"- 低来源匹配题（匹配分 < 0.12）：{sum(score < 0.12 for _, score in matches)} 道",
        "",
        "## 正文页覆盖",
        "",
        "| PDF 页 | 机器高可信匹配题数 | 人工溯源新增题数 |",
        "|---:|---:|---:|",
    ]
    report.extend(f"| {page} | {per_page[page]} | {verified_per_page[page]} |" for page in range(4, 41))

    report.extend(["", "## 最低来源匹配题（优先人工复核）", ""])
    for index in low_matches[:80]:
        question = questions[index]
        page, score = matches[index]
        stem = question.get("question") or question.get("scenario") or "（无题干）"
        report.append(f"- `{question.get('id')}` → PDF 第 {page} 页，匹配分 {score:.3f}：{stem}")

    report.extend(["", "## 近重复题组", ""])
    for group in duplicates:
        items = []
        for index in group:
            question = questions[index]
            items.append(f"`{question.get('id')}` {question.get('question') or question.get('scenario') or ''}")
        report.append("- " + " / ".join(items))

    report.extend(["", "## 机器匹配说明", "", "来源页采用中文字符二元组 IDF 匹配；它适合发现明显范围外题和空白章节，但低分项仍需结合原页人工确认。"])
    Path(args.report).write_text("\n".join(report), encoding="utf-8")

    match_output = Path(args.report).with_suffix(".matches.json")
    match_output.write_text(json.dumps([
        {"id": question.get("id"), "source_page": page, "source_score": round(score, 4)}
        for question, (page, score) in zip(questions, matches)
    ], ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.report} and {match_output}")


if __name__ == "__main__":
    main()
