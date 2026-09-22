# 🍽️ Jedzonko

**Jedzonko** to aplikacja webowa służąca do tworzenia przepisów oraz planowania posiłków.

Projekt został wykonany w ramach kursu **Python Developer w Coders Lab** jako projekt zespołowy realizowany zgodnie z metodologią Scrum.

## 📌 O projekcie

Celem projektu było stworzenie aplikacji dla autorki książki kucharskiej, która chce udostępnić swoim czytelnikom narzędzie ułatwiające planowanie codziennych posiłków.

Aplikacja umożliwia przechowywanie przepisów oraz tworzenie na ich podstawie planów żywieniowych.

## ✨ Funkcjonalności

Aplikacja umożliwia m.in.:

* dodawanie i edytowanie przepisów,
* przeglądanie zapisanych przepisów,
* określanie składników i sposobu przygotowania,
* tworzenie planów posiłków,
* przypisywanie przepisów do konkretnych dni,
* zarządzanie zapisanymi planami i przepisami.

## 🛠️ Technologie

W projekcie wykorzystano:

* **Python**
* **Django**
* **SQL**
* **HTML**
* **CSS**
* **JavaScript**
* **Git**

## 📂 Struktura projektu

```text
scrumlab/
├── scrumlab/        # konfiguracja projektu Django
├── jedzonko/        # główna aplikacja
├── static/          # pliki CSS, JavaScript i grafiki
└── manage.py
```

## ⚙️ Konfiguracja

Dane dostępowe do bazy danych nie są przechowywane w repozytorium.

Konfigurację lokalnej bazy należy umieścić w pliku:

```text
scrumlab/local_settings.py
```

Przykładowa konfiguracja znajduje się w:

```text
scrumlab/local_settings.py.example
```

Po skonfigurowaniu bazy danych należy wykonać migracje:

```bash
python manage.py migrate
```

Następnie aplikację można uruchomić poleceniem:

```bash
python manage.py runserver
```

## 🎓 Informacje o projekcie

Projekt powstał podczas kursu **Python Developer w Coders Lab** i służył praktycznej nauce tworzenia aplikacji webowych w Django oraz pracy zespołowej zgodnie z metodologią Scrum.

Materiały startowe oraz warstwa wizualna projektu zostały dostarczone przez Coders Lab.

## 👨‍💻 Autor

**Bartek**

Projekt prezentowany jako część mojego portfolio programistycznego.
