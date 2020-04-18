# -*- coding: utf-8 -*-

import json
import csv
import xml.etree.ElementTree as ET
from lxml import etree
import sys

def CSV2XML(infile, outfile):
    reader = csv.reader(open(infile, 'r', encoding='utf-8'), delimiter=';')
    next(reader)
    xmlFile = open(outfile, 'wb')

    departments = ET.Element('departments')

    name = 'initialize'
    for row in reader:
        if name != row[1]:
            university = ET.SubElement(departments, 'university', name=row[1], uType=row[0])

        item = ET.SubElement(university, 'item', id=row[3], faculty=row[2])

        if row[5] == '':
            row[5] = 'tr'
        else:
            row[5] = 'en'

        if row[6] == '':
            row[6] = 'öö'
        else:
            row[6] = 'iö'   
        name = ET.SubElement(item, 'name', lang=row[5], second=row[6])
        name.text = row[4]
        period = ET.SubElement(item, 'period')
        period.text = row[8]

        if row[11] == '':
            row[11] = '0'
        quota = ET.SubElement(item, 'quota', spec=row[11])
        quota.text = row[10]
        field = ET.SubElement(item, 'field')
        field.text = row[9]
        if row[12] == '':
            row[12] = '0'
        if row[13] == '':
            row[13] = '0'
        last_min_score = ET.SubElement(item, 'last_min_score', order=row[12])
        last_min_score.text = row[13]
        grant = ET.SubElement(item, 'grant')
        grant.text = row[7]

        name = row[1]

    # create a new XML file with the results
    tree = ET.ElementTree(departments)
    tree.write(xmlFile, encoding=("utf-8"))
    xmlFile.close()


def XML2CSV(inflie, outfile):
    xmlFile = open(inflie, 'r', encoding='utf-8')
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    csvfile = open(outfile, 'w', encoding='utf-8', newline='')
    fieldnames = ['ÜNİVERSİTE_TÜRÜ', 'ÜNİVERSİTE', 'FAKÜLTE', 'PROGRAM_KODU', 'PROGRAM', 'DİL', 'ÖĞRENİM_TÜRÜ', 'BURS', 'ÖĞRENİM_SÜRESİ',
                  'PUAN_TÜRÜ', 'KONTENJAN', 'OKUL_BİRİNCİSİ_KONTENJANI', 'GEÇEN_YIL_MİN_SIRALAMA', 'GEÇEN_YIL_MİN_PUAN']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    tempdict = dict.fromkeys(['ÜNİVERSİTE_TÜRÜ', 'ÜNİVERSİTE', 'FAKÜLTE', 'PROGRAM_KODU', 'PROGRAM', 'DİL', 'ÖĞRENİM_TÜRÜ', 'BURS', 'ÖĞRENİM_SÜRESİ',
                  'PUAN_TÜRÜ', 'KONTENJAN', 'OKUL_BİRİNCİSİ_KONTENJANI', 'GEÇEN_YIL_MİN_SIRALAMA', 'GEÇEN_YIL_MİN_PUAN'])
    for child in root:
        for item in child:
            for subchild in item:
                typedict = {'ÜNİVERSİTE_TÜRÜ' : child.get('uType')}
                tempdict.update(typedict)
                uninamedict = {'ÜNİVERSİTE' : child.get('name')}
                tempdict.update(uninamedict)
                facultydict = {'FAKÜLTE' : item.get('faculty')}
                tempdict.update(facultydict)
                iddict = {'PROGRAM_KODU' : item.get('id')}
                tempdict.update(iddict)
                if subchild.tag == 'name':
                    progdict = {'PROGRAM' : subchild.text}
                    tempdict.update(progdict)
                    lang = subchild.get('lang')
                    if lang == 'tr':
                        lang = ''
                    elif lang == 'en':
                        lang = 'İngilizce'
                    langdict = {'DİL' : lang}
                    tempdict.update(langdict)
                    second = subchild.get('second')
                    if second == 'öö':
                        second = ''
                    elif second == 'iö':
                        second = 'İkinci Öğretim'
                    secdict = {'ÖĞRENİM_TÜRÜ' : second}
                    tempdict.update(secdict)
                elif subchild.tag == 'period':
                    perioddict = {'ÖĞRENİM_SÜRESİ' : subchild.text}
                    tempdict.update(perioddict)
                elif subchild.tag == 'quota':
                    quotadict = {'KONTENJAN' : subchild.text}
                    tempdict.update(quotadict)
                    spec = subchild.get('spec')
                    if spec == '0':
                        spec = ''
                    specdict = {'OKUL_BİRİNCİSİ_KONTENJANI' : spec}
                    tempdict.update(specdict)
                elif subchild.tag == 'field':
                    fielddict = {'PUAN_TÜRÜ' : subchild.text}
                    tempdict.update(fielddict)
                elif subchild.tag == 'last_min_score':
                    last_min_score = subchild.text
                    if last_min_score == '0':
                        last_min_score = ''
                    scoredict = {'GEÇEN_YIL_MİN_PUAN' : last_min_score}
                    tempdict.update(scoredict)
                    order = subchild.get('order')
                    if order == '0':
                        order = ''
                    orderdict = {'GEÇEN_YIL_MİN_SIRALAMA' : order}
                    tempdict.update(orderdict)
                elif subchild.tag == 'grant':
                    grant = subchild.text
                    if grant == '0':
                        grant = ''
                    grantdict = {'BURS' : grant}
                    tempdict.update(grantdict)
            writer.writerow(tempdict)
            

