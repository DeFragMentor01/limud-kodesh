import os
import re
import configparser
from bs4 import BeautifulSoup
import codecs


config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings.ini'))

html_path = config.get('HTML','html_path')
xml_path = config.get('XML','xml_path')


def write_xml(xml_file_name, file, textline):
    
    with codecs.open(os.path.join(xml_file_name,file), "a", encoding='utf-8') as f:
        f.write(f"{textline}\r")
        
def repair_tag(massechet_daf_path):
    
    with open(massechet_daf_path, "r",encoding='utf-8') as f:
        
        data = f.read()
        data = re.sub('[^<,/,a-z]span','<span',data)
    
    with open(massechet_daf_path, "w",encoding='utf-8') as f:
        
        f.write(data)
    
def remove_ref(my_str):
    
    mystr_list = my_str.split()
    open_parenthesis = False
    final_line = []
    
    for item in mystr_list:
        if re.search('\[',item) or re.search('\(',item):
            open_parenthesis = True
            final_line.append(item)
            continue
        if re.search('\]',item) and open_parenthesis == True or re.search('\)',item) and open_parenthesis == True:
            open_parenthesis = False
            final_line.append(item)
            continue
        if re.search('\]',item) and re.search('[א-ת]{0,2}\]',item) and open_parenthesis == False or re.search('\)',item) and re.search('[א-ת]{0,2}\)',item) and open_parenthesis == False:
            continue
        else:
            final_line.append(item)
    
    listToStr = ' '.join([str(elem) for elem in final_line])  
    return listToStr

        
def remove_blank(line_list):

    new_list = []
    skip = False
    line_list = line_list.replace(".",'').replace('None','').replace('( ','(').replace('(:','(')
    line_list = re.sub(r"[\r\n]+", " ", line_list)
    line_list = re.sub(r"\"","&quot;",line_list)
    line_list = re.sub(r"\[[א-ת]\]",'',line_list)
    line_list = line_list.replace(':  ',': ')
    line_list = re.sub('הדרן עלך(.*)','',line_list)
    line_list = line_list.strip()
    line_list = remove_ref(line_list)
    if re.search('רש&quot;י כת&quot;י',line_list):
        skip = True
    line_list = re.sub('רש&quot;י כת&quot;י(.*)','',line_list)
    if len(line_list) > 0:
        new_list.append(line_list)
        if skip == True:
            return new_list[0],skip
        return new_list[0]
    
def check_next_start_file(index,massechet_dir,dibour_hamatril_continue,massechet_path):
    if index < len(massechet_dir) -1:
        path = f'{massechet_path}\\{massechet_dir[index+1]}'
        
        with open(path, "r",encoding='utf-8') as f:
            
            daf = f.read()
            soup = BeautifulSoup(daf, 'html.parser')
            shastext3 = soup.find("div", {"class": "shastext3"})
            
            list_of_line = []
            
            if shastext3 != None:
                
                for index,tags in enumerate(shastext3):
                    tags = re.sub(r"[\r\n\t]+", " ", str(tags))
                    tags = re.sub('הכי גרסינן',' ',tags)
                    tags = re.sub('ה"ג',' ',tags)
                    tags = remove_ref(tags)
                    if re.search('^\s+$|^$',tags) == None:
                        list_of_line.append(tags)
                        if re.search('[<->]',list_of_line[0]) == None:
                            dibour_hamatril_continue['dibourHamatrilContinueInNextFile'] = list_of_line[0]
                            list_of_line = list_of_line.clear()
                            return 'is_continue'
                        else:
                            break
            list_of_line = list_of_line.clear()
    

def built_xml_header(massechet_daf_path,html_file,folder):
    
    with open(massechet_daf_path, "r",encoding='utf-8') as f:

        daf = f.read()
        soup = BeautifulSoup(daf, 'html.parser')

        massechet_name = soup.find_all("title")[0]
        
        if massechet_name.parent.name == 'head':
            
            if re.search('(?<= מסכת).*(?= דף)',str(massechet_name)) != None:
                massechet_name = re.search('(?<= מסכת).*(?= דף)',str(massechet_name)).group()
                massechet_name = re.sub('^\s','',massechet_name)
                daf_amud = re.sub('^(.*?)\.','',html_file)
                daf_amud = daf_amud.replace('.html','').split('.')
                html_file = html_file.replace('.html','.xml') 
                write_xml(xml_path + '\\' + folder,html_file,"<root>\n<massechet name="+"'"+massechet_name+"'"+">\n\t<daf value="+"'"+daf_amud[0]+"'"+">\n\t\t<amud value="+"'"+daf_amud[1]+"'"+">")
            #print('Working on'+massechet_name,daf_amud)

