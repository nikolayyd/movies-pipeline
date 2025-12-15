# Movies ETL Pipeline

## Описание

Този проект реализира **ETL (Extract, Transform, Load) pipeline** за обработка на Movies dataset. Данните се извличат от CSV файл, почистват се и се трансформират в **нормализирана PostgreSQL схема** чрез SQLAlchemy ORM.

Проектът използва **staging таблица** и множество **many-to-many релации**, характерни за реални data engineering решения.

---

## Технологии

- Python 3.x
- Pandas
- SQLAlchemy
- PostgreSQL

---

## Архитектура и Модели

### Основни таблици

- **MovieStaging** – staging таблица за първоначално зареждане на CSV данните
- **Movie** – основна таблица за филмите
- **Genre, Keyword, Cast, ProductionCompany, ProductionCountry, SpokenLanguage, Crew** – нормализирани справочни таблици

### Асоциативни таблици (Many-to-Many)

- **MovieGenre**
- **MovieKeyword**
- **MovieCast**
- **MovieProductionCompany**
- **MovieProductionCountry**
- **MovieSpokenLanguage**
- **MovieCrew**

Тези таблици управляват връзките между филмите и свързаните с тях атрибути.

---

## ETL Процес

### 1. Extract
- CSV файл → Pandas DataFrame → MovieStaging

### 2. Clean
- Премахване и нормализиране на `None`, `NaN`, `NaT`
- Подготовка на данните за безопасна трансформация

### 3. Transform
- Нормализация на колоните в отделни таблици
- Deduplication чрез `get_or_create` логика
- Поддържане на referential integrity между таблиците

### 4. Load
- Зареждане на трансформираните данни в основните таблици
- Попълване на асоциативните таблици

---

## Idempotency

ETL pipeline-ът е **idempotent** – многократно изпълнение не създава дублиращи записи.

- Таблиците се създават само ако не съществуват
- Справочните записи се проверяват за съществуване преди insert
- Many-to-many връзките се добавят само ако липсват

---

## Стартиране

Инсталиране на зависимостите и пускане на програмата:

```bash
pip install -r requirements.txt
python main.py
