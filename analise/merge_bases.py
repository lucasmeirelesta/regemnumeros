import pandas as pd

def import_base(agencia):
    '''
    :param agencia: Agency from which we want to export csv

    :return:
    Returns two data frames, one referring to contributions and the other to the participation mechanisms
    '''

    agencia_dic = {'ana': '1Lj9Gz_JBL5h8j339fpcxlf8m6tfLApUNT52vsvw84D0',
                   'ancine': '1ZFpDOLANZwq1smqV49GBpMRQLB_3tbO_xQmyPOn64ug'}

    contribuicoes = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                                agencia_dic[agencia] +
                                '/export?gid=1665848903&format=csv', encoding = 'utf-8')


    aux_drop = [i for i in contribuicoes.columns if 'Unnamed' in i]
    contribuicoes = contribuicoes.drop(aux_drop, axis=1)

    mecanismos = pd.read_csv('https://docs.google.com/spreadsheets/d/' +
                                 agencia_dic[agencia] +
                                 '/export?gid=256430091&format=csv')

    aux_drop = [i for i in mecanismos.columns if 'Unnamed' in i]
    mecanismos = mecanismos.drop(aux_drop, axis=1)

    return contribuicoes, mecanismos

ana_contribuicoes, ana_mecanismos = import_base('ana')
ancine_contribuicoes, ancine_mecanismos = import_base('ancine')

agencias_contribuicoes = pd.concat([ana_contribuicoes, ancine_contribuicoes])
agencias_mecanismos = pd.concat([ana_mecanismos, ancine_mecanismos])

agencias_mecanismos = agencias_mecanismos.reset_index(drop = True)
agencias_contribuicoes= agencias_contribuicoes.reset_index(drop = True)

agencias_contribuicoes.Categoria_Participante[agencias_contribuicoes['Entidade_Representativa'] == "Sim"] = 'Entidade Representativa'
agencias_contribuicoes = agencias_contribuicoes.drop('Entidade_Representativa', axis = 1)


def remove_r(x):
    if type(x) == str:
        x = x.replace('\r', '')
        x = x.split()
        x = ' '.join(x)
        return x
    else:
        return x

for i in agencias_mecanismos.columns:
    agencias_mecanismos[i] = agencias_mecanismos[i].apply(lambda x: remove_r(x))

for i in agencias_contribuicoes.columns:
    agencias_contribuicoes[i] = agencias_contribuicoes[i].apply(lambda x: remove_r(x))


agencias_mecanismos.to_csv('agencias_mecanismos.csv', index = False)
agencias_contribuicoes.to_csv('agencias_contribuicoes.csv', index =False)



#https://erikrood.com/Posts/py_gsheets.html