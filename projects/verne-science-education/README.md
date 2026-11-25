# Fen eğitiminde NLP ve yapay zekâ destekli doküman analizi

**Gülsüm Meço** · *Denizler Altında Yirmi Bin Fersah* örneği

Bu arşiv, bir edebî eserde fen içeriği ararken izlenen yöntemi ve araştırmacının kodlama kararlarını belgeliyor. Romanın İngilizce metnindeki 1.680 paragrafın her biri bir kimlik numarasıyla izlenebiliyor. Makale, aynı iş akışını başka metinlere uygulamak isteyen araştırmacılar için hazırlanmıştır.

[Tam makaleyi oku (PDF)](manuscripts/Gulsum_Meco_Revised_Full_Manuscript.pdf) · [Word dosyası](manuscripts/Gulsum_Meco_Revised_Full_Manuscript.docx) · [Özgün defteri Colab’da çalıştır](https://colab.research.google.com/github/Biologist1/Biologist1/blob/main/projects/verne-science-education/NLP_Odev1_Gulsum_Meco.ipynb)

## Araştırma nasıl izlendi?

| İncelemek istediğiniz aşama | Dosya |
| --- | --- |
| Romandaki bir paragrafın özgün İngilizce metni | [Paragraf metinleri ve kimlikleri](data/paragraphs.csv) |
| Bir paragrafı hangi sözcüklerin aramaya dâhil ettiği ve farklı aşamalarda aldığı kod | [Tarama kayıtları](data/screening.csv) · [Kayda geçen 131 eşleşme terimi](data/observed_rule_terms.csv) |
| Araştırmacının kör kodu, yapay zekâ önerisi ve son kararın gerekçesi | [50 paragraflık pilot kodlama tablosu](data/pilot.csv) |
| Romanla öğretim programı arasında kurulan bağlantılar | [Ünite adayları](data/unit_links.csv) · [Kazanım düzeyindeki eşleştirmeler](data/outcome_links.csv) · [Ayrı 20 pasajlık pilot](data/curriculum_pilot.csv) |
| Analizin Excel’de nasıl ilerlediği | [Kaynak çalışma kitapları](workbooks/) · [Dosya ve sayfa adları dizini](documentation/workbook_index.csv) |
| Araçlara verilen yönergeler ve kodların tanımları | [Özgün Türkçe yönergeler, İngilizce karşılıkları ve kodlama ölçütleri](documentation/method_and_prompts.md) |
| Sözcük frekansları, n-gramlar ve kelime bulutları | [Çıktılarıyla Colab defteri](reports/NLP_Odev1_Gulsum_Meco_with_outputs.ipynb) · [Özgün analiz raporu (PDF)](reports/NLP_Odev1_Gulsum_Meco%20%281%29.pdf) |
| Tüm kavram ve pasaj kayıtları | [Etkileşimli HTML raporu](reports/Fen_Tum_Kavram_ve_Pasaj_Kayitlari.html) — dosyayı indirip tarayıcıda açabilirsiniz. |

**Bir kararın izi.** P921’de anlatıcı, incinin kimyasal bileşimini ve nasıl oluştuğunu açıklıyor. Kural tabanlı tarama paragrafa 1 (dolaylı ilişki) verdi. Araştırmacı otomatik etiketi görmeden 2 (doğrudan içerik) verdi. Ayrı yapay zekâ önerisi ve son karar da 2 idi. Pilot tablosunda P921’i arayarak bu dört kaydı ve Türkçe gerekçeyi aynı satırda görebilirsiniz.

## Makaledeki sayıları yeniden hesaplayın

Depoyu indirip proje klasöründe aşağıdaki komutu çalıştırın. Python 3.8 veya üzeri yeterlidir. Betik sekiz CSV’yi okur ve sonucu ekrana yazar.

```sh
git clone --depth 1 https://github.com/Biologist1/Biologist1.git
cd Biologist1/projects/verne-science-education
python verify_results.py
```

[Kaydedilmiş sonuçlarla karşılaştırın.](results/result_counts.json) Genişletilmiş taramada 659 paragraf aday olarak işaretlenmiştir. 50 paragraflık pilotta kural tabanlı ön kod ile araştırmacının nihai kararı 29 paragrafta örtüşmüştür. Her aşamanın kodları tarama ve pilot tablolarında ayrı sütunlardadır.

CSV’leri özgün Excel dosyalarından yeniden üretmek için `openpyxl` kuruluyken `python scripts/export_records.py --output yeni_tablolar` komutunu kullanın. Okuma birimlerini, temaları, kod kaynaklarını ve yeniden uygulama adımlarını [yöntem rehberinde](documentation/reproduction.md) bulabilirsiniz.

## Belgeler ve sürümler

- [Makale taslakları ve önceki Türkçe ve İngilizce sürümler](manuscripts/drafts/)
- [Konferans özetleri ve yazarın hakemlere yanıtı](manuscripts/conference/)
- [Kaynakça dosyası](manuscripts/references/) ve [ayrı indirilebilen Türkçe ve İngilizce şekiller](figures/)
- [Yöntem ve veri eki (ZIP)](supplement/EduAI2027_13803_Methods_and_Data.zip) ve [arşivdeki dosyaların listesi](documentation/file_manifest.csv)

Özgün Colab defteri sözcük düzeyindeki analizi içerir. Tarama ve doğrulama betikleri daha sonra yeniden kullanım için hazırlanmıştır. Tarihsel taramada kullanılan beş grubun eksiksiz orijinal sözlüğü, tam tematik tarama betiği ve ChatGPT görüşmelerinin tam dökümü mevcut arşivde bulunmamaktadır. Çalışma kitaplarında kaydedilmiş eşleşmeler ve kodlama kararları dosyalarıyla birlikte sunulmuştur.

**English.** This research archive accompanies Gülsüm Meço’s study of NLP- and AI-assisted document analysis in science education. The full English manuscript, original workbooks, paragraph-level decisions, curriculum links, code, prompts and figures are available above. The [English reproduction guide](documentation/reproduction.md) explains how to recalculate the reported counts and adapt the procedure to another text.

**Metin kaynağı / Text source.** Jules Verne, *Twenty Thousand Leagues under the Sea*, Project Gutenberg eBook 164. [Eser ve künyesi](https://www.gutenberg.org/ebooks/164) · [Project Gutenberg kullanım koşulları](https://www.gutenberg.org/policy/license.html)
