import sqlite3
import hashlib

class Users:
 
    def __init__(self, db, session):
        self.db = db
        self.session = session
        self.errors = None
        if 'username' in session:
            conn = sqlite3.connect(self.db)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            sql = "SELECT id FROM users WHERE username=?"
            cursor.execute(sql, session['username'])
            if cursor.fetchone() == None:
                self.session.clear()
                self.id=None
                self.username=None
                self.last_survey=0
            else:
                self.id=session['id']
                self.username=session['username']
                self.last_survey=session['last_survey']
        else:
            self.id=None
            self.username=None
            self.last_survey=0
        if 'next_question' in session:
            self.next_question=session['next_question']
        else:
            self.next_question=0
        
    def getUsername(self):
        return self.username
    
    def login(self, username, password):
        temp_password = password+'salt'
        hash_password = hashlib.md5(temp_password.encode()).hexdigest()
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = "SELECT id FROM users WHERE username=?"
        cursor.execute(sql, [username])
        if cursor.fetchone() == None:
            cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", [username, hash_password])
            conn.commit()
            self.session['id'] = cursor.lastrowid
            self.session['username'] = username
            self.session['last_survey'] = 0
        else:
            sql = "SELECT id, username, last_survey FROM users WHERE username=? AND password=?"
            cursor.execute(sql, [username, hash_password])
            result = cursor.fetchone()
            if result == None:
                self.errors = 'Password error'
                return False
            self.session['id'] = result['id']
            self.session['username'] = result['username']
            self.session['last_survey'] = result['last_survey']
        return True

    def getNextQuestion(self):
        return self.next_question
    def getErrors(self):
        return self.errors
    def getLastSurvey(self):
        return self.last_survey
