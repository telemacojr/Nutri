#--------------------------------------------------------------------------------------------------#
#                                              Nutri                                               #
#--------------------------------------------------------------------------------------------------#
#                                                                                                  #
#    Data.....: 2023-09-23                                                                         #
#    Autor....: Telêmaco Queiroz Júnior | Henrique Pureza Queiroz                                  #
#    Versão...: 1.0                                                                                #
#    Descrição: aplicativo para montar planos alimentares                                          #
#                                                                                                  #
#--------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------#
#                                           Bibliotecas                                            #
#--------------------------------------------------------------------------------------------------#

import sqlite3

from flask                   import Flask, render_template, request, redirect
from werkzeug.datastructures import MultiDict
from datetime                import datetime
from datetime                import timedelta
from datetime                import date

#--------------------------------------------------------------------------------------------------#
#                                       Funções auxiliares                                         #
#--------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------#
#                                  Função calcula_segunda_feira                                    #
#--------------------------------------------------------------------------------------------------#

def calcula_segunda_feira():
     
    hoje = date.today()

    if   hoje.weekday() == 0:   # segunda-feira - retorna
         return hoje
    else:
         return hoje - timedelta(days = hoje.weekday())

#--------------------------------------------------------------------------------------------------#
#                                        Função soma_dia_data                                      #
#--------------------------------------------------------------------------------------------------#

def soma_dia_data(data, dias):
     
    data_date = datetime.strptime(str(data), "%Y-%m-%d")
    data_soma = data_date + timedelta(days = dias)

    return data_soma

#--------------------------------------------------------------------------------------------------#
#                                        Função soma_dia_data                                      #
#--------------------------------------------------------------------------------------------------#

def dia_semana(data):
     
    if   data.weekday() == 0:
         return 'segunda-feira'
    elif data.weekday() == 1:
         return 'terça-feira'
    elif data.weekday() == 2:
         return 'quarta-feira'
    elif data.weekday() == 3:
         return 'quinta-feira'
    elif data.weekday() == 4:
         return 'sexta-feira'
    elif data.weekday() == 5:
         return 'sábado'
    elif data.weekday() == 6:
         return 'domingo'

#--------------------------------------------------------------------------------------------------#
#                                              ROTAS                                               #
#--------------------------------------------------------------------------------------------------#

app = Flask(__name__)

#--------------------------------------------------------------------------------------------------#
#                                           Página Index                                           #
#--------------------------------------------------------------------------------------------------#

@app.route("/", methods=["GET", "POST"])
def index():
    '''
    Página principal

    Rota: / (raiz)
    '''

    if  request.method == "POST":
        botoes = MultiDict(request.form)

        if   'BotaoPacientes'   in botoes:
              return redirect("/pacientes?filtro_paciente=0")
        elif 'BotaoItens'       in botoes:
              return redirect("/itens?filtro_item=0")

    return render_template("Nutri.html")

#--------------------------------------------------------------------------------------------------#
#                                          Página Paciente                                         #
#--------------------------------------------------------------------------------------------------#

@app.route("/pacientes", methods=["GET", "POST"])
def pagina_paciente():
    '''
    Página Pacientes

    Rota: /pacientes
    '''

    consulta_paciente = request.args.get("filtro_paciente")

    if  request.method == "POST":

        formulario      = request.form.to_dict()
        filtro_paciente = formulario['FiltroPaciente']
        botoes          = MultiDict(request.form)

        if   'BotaoPesquisar'       in botoes:
              return render_template ("Paciente.html",
                                      pacientes         = monta_lista_dicio_pacientes        (filtro_paciente),
                                      filtro_pacientes  = monta_lista_dicio_filtro_pacientes (filtro_paciente))
        elif 'BotaoIncluir'         in botoes:
              print("carregar tela incluir")
              print("chamar rotina que monta tela")
        elif 'BotaoSalvar'          in botoes:
              print("chamar rotina que atualiza dados")
              print("chamar rotina que monta tela")
        elif 'BotaoExcluir'         in botoes:
              print("chamar rotina que deleta dados")
              print("chamar rotina que monta tela")
        elif 'BotaoConsultas'       in botoes:
              return redirect("/consultas?filtro_paciente=" + filtro_paciente)
        elif 'BotaoPlanoDiario'     in botoes:
              return redirect("/plano-diario?filtro_paciente=" + filtro_paciente)
        elif 'BotaoExportarExcel'   in botoes:
              print("chamar rotina que cria o arquivo Excel com o filtro aplicado na tela")
        elif 'BotaoVoltar'          in botoes:
              return redirect("/")

    return render_template("Paciente.html", 
                           pacientes        = monta_lista_dicio_pacientes        (consulta_paciente),
                           filtro_pacientes = monta_lista_dicio_filtro_pacientes (consulta_paciente))

