def get_docx_text(path):
    """
    Take the path of a docx file as argument, return the text in unicode.
    """
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    paragraphs = []
    for paragraph in tree.getiterator(PARA):
        texts = [node.text
                 for node in paragraph.getiterator(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))

    return '\n\n'.join(paragraphs)
#reference: https://gist.github.com/etienned/7539105#file-extractdocx-py
#loop through the directory and extract all R from docx
"""running issue:
    don't run this with docx opened with MS word
because the MS word generates temp file
and I did not set auto-reconize file type method
"""
def generates_lists(texts, output_path):
    output_full_path = output_path + "/paragraph.txt"
    output = open(output_full_path, "w")
    #text method: get_docx_text(doc_path)
    output.write(texts)
    output.close()
    #take R lines in list
    lines = []
    rd = open(output_full_path, "rt")
    for line in rd:
        lines.append(line)
    rd.close()
    #append list here
    for line in lines:
        if line[0] == 'R':
            line = line.translate({ord(c): None for c in 'R:'})
            if len(line.split()) > 1:
                value_list.append(line)
        elif line[0] != 'R':
            if line != '\n' and line[1] == 'R':
                line = line.translate({ord(c): None for c in 'R:'})
                if len(line.split()) > 1:
                    value_list.append(line)
    return value_list

def tidy_markdown(exc_path, kws_path):
    exc = open(exc_path,"rt")
    kws = open(kws_path,"rt")
    with open(sum_path, 'w') as s:
        s.write("**sum:**\n**excerpts:**\n%s\n**keywords:**\n%s\n" % (exc.read(), kws.read(),))
    current_sum = open(sum_path,"rt")
    with open(general_sum, "a") as g:
        g.write("# %s\n%s\n" % (directory_name, current_sum.read(),))
    current_sum.close()
    exc.close()
    kws.close()
    #reset mem
    open(exc_path, 'w').close()
    open(kws_path, 'w').close()
    os.remove(ans_full_path)
    os.remove(exc_path)
    os.remove(kws_path)

if __name__ == '__main__':
    try:
        from xml.etree.cElementTree import XML
    except ImportError:
        from xml.etree.ElementTree import XML
    import os
    import sys
    import errno
    import zipfile
    import argparse
    import main_processes as mp

    # argument parser that passes file pathes
    parser = argparse.ArgumentParser(description='Input the path to text data files.')
    parser.add_argument('-i', '--input', required = True, help = 'The path of text data files.')
    parser.add_argument('-o', '--output', required = True, help = 'The path of output files.')
    parser.add_argument('-p', '--phrase', required = True, help = 'The phrase limit in pytextrank.')
    parser.add_argument('-w', '--word', required = True, help = 'THe word limit in a sentence.')
    args = parser.parse_args()

    """
    Module that extract text from MS XML Word document (.docx).
    (Inspired by python-docx <https://github.com/mikemaccana/python-docx>)
    """
    #********* reference: https://gist.github.com/leonardreidy/5931417
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'

    value_list = []
    special_signs = "Data_Files/special_signs.txt"

    # create path for a general sum markdown
    general_sum = args.output + "/" + "general_sumarization.md"

    """ 1. Get i-th docx texts, put it in output.txt
        2. append output.txt in lines[] (i-th file)
        3. append lines[] in key and value lists[]"""
    """for linux path name only"""
    directory_name = os.path.basename(args.input)
    directory_path = args.output + "/" + directory_name + "/"
    #text to analyze path
    ans_full_path = directory_path + "ans.txt"
    sum_path = directory_path + "sum.md"

    exc_path = directory_path + "exc.txt"
    kws_path = directory_path + "kws.txt"

    try: #in case bad things happen
        os.makedirs(directory_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    #to markdown
    ans_list = generates_lists(get_docx_text(args.input), directory_path)
    # get_one_answer_para_file(ans_list, directory_path)
    for item in ans_list:
        with open(ans_full_path, 'w') as ans:
            ans.write(item)
        mp.structure(ans_full_path, directory_path, special_signs, args.phrase, args.word, exc_path, kws_path)
    tidy_markdown(exc_path, kws_path)
