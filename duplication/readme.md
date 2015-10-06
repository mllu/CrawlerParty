Install distance, PIL first
```
pip install PIL
pip install distance
```
Then
```
python duplicate.py path is_exact
```
The argument path should be containing the path that holds all image files. It can read recursively.
The is_exact should be "true" or "false" to indicate whether we are detecting exact_duplicate or near_duplicate.
