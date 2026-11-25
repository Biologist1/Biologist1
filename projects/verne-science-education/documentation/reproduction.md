# Reproducing and reapplying the Verne study

The analytical unit is one paragraph. Paragraph IDs remain stable across the archived corpus, screening records and pilot decisions. At outcome level, a record is a paragraph–curriculum outcome pair.

## From the source workbooks to the published counts

1. From the project directory, run `python verify_results.py`. It reads the eight CSV tables in [data](../data/) using only the Python standard library. Compare the JSON it prints with [the archived calculation](../results/result_counts.json).
2. To rebuild the CSVs, install `openpyxl` and run `python scripts/export_records.py --output rebuilt_csv` in the same directory. The script names each input workbook and sheet explicitly. A new or empty output directory keeps the published files intact.
3. To redraw the supplementary figures, install `matplotlib` and run `python scripts/plot_supplement.py --output rebuilt_figures`. The script uses the archived result counts.

| Record | Interpretation |
| --- | --- |
| [paragraphs.csv](../data/paragraphs.csv) | English source text for each of the 1,680 paragraph IDs. The paragraph number follows the source workbook. |
| [screening.csv](../data/screening.csv) | Both original candidate searches, candidate themes, the rule-based code, the code used in the combined manuscript version, its provenance, the later automated code and observed term hits. Overlapping theme memberships are retained. |
| [pilot.csv](../data/pilot.csv) | Sampling stratum, the researcher’s initial blind code, a separate AI suggestion, the rule-based code, the final reviewed code and the recorded rationale. The pilot includes six passages from each of five candidate groups and 20 keyword nonmatches. Its recorded sampling seed is 20261015. |
| [observed_rule_terms.csv](../data/observed_rule_terms.csv) | The 131 distinct strings that occurred in the specific-term hits column of the downstream rule-coding workbook, with counts. |
| [curriculum_units.csv](../data/curriculum_units.csv) and [unit_links.csv](../data/unit_links.csv) | The curriculum inventory of 44 units comprising 182 listed outcomes and the 976 candidate unit links found in 437 different paragraphs. |
| [outcome_links.csv](../data/outcome_links.csv) | The 86 proposed links to four selected outcomes in 84 paragraphs. AI contextual scores are recorded for 62 links in 60 paragraphs. An empty score marks one of the 24 unscored pairs. |
| [curriculum_pilot.csv](../data/curriculum_pilot.csv) | The separate 20-passage curriculum pilot, including unassigned records. |

The initial rule-based pass assigned 148 direct, 495 indirect and 1,037 absent codes. The combined preliminary distribution used in the manuscript has 162 direct, 474 indirect and 1,044 absent codes. It retains 1,570 rule codes, 60 priority-passage AI codes and 50 researcher-reviewed pilot codes. A subsequent automated pass is archived in a separate column. The reported pilot percentage compares the rule-based pre-code and the final reviewed code in the same 50 paragraphs.

## Apply the workflow to another corpus

The [author’s original notebook](../NLP_Odev1_Gulsum_Meco.ipynb) retrieves Project Gutenberg eBook 164 and performs lexical preprocessing, frequency and n-gram analysis, word-cloud generation and report export. To inspect its recorded plots, open [the executed copy](../reports/NLP_Odev1_Gulsum_Meco_with_outputs.ipynb). The student's identifier has been removed from the public notebook and report copies. The executed copy retains the plots and numeric outputs. Colab’s browser download callbacks were omitted.

The [reference screening script](../screen_new_corpus.py) and [teaching dictionary](../example_dictionary.csv) were prepared after the study. From the project directory, this command runs the six-sentence example and creates the match table, a blind coding sheet and a separate sampling key.

```sh
python screen_new_corpus.py --paragraphs example_paragraphs.csv --dictionary example_dictionary.csv --per-group 1 --nonmatches 1 --output demo_screen
```

The example yields five candidates and six pilot rows. For your own corpus, supply UTF-8 data with the fields `paragraph_id,text`, edit a copy of the dictionary and set sample sizes appropriate to your corpus. The four Turkish instructions transcribed from the author’s manuscript, their English translations, the coding criteria and two new contextual prompt templates are in the [coding guide](method_and_prompts.md). The workbook records support exact recalculation of the reported counts. Re-executing every historical AI interaction would require the full conversation record and the original model configuration.

## Sources and file versions

The [workbook index](workbook_index.csv) lists every supplied workbook filename, its sheet names and a content hash. Where two differently named files have identical bytes, the same hash identifies them. The [file inventory](file_manifest.csv) includes the sizes and SHA-256 hashes of the public files except the inventory itself.

The source edition is Jules Verne’s *Twenty Thousand Leagues under the Sea*, [Project Gutenberg eBook 164](https://www.gutenberg.org/ebooks/164). [Project Gutenberg terms of use](https://www.gutenberg.org/policy/license.html). The curriculum is the [Türkiye Century Maarif Model Science Course Curriculum](https://tymm.meb.gov.tr/upload/program/2024programfen345678Onayli.pdf).

## Compiling the publication files

The [publication scripts](../scripts/publication/) were prepared during revision. They document how the archived English Word manuscript, translated figure labels, extended abstract and author response were produced. To build into a separate folder from the project root, run the commands below. The figure translation uses Pillow with the Linux Liberation Serif and DejaVu Sans fonts. The Word scripts use lxml and python-docx.

```sh
python scripts/publication/translate_manuscript_figures.py --output build/manuscript-figures
python scripts/publication/revise_full_paper.py --figures build/manuscript-figures --output build/revised_full_manuscript.docx
python scripts/publication/build_conference_documents.py --output build/conference
```
