"""
Arquivo principal da API do aplicativo "Nutri". Contém as rotas dos endpoints da API.
"""

#------------------------------------------------------------------------------#
#                            CONFIGURAÇÃO INICIAL                              #
#------------------------------------------------------------------------------#

# Importações
from flask                   import Flask, jsonify
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
#                              ROTA RAIZ (/api)                                #
#------------------------------------------------------------------------------#

@app.route("/api", methods=["GET", "POST"])
def raiz():
    """
    ### Rota raiz

    Rota: /api
    """

    return jsonify({
        "rota": "/api (raiz)",
        "rotas": {
            "pacientes": "/api/pacientes",
            "itens": "/api/itens",
            "consultas": "/api/consultas",
            "plano diário": "/api/plano_diario"
        }
    }), 200

#------------------------------------------------------------------------------#
#                       ROTA DO PACIENTE (/api/pacientes)                      #
#------------------------------------------------------------------------------#

@app.route("/api/pacientes/<int:paciente_id>", methods=["GET", "POST"])
def pacientes(paciente_id: int):
    """
    ### Página dos pacientes

    Rota: /api/pacientes/[paciente_id]
    """

    pacientes = tabelas.montar_tabela_de_pacientes(paciente_id)
    return jsonify(pacientes), 200

#------------------------------------------------------------------------------#
#                        PÁGINA DOS ITENS (/api/itens)                         #
#------------------------------------------------------------------------------#

@app.route("/api/itens/<int:item_id>", methods=["GET", "POST"])
def itens(item_id: int):
    """
    ### Rota dos itens

    Rota: /api/itens/[item_id]
    """

    itens = tabelas.montar_tabela_de_itens(item_id)
    return jsonify(itens), 200

#------------------------------------------------------------------------------#
#                        PÁGINA DAS CONSULTAS (/consultas)                     #
#------------------------------------------------------------------------------#

@app.route("/api/consultas/<int:paciente_id>", methods=["GET", "POST"])
def consultas(paciente_id: int):
    """
    ### Página das consultas

    Rota: /consultas/[paciente_id]
    """

    consultas = tabelas.montar_tabela_de_consultas(paciente_id)
    return jsonify(consultas)

#------------------------------------------------------------------------------#
#                     PÁGINA DO PLANO DIÁRIO (/plano_diario)                   #
#------------------------------------------------------------------------------#

# @app.route("/plano_diario/<int:paciente_id>", methods=["GET", "POST"])
# def plano_diario(paciente_id: int):
#     """
#     ### Plano diário

#     Rota: /plano_diario
#     """

#     opcoes = [
#         {
#             "opcao_id"  : 1,
#             "opcao"     : 1
#         },
#         {
#             "opcao_id"  : 2,
#             "opcao"     : 2
#         },
#         {
#             "opcao_id"  : 3,
#             "opcao"     : 3
#         }
#     ]

#     data_inicial_date_Ymd   = calcula_segunda_feira()
#     data_inicial_string_Ymd = data_inicial_date_Ymd.strftime("%Y-%m-%d")
#     data_final_string_Ymd   = soma_dia_data(data_inicial_date_Ymd, 6).strftime("%Y-%m-%d")
#     filtro_dia              = data_inicial_string_Ymd

#     return render_template(
#         "PlanoDiario.html",
#         planos_diarios      = tabelas.montar_tabela_do_plano_diario(paciente_id, filtro_dia),
#         filtro_pacientes    = combos.montar_combo_dos_pacientes(paciente_id),
#         filtro_data_inicial = data_inicial_string_Ymd,
#         filtro_data_final   = data_final_string_Ymd,
#         filtro_dias         = combos.montar_selecao_das_datas("", "", ""),
#         opcoes              = opcoes,
#         refeicoes           = combos.montar_combo_das_refeicoes(0),
#         itens               = combos.montar_combo_dos_itens(0),
#         unidades            = combos.montar_combo_das_unidades(0),
#         paciente_id         = paciente_id
#     )

#------------------------------------------------------------------------------#
#                       ROTINA DE EXECUÇÃO DO APLICATIVO                       #
#------------------------------------------------------------------------------#

if __name__ == "__main__":
    app.run(debug=True, port=8080)
