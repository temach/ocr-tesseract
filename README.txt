Installed tesseract package.

On ubuntu by default tesseract_fast gets installed.

The models are installed into /usr/local/share/tessdata

View installed language models with:
```
tesseract --list-langs
```

There is a legacy engine (--oem 0) and a new neural LSTM engine (--oem 1).
To run them both pass --oem 2.

The models are:
- tessdata_best - most accurate and slow, can be re-trained
- tessdata_fast - fast and ships by default on ubuntu, etc. 

Download combined models (one file for both --oem 0 and --oem 1 in other words its --oem 2):
https://github.com/tesseract-ocr/tessdata

Download LSTM only (--oem 1) models:
https://github.com/tesseract-ocr/tessdata_best

Place the models into /usr/local/share/tessdata