def CSV2JSON(inflie, outfile):
    # Reads the file the same way that you did
    csv_file = csv.DictReader(open(inflie, 'r', encoding='utf-8'), delimiter=';')

    jsonfile = open(outfile, 'w', encoding='utf-8')
    
    # Created a list and adds the rows to the list
    deutemp = "DOKUZ EYLÜL ÜNİVERSİTESİ"
    jsonfile.write('[\n')
    temp = "temp"
    differentTemp = "different"

    for row in csv_file:
        if differentTemp != "different" :
            if row['ÜNİVERSİTE'] == deutemp :    
                jsonfile.write('},\n')
            else:
                jsonfile.write('}\n')  

        differentTemp = "anotherDifferent"
        
        if row['ÜNİVERSİTE'] != deutemp :
            jsonfile.write(']\n')
            jsonfile.write('}\n')
            jsonfile.write(']\n')
            jsonfile.write('},\n')
    
        if row['ÜNİVERSİTE'] != temp:
            jsonfile.write('{\n')
            jsonfile.write('\"university name\" : ')
            jsonfile.write(json.dumps(row['ÜNİVERSİTE'], indent=4, ensure_ascii=False))
            jsonfile.write(',\n')
            jsonfile.write('\"uType\" : ')
            jsonfile.write(json.dumps(row['ÜNİVERSİTE_TÜRÜ'], indent=4, ensure_ascii=False))
            jsonfile.write(',\n')
            jsonfile.write('\"item\" : [\n')
            jsonfile.write('{')
            jsonfile.write('\"faculty\" : ')
            jsonfile.write(json.dumps(row['FAKÜLTE'], indent=4, ensure_ascii=False))
            jsonfile.write(',\n')
            jsonfile.write('\"department\" : [\n')
            temp = row['ÜNİVERSİTE']

        jsonfile.write('{\n')
        jsonfile.write('\"id\" : ')
        jsonfile.write(json.dumps(row['PROGRAM_KODU'], indent=4, ensure_ascii=False))
        jsonfile.write(',\n')
        jsonfile.write('\"name\" : ')
        jsonfile.write(json.dumps(row['PROGRAM'], indent=4, ensure_ascii=False))
        jsonfile.write(',\n')
        jsonfile.write('\"lang\" : ')
        jsonfile.write(json.dumps(row['DİL'], indent=4, ensure_ascii=False))
        jsonfile.write(',\n')
        jsonfile.write('\"second\" : ')
        jsonfile.write(json.dumps(row['ÖĞRENİM_TÜRÜ'], indent=4, ensure_ascii=False))
        jsonfile.write(',\n')
        jsonfile.write('\"period\" : ')
        jsonfile.write(json.dumps(row['ÖĞRENİM_SÜRESİ'], indent=4, ensure_ascii=False))
        jsonfile.write(',\n')
        jsonfile.write('\"spec\" : ')
        jsonfile.write(json.dumps(row['OKUL_BİRİNCİSİ_KONTENJANI'], indent=4, ensure_ascii=False))
        jsonfile.write(',\n')
        jsonfile.write('\"quota\" : ')
        jsonfile.write(json.dumps(row['KONTENJAN'], indent=4, ensure_ascii=False))
        jsonfile.write(',\n')
        jsonfile.write('\"field\" : ')
        jsonfile.write(json.dumps(row['PUAN_TÜRÜ'], indent=4, ensure_ascii=False))
        jsonfile.write(',\n')
        jsonfile.write('\"last_min_score\" : ')
        jsonfile.write(json.dumps(row['GEÇEN_YIL_MİN_PUAN'], indent=4, ensure_ascii=False))
        jsonfile.write(',\n')
        jsonfile.write('\"last_min_order\" : ')
        jsonfile.write(json.dumps(row['GEÇEN_YIL_MİN_SIRALAMA'], indent=4, ensure_ascii=False))
        jsonfile.write(',\n')
        jsonfile.write('\"grant\" : ')
        jsonfile.write(json.dumps(row['BURS'], indent=4, ensure_ascii=False))
        jsonfile.write('\n')
        temp = row['ÜNİVERSİTE']
        deutemp = row['ÜNİVERSİTE']
  
    jsonfile.write('}\n')
    jsonfile.write(']\n')
    jsonfile.write('}\n')
    jsonfile.write(']\n')
    jsonfile.write('}\n')
    jsonfile.write(']')
    jsonfile.close()
            