#--------------------------------------------------------------------------------------------------#
#                                            Página Itens                                          #
#--------------------------------------------------------------------------------------------------#

@app.route("/itens", methods=["GET", "POST"])
def pagina_item():
    '''
    Página Itens

    Rota: /itens
    '''

    consulta_item = request.args.get("filtro_item")

    if  request.method == "POST":

        formulario  = request.form.to_dict()
        filtro_item = formulario['FiltroItem']

        le_formulario(formulario)

        botoes      = MultiDict(request.form)

        if   'BotaoPesquisar'       in botoes:
              return render_template ("Item.html",
                                      itens        = monta_lista_dicio_itens        (filtro_item),
                                      filtro_itens = monta_lista_dicio_filtro_itens (filtro_item))
        elif 'BotaoIncluir'         in botoes:
              print("carregar tela incluir")
              print("chamar rotina que monta tela")
        elif 'BotaoSalvar'          in botoes:
              salva_item(formulario)
        elif 'BotaoExcluir'         in botoes:
              exclui_item(formulario)
        elif 'BotaoExportarExcel'   in botoes:
              print("chamar rotina que cria o arquivo Excel com o filtro aplicado na tela")
        elif 'BotaoVoltar'          in botoes:
              return redirect("/")

    return render_template("Item.html", 
                           itens        = monta_lista_dicio_itens        (consulta_item),
                           filtro_itens = monta_lista_dicio_filtro_itens (consulta_item))

#--------------------------------------------------------------------------------------------------#
#                                          Página Consultas                                        #
#--------------------------------------------------------------------------------------------------#

@app.route("/consultas", methods=["GET", "POST"])
def pagina_consultas():
    '''
    Página Consultas

    Rota: /consultas
    '''

    consulta_paciente = request.args.get("filtro_paciente")

    if  request.method  == "POST":

        formulario      = request.form.to_dict()
        filtro_paciente = formulario['FiltroPaciente']
        botoes          = MultiDict(request.form)

        if   'BotaoPesquisar'       in botoes:
              return render_template("Consultas.html", 
                                     consultas        = monta_lista_dicio_consultas        (filtro_paciente),
                                     filtro_pacientes = monta_lista_dicio_filtro_pacientes (filtro_paciente))
        elif 'BotaoIncluir'         in botoes:
              print("carregar tela incluir")
              print("chamar rotina que monta tela")
        elif 'BotaoSalvar'          in botoes:
              print("chamar rotina que atualiza dados")
              print("chamar rotina que monta tela")
        elif 'BotaoExcluir'         in botoes:
              print("chamar rotina que deleta dados")
              print("chamar rotina que monta tela")
        elif 'BotaoExportarExcel'   in botoes:
              print("chamar rotina que cria o arquivo Excel com o filtro aplicado na tela")
        elif 'BotaoVoltar'          in botoes:
              return redirect("/pacientes?filtro_paciente=" + filtro_paciente)

    return render_template("Consultas.html", 
                           consultas        = monta_lista_dicio_consultas        (consulta_paciente),
                           filtro_pacientes = monta_lista_dicio_filtro_pacientes (consulta_paciente))

#--------------------------------------------------------------------------------------------------#
#                                          Página Consultas                                        #
#--------------------------------------------------------------------------------------------------#

