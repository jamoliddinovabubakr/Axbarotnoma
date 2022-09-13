from docxcompose.composer import Composer
from docx import Document as Document_compose


def combine_all_docx(filename_master, files_list):
    try:
        number_of_sections = len(files_list)
        master = Document_compose(filename_master)
        composer = Composer(master)
        for i in range(1, number_of_sections):
            doc_temp = Document_compose(files_list[i])
            composer.append(doc_temp)
        composer.save("C:\\Django\\axborotnomadtm\\media\\combined_file.docx")

    except PermissionError:
        print('Siz birinchi faylni yopishingiz kerak !')


# filename_master = 'C:\\Django\\axborotnomadtm\\media\\files\\user_1\\6._Тўраев_Юсуф_Жумма_угли_nfbMPRj.docx'
# files_list = [
#     'C:\\Django\\axborotnomadtm\\media\\files\\user_1\\6._Тўраев_Юсуф_Жумма_угли_nfbMPRj.docx',
#     'C:\\Django\\axborotnomadtm\\media\\files\\user_1\\data_count_kvq5Zgy.docx',
#     'C:\\Django\\axborotnomadtm\\media\\files\\user_4\\Ахборотнома_журнали_муаллифлари_учун_коидалар.docx',
#     'C:\\Django\\axborotnomadtm\\media\\files\\user_5\\Ахборотнома_журнали_муаллифлари_учун_коидалар.docx'
# ]
#
# combine_all_docx(filename_master, files_list)