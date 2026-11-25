# NLP-assisted document analysis in science education

Research code for Gülsüm Meço’s study of Jules Verne’s *Twenty Thousand Leagues under the Sea*. The original Colab notebook contains the lexical analysis. The two Python scripts accompany the study and were prepared afterwards to support reuse and verification.

## Run the original analysis in Colab

[Open the author’s notebook in Colab](https://colab.research.google.com/github/Biologist1/Biologist1/blob/main/projects/verne-science-education/NLP_Odev1_Gulsum_Meco.ipynb). Choose **Runtime → Run all**. The notebook retrieves the English text of Project Gutenberg eBook 164, tokenizes it, removes English stopwords and applies Porter stemming. It then calculates word and n-gram frequencies, draws word clouds and produces a PDF report. The text and NLTK stopword list are retrieved online. The original Turkish explanations and analytical code are preserved. Saved cell outputs and the student number in the report heading were removed for public release.

## Try keyword screening on a new text

The example CSV contains six invented sentences. With Python 3.8 or later, download this project folder, open a terminal in it, and run the following command.

```sh
python screen_new_corpus.py --paragraphs example_paragraphs.csv --dictionary example_dictionary.csv --per-group 1 --nonmatches 1 --output demo_screen
```

The example yields five keyword candidates and a six-paragraph pilot. The output includes the matches, a coding sheet without the automated labels, and a separate sampling key. For another text, supply a UTF-8 CSV with the columns `paragraph_id,text`, adapt the dictionary and select sample sizes appropriate to your corpus. The dictionary is a small teaching example. The original five-group search dictionary and complete thematic screening script were not recovered. The reference script uses only the Python standard library.

## Recalculate the reported study counts

`verify_results.py` reads the archived paragraph, screening, pilot and curriculum tables from the study supplement. To reproduce the counts, place its extracted `data/` directory alongside the script and run the command below. The script uses only the Python standard library. The research records are supplied separately from this public code folder.

```sh
python verify_results.py
```

The corpus distribution uses the archived combined preliminary codes. The pilot comparison uses the initial rule-based code and the researcher’s final contextual decision for each sampled paragraph. Each proposed curriculum link is counted once per paragraph and learning outcome.