@app.route("/plano-diario", methods=["GET", "POST"])
def plano_diario():
    '''
    Plano diário

    Rota: /plano-diario
    '''

    consulta_paciente = request.args.get("filtro_paciente")
    
    if  request.method      == "POST":
        formulario          = request.form.to_dict()
        filtro_paciente     = formulario['FiltroPaciente']
        filtro_data_inicial = formulario['FiltroDataInicial']
        filtro_data_final   = formulario['FiltroDataFinal']
        filtro_dia          = formulario['FiltroDia']
        botoes              = MultiDict(request.form)

        if   'BotaoPesquisar' in botoes: 

              data_inicial_string_Ymd = filtro_data_inicial
              data_final_string_Ymd   = filtro_data_final
              data_dia_string_dmY     = filtro_dia[0:10]
              data_dia_date_Ymd       = datetime.strptime(data_dia_string_dmY,"%d/%m/%Y")
              data_dia_string_Ymd     = data_dia_date_Ymd.strftime("%Y-%m-%d")

              return render_template("PlanoDiario.html", 
                                     planos_diarios      = monta_lista_dicio_plano_diario (filtro_paciente, data_dia_string_Ymd),
                                     filtro_pacientes    = monta_lista_dicio_filtro_pacientes (filtro_paciente),
                                     filtro_data_inicial = data_inicial_string_Ymd,
                                     filtro_data_final   = data_final_string_Ymd,
                                     filtro_dias         = monta_lista_dicio_filtro_dia(data_inicial_string_Ymd, data_final_string_Ymd, data_dia_string_Ymd),
                                     opcoes              = [{'opcao_id': 1, 'opcao': 1},{'opcao_id': 2, 'opcao': 2},{'opcao_id': 3, 'opcao': 3}],
                                     refeicoes           = monta_lista_dicio_filtro_refeicoes ('0'),
                                     itens               = monta_lista_dicio_filtro_itens ('0'),
                                     unidades            = monta_lista_dicio_filtro_unidades ('0'))        
        elif 'BotaoIncluir'       in botoes:
              print("carregar tela incluir")
              print("chamar rotina que monta tela")
        elif 'BotaoSalvar'        in botoes:
              print("chamar rotina que atualiza dados")
              print("chamar rotina que monta tela")
        elif 'BotaoExcluir'       in botoes:
              print("chamar rotina que deleta dados")
              print("chamar rotina que monta tela")
        elif 'BotaoCopiar'        in botoes:
              print("chamar rotina que copia uma linha da tabela referente a uma data em outra ou na mesma")
              print("chamar rotina que monta tela")
        elif 'BotaoCopiarPeriodo' in botoes:
              print("chamar rotina que copia um período dentro de uma data de um outro")
              print("chamar rotina que monta tela")
        elif 'BotaoExportarExcel' in botoes:
              print("chamar rotina que cria o arquivo Excel com o filtro aplicado na tela")
        elif 'BotaoVoltar'        in botoes:
              return redirect("/pacientes?filtro_paciente=" + filtro_paciente)
    
    data_inicial_date_Ymd   = calcula_segunda_feira()
    data_inicial_string_Ymd = data_inicial_date_Ymd.strftime("%Y-%m-%d")
    data_final_string_Ymd   = soma_dia_data(data_inicial_date_Ymd, 6).strftime("%Y-%m-%d")
    filtro_dia              = data_inicial_string_Ymd

    return render_template("PlanoDiario.html", 
                           planos_diarios      = monta_lista_dicio_plano_diario (consulta_paciente, filtro_dia),
                           filtro_pacientes    = monta_lista_dicio_filtro_pacientes (consulta_paciente),
                           filtro_data_inicial = data_inicial_string_Ymd,
                           filtro_data_final   = data_final_string_Ymd,
                           filtro_dias         = monta_lista_dicio_filtro_dia("", "", ""),
                           opcoes              = [{'opcao_id': 1, 'opcao': 1},{'opcao_id': 2, 'opcao': 2},{'opcao_id': 3, 'opcao': 3}],
                           refeicoes           = monta_lista_dicio_filtro_refeicoes ('0'),
                           itens               = monta_lista_dicio_filtro_itens ('0'),
                           unidades            = monta_lista_dicio_filtro_unidades ('0'))

