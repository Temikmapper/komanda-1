# Веб-сайт для управления бюджетом

## О проекте

Сайт помогает решить следующие цели:

- Контролировать ежедневные траты, отображать текущие свободные средства
- Визуализировать повседневные траты на диаграммах
- Следить за достижением финансовых целей
- Отслеживать регулярные ежемесячные траты
- Копить средства

## Сборка проекта

Требования: Python 3.7+, pip3.

- `git clone https://github.com/Temikmapper77/komanda.git`
- `cd komanda`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip3 install -r komanda/requirements/production.txt`
- `cd komanda`
- `python3 manage.py makemigrations expenses incomes goals piggy monthly`
- `python3 manage.py migrate`
- `python3 manage.py runserver`

## Скриншоты

<details>
<summary>Посмотреть</summary>

### Страница добавления трат

![Добавление траты](README_pics/add_expense.png)

### Список недавно добавленных трат

![10 последних трат](README_pics/expenses_list.png)

### Список добавленных категорий

![Добавленные категории](README_pics/categories_list.png)

### Таблица ежемесячных трат

![Таблица ежемесячных трат](README_pics/monthly_list.png)

### График с ежемесячными тратами

![Добавленные категории](README_pics/monthly_graph.png)

### Страница с финансовой целью

![Страница с финансовой целью](README_pics/goal_view.png)
</details>
