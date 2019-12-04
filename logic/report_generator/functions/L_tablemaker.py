'''
makes a table from an entered dataframe
columns should be string in the format of latex code (ie. 'c|rr|l' for centered, right right and left aligned columns
with vertical line after first and third column (number of columns must be equal to dataframe columns)
'''
ent = '\n'

def centertable(data,columns,label,caption):

    NR = len(data[data.columns[0]])
    NC = len(data.columns)
    #title row
    title = ''
    for head in data.columns:
        title = title + head + '&'
    title = title[0:(len(title)-1)] + '\\\ \\hline '

    body = ''

    for r in range(NR):
        for c in range(NC):
            body = body+str(data[data.columns[c]][r])+'&'
        body = body[0:(len(body)-1)] + '\\\ '+ ent

    tab = \
    '\n\\begin{minipage}[t]{0.5\\textwidth}'+ent+\
    '{\\color{black}'+\
    '\\begin{flushleft}'+ent+\
    '\\begin{tabular}{'+ columns +'}'+ent+\
    '\\hline '+ title   +ent+\
    body +\
    '\\hline'+ent+\
    '\\end{tabular}'+ent+\
    '\\captionof{table}{'+caption+'}'+\
    '\\label{tab:'+label+'}'+ent+\
    '\\end{flushleft}}'+\
    '\\vspace{0.5mm}'+\
    '\\end{minipage}'
    return tab

#only two columned tables.
#\usepackage{currency}
#\DefineCurrency{EUR}{name={euro},plural={euros},symbol={\euro},iso={EUR},kind=iso,base=2}

'''
moneycolumn is the index of the column in the df that contains the money; default the second column
'''
def centermoneytable(data,columns,label,caption,moneycolumn=1):

    NR = len(data[data.columns[0]])
    NC = len(data.columns)
    #title row
    title = ''
    for head in data.columns:
        title = title + head + '&'
    title = title[0:(len(title)-1)] + '\\\ \\hline '

    body = ''

    for r in range(NR):
        for c in range(NC):
            if c == moneycolumn:
                body = body+'\\texteuro \\hfill'+str(data[data.columns[c]][r])+'&'
            else:
                body = body+str(data[data.columns[c]][r])+'&'
        body = body[0:(len(body)-1)] + '\\\ '+ ent

    tab = \
    '\n\\begin{minipage}[t]{0.5\\textwidth}'+\
    '{\\color{black}'+\
    '\\begin{flushleft}'+\
    '\\begin{tabular}{'+ columns +'}'+\
    '\\hline '+ title+ent+\
    body +\
    '\\hline'+ent+\
    '\\end{tabular}'+ent+\
    '\\label{tab:'+label+'}'+ent+\
    '\\captionof{table}{'+caption+'}'+\
    '\\end{flushleft}}'+\
    '\\vspace{0.5mm}'+\
    '\\end{minipage}'
    return tab
