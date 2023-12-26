# Сниппет: Создание токенизатора с помощью BPE
В этом сниппете мы будем создавать токенизатор, использующий подход Byte Pair Encoding (BPE) для обучения на конкретном текстовом файле. 

## Что такое BPE?
BPE - это метод, который позволяет сжимать текст без потери информации. Обучение на BPE позволяет токенизатору делить слова на подслова, если они редкие или вообще не встречались в учебном материале.

```python
import os

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer

tokenizer = Tokenizer(BPE())
```

Сначала мы импортируем необходимые модули и создаем токенизатор BPE.

```python
custom_tokens = [
    # кастомные токены
]

tokenizer.add_tokens(custom_tokens)
```

Мы можем добавить кастомные токены, которые не должны быть разделены на подслова.

```python
vocab_size = 100000

trainer = BpeTrainer(
    vocab_size=vocab_size,
    special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"],
    show_progress=True,
)
```

Создаем тренер BPE, указываем размер словаря и специальные токены. 

```python
file_path = os.path.join(file_dir, file_name)

tokenizer.train([file_path], trainer)
```

Тренируем токенизатор на нашем файле.

```python
tokenizer_dir = '../data/processed/tokenizer'
tokenizer_file_name = f'bpe_{vocab_size}.tokenizer.json'
tokenizer_file_path = os.path.join(tokenizer_dir, tokenizer_file_name)

tokenizer.save(tokenizer_file_path, pretty=True)
```

Сохраняем обученный токенизатор в файл.

```python
encoded = tokenizer.encode('Текст для токенизации.')
print(encoded.tokens)
```

Используем токенизатор для преобразования текста в последовательность токенов.

Применяя процедуру описанную выше, вы можете создавать настраиваемые токенизаторы, которые будут эффективно работать с вашими конкретными текстовыми данными.