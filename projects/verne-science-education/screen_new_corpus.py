"""Reference implementation for applying the documented screening procedure to a new corpus.

Usage: python screen_new_corpus.py --paragraphs data/paragraphs.csv \
           --dictionary example_dictionary.csv --output new_screen
"""
import argparse
import csv
from pathlib import Path
import random
import re


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, header, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)


def read_dictionary(path):
    rules = {}
    for row in read_csv(path):
        group, pattern = row["group"].strip(), row["pattern"].strip()
        if not group or not pattern:
            raise ValueError("Every dictionary row needs a group and regular expression.")
        compiled = re.compile(pattern, re.IGNORECASE)
        if compiled.search(""):
            raise ValueError("Empty-matching pattern: " + pattern)
        rules.setdefault(group, []).append(compiled)
    if not rules:
        raise ValueError("The dictionary is empty.")
    return rules


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paragraphs", required=True, type=Path, help="CSV with paragraph_id and text")
    parser.add_argument("--dictionary", required=True, type=Path, help="CSV with group and pattern")
    parser.add_argument("--output", required=True, type=Path, help="New directory for output files")
    parser.add_argument("--per-group", type=int, default=6)
    parser.add_argument("--nonmatches", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20261015)
    args = parser.parse_args()
    if min(args.per_group, args.nonmatches) < 0:
        parser.error("Sample sizes must be non-negative.")
    rules = read_dictionary(args.dictionary)
    text = {}
    matches = {}
    for row in read_csv(args.paragraphs):
        pid, paragraph = row["paragraph_id"].strip(), row["text"].strip()
        if not pid or not paragraph or pid in text:
            raise ValueError("Paragraph IDs and texts must be present. IDs must be unique.")
        text[pid] = paragraph
        hits = {}
        for group, patterns in rules.items():
            evidence = sorted({m.group().lower() for pat in patterns for m in pat.finditer(paragraph)})
            if evidence:
                hits[group] = evidence
        matches[pid] = hits
    if not text:
        parser.error("The corpus is empty.")

    # Fill the smallest groups first to limit competition for multi-group paragraphs.
    pools = {g: [pid for pid in text if g in matches[pid]] for g in rules}
    rng = random.Random(args.seed)
    selected = {}
    for group in sorted(pools, key=lambda g: (len(pools[g]), g)):
        available = sorted(pid for pid in pools[group] if pid not in selected)
        if len(available) < args.per_group:
            parser.error(f"{group} has only {len(available)} unused candidates. Reduce --per-group.")
        for pid in rng.sample(available, args.per_group):
            selected[pid] = group
    negative_pool = sorted(pid for pid, evidence in matches.items() if not evidence)
    if len(negative_pool) < args.nonmatches:
        parser.error(f"Only {len(negative_pool)} unmatched paragraphs. Reduce --nonmatches.")
    for pid in rng.sample(negative_pool, args.nonmatches):
        selected[pid] = "no match"
    order = list(selected)
    rng.shuffle(order)
    args.output.mkdir(parents=True, exist_ok=False)
    write_csv(args.output / "screening.csv", ["paragraph_id","candidate","groups","matched_text"],
              ((pid, int(bool(hits)), "|".join(hits), " | ".join(
                  f"{g}: {', '.join(words)}" for g, words in hits.items())) for pid,hits in matches.items()))
    write_csv(args.output / "pilot_blind.csv", ["paragraph_id","text","human_code_0_1_2","evidence"],
              ((pid,text[pid],"","") for pid in order))
    write_csv(args.output / "pilot_selection_key.csv", ["paragraph_id","sample_group"],
              ((pid,selected[pid]) for pid in order))
    print(f"{len(text)} paragraphs, {sum(bool(h) for h in matches.values())} candidates, "
          f"{len(order)} blind pilot records. Results in {args.output}.")


if __name__ == "__main__":
    main()