#--------------------------------------------------------------------------------------------------#
#                             Funções para montagem de filtros das páginas                         #
#--------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------#
#                               Função monta_lista_dicio_filtro_pacientes                          #
#--------------------------------------------------------------------------------------------------#

def monta_lista_dicio_filtro_pacientes(filtro_paciente):
    '''
    Monta dicionários para carga de campos e tabelas das páginas

    Função....: monta_lista_dicio_filtro_pacientes
    Parametros: filtro_paciente

    Retorno: lista de dicionários filtro_pacientes com campos:
        - PacienteID: numérico
        - Paciente..: alfanumérico
    '''
    global config

    conn   = sqlite3.connect(config['StringConexao'])
    cursor = conn.cursor()

    sql = ""
    sql = sql + " SELECT PacienteID, "
    sql = sql + "        Paciente "
    sql = sql + " FROM   Paciente "

    cursor.execute(sql)

    dict_pacientes     = {"paciente_id": None,
                          "paciente":    None,
                          "selected":    None}

    filtro_pacientes   = []

    if  filtro_paciente == '0':
        dict_pacientes  = {"paciente_id": 0,
                           "paciente":    "",
                           "selected":    True}
    else:
        dict_pacientes  = {"paciente_id": 0,
                           "paciente":    "",
                           "selected":    False}

    filtro_pacientes.append(dict_pacientes)

    row = cursor.fetchone()

    while row:

        paciente_id = row[0]
        paciente    = row[1]

        if  str(filtro_paciente) == str(paciente_id):
            selected = True
        else:
            selected = False

        dict_pacientes = {"paciente_id": paciente_id,
                          "paciente":    paciente,
                          "selected":    selected}

        filtro_pacientes.append(dict_pacientes)

        row = cursor.fetchone()

    return filtro_pacientes

#--------------------------------------------------------------------------------------------------#
#                                  Função monta_lista_dicio_filtro_dia                             #
#--------------------------------------------------------------------------------------------------#

def monta_lista_dicio_filtro_dia(data_inicial_string_Ymd, data_final_string_Ymd, data_dia_string_Ymd):
    '''
    Monta dicionários para carga de campos e tabelas das páginas

    Função....: monta_lista_dicio_filtro_dia
    Parametros: data_inicial
                data_final

    Retorno: lista de dicionários filtro_dia com campos:
        - dia (data + dia da semana): alfanumérico
    '''

    if  data_inicial_string_Ymd == "" and data_final_string_Ymd == "":
        data_inicial_date_Ymd   = calcula_segunda_feira()
        data_inicial_string_Ymd = data_inicial_date_Ymd.strftime("%Y-%m-%d")
        data_inicial_string_dmY = data_inicial_date_Ymd.strftime("%d/%m/%Y")
        data_final_string_Ymd   = soma_dia_data(data_inicial_date_Ymd, 6).strftime("%Y-%m-%d")
    else:
        data_inicial_date_Ymd   = datetime.strptime(data_inicial_string_Ymd,"%Y-%m-%d")
        data_inicial_string_dmY = data_inicial_date_Ymd.strftime("%d/%m/%Y")
        data_inicial_string_Ymd = data_inicial_date_Ymd.strftime("%Y-%m-%d")
        
    filtro_dias = []

    if data_dia_string_Ymd == data_inicial_string_Ymd or data_dia_string_Ymd == "":
       selected = True
    else:
       selected = False
         
    dict_dias = {"dia":      data_inicial_string_dmY + " (" + dia_semana(data_inicial_date_Ymd) + ")",
                 "selected": selected}
    
    filtro_dias.append(dict_dias)

    data_inicial_date_Ymd = datetime.strptime(data_inicial_string_Ymd, "%Y-%m-%d")
    data_final_date_Ymd   = datetime.strptime(data_final_string_Ymd,   "%Y-%m-%d")
    data_somada_date_Ymd  = data_inicial_date_Ymd

    while data_somada_date_Ymd < data_final_date_Ymd:

        data_somada_date_Ymd   = data_somada_date_Ymd + timedelta(days = 1)

        if data_dia_string_Ymd == data_somada_date_Ymd.strftime("%Y-%m-%d"):
           selected = True
        else:
           selected = False
            
        dict_dias   = {"dia":      datetime.strftime(data_somada_date_Ymd, "%d/%m/%Y") + " (" + 
                                   dia_semana(data_somada_date_Ymd)                    + ")",
                       "selected": selected}        
        
        filtro_dias.append(dict_dias)

    return filtro_dias

