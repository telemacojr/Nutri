"""
Arquivo principal do aplicativo "Nutri". Contém as rotas das páginas.
"""

#------------------------------------------------------------------------------#
#                            CONFIGURAÇÃO INICIAL                              #
#------------------------------------------------------------------------------#

# Importações
from flask                   import Flask, request, render_template
from utils.misc              import obter_configuracoes, calcula_segunda_feira, soma_dia_data
from utils.combos            import Combos
from utils.tabelas           import Tabelas
from utils.crud              import CRUD
from datetime                import datetime

# Obter caminho do banco de dados
db_path = obter_configuracoes("./config.xml")["BancoDeDados"]

# Instância do aplicativo Flask e das classes dos Combos e Tabelas
app     = Flask     (__name__)
combos  = Combos    (db_path)
tabelas = Tabelas   (db_path)
crud    = CRUD      (db_path)

#------------------------------------------------------------------------------#
#                              PÁGINA INICIAL (/)                              #
#------------------------------------------------------------------------------#

@app.route("/", methods=["GET", "POST"])
def pagina_inicial():
    """
    ### Página inicial

    Rota: /
    """

    return render_template("index.html")

#------------------------------------------------------------------------------#
#                         PÁGINA DO PACIENTE (/pacientes)                      #
#------------------------------------------------------------------------------#

@app.route("/pacientes", methods=["GET", "POST"])
def pagina_dos_pacientes():
    """
    ### Página dos pacientes

    Rota: /pacientes
    """

    # Obtêm o id numérico do paciente
    paciente_id = request.args.get("paciente_id")
    paciente_id = int(paciente_id) if paciente_id else 0

    # Recebe um formulário via POST com todos os inputs da página
    if request.method == "POST":
        # Obtêm os dados em dicionários com e sem o botão que os enviou
        formulario      = request.form.to_dict()

        # Obtêm o id do paciente selecionado
        id_paciente_selecionado = int(formulario["ComboPaciente"])

        # Formulário
        if "Pesquisar" in formulario:
            return render_template(
                "Paciente.html",
                pacientes           = tabelas.montar_tabela_de_pacientes(id_paciente_selecionado),
                combo_pacientes     = combos.montar_combo_dos_pacientes(id_paciente_selecionado),
                paciente_id         = id_paciente_selecionado
            )
        # elif "Incluir" in botoes:
            # Código a ser escrito
        # elif "Salvar" in botoes:
            # Código a ser escrito
        # elif "ExportarExcel" in botoes:
            # Código a ser escrito

    return render_template(
        "Paciente.html",
        pacientes           = tabelas.montar_tabela_de_pacientes(paciente_id),
        combo_pacientes     = combos.montar_combo_dos_pacientes(paciente_id),
        paciente_id         = paciente_id
    )


#------------------------------------------------------------------------------#
#                            PÁGINA DOS ITENS (/itens)                         #
#------------------------------------------------------------------------------#

