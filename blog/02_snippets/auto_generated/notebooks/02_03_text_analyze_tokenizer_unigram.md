# Объяснение кода для токенизации текста методом unigram
Данный код производит токенизацию текстового файла (разбиение текста на отдельные элементы - токены). В качестве модели для разбиения используется метод unigram.


```python
import os

from tokenizers import Tokenizer
from tokenizers.models import Unigram
from tokenizers.trainers import UnigramTrainer

tokenizer = Tokenizer(Unigram())
```
Первым делом мы импортируем нужные нам библиотеки и создаем экземпляр Unigram токенизатора.

```python
...
custom_tokens = [ ... ]

tokenizer.add_tokens(custom_tokens)

vocab_size = 30000

trainer = UnigramTrainer(
    vocab_size=vocab_size,
    special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"],
    show_progress=True,
    unk_token='UNK'
)
```
Перед обучением токенизатора мы добавляем кастомные токены и создаем экземпляр тренера для настройки параметров обучения и обучения токенизатора.

```python
file_dir = '../data/processed/word_freqs'
file_name = 'freq_1000000_oshhamaho.txt'
file_path = os.path.join(file_dir, file_name)

tokenizer.train([file_path], trainer)
```
В этом блоке мы указываем путь к файлу, который будем использовать для обучения токенизатора, и запускаем процесс обучения.

```python
tokenizer_dir = '../data/processed/tokenizer'
tokenizer_file_name = f'words_unigram_{vocab_size}.tokenizer.json'
tokenizer_file_path = os.path.join(tokenizer_dir, tokenizer_file_name)
tokenizer.save(tokenizer_file_path, pretty=True)
```
После обучения токенизатора мы сохраняем его в файл, чтобы иметь возможность использовать его позже без необходимости повторного обучения.

```python
encoded = tokenizer.encode('ЦӀыхум и гум удыхьэн папщӀэ, абы и бгъэр зэгуэбгъэжын хуейкъым.')
print(encoded.tokens)
```
Этот код проверяет работоспособность токенизатора. Мы берем пример текста и смотрим, как он будет разбит на токены.

```python
for word in test_words:
    print(tokenizer.encode(word).tokens)
```
Этот код проверяет работоспособность токенизатора на серии тестовых слов.

Таким образом, мы создали Unigram токенизатор, обучили его и проверили его работу на примерах.