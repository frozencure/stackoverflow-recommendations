from lxml import etree
import csv

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

    def __fastParse(self, func, args):
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
        self.__fastParse(self.__parseElemToCsv, args=(writer,))


