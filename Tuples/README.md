# Extract Tuples from Project Gutenberg books according to defined dependency--parse patterns

see [configs](https://github.com/ryanbrate/LREC_2024_submission/blob/main/Tuples/configs.json)

Pipeline.py does several things:

- It reads configs.json, iterating through each config in turn (Note: for each config, n\_processes is specified). For each config:

    - a list of file paths for missing books, i.e., input\_dir - output\_dir, is identified;
    - whether n\_processes is 1 or more: fps\_lists dir is created, and populated with sub-lists of missing book fps wrt., each specified process. If fps\_lists dir contains sublists matching number of specified threads, then 

if n\_processes == 1, run:
```
python3 pipeline.py
```

if n\_processes>1, run in separate terminals:
```
python3 pipeline.py 1
```
Note: this first run, builds the sub-lists





