# COHA_to_googlengram
Converts the COHA corpus to the same form as the google ngram corpus.

To make an ngram of length 20 from the word mouse simply enter the path
of all the files you want converted into a file, then run:

```python
python3 convert.py 20 mouse file.txt True
```

The files will be in the Converted_files folder

If you want to give it a directory of files and sub folders with files to convert
then you should enter

```python3
python3 convert.py 20 mouse /User/Jdoe/files
```
