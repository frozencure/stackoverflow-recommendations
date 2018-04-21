from XMLParser.XmlParser import *
import os


resourcesPath = 'C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources'
sourcePath = resourcesPath + '/demoVotes.xml'
destPath = resourcesPath + '/demoVotes.csv'

parser = XMLParser(sourcePath, 'row', ['UserId', 'PostId'])

parser.parseToCsv(destPath)