"""Recompute the reported counts from archived paragraph and curriculum records.

Run with Python 3.8 or newer. No packages, model calls or network access are required.
"""
import csv
import json
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"


def read_table(filename):
    with (DATA / filename).open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def counts(rows, column):
    return dict(sorted(Counter(row[column] for row in rows).items()))


def matrix(rows, row_label, column_label):
    result = [[0] * 3 for _ in range(3)]
    for row in rows:
        result[int(row[row_label])][int(row[column_label])] += 1
    return result


def overlap(rows, first, second):
    n_same = sum(row[first] == row[second] for row in rows)
    return {"same": n_same, "n": len(rows), "percent": round(100 * n_same / len(rows), 2)}


def main():
    corpus = read_table("screening.csv")
    ids = [r["paragraph_id"] for r in corpus]
    if len(set(ids)) != len(ids) or set(ids) != {r["paragraph_id"] for r in read_table("paragraphs.csv")}:
        raise ValueError("Paragraph IDs must be unique and match the text file.")
    pilot = read_table("pilot.csv")
    by_id = {r["paragraph_id"]: r for r in corpus}
    if any(r["rule_code"] != by_id[r["paragraph_id"]]["rule_code"] for r in pilot):
        raise ValueError("Pilot and corpus rule codes differ.")
    candidates = [r for r in corpus if r["expanded_candidate"] == "1"]
    theme_counts = Counter(g for r in candidates for g in r["candidate_groups"].split("|") if g)
    groups = counts(corpus, "combined_code")
    main_setup = {code: {"n": n, "percent": round(100*n / len(corpus), 2)} for code,n in groups.items()}
    outcome_links = read_table("outcome_links.csv")
    scored = [r for r in outcome_links if r["AI_alignment_score"] != ""]
    units = read_table("curriculum_units.csv")
    unit_matches = read_table("unit_links.csv")
    pilot_control = [r for r in pilot if r["sample_group"] == "no match"]
    result = {
        "corpus_paragraphs": len(corpus),
        "earlier_keyword_candidates": sum(r["earlier_candidate"] == "1" for r in corpus),
        "expanded_keyword_candidates": len(candidates),
        "expanded_keyword_nonmatches": len(corpus) - len(candidates),
        "expanded_candidates_percent": round(100 * len(candidates) / len(corpus), 2),
        "overlapping_candidate_groups": dict(theme_counts.most_common()),
        "initial_rule_codes": counts(corpus, "rule_code"),
        "combined_preliminary_codes": main_setup,
        "combined_code_provenance": counts(corpus, "combined_source"),
        "later_preliminary_codes": counts(corpus, "later_code"),
        "changed_combined_to_later": sum(r["combined_code"] != r["later_code"] for r in corpus),
        "pilot_sample_groups": counts(pilot, "sample_group"),
        "rule_vs_final_review": overlap(pilot, "rule_code", "final_reviewed_code"),
        "rule_vs_initial_blind_review": overlap(pilot, "rule_code", "initial_blind_code"),
        "initial_blind_vs_final_review": overlap(pilot, "initial_blind_code", "final_reviewed_code"),
        "pilot_matrix_rows_rule_columns_final_0_1_2": matrix(pilot, "rule_code", "final_reviewed_code"),
        "reviewed_codes_in_keyword_nonmatch_controls": counts(pilot_control, "final_reviewed_code"),
        "curriculum_units": len(units),
        "curriculum_outcomes_in_inventory": sum(int(r["number_of_listed_outcomes"]) for r in units),
        "unit_link_records": len(unit_matches),
        "distinct_paragraphs_with_candidate_unit": len({r["paragraph_id"] for r in unit_matches}),
        "focused_outcomes": counts(outcome_links, "outcome_id"),
        "candidate_outcome_links": len(outcome_links),
        "distinct_outcome_candidate_paragraphs": len({r["paragraph_id"] for r in outcome_links}),
        "scored_outcome_links": len(scored),
        "distinct_scored_paragraphs": len({r["paragraph_id"] for r in scored}),
        "scored_outcome_codes": counts(scored, "AI_alignment_score"),
        "unscored_outcome_links": len(outcome_links) - len(scored),
        "separate_20_passage_curriculum_pilot_blank_means_unassigned":
            counts(read_table("curriculum_pilot.csv"), "reviewed_score"),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
