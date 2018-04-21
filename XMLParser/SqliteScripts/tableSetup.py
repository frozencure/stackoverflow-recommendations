import sqlite3
from XMLParser.xmlParser import XMLParser
import logging


db = sqlite3.connect('recommenderDb.sqlite')
cursor = db.cursor()
TAGS_PATH = "C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources/Tags.xml"
QUESTIONS_PATH = "C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources/Posts.xml"
VOTES_PATH = "C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources/Votes.xml"

def setupTables():
    cursor.execute('''
        CREATE TABLE question(id INTEGER PRIMARY KEY UNIQUE,
                              postTypeId INTEGER NOT NULL,
                              tags TEXT NOT NULL);
    ''')
    logging.info("Created question table")
    cursor.execute('''
        CREATE TABLE tag(id INTEGER PRIMARY KEY UNIQUE,
                          tagname TEXT NOT NULL,
                          subscriber_count INTEGER NOT NULL)''')
    db.commit()
    logging.info("Created tag table")
    cursor.execute('''
        CREATE TABLE vote(id INTEGER PRIMARY KEY AUTOINCREMENT,
                        questionId INTEGER NOT NULL,
                        userId INTEGER NOT NULL,
                        voteTypeId INTEGER,
                        FOREIGN KEY(questionId) REFERENCES question(id));
    ''')
    db.commit()
    logging.info("Created vote table")
    cursor.execute('''
        CREATE TABLE question_tag(id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  questionId INTEGER NOT NULL,
                                  tagId INTEGER NOT NULL,
                                  FOREIGN KEY(questionId) REFERENCES question(id),
                                  FOREIGN KEY(tagId) REFERENCES tag(id))
    ''')
    db.commit()
    logging.info("Created question_tag table")

def insertTags(path):
    parser = XMLParser(path=path, tag="row", elements=['Id', 'TagName', 'Count'])
    query = '''INSERT INTO tag(id, tagname, subscriber_count) VALUES(?,?,?);'''
    parser.parseToSqlite(cursor=cursor, query=query)
    db.commit()
    logging.info("Inserted all tags from xml")

def insertQuestions(path):
    parser = XMLParser(path=path, tag="row", elements=['Id', 'PostTypeId', 'Tags'])
    query = '''INSERT INTO question(id, postTypeId, tags) VALUES(?,?,?);'''
    parser.parseToSqlite(cursor=cursor, query=query, conditionValue="1", conditionIndex=1)
    db.commit()
    logging.info("Inserted all questions from xml")

def insertVotes(path):
    parser = XMLParser(path=path, tag="row", elements=['PostId', 'VoteTypeId', 'UserId'])
    query = '''INSERT INTO vote(questionId, voteTypeId, userId) VALUES(?,?,?);'''
    parser.parseToSqlite(cursor=cursor, query=query, conditionIndex=1, conditionValue="5")
    db.commit()
    logging.info("Inserted all votes from xml")

def removeNotVotedQuestions():
    cursor.execute('''SELECT vote.id FROM vote
                          LEFT JOIN question ON question.id = vote.questionId
                          WHERE question.id IS NULL''')
    unusedVotes = cursor.fetchall()
    for vote in unusedVotes:
        cursor.execute('''DELETE FROM vote WHERE id = (?)''', (vote[0],))
        print('Delete vote: %s' % (vote[0]))
    db.commit()

    cursor.execute('''SELECT question.id FROM question
                    LEFT JOIN vote ON question.id = vote.questionId
                    WHERE vote.questionId IS NULL''')
    questionIds = cursor.fetchall()
    for question in questionIds:
        cursor.execute('''DELETE FROM question WHERE id = (?)''', (question[0],))
        print('Delete question: %s' % (question[0]))
    db.commit()


def addQuestionTags():
    cursor.execute('''SELECT id, tagname FROM tag;''')
    tags = cursor.fetchall()
    tagsDict = dict(map(reversed, tags))
    cursor.execute('''SELECT id, tags FROM question''')
    questions = cursor.fetchall()
    for question in questions:
        tagArray = question[1].replace('><', ' ').replace('<', '').replace('>', '').split(' ')
        for tag in tagArray:
            tagId = tagsDict.get(tag)
            row = (question[0], tagId)
            cursor.execute('''INSERT INTO question_tag(questionId, tagId) VALUES(?,?)''', row)
            print('${0} inserted'.format(row))
    db.commit()


def insert(tagsPath, questionsPath, votesPath):
    insertTags(tagsPath)
    insertQuestions(questionsPath)
    insertVotes(votesPath)

def postInsertSetup():
    removeNotVotedQuestions()
    addQuestionTags()

def main(tagsPath, questionsPath, votesPath):
    setupTables()
    insert(tagsPath, questionsPath, votesPath)
    postInsertSetup()
    db.close()


