"""
Funções utilitárias que montam combos/filtros do aplicativo "Nutri".

Instancie a classe `Combos` com o caminho do banco de dados.
"""

#-------------------------------------------------------------------------------#
#                            Configuração Inicial                               #
#-------------------------------------------------------------------------------#

# Importações
import sqlite3
from datetime   import datetime, timedelta
from utils.misc import calcula_segunda_feira, soma_dia_data, dia_semana

#-------------------------------------------------------------------------------#
#                           Criação da classe Combos                            #
#-------------------------------------------------------------------------------#

class Combos:
    """
    Funções utilitárias que montam combos/filtros do aplicativo "Nutri".

    Parâmetros:
    - :param: caminho_do_banco (str): o caminho do banco de dados.
    """

    def __init__(self, caminho_do_banco: str):
        self.db_path = caminho_do_banco

#-------------------------------------------------------------------------------#
#                       Função montar_combo_dos_pacientes                       #
#-------------------------------------------------------------------------------#

    def montar_combo_dos_pacientes(
        self, paciente_selecionado_id: int
    ) -> "list[dict]":
        """
        ### montar_combo_dos_pacientes

        Monta uma lista de dicionários para compor a combo de seleção dos pacientes.

        #### Parâmetros:
        - :param: paciente_selecionado_id (int): o ID do paciente selecionado.

        #### Retorna:
        - Uma lista de dicionários com todos os pacientes.
        """

        # Conecta ao banco de dados
        conn    = sqlite3.connect(self.db_path)
        cur     = conn.cursor()

        # Obtêm todos os pacientes e seus respectivos IDs
        sql = """
        SELECT  PacienteID,
                Paciente
        FROM    Paciente
        """
        cur.execute(sql)

        # Monta uma lista de dicionários com o
        # paciente, o ID e se ele está selecionado
        dict_paciente_inicial = {
            "paciente_id"   : None,
            "paciente"      : None,
            "selected"      : None
        }
        lista_pacientes = []

        # Verifica se o "vazio" está selecionado
        if paciente_selecionado_id == 0:
            dict_paciente_inicial = {
                "paciente_id"   : 0,
                "paciente"      : "",
                "selected"      : True,
            }
        else:
            dict_paciente_inicial = {
                "paciente_id"   : 0,
                "paciente"      : "",
                "selected"      : False
            }
        lista_pacientes.append(dict_paciente_inicial)

        # Recursão: colocar todos os pacientes na lista de dicionários
        row = cur.fetchone()

        while row:
            paciente_id : int = row[0]
            paciente    : str = row[1]

            if paciente_selecionado_id == paciente_id:
                selected = True
            else:
                selected = False

            dict_pacientes = {
                "paciente_id"   : paciente_id,
                "paciente"      : paciente,
                "selected"      : selected
            }

            lista_pacientes.append(dict_pacientes)

            row = cur.fetchone()

        return lista_pacientes

#-------------------------------------------------------------------------------#
#                        Função montar_selecao_das_datas                        #
#-------------------------------------------------------------------------------#

    def montar_selecao_das_datas(
        self,
        data_inicial_string_Ymd: str,
        data_final_string_Ymd: str,
        data_dia_string_Ymd: str
    ) -> "list[dict]":
        """
        ### montar_selecao_das_datas

        Monta uma lista de dicionários para compor a seleção das datas.

        #### Parâmetros:
        - :param: data_inicial_string_Ymd (str): data inicial, em ano-mês-dia.
        - :param: data_final_string_Ymd (str): data final, em ano-mês-dia.
        - :param: data_dia_string_Ymd` (str): dia escolhido, em ano-mês-dia.

        #### Retorna:
        - Uma lista de dicionários com as datas calculadas.
        """

        # Conversões de datas
        if data_inicial_string_Ymd == "" and data_final_string_Ymd == "":
            data_inicial_date_Ymd   = calcula_segunda_feira()
            data_inicial_string_Ymd = data_inicial_date_Ymd.strftime("%Y-%m-%d")
            data_inicial_string_dmY = data_inicial_date_Ymd.strftime("%d/%m/%Y")
            data_final_date_Ymd     = soma_dia_data(data_inicial_date_Ymd, 6)
            data_final_string_Ymd   = data_final_date_Ymd.strftime("%Y-%m-%d")
        else:
            data_inicial_date_Ymd   = datetime.strptime(
                data_inicial_string_Ymd, "%Y-%m-%d"
            )
            data_inicial_string_dmY = data_inicial_date_Ymd.strftime("%d/%m/%Y")
            data_inicial_string_Ymd = data_inicial_date_Ymd.strftime("%Y-%m-%d")
            data_final_date_Ymd     = datetime.strptime(
                data_final_string_Ymd, "%Y-%m-%d"
            )

        # Começa a montar a lista de dicionários,
        # verificando se o dia fornecido é o inicial ou vazio
        lista_dias = []

        if data_dia_string_Ymd == data_inicial_string_Ymd or data_dia_string_Ymd == "":
            selected = True
        else:
            selected = False

        dict_dias_inicial = {
            "dia"       :   data_inicial_string_dmY +
                            f"({dia_semana(data_inicial_date_Ymd)})",
            "selected"  :   selected
        }
        lista_dias.append(dict_dias_inicial)

        data_inicial_date_Ymd   = datetime.strptime(
            data_inicial_string_Ymd, "%Y-%m-%d"
        )
        data_final_date_Ymd     = datetime.strptime(
            data_final_string_Ymd, "%Y-%m-%d"
        )
        data_somada_date_Ymd    = data_inicial_date_Ymd

        while data_somada_date_Ymd < data_final_date_Ymd:

            data_somada_date_Ymd = data_somada_date_Ymd + timedelta(1)

            if data_dia_string_Ymd == data_somada_date_Ymd.strftime("%Y-%m-%d"):
                selected = True
            else:
                selected = False

            dict_dias = {
                "dia"       :   datetime.strftime(
                                    data_somada_date_Ymd, "%d/%m/%Y"
                                ) + f'({dia_semana(data_somada_date_Ymd)})',
                "selected"  :   selected
            }

            lista_dias.append(dict_dias)

        return lista_dias

