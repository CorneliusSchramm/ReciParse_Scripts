`Converting to .spacy:`   

```python
python -m spacy convert "data/train.json" "data"
```

`Training:`

```python
python -m spacy train "config.cfg" --output "models" --code scripts/functions.py
```

`Evaluate:`

```python
python -m spacy evaluate "models/model-best" "data/test.spacy" --code scripts/functions.py
```