#--------------------------------------------------------------------------------------------------#
#                               Função monta_lista_dicio_filtro_refeicoes                          #
#--------------------------------------------------------------------------------------------------#

def monta_lista_dicio_filtro_refeicoes(filtro_refeicao):
    '''
    Monta dicionários para carga de campos e tabelas das páginas

    Função....: monta_lista_dicio_filtro_refeicoes
    Parametros: filtro_refeicao

    Retorno: lista de dicionários filtro_refeicao com campos:
        - RefeicaoID: numérico
        - Refeicao..: alfanumérico
    '''
    global config

    conn   = sqlite3.connect(config['StringConexao'])
    cursor = conn.cursor()

    sql = ""
    sql = sql + " SELECT RefeicaoID, "
    sql = sql + "        Refeicao "
    sql = sql + " FROM   Refeicao "

    cursor.execute(sql)

    dict_refeicao  = {"refeicao_id":  None,
                      "refeicao":     None,
                      "selected":     None}

    filtro_refeicao = []

    if  filtro_refeicao == '0':
        dict_refeicao  = {"refeicao_id": 0,
                          "refeicao":    "",
                          "selected":    True}
    else:
        dict_refeicao  = {"refeicao_id": 0,
                          "refeicao":    "",
                          "selected":    False}

    filtro_refeicao.append(dict_refeicao)

    row = cursor.fetchone()

    while row:

        refeicao_id = row[0]
        refeicao    = row[1]

        if  str(filtro_refeicao) == str(refeicao_id):
            selected = True
        else:
            selected = False

        dict_refeicao  = {"refeicao_id": refeicao_id,
                          "refeicao":    refeicao,
                          "selected":    selected}

        filtro_refeicao.append(dict_refeicao)

        row = cursor.fetchone()

    return filtro_refeicao

#--------------------------------------------------------------------------------------------------#
#                                 Função monta_lista_dicio_filtro_itens                            #
#--------------------------------------------------------------------------------------------------#

def monta_lista_dicio_filtro_itens(filtro_item):
    '''
    Monta dicionários para carga de campos e tabelas das páginas

    Função....: monta_lista_dicio_filtro_itens
    Parametros: item

    Retorno: lista de dicionários filtro_pacientes com campos:
        - ItemID: numérico
        - Item..: alfanumérico
    '''
    global config

    conn   = sqlite3.connect(config['StringConexao'])
    cursor = conn.cursor()

    sql = ""
    sql = sql + " SELECT   ItemID, "
    sql = sql + "          Item "
    sql = sql + " FROM     Item "
    sql = sql + " ORDER BY Item "

    cursor.execute(sql)

    dict_itens  = {"item_id":  None,
                   "item":     None,
                   "selected": None}

    filtro_itens = []

    if  filtro_item == '0':
        dict_itens  = {"item_id":  0,
                       "item":     "",
                       "selected": True}
    else:
        dict_itens  = {"item_id":   0,
                       "item":      "",
                       "selected":  False}

    filtro_itens.append(dict_itens)

    row = cursor.fetchone()

    while row:

        item_id = row[0]
        item    = row[1]

        if  str(filtro_item) == str(item_id):
            selected = True
        else:
            selected = False

        dict_itens  = {"item_id":  item_id,
                       "item":     item,
                       "selected": selected}

        filtro_itens.append(dict_itens)

        row = cursor.fetchone()

    return filtro_itens

