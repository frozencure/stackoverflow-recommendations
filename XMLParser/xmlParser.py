from lxml import etree
import csv
import sqlite3

class XMLParser:

    """
    Attributes:
        path: file path to be parsed
        tag: parent tag from which will be extracted
        elements: tags of the children whose values will be extracted
    """


    def __init__(self, path, tag, elements = []):
        self.path = path
        self.tag = tag
        self.elements = elements

    def fastParse(self, func, args):
        """Iteratively reads the xml file and executes the given function for each row"""
        context = etree.iterparse(self.path, events=('end',), tag= self.tag)
        for event, elem in context:
            func(elem, *args)
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

    def __parseElemToCsv(self, elem, writer):
        values = []
        for tag in self.elements:
            values.append(elem.attrib.get(tag))
        writer.writerow(values)
        del values


    def parseToCsv(self, output):
        """Parses the given xml items to a (new) csv file."""
        file = open(output, 'w', newline='')
        writer = csv.writer(file, delimiter=',')
        writer.writerow(self.elements)
        self.fastParse(self.__parseElemToCsv, args=(writer,))

    def __parseRowToSqlite__(self, elem, cursor, query, conditionIndex=None, conditionValue=None):
        values = []
        for tag in self.elements:
            values.append(elem.attrib.get(tag))
        if conditionIndex is not None and conditionValue is not None:
            if values[conditionIndex] == conditionValue:
                row = tuple(values)
                try:
                    cursor.execute(query, row)
                except sqlite3.Error as e:
                    print(e.message)
                del row
        else:
            row = tuple(values)
            cursor.execute(query, row)
            del row
        del values

    def parseToSqlite(self, cursor, query, conditionIndex=None, conditionValue=None):
        self.fastParse(self.__parseRowToSqlite__, args=(cursor, query, conditionIndex, conditionValue,))


