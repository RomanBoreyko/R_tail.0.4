print("Скрипт стартовал")

import os

# Задаём рабочую папку и имя итогового файла
folder = r'c:\Users\User\Documents\r-note03\tachmap'
output_file = os.path.join(folder, 'result.md')

try:
    # Список файлов, которые не должны попадать в сборку
    exclude = ['result.md', 'README.md', 'туду.md', 'Голосарий.md']

    # Получаем список всех .md файлов, кроме исключённых
    files = [f for f in os.listdir(folder) if f.endswith('.md') and f not in exclude]
    files.sort()
    print("Найдено файлов:", files)

    toc = []       # Список для оглавления
    chapters = []  # Список для глав

    # Формируем главы и оглавление
    for idx, filename in enumerate(files, 1):
        print(f"Обрабатывается файл: {filename}")
        path = os.path.join(folder, filename)
        with open(path, encoding='utf-8') as f:
            lines = f.readlines()
        title = None
        # Ищем первый заголовок в файле для оглавления
        for line in lines:
            if line.strip().startswith('#'):
                title = line.strip().lstrip('#').strip()
                break
        if not title:
            title = filename
        toc.append(f"{idx}. {title}")
        # chapters.append(f"\n\n# Глава {idx}: {title}\n\n" + ''.join(lines))
        # Стало:
        chapters.append('\n' + ''.join(lines))

    # Открываем итоговый файл для записи
    with open(output_file, 'w', encoding='utf-8') as out:
        # Записываем оглавление
        out.write("# Содержание\n\n")
        for item in toc:
            out.write(item + '\n')
        out.write('\n---\n')
        # Записываем главы
        for chapter in chapters:
            out.write(chapter)
            out.write('\n\n---\n')

        # --- Добавляем глоссарий в конец файла ---
        glossary_path = os.path.join(folder, 'Голосарий.md')
        if os.path.exists(glossary_path):
            out.write('\n\n---\n')
            # out.write('## Глоссарий и перекрёстные ссылки\n\n')
            with open(glossary_path, encoding='utf-8') as gloss:
                lines = gloss.readlines()
                # Если первая строка — заголовок, пропускаем её
                if lines and lines[0].strip().startswith('##'):
                    lines = lines[1:]
                out.writelines(lines)

    # Сообщаем об успешном завершении
    print(f"Склейка завершена! Итоговый файл: {output_file}")

except Exception as e:
    # Выводим ошибку, если что-то пошло не так
    print("Ошибка:", e)