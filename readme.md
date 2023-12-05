# Интерпретатор Piet

v1.0

**Автор:** Карпов Виталий (vitvit0312@gmail.com)


## Описание

Данное приложение является реализацией интерпретатора языка Piet -
эзотерического языка программирования, кодом которого являются
разноцветные изображения.


## Требования

* Python версии не ниже 3.10

### Использованные пакеты

* argparse
* enum
* operator
* os
* PIL
* unittest
* sys


## Состав

* Запускаемый файл: `piet_interpreter_task.py`
* Модули: `piet_vitvit/`
* Тесты: `piet_vitvit_tests/`


## Запуск

Справка по запуску: `./piet_interpreter_task.py -h`

Пример запуска: `./piet_interpreter_task.py -s 64 -l 200000 -din -dvm C:\vitvit_files\example.png`  
*(порядок, в котором указываются параметры, не важен)*
