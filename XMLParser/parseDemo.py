from XMLParser.xmlParser import *

path = 'C:/Users/Iancu/Desktop/stackOv_dataset/Votes.xml'
parser = XMLParser(path, 'row', ['UserId', 'PostId'])

parser.parseToCsv('./Votes.csv')