def built_xml_content(massechet_daf_path,folder,html_file,dibour_hamatril_continue,index_file,massechet_dir,massechet_path):

    stop = False
    mishna = False
    guemara = False
    
    with open(massechet_daf_path, "r",encoding='utf-8') as f:

        html_file = html_file.replace('.html','.xml')
        soup = BeautifulSoup(f, 'html5lib')
        
        shastext3 = soup.find("div", {"class": "shastext3"})
        
        dibour_hamatril = ''
        content = ''
        len_after_colon = 0
        
        if shastext3 != None:
        
        
            for index,tags in enumerate(shastext3):

                if tags.name == 'span':

                    if tags['class'][0] == 'five' and re.search('\.',tags.text) != None:
                
                        mishna = False
                        guemara = False
                        
                        dibour_hamatril_text = remove_blank(tags.text)
                        
                        if type(dibour_hamatril_text) == tuple:
                            dibour_hamatril_text = dibour_hamatril_text[0]
                            dibour_hamatril_text = re.sub('\s+$','',dibour_hamatril_text)
                            dibour_hamatril_text2 = dibour_hamatril_text.rsplit(' ', 1)[0]
                            textline = f'<DibourHamatrilNameContinue name="{dibour_hamatril_text2}"/>'
                            write_xml(xml_path + '\\' + folder,html_file,textline)
                            dibour_hamatril_continue['dibourHamatrilNameContinue'] = dibour_hamatril_text
                            dibour_hamatril = ''
                            content = ''
                            len_after_colon = 0
                            continue
                        
                        if tags.text.split('\n')[-1] == '                    ':
                            if check_next_start_file(index_file,massechet_dir,dibour_hamatril_continue,massechet_path) == 'is_continue':
                                dibour_hamatril_text = re.sub('\s+$','',dibour_hamatril_text)
                                dibour_hamatril_text2 = dibour_hamatril_text.rsplit(' ', 1)[0]
                                textline = f'<DibourHamatrilNameContinue name="{dibour_hamatril_text2}"/>'
                                write_xml(xml_path + '\\' + folder,html_file,textline)
                                dibour_hamatril_continue['dibourHamatrilNameContinue'] = dibour_hamatril_text2
                                dibour_hamatril = ''
                                content = ''
                                len_after_colon = 0
                                continue
                            else:
                                dibour_hamatril_text = re.sub('\s+$','',dibour_hamatril_text)
                                dibour_hamatril_text2 = dibour_hamatril_text.rsplit(' ', 1)[0]
                                textline = f'<DibourHamatrilNameContinue name="{dibour_hamatril_text2}"/>'
                                write_xml(xml_path + '\\' + folder,html_file,textline)
                                dibour_hamatril_continue['dibourHamatrilNameContinue'] = dibour_hamatril_text2
                                dibour_hamatril = ''
                                content = ''
                                len_after_colon = 0
                                continue
                                
                                
                        dibour_hamatril += ' ' + dibour_hamatril_text
                        dibour_hamatril = re.sub('^\s+','',dibour_hamatril)
                        dibour_hamatril = dibour_hamatril.replace("הכי גרסי' ","").replace('   ',' ').replace(':','')
                        continue
                    
                    if tags['class'][0] == 'five' and re.search('\.',tags.text) == None:
                        
                        mishna = False
                        guemara = False
                        
                        dibour_hamatril_text2 = remove_blank(tags.text)
                    
                        if type(dibour_hamatril_text2) == tuple:
                            dibour_hamatril_text2 = dibour_hamatril_text2[0]
                        
                        dibour_hamatril += ' '+ dibour_hamatril_text2
                        
                        if tags.text.split('\n')[-1] == '                    ':
                            if check_next_start_file(index_file,massechet_dir,dibour_hamatril_continue,massechet_path) == 'is_continue':
                                dibour_hamatril = re.sub('\s+$','',dibour_hamatril)
                                dibour_hamatril_text2 = dibour_hamatril.rsplit(' ', 1)[0]
                                textline = f'<DibourHamatrilNameContinue name="{dibour_hamatril_text2}"/>'
                                write_xml(xml_path + '\\' + folder,html_file,textline)
                                dibour_hamatril_continue['dibourHamatrilNameContinue'] = dibour_hamatril_text2
                                dibour_hamatril = ''
                                content = ''
                                len_after_colon = 0
                                continue
                            else:
                                dibour_hamatril = re.sub('\s+$','',dibour_hamatril)
                                dibour_hamatril_text2 = dibour_hamatril.rsplit(' ', 1)[0]
                                textline = f'<DibourHamatrilNameContinue name="{dibour_hamatril_text2}"/>'
                                write_xml(xml_path + '\\' + folder,html_file,textline)
                                dibour_hamatril_continue['dibourHamatrilNameContinue'] = dibour_hamatril_text2
                                dibour_hamatril = ''
                                content = ''
                                len_after_colon = 0
                                continue
                        
                        continue
                                           
                    if tags['class'][0] == 'mareimakom':
                        mareimakom = remove_blank(tags.text)
                        content += ' ' + mareimakom
                        continue
                    
                    
                    if tags['class'][0] == 'shastitle7':
                        if tags.text == "מתני'":
                            mishna = True
                            continue
                        if tags.text == "גמ'":
                            guemara = True
                            continue
                        else:
                            dibour_hamatril += ' '+ remove_blank(tags.text)
                        continue 
                    
                if tags.name == None:
                    
                    text = remove_blank(tags)
                    
                    if type(text) == tuple:
                        text = text[0]
                        stop = True
                    
                    text = str(text).replace(": הכי גרסי'",':').replace(': הכי גרסינן',':')
                    text = re.sub('^הכי גרסינן','',text)
                    text = re.sub('^\s+הכי גרסינן','',text)
                    text = re.sub('^גרסינן:','',text)
                    text = re.sub('^\s+גרסינן:','',text)
                    text = re.sub('^ה&quot;ג','',text)
                    text = re.sub('^\s+ה&quot;ג','',text)
                    
                    if text == '' or text == None or text == 'None':
                        continue
                    
                    
                    after_colon = re.search(':\s(.*)',str(text))
                    
                    if after_colon != None:
                        len_after_colon = len(after_colon.group().split())
                    
                    if len_after_colon == 2 and after_colon != None:
                            text = re.sub(re.escape(after_colon.group()),':',text)
                    
                    if text != None:
                        for item in text.split('\n'):
                            if (':' not in item or len_after_colon > 2) and tags.split('\n')[-1] == '                    ':
                                dibour_hamatril_continue['dibour_hamatril_continue'] = dibour_hamatril  
                                if dibour_hamatril_continue['dibour_hamatril_continue'] == '':
                                    for key in list(dibour_hamatril_continue):
                                        del dibour_hamatril_continue[key]
                            if ':' in item and len_after_colon == 2 and tags.split('\n')[-1] == '                    ':
                                if check_next_start_file(index_file,massechet_dir,dibour_hamatril_continue,massechet_path) == 'is_continue':
                                    dibour_hamatril_continue['dibour_hamatril_colon'] = dibour_hamatril          
                    
                    if tags.split('\n')[-1] == '                    ' and guemara == True:
                        dibour_hamatril_continue['DibourHamatrilGuemaraContinue'] = 'continue'
                        write_xml(xml_path + '\\' + folder,html_file,'<DibourHamatrilGuemaraContinue/>')
                        guemara = False
                        continue
                    
                    if mishna and re.search(':$',text):
                        
                        content += ' ' + text
                        content = content.replace('None','').replace('  ',' ').replace(' :',':')
                        textline = '<DibourHamatrilMishna/>\n'+content+'\n<EndDibourHamatrilMishna/>'
                        write_xml(xml_path + '\\' + folder,html_file,textline)
                        content = ''
                        len_after_colon = 0
                        mishna = False
                        continue
                    
                    if guemara and re.search(':$',text) or 'DibourHamatrilGuemaraContinue' in dibour_hamatril_continue and re.search(':$',text):
                        
                        content += ' ' + text
                        content = content.replace('None','').replace('  ',' ').replace(' :',':')
                        textline = '<DibourHamatrilGuemara/>\n'+content+'\n<EndDibourHamatrilGuemara/>'
                        write_xml(xml_path + '\\' + folder,html_file,textline)
                        for key in list(dibour_hamatril_continue):
                            del dibour_hamatril_continue[key]
                        content = ''
                        len_after_colon = 0
                        guemara = False
                        continue
                    
                    if 'dibour_hamatril_colon' in dibour_hamatril_continue and 'dibour_hamatril_colon_start' not in dibour_hamatril_continue:
                        content += ' '+ text
                        
                        content = content.replace('None','').replace('  ',' ').replace(' :',':')
                        content = re.sub(':\s',' ',content)

                        textline = f'<StartDibourHamatril name="{dibour_hamatril}"/>\n'+content+'\n<DibourHamatrilContinue/>'
                        write_xml(xml_path + '\\' + folder,html_file,textline)
                        dibour_hamatril_continue['dibour_hamatril_colon_start'] = dibour_hamatril
                        dibour_hamatril = ''
                        content = ''
                        len_after_colon = 0
                        continue
                    
                    if 'dibour_hamatril_colon_start' in dibour_hamatril_continue and re.search(':$',text):
                        content += ' '+ text
                        
                        content = content.replace('None','').replace('  ',' ').replace(' :',':')
                        content = re.sub(':\s',' ',content)

                        textline = '<DibourHamatrilContinue "'+dibour_hamatril_continue['dibour_hamatril_colon_start']+'"/>\n'+content+'\n<EndDibourHamatril/>'
                        write_xml(xml_path + '\\' + folder,html_file,textline)
                        dibour_hamatril = ''
                        content = ''
                        len_after_colon = 0
                        guemara = False
                        mishna = False
                        for key in list(dibour_hamatril_continue):
                            del dibour_hamatril_continue[key]
                        continue
                        
                    
                    if 'dibour_hamatril_continue_start' in dibour_hamatril_continue and re.search(':$',text):
                            
                        content += ' '+ text
                        
                        content = content.replace('None','').replace('  ',' ').replace(' :',':')
                        content = re.sub(':\s',' ',content)

                        textline = '<DibourHamatrilContinue name="'+dibour_hamatril_continue['dibour_hamatril_continue_start']+'"/>\n'+content+'\n<EndDibourHamatril/>'
                        write_xml(xml_path + '\\' + folder,html_file,textline)
                        dibour_hamatril = ''
                        content = ''
                        len_after_colon = 0
                        for key in list(dibour_hamatril_continue):
                            del dibour_hamatril_continue[key]
                        continue
                    
                    if 'dibourHamatrilNameContinue' in dibour_hamatril_continue and 'dibourHamatrilContinueInNextFile' not in dibour_hamatril_continue and re.search(':$',text):
                            
                        content += ' '+ text
                        
                        content = content.replace('None','').replace('  ',' ').replace(' :',':')
                        content = re.sub(':\s',' ',content)

                        textline = '<DibourHamatrilNameContinue name="'+dibour_hamatril_continue['dibourHamatrilNameContinue']+'"/>\n'+content+'\n<EndDibourHamatril/>'
                        write_xml(xml_path + '\\' + folder,html_file,textline)
                        dibour_hamatril = ''
                        content = ''
                        len_after_colon = 0
                        for key in list(dibour_hamatril_continue):
                            del dibour_hamatril_continue[key]
                        continue
                    
                    if 'dibourHamatrilContinueInNextFile' in dibour_hamatril_continue and re.search(':$',text):
                        
                        content += ' '+ text
                        
                        content = content.replace('None','').replace('  ',' ').replace(' :',':')
                        content = re.sub(':\s',' ',content)
                        
                        Final_dibour_hamatril = dibour_hamatril_continue['dibourHamatrilNameContinue'] + ' ' +dibour_hamatril_continue['dibourHamatrilContinueInNextFile'].replace('.','')
                        content = re.sub(dibour_hamatril_continue['dibourHamatrilContinueInNextFile'],'',content)
                        
                        textline = f'<DibourHamatrilNameContinue name="{Final_dibour_hamatril}"/>\n{content}\n<EndDibourHamatril/>'
                        write_xml(xml_path + '\\' + folder,html_file,textline)
                        dibour_hamatril = ''
                        content = ''
                        len_after_colon = 0
                        for key in list(dibour_hamatril_continue):
                            del dibour_hamatril_continue[key]
                        continue
                    
                    if 'dibour_hamatril_continue' in dibour_hamatril_continue and 'dibour_hamatril_continue_start' not in dibour_hamatril_continue:
                             
                        content += ' '+ text
                        content = re.sub('\s+$','',content)
                        content = content.rsplit(' ', 1)[0]
                        content = content.replace('None','').replace('  ',' ').replace(' :',':')
                        content = re.sub(':\s',' ',content)
                        dibour_hamatril = dibour_hamatril.replace('  ',' ')
                        
                        if content == '':
                            continue
                        
                        textline = f'<StartDibourHamatril name="{dibour_hamatril}">\n{content}\n<DibourHamatrilContinue/>'
                        write_xml(xml_path + '\\' + folder,html_file,textline)
                        dibour_hamatril_continue['dibour_hamatril_continue_start'] = dibour_hamatril
                        dibour_hamatril = ''
                        content = ''
                        len_after_colon = 0
                        if stop == True:
                            break
                        continue
                    
                    if re.search("^:$",text):
                               
                        content += ' '+ text
                        content = content.replace('None','').replace('  ',' ').replace(' :',':')   
                        content = re.sub(':\s',' ',content)
                        
                        if content == ':':
                            dibour_hamatril += ' '+content
                            continue 
                    
                    if text != None and content != None and (re.search(':$',text) or len_after_colon == 2) and any(dibour_hamatril_continue) == False:

                        content += ' '+ text
                        content = content.replace('None','').replace('  ',' ').replace(' :',':').replace('::',':')   
                        content = re.sub(':\s',' ',content)
                        content = re.sub('^\s','',content)
                        
                        dibour_hamatril = dibour_hamatril.replace('  ',' ')

                        if re.search('^\(.*\):$',content):
                            content = ''
                            dibour_hamatril = ''
                            len_after_colon = 0
                            continue
                        
                        textline = f'<StartDibourHamatril name="{dibour_hamatril}">\n{content}\n<EndDibourHamatril/>'
                        write_xml(xml_path + '\\' + folder,html_file,textline)
                        content = ''
                        dibour_hamatril = ''
                        len_after_colon = 0
                        if stop == True:
                            break
                        continue
                    
                    if stop == True and ':' not in text:
                        content += ' '+ text
                        content = re.sub('\s+$','',content)
                        content = content.rsplit(' ', 1)[0]
                        content = content.replace('None','').replace('  ',' ')
                        dibour_hamatril = dibour_hamatril.replace('  ',' ')
                        
                        textline = f'<StartDibourHamatril name="{dibour_hamatril}">\n{content}\n<DibourHamatrilContinue/>'
                        write_xml(xml_path + '\\' + folder,html_file,textline)
                        dibour_hamatril_continue['dibour_hamatril_continue_start'] = dibour_hamatril
                        content = ''
                        dibour_hamatril = ''
                        len_after_colon = 0
                        break

                    if text != None:

                        content += ' ' + text 
                        content = content.replace(':','')
                        continue
                    
                        
                    
def built_xml_footer(massechet_daf_path,folder,html_file):

        html_file = html_file.replace('.html','.xml')
        footer = '</amud>\n</daf>\n</masechet>\n</root>'
        write_xml(xml_path + '\\' + folder,html_file,footer)


def main ():
        
    for folder in os.listdir(html_path):
        
        if not os.path.exists(xml_path+ '\\' + folder):
            os.makedirs(xml_path + '\\' + folder)
        
        dibour_hamatril_continue = {}
        
        for index_file,html_file in enumerate(os.listdir(f"{html_path}\\{folder}")):
            
            massechet_dir = os.listdir(f"{html_path}\\{folder}")
            massechet_daf_path = f"{html_path}\\{folder}\\{html_file}"
            massechet_path = f"{html_path}\\{folder}"
            repair_tag(massechet_daf_path)
            built_xml_header(massechet_daf_path,html_file,folder)
            built_xml_content(massechet_daf_path,folder,html_file,dibour_hamatril_continue,index_file,massechet_dir,massechet_path)
            built_xml_footer(massechet_daf_path,folder,html_file)
            
if __name__ == '__main__':
    main()