@app.route("/itens", methods=["GET", "POST"])
def pagina_dos_itens():
    """
    ### Página dos itens

    Rota: /itens
    """

    # Obtêm o id numérico do item a ser exibido
    item_id = request.args.get("item_id")
    item_id = int(item_id) if item_id else 0

    # Recebe um formulário via POST com todos os inputs da página
    if request.method == "POST":

        # Obtêm os dados em dicionários com e sem o botão que os enviou
        formulario = request.form.to_dict()

        # Obtêm o item selecionado
        item_selecionado = int(formulario["ComboItem"])
        # crud.ler_formulario(formulario)

        # Redirecionamentos dos botões
        if "Pesquisar" in formulario:
            return render_template(
                "Item.html",
                combo_itens = combos.montar_combo_dos_itens(item_selecionado),
                itens       = tabelas.montar_tabela_de_itens(item_selecionado, False)
            )
        elif "Incluir" in formulario:
            return render_template(
                "Item.html",
                combo_itens = combos.montar_combo_dos_itens(0),
                itens       = tabelas.montar_tabela_de_itens(0, True)
            )
        elif "Salvar" in formulario:
            # Se estiver incluindo um item novo
            if "CheckboxSeleciona_0" in formulario:
                if formulario["Item_0"]:
                    success = crud.incluir_item(formulario["Item_0"])

                    if success:
                        return render_template(
                            "Item.html",
                            combo_itens = combos.montar_combo_dos_itens(0),
                            itens       = tabelas.montar_tabela_de_itens(0, False),
                            mensagem    = "Item incluído com sucesso!"
                        )
                    else:
                        return render_template(
                            "Item.html",
                            combo_itens = combos.montar_combo_dos_itens(0),
                            itens       = tabelas.montar_tabela_de_itens(0, True),
                            mensagem    = "Erro: item com esse nome já existe. Digite outro nome."
                        )
                else:
                    return render_template(
                        "Item.html",
                        combo_itens = combos.montar_combo_dos_itens(0),
                        itens       = tabelas.montar_tabela_de_itens(0, True),
                        mensagem    = "Erro: digite um nome para o item."
                    )
            # Atualizando item
            else:
                for key in formulario.keys():
                    if key.startswith("CheckboxSeleciona_"):
                        crud.atualizar_item(key.split("_")[1], formulario[f'Item_{key.split("_")[1]}'])

                        return render_template(
                            "Item.html",
                            combo_itens = combos.montar_combo_dos_itens(item_id),
                            itens       = tabelas.montar_tabela_de_itens(item_id, False),
                            mensagem    = "Item atualizado com sucesso!"
                        )

                return render_template(
                    "Item.html",
                    combo_itens = combos.montar_combo_dos_itens(item_id),
                    itens       = tabelas.montar_tabela_de_itens(item_id, False),
                    mensagem    = "Erro: marque qual item vai atualizar."
                )
        elif "Excluir" in formulario:
            for key in formulario.keys():
                if key.startswith("CheckboxSeleciona_"):
                    crud.excluir_item(key.split("_")[1])

                    return render_template(
                        "Item.html",
                        combo_itens = combos.montar_combo_dos_itens(item_id),
                        itens       = tabelas.montar_tabela_de_itens(item_id, False),
                        mensagem    = "Item excluído com sucesso!"
                    )

            return render_template(
                "Item.html",
                combo_itens = combos.montar_combo_dos_itens(item_id),
                itens       = tabelas.montar_tabela_de_itens(item_id, False),
                mensagem    = "Erro: marque qual item vai excluir."
            )
        # elif "ExportarExcel" in botoes:
            # Código a adicionar

    return render_template(
        "Item.html",
        combo_itens = combos.montar_combo_dos_itens(item_id),
        itens       = tabelas.montar_tabela_de_itens(item_id, False)
    )

#------------------------------------------------------------------------------#
#                        PÁGINA DAS CONSULTAS (/consultas)                     #
#------------------------------------------------------------------------------#

@app.route("/consultas", methods=["GET", "POST"])
def pagina_das_consultas():
    """
    ### Página das consultas

    Rota: /consultas
    """

    # Obtêm o id numérico do paciente
    paciente_id = request.args.get("paciente_id")
    paciente_id = int(paciente_id) if paciente_id else 0

    # Formulário enviado via POST com todos os inputs da página
    if request.method == "POST":

        # Obtêm os inputs como dicionários com e sem o botão que os enviou
        formulario  = request.form.to_dict()

        # Obtêm o paciente selecionado
        id_paciente_selecionado = int(formulario["ComboPaciente"])

        # Redirecionamentos dos botões
        if "Pesquisar" in formulario:
            return render_template(
                "Consultas.html",
                consultas       = tabelas.montar_tabela_de_consultas(id_paciente_selecionado),
                combo_pacientes = combos.montar_combo_dos_pacientes(id_paciente_selecionado),
                paciente_id     = id_paciente_selecionado
            )
        # elif "Incluir" in botoes:
            # Código a adicionar
        # elif "Salvar" in botoes:
            # Código a adicionar
        # elif "Excluir" in botoes:
            # Código a adicionar
        # elif "ExportarExcel" in botoes:
            # Código a adicionar

    return render_template(
        "Consultas.html",
        consultas       = tabelas.montar_tabela_de_consultas(paciente_id),
        combo_pacientes = combos.montar_combo_dos_pacientes(paciente_id),
        paciente_id     = paciente_id
    )


