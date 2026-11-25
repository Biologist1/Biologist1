"""Rebuild the eight study CSVs. Requires openpyxl."""
from collections import Counter
from pathlib import Path
import csv
from openpyxl import load_workbook

import argparse
parser = argparse.ArgumentParser(description="Extract the study’s archived CSVs from the source workbooks.")
parser.add_argument("--output", type=Path, required=True, help="A new or empty directory for the eight CSV files.")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
workbooks = root / "workbooks"
out = args.output
out.mkdir(parents=True, exist_ok=True)
if any(out.iterdir()):
    parser.error("Choose an empty output directory.")
def rows(filename, sheet):
    wb = load_workbook(workbooks / filename, data_only=True, read_only=True)
    try:
        return list(wb[sheet].values)
    finally:
        wb.close()

def write_csv(filename, header, data):
    with (out / filename).open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(data)

themes = {
    "Doğal çevre ve etkileşim": "Natural environment and interactions",
    "Canlılar ve biyoçeşitlilik": "Living organisms and biodiversity",
    "Bilim ve teknoloji": "Science and technology",
    "Dünya ve Yer Bilimleri": "Earth and geosciences",
    "Ek fen taraması": "Supplementary science search",
}
sources_of_code = {
    "Regex/anahtar sözcük + kural tabanlı otomatik ön kod": "rule",
    "AI bağlamsal incelemesi — henüz araştırmacı onayı yok": "AI contextual review",
    "Pilot araştırmacı uzlaşı kodu": "researcher-reviewed pilot",
}
def keyed(data, position):
    result = {}
    for row in data:
        if len(row) <= position or not isinstance(row[position], int):
            continue
        key = row[position]
        assert key not in result, key
        result[key] = row
    return result

corpus = keyed(rows("Fen_Egitimi_Kesinlestirilmis_Analiz(1).xlsx", "KORPUS_1680")[1:], 0)
combined = keyed(rows("Fen_Egitimi_Tek_Seferlik_Tam_Dogrulama(2).xlsx", "TEK_KONTROL_TABLOSU")[6:], 1)
later = keyed(rows("Fen_Roman_1680_Paragraf_AI_Yeniden_Degerlendirme.xlsx", "TEK_KONTROL_TABLOSU")[6:], 1)
rules = keyed(rows("Fen_NLP_Otomatik_On_Kodlama.xlsx", "TUM_KORPUS")[1:], 0)
primary = keyed(rows("Fen_Tam_Metin_Analizi(2).xlsx", "Aday Paragraflar")[1:], 0)
expanded = keyed(rows("Fen_Genisletilmis_Analiz(2).xlsx", "Aday Paragraflar")[1:], 0)
assert set(corpus) == set(combined) == set(later)
assert set(primary) <= set(expanded) <= set(corpus)
paragraph_rows, code_rows, all_terms = [], [], Counter()
for id_, case in sorted(corpus.items()):
    label = f"P{id_}"
    screened = combined[id_]
    assert screened[2] == case[7] and later[id_][3] == screened[3]
    candidate = id_ in expanded
    assert candidate == (case[1] == "Aday")
    group_names = [themes[x.strip()] for x in case[2].split(",")] if candidate else []
    term_list = [t.strip() for t in str(rules[id_][11] or "").split(",") if t.strip()]
    all_terms.update(set(term_list))
    paragraph_rows.append([label, case[7]])
    code_rows.append([label, int(id_ in primary), int(candidate), "|".join(group_names),
                      case[3], screened[3], sources_of_code[screened[16]], later[id_][19],
                      "|".join(term_list)])
write_csv("paragraphs.csv", ["paragraph_id","text"], paragraph_rows)
write_csv("screening.csv", ["paragraph_id","earlier_candidate","expanded_candidate","candidate_groups",
          "rule_code","combined_code","combined_source","later_code","recorded_rule_term_hits"], code_rows)
write_csv("observed_rule_terms.csv", ["term_as_recorded","paragraphs_with_term_recorded"],
          sorted(all_terms.items(), key=lambda item: (-item[1],item[0])))

pilot = keyed(rows("Fen_Pilot_50_Nihai_Uzlasma(2).xlsx", "KODLAMA")[1:], 1)
selection = keyed(rows("Fen_Pilot_50_Nihai_Uzlasma(2).xlsx", "ORNEKLEM_KAYDI")[1:], 1)
initial = keyed(rows("Fen_Pilot_50_Paragraf_Kodlama(3).xlsx", "KODLAMA")[1:], 1)
pilot_summary = keyed(rows("Fen_Egitimi_Kesinlestirilmis_Analiz(1).xlsx", "PILOT_50")[1:], 0)
assert set(pilot) == set(selection) == set(initial) == set(pilot_summary)
pilot_rows = []
for id_, row in sorted(pilot.items(), key=lambda item:item[1][0]):
    reviewed = pilot_summary[id_]
    assert row[3] == initial[id_][3] == reviewed[1]
    assert row[9] == reviewed[3] and reviewed[2] == corpus[id_][3]
    group = selection[id_][3]
    pilot_rows.append([f"P{id_}", row[0], "no match" if group=="Kontrol" else group, row[3],
                       row[5], reviewed[2], row[9], reviewed[4]])
write_csv("pilot.csv", ["paragraph_id","sample_order","sample_group","initial_blind_code",
          "AI_contextual_suggestion","rule_code","final_reviewed_code","recorded_reason_tr"],pilot_rows)

curr_file = "Fen_Egitimi_60_Baglam_ve_TYMM_Kontrol(1).xlsx"
scored = {(r[1],r[2]):r[4] for r in rows(curr_file,"10_TYMM_INCELEME_60")[1:]
          if r and isinstance(r[0],int)}
proposed = [r for r in rows(curr_file,"05_MAARIF_ON_ADAY")[1:] if r and isinstance(r[0],int)]
assert len({(r[0],r[1]) for r in proposed}) == len(proposed) == 86
assert set(scored) <= {(r[0],r[1]) for r in proposed}
write_csv("outcome_links.csv",["paragraph_id","outcome_id","official_description_tr","AI_alignment_score"],
          [[f"P{r[0]}",r[1],r[2],scored.get((r[0],r[1]))] for r in proposed])
unit_file="Fen_Tum_Maarif_Modeli_44_Unite_182_Cikti_Otomatik_Tarama.xlsx"
units=[r for r in rows(unit_file,"02_44_UNITE_DAGILIMI")[1:] if isinstance(r[0],int)]
write_csv("curriculum_units.csv",["grade","unit_number","unit_title_tr","number_of_listed_outcomes","concept_groups_as_recorded"],
          [[r[0],r[1],r[2],r[3],r[6]] for r in units])
links=[r for r in rows(unit_file,"04_OTOMATIK_TEMATIK_ADAY")[1:] if isinstance(r[0],int)]
write_csv("unit_links.csv",["paragraph_id","grade","unit_number","recorded_evidence_terms"],
          [[f"P{r[0]}",r[1],r[2],r[6]] for r in links])
curr_pilot=rows("Fen_Egitimi_Kesinlestirilmis_Analiz(1).xlsx","MEB_PILOT_20")[1:]
write_csv("curriculum_pilot.csv",["passage_number","screening_word","proposed_outcome","reviewed_score","excerpt_as_recorded"],
          [[r[0],r[2],r[3],r[4] if r[4] in (0,1,2) else "",r[8]] for r in curr_pilot])