#--------------------------------------------------------------------------------------------------#
#                               Função monta_lista_dicio_filtro_unidades                           #
#--------------------------------------------------------------------------------------------------#

def monta_lista_dicio_filtro_unidades(filtro_unidade):
    '''
    Monta dicionários para carga de campos e tabelas das páginas

    Função....: monta_lista_dicio_filtro_unidades
    Parametros: unidade

    Retorno: lista de dicionários filtro_pacientes com campos:
        - unidadeID: numérico
        - unidade..: alfanumérico
    '''
    global config

    conn   = sqlite3.connect(config['StringConexao'])
    cursor = conn.cursor()

    sql = ""
    sql = sql + " SELECT UnidadeID, "
    sql = sql + "        Unidade "
    sql = sql + " FROM   Unidade "

    cursor.execute(sql)

    dict_unidades  = {"unidade_id": None,
                      "unidade":    None,
                      "selected":   None}

    filtro_unidades = []

    if  filtro_unidade == '0':
        dict_unidades  = {"unidade_id": 0,
                          "unidade":    "",
                          "selected":   True}
    else:
        dict_unidades  = {"unidade_id": 0,
                          "unidade":    "",
                          "selected":   False}

    filtro_unidades.append(dict_unidades)

    row = cursor.fetchone()

    while row:

        unidade_id = row[0]
        unidade    = row[1]

        if  str(filtro_unidade) == str(unidade_id):
            selected = True
        else:
            selected = False

        dict_unidades  = {"unidade_id": unidade_id,
                          "unidade":    unidade,
                          "selected":   selected}

        filtro_unidades.append(dict_unidades)

        row = cursor.fetchone()

    return filtro_unidades

#--------------------------------------------------------------------------------------------------#
#                             Funções para montagem das tabelas das páginas                        #
#--------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------#
#                                   Função monta_lista_dicio_pacientes                             #
#--------------------------------------------------------------------------------------------------#

def monta_lista_dicio_pacientes(filtro_paciente):
    '''
    Função....: monta_lista_dicio_pacientes
    Parametros: filtro_paciente

    Retorno: lista de dicionários filtro_pacientes com campos:
        - PacienteID....: numérico
        - Paciente......: alfanumérico
        - DataNascimento: data
        - Telefone......: alfanumérico
        - Email.........: alfanumérico
    '''

    conn   = sqlite3.connect(config['StringConexao'])
    cursor = conn.cursor()

    sql = ""
    sql = sql + " SELECT PacienteID, "
    sql = sql + "        Paciente, "
    sql = sql + "        DataNascimento, "
    sql = sql + "        Telefone, "
    sql = sql + "        Email "
    sql = sql + " FROM   Paciente "

    if  filtro_paciente > '0':
        sql = sql + " WHERE  PacienteID = '" + filtro_paciente + "'"

    cursor.execute(sql)

    dict_pacientes = {"paciente_id":        None,
                      "paciente":           None,
                      "data_de_nascimento": None,
                      "telefone":           None,
                      "email":              None}

    pacientes = []
    row       = cursor.fetchone()

    while row:

        dict_pacientes = {"paciente_id":        row[0],
                          "paciente":           row[1],
                          "data_de_nascimento": row[2],
                          "telefone":           row[3],
                          "email":              row[4]}

        pacientes.append(dict_pacientes)

        row = cursor.fetchone()

    return pacientes

#--------------------------------------------------------------------------------------------------#
#                                     Função monta_lista_dicio_itens                               #
#--------------------------------------------------------------------------------------------------#

