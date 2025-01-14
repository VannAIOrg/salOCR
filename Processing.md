
- **Following is an example of the how the bulk.py file (in salOCR directory) processes the PDFs stored in a folder.**
- **In this example, a folder called "HindiBooks" containing 20 hindi pdf files was stored in the salOCR directory**
- **The processing was initiated with :**
    python main.py


Result:
1. Average time taken to process each page was about 5 seconds
2. PDFs with only text showed the best results, while PDFs with some images or illustrations was processed very poorly - #TODO
3. The accuracy of the conversion was quite high - no quantitative analysis on the results was done, this is an estimate from eyballing the resultant output text

TODO:
1. Improve PDF to text for files with images and illustrations
2. Improve conversion of files that have 'old' hindi alphabet prints symbols
3. Make the ouput cleaner if the input file has too much noise
4. Parallel processing to speed up the pdf to text conversion


#_____________________________________________________________________________________
Folder Name: HindiBooks (stored in salOCR directory)
No. of PDFs = 20

#_____________________________________________________________________________________

Processing PDF 1 of 20: karmbhumi.pdf ## Slow processing 'cz computer was on sleep mode for almost 20-30 min
Processing Pages for karmbhumi.pdf: 100%|███████████████████████████████████████████████████████████████████████████████████████| 279/279 [44:22<00:00,  9.54s/it]
Processing PDF 2 of 20: daur-mamta-kalia.pdf
Processing Pages for daur-mamta-kalia.pdf: 100%|██████████████████████████████████████████████████████████████████████████████████| 46/46 [03:31<00:00,  4.60s/it]
Processing PDF 3 of 20: Ekgadhekivapsi-KrishnChandar.pdf
Processing Pages for Ekgadhekivapsi-KrishnChandar.pdf: 100%|██████████████████████████████████████████████████████████████████████| 10/10 [00:46<00:00,  4.65s/it]
Processing PDF 4 of 20: devdas-sharat.pdf
Processing Pages for devdas-sharat.pdf: 100%|█████████████████████████████████████████████████████████████████████████████████████| 72/72 [04:53<00:00,  4.07s/it]
Processing PDF 5 of 20: Juari The Gambler Dostoevsky.pdf
Processing Pages for Juari The Gambler Dostoevsky.pdf: 100%|████████████████████████████████████████████████████████████████████| 154/154 [09:38<00:00,  3.75s/it]
Processing PDF 6 of 20: SambhogSeSmadhiKiAur.pdf
Processing Pages for SambhogSeSmadhiKiAur.pdf: 100%|████████████████████████████████████████████████████████████████████████████| 438/438 [30:09<00:00,  4.13s/it]
Processing PDF 7 of 20: Durgeshnandini.pdf
Processing Pages for Durgeshnandini.pdf: 100%|████████████████████████████████████████████████████████████████████████████████████| 85/85 [04:13<00:00,  2.98s/it]
Processing PDF 8 of 20: nirmala.pdf
Processing Pages for nirmala.pdf: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 123/123 [09:59<00:00,  4.88s/it]
Processing PDF 9 of 20: Anuradha.pdf
Processing Pages for Anuradha.pdf: 100%|██████████████████████████████████████████████████████████████████████████████████████████| 44/44 [02:08<00:00,  2.92s/it]
Processing PDF 10 of 20: Ramji-Jaag-Utha.pdf
Processing Pages for Ramji-Jaag-Utha.pdf: 100%|███████████████████████████████████████████████████████████████████████████████████| 32/32 [05:34<00:00, 10.46s/it]
Processing PDF 11 of 20: AnimalFarm.pdf
Processing Pages for AnimalFarm.pdf: 100%|████████████████████████████████████████████████████████████████████████████████████████| 69/69 [05:33<00:00,  4.83s/it]
Processing PDF 12 of 20: gaban.pdf
Processing Pages for gaban.pdf: 100%|███████████████████████████████████████████████████████████████████████████████████████████| 234/234 [18:04<00:00,  4.63s/it]
Processing PDF 13 of 20: Aparadh-aur-dand-fyodor-dostoveyaski.hindibookspdf.com.pdf
Processing Pages for Aparadh-aur-dand-fyodor-dostoveyaski.hindibookspdf.com.pdf: 100%|██████████████████████████████████████████| 581/581 [39:07<00:00,  4.04s/it]
Processing PDF 14 of 20: aanandmath.pdf
Processing Pages for aanandmath.pdf: 100%|████████████████████████████████████████████████████████████████████████████████████████| 78/78 [05:43<00:00,  4.41s/it]
Processing PDF 15 of 20: sherlock.pdf
Processing Pages for sherlock.pdf: 100%|██████████████████████████████████████████████████████████████████████████████████████████| 88/88 [06:58<00:00,  4.75s/it]
Processing PDF 16 of 20: Grihdah.pdf
Processing Pages for Grihdah.pdf: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 321/321 [15:37<00:00,  2.92s/it]
Processing PDF 17 of 20: dukkham-sukkham-mamta-kalia.pdf
Processing Pages for dukkham-sukkham-mamta-kalia.pdf: 100%|█████████████████████████████████████████████████████████████████████| 221/221 [15:07<00:00,  4.11s/it]
Processing PDF 18 of 20: Manjhali Didi .pdf
Processing Pages for Manjhali Didi .pdf: 100%|████████████████████████████████████████████████████████████████████████████████████| 39/39 [01:56<00:00,  2.99s/it]
Processing PDF 19 of 20: Brahman Ki Beti.pdf
Processing Pages for Brahman Ki Beti.pdf: 100%|███████████████████████████████████████████████████████████████████████████████████| 94/94 [04:51<00:00,  3.10s/it]
Processing PDF 20 of 20: katra-dar-katra-sampurna.pdf
Processing Pages for katra-dar-katra-sampurna.pdf: 100%|██████████████████████████████████████████████████████████████████████████| 70/70 [04:03<00:00,  3.47s/it]
Saved: HindiBooks/combined_text_f20/combined_text_f20.txt

--- Processing Complete ---
Total PDFs processed: 20
PDF Names: karmbhumi.pdf, daur-mamta-kalia.pdf, Ekgadhekivapsi-KrishnChandar.pdf, devdas-sharat.pdf, Juari The Gambler Dostoevsky.pdf, SambhogSeSmadhiKiAur.pdf, Durgeshnandini.pdf, nirmala.pdf, Anuradha.pdf, Ramji-Jaag-Utha.pdf, AnimalFarm.pdf, gaban.pdf, Aparadh-aur-dand-fyodor-dostoveyaski.hindibookspdf.com.pdf, aanandmath.pdf, sherlock.pdf, Grihdah.pdf, dukkham-sukkham-mamta-kalia.pdf, Manjhali Didi .pdf, Brahman Ki Beti.pdf, katra-dar-katra-sampurna.pdf
Total word count: 1,296,897

#_____________________________________________________________________________________