#-------------------------------------------------------------------------------#
#                       Função montar_combo_das_refeicoes                       #
#-------------------------------------------------------------------------------#

    def montar_combo_das_refeicoes(
        self, refeicao_selecionada_id: int
    ) -> "list[dict]":
        """
        ### montar_combo_das_refeicoes

        Monta uma lista de dicionários para compor a combo de seleção das refeições.

        #### Parâmetros:
        - :param: refeicao_selecionada_id (int): o ID da refeição selecionada.

        #### Retorna:
        - Uma lista de dicionários com todas as refeições.
        """

        # Conecta ao banco de dados
        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        # Obtêm as refeições e seus IDs
        sql = """
        SELECT  RefeicaoID,
                Refeicao
        FROM    Refeicao
        """
        cur.execute(sql)

        # Cria o dicionário inicial e o insere na lista
        dict_refeicao_inicial = {
            "refeicao_id"   : None,
            "refeicao"      : None,
            "selected"      : None
        }

        lista_refeicao = []

        if refeicao_selecionada_id == 0:
            dict_refeicao_inicial = {
                "refeicao_id"   : 0,
                "refeicao"      : "",
                "selected"      : True
            }
        else:
            dict_refeicao_inicial = {
                "refeicao_id"   : 0,
                "refeicao"      : "",
                "selected"      : False
            }

        lista_refeicao.append(dict_refeicao_inicial)

        # Recursão para montar o resto da lista de refeições
        rows = cur.fetchall()

        for row in rows:

            refeicao_id = row[0]
            refeicao    = row[1]

            if refeicao_selecionada_id == refeicao_id:
                selected = True
            else:
                selected = False

            dict_refeicao = {
                "refeicao_id"   : refeicao_id,
                "refeicao"      : refeicao,
                "selected"      : selected
            }

            lista_refeicao.append(dict_refeicao)

        return lista_refeicao

#-------------------------------------------------------------------------------#
#                        Função montar_combo_dos_itens                          #
#-------------------------------------------------------------------------------#

    def montar_combo_dos_itens(self, item_selecionado_id: int) -> "list[dict]":
        """
        ### montar_combo_dos_itens

        Monta uma lista de dicionários para compor a combo de seleção dos itens.

        #### Parâmetros:
        - :param: item_selecionado_id (int): o ID do item selecionado.

        #### Retorna:
        - Uma lista de dicionários com todos os itens.
        """

        # Conecta ao banco de dados
        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        # Obtêm os itens e seus IDs, ordenados em ordem alfabética do nome do item
        sql = """
        SELECT      ItemID,
                    Item
        FROM        Item
        ORDER BY    Item
        """
        cur.execute(sql)

        # Cria o dicionário inicial e o coloca na lista
        dict_itens_inicial = {
            "item_id"   : None,
            "item"      : None,
            "selected"  : None
        }

        lista_itens = []

        if item_selecionado_id == 0:
            dict_itens_inicial = {
                "item_id"   : 0,
                "item"      : "",
                "selected"  : True
            }
        else:
            dict_itens_inicial = {
                "item_id"   : 0,
                "item"      : "",
                "selected"  : False
            }

        lista_itens.append(dict_itens_inicial)

        # Recursão: termina de montar a lista
        rows = cur.fetchall()

        for row in rows:

            item_id : int = row[0]
            item    : int = row[1]

            if item_selecionado_id == item_id:
                selected = True
            else:
                selected = False

            dict_itens = {
                "item_id"   : item_id,
                "item"      : item,
                "selected"  : selected
            }

            lista_itens.append(dict_itens)

        return lista_itens

#-------------------------------------------------------------------------------#
#                        Função montar_combo_das_unidades                       #
#-------------------------------------------------------------------------------#

    def montar_combo_das_unidades(
        self, unidade_selecionada_id: int
    ) -> "list[dict]":
        """
        ### montar_combo_das_unidades

        Monta uma lista de dicionários para compor a combo de seleção das unidades.

        #### Parâmetros:
        - :param: unidade_selecionada_id (int): o ID da unidade selecionada.

        #### Retorna:
        - Uma lista de dicionários com todos as unidades.
        """

        # Conecta ao banco de dados
        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        # Obtêm as unidades e seus IDs
        sql = """
        SELECT  UnidadeID,
                Unidade
        FROM    Unidade
        """
        cur.execute(sql)

        # Cria o dicionário inicial
        dict_unidades  = {
            "unidade_id"    : None,
            "unidade"       : None,
            "selected"      : None
        }

        lista_unidades = []

        if  unidade_selecionada_id == 0:
            dict_unidades  = {
                "unidade_id"    : 0,
                "unidade"       : "",
                "selected"      : True
            }
        else:
            dict_unidades  = {
                "unidade_id"    : 0,
                "unidade"       : "",
                "selected"      : False
            }
        lista_unidades.append(dict_unidades)

        # Recursão que termina de criar a lista
        row = cur.fetchone()

        while row:

            unidade_id = row[0]
            unidade    = row[1]

            if unidade_selecionada_id == unidade_id:
                selected = True
            else:
                selected = False

            dict_unidades  = {"unidade_id": unidade_id,
                            "unidade":    unidade,
                            "selected":   selected}
            lista_unidades.append(dict_unidades)

            row = cur.fetchone()

        return lista_unidades
