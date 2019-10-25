'''
makes a table from an ented dataframe
columns should be string in the format of latex code (ie. 'c|rr|l' for centered, right right and left aligned columns 
with vertical line after first and third column (number of columns must be equal to dataframe columns)
'''
ent = '\r\n'

def table(data,columns,label,caption):
    
    NR = len(data[data.columns[0]])
    NC = len(data.columns)
    #title row
    title = ''
    for head in data.columns:
        title = title + head + '&'
    title = title[0:(len(title)-1)] + '\\\ \hline '

    body = ''
    
    for r in range(NR):
        for c in range(NC):
            body = body+str(data[data.columns[c]][r])+'&'
        body = body[0:(len(body)-1)] + '\\\ '+ ent
    
    tab = \
    '\\begin{table}[h]'+ent+\
    '\\centering'+ent+\
    '\\begin{tabular}{'+ columns +'}'+ent+\
    title   +ent+\
    body +\
    '\\end{tabular}'+ent+\
    '\\label{tab:'+label+'}'+ent+\
    '\\caption{'+caption+'}'+ent+\
    '\\end{table}'
    
    return tab

def centertable(data,columns,label,caption):
    
    NR = len(data[data.columns[0]])
    NC = len(data.columns)
    #title row
    title = ''
    for head in data.columns:
        title = title + head + '&'
    title = title[0:(len(title)-1)] + '\\\ \hline '

    body = ''
    
    for r in range(NR):
        for c in range(NC):
            body = body+str(data[data.columns[c]][r])+'&'
        body = body[0:(len(body)-1)] + '\\\ '+ ent
    
    tab = \
    '\\begin{center}'+ent+\
    '\\begin{tabular}{'+ columns +'}'+ent+\
    title   +ent+\
    body +\
    '\\end{tabular}'+ent+\
    '\\label{tab:'+label+'}'+ent+\
    '\\end{center}'+ent+\
    '\\captionof{table}{'+caption+'}'+ent+\
    '\\vspace(2.5mm)'
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
    title = title[0:(len(title)-1)] + '\\\ \hline '

    body = ''
    
    for r in range(NR):
        for c in range(NC):
            if c == moneycolumn:
                body = body+'\\texteuro '+str(data[data.columns[c]][r])+'&'
            else:
                body = body+str(data[data.columns[c]][r])+'&'
        body = body[0:(len(body)-1)] + '\\\ '+ ent
    
    tab = \
    '\\begin{center}'+ent+\
    '\\begin{tabular}{'+ columns +'}'+ent+\
    title   +ent+\
    body +\
    '\\end{tabular}'+ent+\
    '\\label{tab:'+label+'}'+ent+\
    '\\end{center}'+ent+\
    '\\captionof{table}{'+caption+'}'+ent+\
    '\\vspace(2.5mm)'
    return tab
def moneytable(data,label,caption):


    NR = len(data[data.columns[0]])
    NC = len(data.columns)
    #title row
    title = ''
    for head in data.columns:
        title = title + head + '&'
    title = title[0:(len(title)-1)] + '\\\ \hline '

    body = ''
    
    for r in range(NR):
        for c in range(NC):
            body = body+str(data[data.columns[c]][r])+'&'
        body = body[0:(len(body)-1)] + '\\\ '+ ent
    
    tab = \
    '\\begin{table}[h]'+ent+\
    '\\centering'+ent+\
    '\\begin{tabular}{'+ columns +'}'+ent+\
    title   +ent+\
    body +\
    '\\end{tabular}'+ent+\
    '\\label{tab:'+label+'}'+ent+\
    '\\caption{'+caption+'}'+ent+\
    '\\end{table}'
    
    return tab