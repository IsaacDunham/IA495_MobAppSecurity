#!/usr/bin/python

### Imports ###

import json
import datetime
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

### Static Variables ###

# JSON Information
path = os.getcwd() + "/"
myjson = path + "scan_results.json"

with open(myjson, "r") as f:
    data = json.load(f)

# Common arguments for ParagraphStyle
CommonOptions = dict(fontSize=12)

### Functions ###
def expandParaDict(doc, d):
  for k,v in d.items(): 
    addParagraph(doc, k + ": ")       
    if isinstance(v, dict):
         expandParaDict(v)

    if isinstance(v, list):
        for i in v:
            if isinstance(i, dict):
                expandParaDict(i)
            else:
                i = str(i)
                addParagraph(doc, i, leftIndent = 24)
    else:            
        addParagraph(doc, v)


def addParagraph(doc, text, **kwargs):
    kwargs.setdefault("leftIndent", 12)
    if isinstance(text, dict):
        expandParaDict(doc, text)

    else:
        doc.append(Paragraph(str(text), 
                         ParagraphStyle(**CommonOptions, 
                                        name = "paragraph",
                                        alignment=TA_LEFT, 
                                        fontName="Times-Roman",
                                        **kwargs)))


def addL1Header(doc, heading):
    heading = heading.title()
    doc.append(Paragraph(heading,
                        ParagraphStyle(fontSize = 16, name = heading,
                                        alignment=TA_CENTER, 
                                        fontName="Times-Bold",
                                        leading = 32)))
    
def addL2Header(doc, heading):
    heading = heading.title()
    doc.append(Paragraph(heading,
                         ParagraphStyle(fontSize = 14, name = heading,
                                        alignment=TA_LEFT, 
                                        fontName="Times-Bold",
                                        leading = round(1.5*14))))

def addL3Header(doc, heading):
    heading = heading.title()
    doc.append(Paragraph(heading,
                         ParagraphStyle(fontSize = 14, name = heading,
                                        alignment=TA_LEFT, 
                                        fontName="Times-BoldItalic",
                                        leading = round(1.5*14))))

def addL4Header(doc, heading):
    heading = heading.title()
    doc.append(Paragraph(heading,
                         ParagraphStyle(fontSize = 14, name = heading,
                                        alignment=TA_LEFT, 
                                        fontName="Times-Italic", 
                                        leading = round(1.5*14))))

def addL5Header(doc, heading):
     heading = heading.title() + ":"
     doc.append(Paragraph(heading,
                          ParagraphStyle(**CommonOptions, name = heading,
                                         alignment=TA_LEFT, 
                                         fontName="Times-Bold",
                                         leading = round(1.5*12)))) #18 pt = .25 inch

def addL6Header(doc, heading):
    heading = heading.title() + ":"
    doc.append(Paragraph(heading,
                         ParagraphStyle(**CommonOptions, name = heading,
                                        alignment=TA_LEFT, 
                                        fontName="Times-BoldItalic",
                                        leading = round(1.5*12))))

def addL7Header (doc, heading):
    heading = heading.title() + ":"
    doc.append(Paragraph(heading,
                         ParagraphStyle(**CommonOptions, name = heading,
                                        alignment=TA_LEFT, 
                                        fontName="Times-Italic",
                                        leading = round(1.5*12))))

def addL8Header (doc, heading):
    heading = heading.title() + ":"
    doc.append(Paragraph(heading,
                         ParagraphStyle(**CommonOptions, name = heading,
                                        alignment=TA_LEFT, 
                                        fontName="Times-Italic",
                                        leading = round(1.5*12),
                                        underline = True)))

def pickLevelFunc(level):
    if level == 1:
        return addL1Header
    if level == 2:
        return addL2Header
    if level == 3:
        return addL3Header
    if level == 4:
        return addL4Header
    if level == 5:
        return addL5Header
    if level == 6:
        return addL6Header
    if level == 7:
        return addL7Header
    if level == 8:
        return addL8Header
    if level > 8:
        return addParagraph
    
#Main doc creation

level = 2

def iterdict(data):
    global level
    print("Level is ", level)
    for k, v in data.items():
        headerFunc = pickLevelFunc(level)
        headerFunc(document, k)
        if isinstance(v, dict):
            level += 1
            iterdict(v)
            level -= 1 
        else:
            if isinstance(v, list):
                for item in v:
                    addParagraph(document, item)
            else:
                addParagraph(document, v)


document = []

now = datetime.datetime.now()
docTitle = "Security Scan Results: " + str(now.strftime("%m/%d/%Y %H:%M"))
docFileName = "ScanResults_" + str(now.strftime("%m%d%Y_%H%M")) + ".pdf"

addL1Header(document, docTitle)
iterdict(data)

SimpleDocTemplate(path + docFileName, pagesize = letter, 
                    rightMargin = 72, leftMargin = 72,
                    topMargin = 72, bottomMargin = 72, 
                    title = docTitle).build(document)