def monta_lista_dicio_itens(filtro_item):
    '''
    Função....: monta_lista_dicio_itens
    Parametros: filtro_item

    Retorno: lista de dicionários filtro_itens com campos:
        - itemID: numérico
        - item..: alfanumérico
    '''

    conn   = sqlite3.connect(config['StringConexao'])
    cursor = conn.cursor()

    sql = ""
    sql = sql + " SELECT   ItemID, "
    sql = sql + "          Item "
    sql = sql + " FROM     Item "

    if  filtro_item > '0':
        sql = sql + " WHERE itemID = " + filtro_item

    sql = sql + " ORDER BY item"

    cursor.execute(sql)

    dict_itens = {"linha":   None,
                  "item_id": None,
                  "item":    None}

    itens = []
    linha = 1
    row   = cursor.fetchone()

    while row:

        dict_itens = {"linha":   linha,
                      "item_id": row[0],
                      "item":    row[1]}

        itens.append(dict_itens)

        linha = linha + 1

        row   = cursor.fetchone()

    return itens

#--------------------------------------------------------------------------------------------------#
#                                   Função monta_lista_dicio_consultas                             #
#--------------------------------------------------------------------------------------------------#

def monta_lista_dicio_consultas(filtro_paciente):
    '''
    Função....: monta_lista_dicio_consultas
    Parametros: filtro_paciente

    Retorno: lista de dicionários filtro_pacientes com campos:
        - Data: data
        - IMC.: alfanumérico
        - CC..: alfanumérico
        - G...: alfanumérico        
    '''
    conn   = sqlite3.connect(config['StringConexao'])
    cursor = conn.cursor()

    sql = ""
    sql = sql + " SELECT Data, "
    sql = sql + "        IMC, "
    sql = sql + "        CC, "
    sql = sql + "        G "
    sql = sql + " FROM   Consulta "
    sql = sql + " WHERE  PacienteID = " + filtro_paciente

    cursor.execute(sql)

    dict_consultas = {"data": None,
                      "imc":  None,
                      "cc":   None,
                      "g":    None}

    consultas = []
    row       = cursor.fetchone()

    while row:

        dict_consultas = {"data": row[0],
                          "imc":  row[1],
                          "cc":   row[2],
                          "g":    row[3]}

        consultas.append(dict_consultas)

        row = cursor.fetchone()

    return consultas

#--------------------------------------------------------------------------------------------------#
#                              Função monta_lista_dicio_plano_diario                               #
#--------------------------------------------------------------------------------------------------#

def monta_lista_dicio_plano_diario(filtro_paciente, data_dia_string_Ymd):
    '''
    Função....: monta_lista_dicio_plano_diario
    Parametros: filtro_paciente

    Retorno: lista de dicionários filtro_plano_diario com campos:     
        - Data:       alfanumérico
        - RefeicaoID: numérico
        - Refeicao:   alfanumérico
        - Horario:    alfanumérico
        - Opcao:      numérico
        - ItemID:     numérico
        - Item:       alfanumérico             
        - Quantidade: numérico
        - UnidadeID:  numérico
        - Unidade:    alfanumérico
    '''    

    conn   = sqlite3.connect(config['StringConexao'])
    cursor = conn.cursor()

    sql = ""
    sql = sql + " SELECT     PD.Data, "
    sql = sql + "            CASE "
    sql = sql + "               WHEN R.RefeicaoID = 6 "
    sql = sql + "               THEN 9 "
    sql = sql + "               ELSE R.RefeicaoID "
    sql = sql + "            END         AS RefeicaoID, "
    sql = sql + "            R.Refeicao, "
    sql = sql + "            R.Horario, "
    sql = sql + "            P.Opcao, "
    sql = sql + "            I.ItemID, "
    sql = sql + "            I.Item, "
    sql = sql + "            C.Quantidade, "
    sql = sql + "            U.UnidadeID, "
    sql = sql + "            U.Unidade "
    sql = sql + " FROM       PlanoDiario AS PD "
    sql = sql + " INNER JOIN Paciente    AS Pac ON PD.PacienteID = Pac.PacienteID "
    sql = sql + " INNER JOIN Plano       AS P   ON PD.PlanoID    = P.PlanoID "
    sql = sql + " INNER JOIN Refeicao    AS R   ON P.RefeicaoID  = R.RefeicaoID "
    sql = sql + " INNER JOIN Cardapio    AS C   ON P.CardapioID  = C.CardapioID "
    sql = sql + " INNER JOIN Item        AS I   ON C.ItemID      = I.ItemID "
    sql = sql + " INNER JOIN Unidade     AS U   ON C.UnidadeID   = U.UnidadeID "
    sql = sql + " WHERE      PD.PacienteID  = "  + filtro_paciente
    sql = sql + " AND        PD.Data        = '" + data_dia_string_Ymd + "'"

    cursor.execute(sql)

    dict_plano_diario   = {"Data":       None,
                           "RefeicaoID": None,
                           "Refeicao":   None,
                           "Horario":    None,
                           "Opcao":      None,
                           "ItemID":     None,
                           "Item":       None,                           
                           "Quantidade": None,
                           "UnidadeID":  None,
                           "Unidade":    None}

    plano_diario = []
    row          = cursor.fetchone()

    while row:

        dict_plano_diario   = {"Data":       row[0],
                               "RefeicaoID": row[1],
                               "Refeicao":   row[2],
                               "Horario":    row[3],
                               "Opcao":      row[4],
                               "ItemID":     row[5],
                               "Item":       row[6],                               
                               "Quantidade": row[7],
                               "UnidadeID":  row[8],
                               "Unidade":    row[9]}
    
        plano_diario.append(dict_plano_diario)

        row = cursor.fetchone()

    return plano_diario

