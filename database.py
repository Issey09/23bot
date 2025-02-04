import sqlite3
import openpyxl

conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()

# Создание таблицы, если она еще не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class INTEGER NOT NULL,
    class_letter TEXT NOT NULL,
    day TEXT NOT NULL,
    lesson_number INTEGER NOT NULL,
    lesson_name TEXT,
    classroom TEXT
)
''')


def insertData():

    book = openpyxl.load_workbook("расписание 23-24 5-11.xlsx")
    sheet = book.worksheets[-1]

    start1 = ord('C')
    start2 = ord('D')
    k = 3
    for a in range(1, 4):
        currentClass = sheet.cell(row=1, column=k).value
        k += 2
        ceils = sheet[f"{chr(start1).upper()}2": f"{chr(start2).upper()}41"]
        start1 += 2
        start2 += 2
        days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
        num = 1
        day_index = 0
        for lesson, kab  in ceils:


            if (num == 9):
                day_index += 1
                num = 1

            parts = currentClass.split(" ")
            number = parts[0]  # '11'
            letter = parts[1].upper()


            cursor.execute('''
                            INSERT INTO schedule (class, class_letter, day, lesson_number, lesson_name, classroom)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                number,
                letter,
                days_of_week[day_index],
                num,
                lesson.value,
                kab.value
            ))

            num += 1




def getlessons(class_num, class_letter, day):
    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT lesson_number, lesson_name, classroom 
        FROM schedule 
        WHERE class = ? AND class_letter = ? AND day = ?
        ORDER BY lesson_number
    ''', (class_num, class_letter, day))

    schedule = cursor.fetchall()

    conn.close()

    return schedule



# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()