def JSON2CSV(inflie, outfile):
    jsonFile = open(inflie, encoding='utf-8')
    data = json.loads(jsonFile.read())
    csvFile = open(outfile, 'w', encoding='utf-8', newline='')
    fieldnames = ['ÜNİVERSİTE_TÜRÜ', 'ÜNİVERSİTE', 'FAKÜLTE', 'PROGRAM_KODU', 'PROGRAM', 'DİL', 'ÖĞRENİM_TÜRÜ', 'BURS', 'ÖĞRENİM_SÜRESİ',
                  'PUAN_TÜRÜ', 'KONTENJAN', 'OKUL_BİRİNCİSİ_KONTENJANI', 'GEÇEN_YIL_MİN_SIRALAMA', 'GEÇEN_YIL_MİN_PUAN']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for elem in data:
        for subelem in elem['item']:
            for departelem in subelem['department']:
                writer.writerow({'ÜNİVERSİTE_TÜRÜ': elem['uType'], 'ÜNİVERSİTE': elem['university name'],
                                 'FAKÜLTE': subelem['faculty'], 'PROGRAM_KODU': departelem['id'],
                                'PROGRAM': departelem['name'], 'DİL': departelem['lang'], 'ÖĞRENİM_TÜRÜ': departelem['second'],
                                'BURS': departelem['grant'], 'ÖĞRENİM_SÜRESİ': departelem['period'], 'PUAN_TÜRÜ': departelem['field'],
                                'KONTENJAN': departelem['quota'], 'OKUL_BİRİNCİSİ_KONTENJANI': departelem['spec'],
                                'GEÇEN_YIL_MİN_SIRALAMA': departelem['last_min_order'], 'GEÇEN_YIL_MİN_PUAN': departelem['last_min_score']})