#--------------------------------------------------------------------------------------------------#
#                                       Função obtem_parametros                                    #
#--------------------------------------------------------------------------------------------------#

def obtem_parametros():
     
    config = {'StringConexao':   None}

    Pasta   = 'C:/Users/telem/Documents/PythonCourse/Nutri/' 
    Arquivo = 'config.txt'

    with open(Pasta + Arquivo,'r') as f:
        linhas = f.readlines()

    for linha in linhas:
        linha_campos            = linha.strip().split(chr(9))
        config[linha_campos[0]] = linha_campos[1]

    f.close()

    return config

#--------------------------------------------------------------------------------------------------#
#                                       Função obtem_parametros                                    #
#--------------------------------------------------------------------------------------------------#

def le_formulario(formulario):

    #print(formulario)

    for  campo in formulario:
         #print(campo, ':', formulario[campo])
         if campo[0:17] == 'CheckboxSeleciona':
            print(campo[0:17], ':', campo[18:20], formulario['Item_' + campo[18:20]])

#--------------------------------------------------------------------------------------------------#
#                                 Rotinas para Incluir, Salvar, Excluir                            #
#--------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------#
#                                          Função inclui_item                                      #
#--------------------------------------------------------------------------------------------------#

def inclui_item():
     
     print('x')

#--------------------------------------------------------------------------------------------------#
#                                          Função salva_item                                       #
#--------------------------------------------------------------------------------------------------#

def  salva_item(formulario):

    conn   = sqlite3.connect(config['StringConexao'])
    cursor = conn.cursor()
   
    for  campo in formulario:

         if campo[0:17] == 'CheckboxSeleciona':

            sql = ""
            sql = sql + " UPDATE Item "
            sql = sql + " SET    Item = '" + formulario['Item_' + campo[18:20]] + "'"
            sql = sql + " WHERE  ItemID = " + campo[18:20]

            cursor.execute(sql)
            conn.commit()

#--------------------------------------------------------------------------------------------------#
#                                         Função exclui_item                                       #
#--------------------------------------------------------------------------------------------------#

def  exclui_item(formulario):

    conn   = sqlite3.connect(config['StringConexao'])
    cursor = conn.cursor()
   
    for  campo in formulario:

         if campo[0:17] == 'CheckboxSeleciona':

            sql = ""
            sql = sql + " DELETE "
            sql = sql + " FROM   Item "
            sql = sql + " WHERE  ItemID = " + campo[18:20]

            cursor.execute(sql)
            conn.commit()

#--------------------------------------------------------------------------------------------------#
#                                           Rotina principal                                       #
#--------------------------------------------------------------------------------------------------#

if  __name__ == "__main__":
    config = obtem_parametros()    
    app.run(debug=True)