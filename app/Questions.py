import sqlite3

class Questions:
 
    def __init__(self, db, session):
        self.db = db
        self.session = session
        
    def getQuestion(self, id):
        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        sql = "SELECT * FROM questions WHERE id=?"
        cursor.execute(sql, [id])
        temp = cursor.fetchall()
        if temp == []:
            return False
        question = [dict(row) for row in temp][0]
        if question['type'] != 'default':
            sql = "SELECT name, value FROM answers WHERE question_id=?"
            cursor.execute(sql, [id])
            question['answers']=[dict(row) for row in cursor.fetchall()]
        return question

    def setAnswer(self, id, answer):
        self.session['next_question']=id+1
        temp = []
        if 'answers' in self.session:
            temp = self.session['answers']
        temp.append({'question_id': id, 'answer': answer.getlist(str(id))})
        self.session['answers']=temp
        return True

    def setFinish(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        for question in self.session['answers']:
            cursor.execute("INSERT INTO results (user_id, last_survey, question) VALUES (?,?,?)", [self.session['id'], self.session['last_survey'],question['question_id']])
            result_id=cursor.lastrowid
            for ans in question['answer']:
                cursor.execute("INSERT INTO ans (result_id, value) VALUES (?,?)", [result_id,ans])

        cursor.execute("UPDATE users SET last_survey=+1 WHERE id=?", [self.session['id']])
        conn.commit()
        self.session['last_survey']+=1
        self.session['answers']=[]
        self.session['next_question']=0
        return True

    def getResults(self):
        result = []
        temp_result=[]
        temp_last=0

        conn = sqlite3.connect(self.db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT r.id, r.last_survey, q.answer `answer_true`, q.quest, q.id `q_id` FROM results r INNER JOIN questions q ON q.id = r.question WHERE user_id=?", [self.session['id']])
        temp = cursor.fetchall()
        if temp == []:
            return []
        temp=[dict(row) for row in temp]
        for ans in temp:
            if temp_last != ans['last_survey']:
                temp_last = ans['last_survey']
                result.append(temp_result)
                temp_result=[]
            answer = ''
            temp_q_id = None
            cursor.execute("SELECT value FROM ans WHERE result_id=?", [ans['id']])
            question_ans = [dict(row) for row in cursor.fetchall()]
            for one_ans in question_ans:
                if temp_q_id != ans['q_id']:
                    temp_q_id=ans['q_id']
                    answer = ''
                cursor.execute("SELECT value FROM answers WHERE question_id=? AND name=?", [ans['q_id'],one_ans['value']])
                quest = one_ans['value']
                for row in cursor.fetchall():
                    quest=dict(row)['value']
                answer+=quest + '; '
            temp_result.append({'question': ans['quest'], 'answer': answer, 'answer_true': ans['answer_true']})
        result.append(temp_result)  
        return result