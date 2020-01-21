import sqlite3
from app import app

conn = sqlite3.connect(app.database_url)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='users'")
if cursor.fetchone()[0] == 0:
	cursor.executescript("""
		CREATE TABLE "users" (
			"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
			"username"	TEXT NOT NULL,
			"password"	TEXT NOT NULL,
			"last_survey"		INTEGER DEFAULT 0
		);

		CREATE TABLE "questions" (
			"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
			"quest"	TEXT NOT NULL,
			"type"	TEXT NOT NULL,
			"answer" TEXT NOT NULL
		);

		CREATE TABLE "answers" (
			"question_id"	INTEGER NOT NULL,
			"name"	TEXT NOT NULL,
			"value"	TEXT NOT NULL
		);

		CREATE TABLE "results" (
			"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
			"user_id"	INTEGER,
			"last_survey"	INTEGER,
			"question"	INTEGER
		);

		CREATE TABLE "ans" (
			"result_id"	INTEGER,
			"value"	TEXT
		);
	""")
	
	questions = [
		(1,'Правильное ударение "премирова́ть"', 'default', 'Да; '),
		(2,'Выберите правильное ударение', 'radio', 'алкого́ль; '),
		(3,'Выберите пары слов с правильными ударениями', 'checkbox', 'бензопрово́д и водопрово́д; аэропо́ртов и букси́ровать; ')
	]

	cursor.executemany("INSERT INTO questions (id, quest, type, answer) VALUES (?,?,?,?);", questions)

	answers = [
		(2,'v1', 'а́лкоголь'),
		(2,'v2', 'алко́голь'),
		(2,'v3', 'алкого́ль'),
		(3,'v1', 'алфави́т и аристократи́я'),
		(3,'v2', 'ба́лованный и ба́ловать'),
		(3,'v3', 'бензопрово́д и водопрово́д'),
		(3,'v4', 'аэропо́ртов и букси́ровать'),
		(3,'v5', 'газопро́вод и втри́дорога')
	]

	cursor.executemany("INSERT INTO answers (question_id, name, value) VALUES (?,?,?);", answers)
	conn.commit()