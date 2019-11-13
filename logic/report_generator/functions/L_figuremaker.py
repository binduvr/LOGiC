enter =  '\r\n'

def figure(figurepath, caption ,label):
    figurecode = \
    '\\begin{figure}[h]' + enter + \
    '\\centering' + enter + \
    '\\includegraphics[width=\\linewidth]{'+figurepath+'}' + enter + \
    '\\caption{'+caption+'}' + enter + \
    '\\label{fig:'+label+'}' + enter + \
    '\\end{figure}'
    return figurecode

# following function requires package 'caption'
def multicolfigure(figurepath, caption ,label):
    figurecode = \
    '\\begin{center}' + enter + \
    '\\includegraphics[width=\\linewidth]{'+figurepath+'}' + enter + \
    '\\end{center}'
    if caption != None:
        figurecode = figurecode +enter+\
        '\\captionof{figure}{'+caption+'}' + enter
    return figurecode

def rightsmallfigure(figurepath, caption ,label):
    figurecode = \
    '\\begin{flushright}' + enter + \
    '\\includegraphics[width=0.4\\linewidth]{'+figurepath+'}' + enter + \
    '\\end{flushright}'
    if caption != None:
        figurecode = figurecode +enter+\
        '\\captionof{figure}{'+caption+'}' + enter
    return figurecode