def XML2JSON(inflie, outfile):
    """  xml file opennig... """
    xmlFile = open(inflie, 'r', encoding='utf-8')
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    
    """  json file opennig... """
    jsonfile = open(outfile, 'w', encoding='utf-8')
    
    unilist = []
    
    for child in root:
        departslist = []
        itemlist = []
        unidict = {"university name":"", "uType":"", 'item' : itemlist}
        itemdict = {"faculty":"", 'departments' : departslist}  
        typedict = {'uType' : child.get('uType')}
        unidict.update(typedict)
        uninamedict = {'university name' : child.get('name')}
        for item in child:
            departdict = { "id":"", "name":"", "lang":"", "second":"", "period":"",
                  "spec":"", "quota":"", "field":"", "last_min_score":"", "last_min_order":"", "grant":""}
            for subchild in item:
                facultydict = {'faculty' : item.get('faculty')}
                itemdict.update(facultydict)
                unidict.update(uninamedict)
                iddict = {'id' : item.get('id')}
                if subchild.tag == 'name':
                    departdict.update(iddict)
                    progdict = {'name' : subchild.text}
                    departdict.update(progdict)
                    lang = subchild.get('lang')
                    if lang == 'tr':
                        lang = ''
                    elif lang == 'en':
                        lang = 'İngilizce'
                    langdict = {'DİL' : lang}
                    departdict.update(langdict)
                    second = subchild.get('second')
                    if second == 'öö':
                        second = ''
                    elif second == 'iö':
                        second = 'İkinci Öğretim'
                    secdict = {'second' : second}
                    departdict.update(secdict)
                elif subchild.tag == 'period':
                    perioddict = {'period' : subchild.text}
                    departdict.update(perioddict)
                elif subchild.tag == 'quota':
                    quotadict = {'quota' : subchild.text}
                    departdict.update(quotadict)
                    spec = subchild.get('spec')
                    if spec == '0':
                        spec = ''
                    specdict = {'spec' : spec}
                    departdict.update(specdict)
                elif subchild.tag == 'field':
                    fielddict = {'field' : subchild.text}
                    departdict.update(fielddict)
                elif subchild.tag == 'last_min_score':
                    last_min_score = subchild.text
                    if last_min_score == '0':
                        last_min_score = ''
                    scoredict = {'last_min_score' : last_min_score}
                    departdict.update(scoredict)
                    order = subchild.get('order')
                    if order == '0':
                        order = ''
                    orderdict = {'last_min_order' : order}
                    departdict.update(orderdict)
                elif subchild.tag == 'grant':
                    grant = subchild.text
                    if grant == '0':
                        grant = ''
                    grantdict = {'grant' : grant}
                    departdict.update(grantdict)
            departslist.append(departdict)
            tmpdict = {'departments' : departslist}
            itemdict.update(tmpdict)
        itemlist.append(itemdict)

        unilist.append(unidict)
    jsonfile.write(json.dumps(unilist, indent=4, ensure_ascii=False))

def JSON2XML(inflie, outfile):
    jsonFile = open(inflie, encoding='utf-8')
    data = json.loads(jsonFile.read())
    
    f = open(outfile, 'wb')
    name = 'initialize'
    departments = ET.Element('departments')
    for elem in data:
        for subelem in elem['item']:
            for departelem in subelem['department']:
                if name != elem['university name']:
                    university = ET.SubElement(departments, 'university', name=elem['university name'], uType=elem['uType'])

                item = ET.SubElement(university, 'item', id=departelem['id'], faculty=subelem['faculty'])

                if departelem['lang']:
                        departelem['lang'] = 'tr'
                else:
                    departelem['lang'] = 'en'

                if departelem['second'] == '':
                        departelem['second'] = 'öö'
                else:
                    departelem['second'] = 'iö'   
                name = ET.SubElement(item, 'name', lang=departelem['lang'], second=departelem['second'])
                name.text = departelem['name']
                period = ET.SubElement(item, 'period')
                period.text = departelem['period']

                if departelem['spec'] == '':
                    departelem['spec'] = '0'
                quota = ET.SubElement(item, 'quota', spec=departelem['spec'])
                quota.text = departelem['quota']
                field = ET.SubElement(item, 'field')
                field.text = departelem['field']
                if departelem['last_min_score'] == '':
                    departelem['last_min_score'] = '0'
                if departelem['last_min_order'] == '':
                    departelem['last_min_order'] = '0'
                last_min_score = ET.SubElement(item, 'last_min_score', order=departelem['last_min_order'])
                last_min_score.text = departelem['last_min_score']
                grant = ET.SubElement(item, 'grant')
                grant.text = departelem['grant']
    
    # create a new XML file with the results
    tree = ET.ElementTree(departments)
    tree.write(f, encoding=("utf-8"))
    f.close()
    

def validateXSD(inflie, outfile):
    doc = etree.parse(inflie)
    root = doc.getroot()
    #print(etree.tostring(root))
    xmlschema_doc = etree.parse(outfile)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.XML(etree.tostring(root))
    validation_result = xmlschema.validate(doc)
    print(validation_result)

def main():
    if sys.argv[3] == '1':
        CSV2XML(sys.argv[1], sys.argv[2])
    if sys.argv[3] == '2':
        XML2CSV(sys.argv[1], sys.argv[2])
    if sys.argv[3] == '3':
        XML2JSON(sys.argv[1], sys.argv[2])
    if sys.argv[3] == '4':
        JSON2XML(sys.argv[1], sys.argv[2])
    if sys.argv[3] == '5':
        CSV2JSON(sys.argv[1], sys.argv[2])
    if sys.argv[3] == '6':
        JSON2CSV(sys.argv[1], sys.argv[2])
    if sys.argv[3] == '7':
        validateXSD(sys.argv[1], sys.argv[2])

main()
