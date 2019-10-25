

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
    '\\end{center}' +enter+\
    '\\captionof{figure}{'+caption+'}' + enter

    return figurecode