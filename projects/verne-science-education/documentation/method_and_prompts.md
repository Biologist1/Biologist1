# Coding guide and AI instructions

## The four instructions documented in the Turkish manuscript

The Turkish text below is transcribed from the author’s manuscript. The English text translates it for readers. These are manuscript-reported instructions for generating Python code. The original work used ChatGPT and Python in Google Colab. The specific ChatGPT model snapshot, generation parameters and full conversational exchanges were not recorded in the materials available for this revision.

### 1. Prepare the paragraph corpus

Turkish

> Dosyadaki roman dışı açıklamaları ve içindekiler bölümünü çıkar; kalan metni paragraflara ayır ve her paragrafa numara ver

English translation

> Remove the material outside the novel and the table of contents from the file. Divide the remaining text into paragraphs and give each paragraph a number.

### 2. Normalize a separate copy

Turkish

> Metnin bir kopyasında harfleri küçült, metni sözcüklere ayır, üç harften kısa sözcükleri ve the, and, was gibi sık kullanılan yardımcı sözcükleri çıkar; PorterStemmer ile sözcüklerin farklı biçimlerini ortak köklerde birleştir

English translation

> On a copy of the text, lowercase the letters and split the text into words. Remove words shorter than three letters and frequent function words (for example, “the”, “and”, “was”). Use PorterStemmer to reduce different word forms to common stems.

### 3. Search the original wording

Turkish

> Bu sözcükleri özgün paragraflarda ara; bulunan sözcükleri ve ilgili temaları kaydet

English translation

> Search the original paragraphs for these words and record the words found and their associated themes.

### 4. Export both hits and misses

Turkish

> Paragraf numarası, özgün metin, bulunan anahtar sözcükler ve tema bilgilerini bir tabloya aktar; eşleşme bulunmayan paragrafları da koru

English translation

> Transfer the paragraph number, original text, matched keywords and themes to a table. Retain paragraphs with no match.

## Paragraph coding guide

| Code | Decision | Case from the pilot |
| --- | --- | --- |
| 0 | The term is incidental, figurative or confined to character dialogue, with no substantive science content. | P932 asks about fear of sharks. |
| 1 | A relevant entity, phenomenon or process is mentioned without a concrete scientific observation or explanation. | P1201 mentions weather conditions in the narrative. |
| 2 | The passage gives a concrete observation, measurement, classification, description of a process, or causal explanation. | P921 gives evidence about pearl formation and composition. |

The pilot worksheets preserve the researcher’s original blind code, the separate contextual AI suggestion, and the researcher’s final decision. A rule-based pre-code is stored in its own field. For disagreements, inspect the full paragraph and identify the wording that meets a criterion.

## Curriculum alignment guide

Use one row per paragraph–outcome pair. Read both the topic and the cognitive action in the official wording. Assign 0 if the proposed relationship is unsupported, 1 for a partial topic or skill connection, and 2 for a direct conceptual relationship to the specified concept or process. Keep unreviewed pairs blank. A suggested teaching activity can ask students to perform an action that a fictional passage itself only illustrates.

## Templates for a new application

The next two prompts reconstruct the tasks described in the manuscript. They are new reusable wording. The verbatim historical conversations for these stages are unavailable.

### Contextual science coding

**Turkish**

> Aşağıdaki paragrafı bir bütün olarak oku. Fen içeriğini kodlama rehberindeki 0, 1 veya 2 ölçütüyle değerlendir. Paragraf kimliğini, önerdiğin kodu, ilgili fen temasını ve kararı destekleyen kısa bir metin parçasını yaz. Bir cümleyle gerekçelendir. Bağlam kararı vermeye yetmiyorsa bunu ayrıca belirt. Paragraf kimliği: [kimlik]. Paragraf: [özgün metin]. Kodlama rehberi: [ölçütler].

**English**

> Read the whole paragraph and apply the 0, 1 and 2 criteria in the coding guide. Return its ID, proposed code, theme, a short piece of textual evidence and a one-sentence justification. Flag cases that need more context. Paragraph ID: [ID]. Paragraph: [original text]. Coding guide: [criteria].

### Paragraph–outcome alignment

**Turkish**

> Özgün paragrafı ve öğrenme çıktısının tam metnini birlikte oku. Çıktıdaki kavramı ve öğrenciden beklenen eylemi belirle. İlişki için 0 (desteklenmiyor), 1 (kısmi) veya 2 (doğrudan kavramsal ilişki) öner. Paragraf kimliğini, çıktı kodunu ve önerinin metne dayalı kısa gerekçesini yaz. Paragraf: [kimlik, metin]. Öğrenme çıktısı: [kod, tam metin].

**English**

> Read the original paragraph and the full learning outcome together. Identify the concept and the action expected of the learner. Propose 0 (unsupported), 1 (partial) or 2 (direct conceptual relationship). Return the paragraph ID, outcome ID and a brief justification grounded in the wording of both. Paragraph: [ID, text]. Learning outcome: [ID, full wording].

For a new run, record the model identifier, date, complete prompt, response and any researcher revision. These records make the proposed interpretation traceable even when another model run supplies a different label.
