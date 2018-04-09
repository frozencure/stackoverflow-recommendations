import sqlite3
from collaborativeFiltering.SparseDataframe import SparseDataframe

db = sqlite3.connect('recommenderDb.sqlite')
cursor = db.cursor()

def setupTables():
    cursor.execute('''
        CREATE TABLE user(id INTEGER PRIMARY KEY UNIQUE);
    ''')
    cursor.execute('''
        CREATE TABLE question(id INTEGER PRIMARY KEY UNIQUE);
    ''')
    db.commit()
    cursor.execute('''
        CREATE TABLE vote(id INTEGER PRIMARY KEY AUTOINCREMENT,
                        userId INTEGER NOT NULL,
                        questionId INTEGER NOT NULL,
                        voteValue INTEGER,
                        FOREIGN KEY(userId) REFERENCES user(id),
                        FOREIGN KEY(questionId) REFERENCES question(id));
    ''')
    db.commit()


def insertUsers(userIds):
    cursor.executemany(''' INSERT INTO user(id) VALUES(?);''', userIds)
    db.commit()

def insertQuestions(questionIds):
    cursor.executemany(''' INSERT INTO question(id) VALUES(?);''', questionIds)
    db.commit()

def insertVotes(votes):
    """votes contains: userId, questionId and vote"""
    cursor.executemany(''' INSERT INTO vote(questionId, userId, voteValue) VALUES(?,?,?);''', votes)
    db.commit()

setupTables()

path = 'C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources/FilteredVotes.csv'
sparseDf = SparseDataframe(csvPath=path)
uniqueUsers = [(x,) for x in sparseDf.uniqueUsers]
uniqueItems = [(x,) for x in sparseDf.uniqueItems]

insertUsers(uniqueUsers)
insertQuestions(uniqueItems)

columns = sparseDf.columns
votesArr = sparseDf.dataframe[[columns[0], columns[1], columns[2]]]
votes = [tuple(x) for x in votesArr.values]
insertVotes(votes)
