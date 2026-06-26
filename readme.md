# MkDocs-отчёт по лабораторным работам

Это отдельный проект с отчётом для GitHub Pages/MkDocs.

## Локальный запуск

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

Открыть:

```text
http://127.0.0.1:8000/
```

## Сборка HTML

```powershell
mkdocs build
```

## Публикация на GitHub Pages

Перед публикацией нужно заменить `USERNAME/REPOSITORY` в `mkdocs.yml` на свой GitHub-репозиторий.

```powershell
mkdocs gh-deploy
```
