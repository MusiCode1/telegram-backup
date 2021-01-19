# telegram-backup
<div dir="rtl" text-align="right">

גיבוי MySQL לענן של טלגרם.
 - דחיסת הקבצים ב-gzip.
 - תמיכה בפיצול קבצים מעבר ל-2 ג'יגה.
 - עובד באמצעות הזרמה - לא תופס הרבה מקום בזיכרון ה-Ram

הקבצים נשמרים בצורה זמנית על הדיסק הקשיח, היות ואי אפשר להעלות לטלגרם קבצים בלי לדעת את גודלם המדוייק.

## התקנת תלויות:
 - פייתון
 - פייתון-ENV
 - פייתון-pip
 - pipenv

 <div dir="ltr" text-align="left">

    pip install pipenv

<div dir="rtl" text-align="right">

## התקנה (שכפול הפרוייקט):

<div dir="ltr" text-align="left">

    git clone https://github.com/MusiCode1/telegram-backup.git

<div dir="rtl" text-align="right">

התקנת סביבת עבודה של pipenv:

<div dir="ltr" text-align="left">

    pipenv install

<div dir="rtl" text-align="right">

## שימוש

הכנסת הערכים של הריצה:

<div dir="ltr" text-align="left">

    cp .env-exemple .env

<div dir="rtl" text-align="right">

יש לשנות את הפרטים בקובץ `.env`.

<div dir="ltr" text-align="left">

    api_id=156
    api_hash=ytn86ty9umj98u

    db=db_name
    db_user=root
    db_password=1234

    program=C:/xampp/mysql/bin/mysqldump
    entity=5678

    name=my name

<div dir="rtl" text-align="right">

הרצה:

<div dir="ltr" text-align="left">

    pipenv shell

    python ./main.py