#------------------------------------------------------------------------------#
#                     PÁGINA DO PLANO DIÁRIO (/plano_diario)                   #
#------------------------------------------------------------------------------#

@app.route("/plano_diario", methods=["GET", "POST"])
def pagina_do_plano_diario():
    """
    ### Plano diário

    Rota: /plano_diario
    """

    paciente_id = request.args.get("paciente_id")
    paciente_id = int(paciente_id) if paciente_id else 0

    opcoes = [
        {
            "opcao_id"  : 1,
            "opcao"     : 1
        },
        {
            "opcao_id"  : 2,
            "opcao"     : 2
        },
        {
            "opcao_id"  : 3,
            "opcao"     : 3
        }
    ]

    if  request.method      == "POST":
        formulario          = request.form.to_dict()
        filtro_paciente     = formulario['FiltroPaciente']
        filtro_data_inicial = formulario['FiltroDataInicial']
        filtro_data_final   = formulario['FiltroDataFinal']
        filtro_dia          = formulario['FiltroDia']

        if 'Pesquisar' in formulario:
            data_inicial_string_Ymd = filtro_data_inicial
            data_final_string_Ymd   = filtro_data_final
            data_dia_string_dmY     = filtro_dia[0:10]
            data_dia_date_Ymd       = datetime.strptime(data_dia_string_dmY,"%d/%m/%Y")
            data_dia_string_Ymd     = data_dia_date_Ymd.strftime("%Y-%m-%d")

            return render_template(
                "PlanoDiario.html",
                planos_diarios      = tabelas.montar_tabela_do_plano_diario(paciente_id, data_dia_string_Ymd),
                filtro_pacientes    = combos.montar_combo_dos_pacientes(paciente_id),
                filtro_data_inicial = data_inicial_string_Ymd,
                filtro_data_final   = data_final_string_Ymd,
                filtro_dias         = combos.montar_selecao_das_datas(data_inicial_string_Ymd, data_final_string_Ymd, data_dia_string_Ymd),
                opcoes              = opcoes,
                refeicoes           = combos.montar_combo_das_refeicoes(0),
                itens               = combos.montar_combo_dos_itens(0),
                unidades            = combos.montar_combo_das_unidades(0),
                paciente_id         = paciente_id
            )
        # elif 'BotaoIncluir'       in botoes:
        # elif 'BotaoSalvar'        in botoes:
        # elif 'BotaoExcluir'       in botoes:
        # elif 'BotaoCopiar'        in botoes:
        # elif 'BotaoCopiarPeriodo' in botoes:
        # elif 'BotaoExportarExcel' in botoes:


    data_inicial_date_Ymd   = calcula_segunda_feira()
    data_inicial_string_Ymd = data_inicial_date_Ymd.strftime("%Y-%m-%d")
    data_final_string_Ymd   = soma_dia_data(data_inicial_date_Ymd, 6).strftime("%Y-%m-%d")
    filtro_dia              = data_inicial_string_Ymd

    return render_template(
        "PlanoDiario.html",
        planos_diarios      = tabelas.montar_tabela_do_plano_diario(paciente_id, filtro_dia),
        filtro_pacientes    = combos.montar_combo_dos_pacientes(paciente_id),
        filtro_data_inicial = data_inicial_string_Ymd,
        filtro_data_final   = data_final_string_Ymd,
        filtro_dias         = combos.montar_selecao_das_datas("", "", ""),
        opcoes              = opcoes,
        refeicoes           = combos.montar_combo_das_refeicoes(0),
        itens               = combos.montar_combo_dos_itens(0),
        unidades            = combos.montar_combo_das_unidades(0),
        paciente_id         = paciente_id
    )


#------------------------------------------------------------------------------#
#                       ROTINA DE EXECUÇÃO DO APLICATIVO                       #
#------------------------------------------------------------------------------#

if __name__ == "__main__":
    app.run(debug=True)
