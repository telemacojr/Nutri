"""
Funções utilitárias que montam as tabelas do aplicativo "Nutri".

Instancie a classe Tabelas com o caminho do banco de dados.
"""

#-------------------------------------------------------------------------------#
#                            Configuração Inicial                               #
#-------------------------------------------------------------------------------#

# Importações
import sqlite3

#-------------------------------------------------------------------------------#
#                            Criação da classe Tabelas                          #
#-------------------------------------------------------------------------------#

class Tabelas:
    """
    Funções utilitárias que montam as tabelas do aplicativo "Nutri".

    Parâmetros:
    - :param: caminho_do_banco (str): o caminho do banco de dados.
    """
    def __init__(self, caminho_do_banco: str):
        self.db_path = caminho_do_banco

#-------------------------------------------------------------------------------#
#                        Função montar_tabela_de_pacientes                      #
#-------------------------------------------------------------------------------#

    def montar_tabela_de_pacientes(self, paciente_selecionado_id: int) -> "list[dict]":
        """
        ### montar_tabela_de_pacientes

        Monta uma lista de dicionários para compor a tabela dos pacientes.

        #### Parâmetros:
        - :param: paciente_selecionado_id (int): o ID do paciente selecionado.

        #### Retorna:
        - Uma lista de dicionários com todos ou apenas o paciente selecionado.
        """

        # Conecta ao banco de dados
        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        # Se o id fornecido for 0, retorna todos os pacientes, senão,
        # apenas o com o ID fornecido.
        if paciente_selecionado_id == 0:
            sql  = """
            SELECT  PacienteID,
                    Paciente,
                    DataNascimento,
                    Telefone,
                    Email
            FROM    Paciente
            """
        else:
            sql  = f"""
            SELECT  PacienteID,
                    Paciente,
                    DataNascimento,
                    Telefone,
                    Email
            FROM    Paciente
            WHERE   PacienteID = {paciente_selecionado_id}
            """
        cur.execute(sql)

        # Dicionário dos pacientes
        dict_pacientes = {
            "paciente_id"           : None,
            "paciente"              : None,
            "data_de_nascimento"    : None,
            "telefone"              : None,
            "email"                 : None
        }

        lista_pacientes = []

        rows = cur.fetchall()

        for row in rows:
            dict_pacientes = {
                "paciente_id"           : row[0],
                "paciente"              : row[1],
                "data_de_nascimento"    : row[2],
                "telefone"              : row[3],
                "email"                 : row[4]
            }

            lista_pacientes.append(dict_pacientes)

        return lista_pacientes

#-------------------------------------------------------------------------------#
#                        Função montar_tabela_de_itens                          #
#-------------------------------------------------------------------------------#

    def montar_tabela_de_itens(
        self, item_selecionado_id: int, incluir_item: bool
    ) -> "list[dict]":
        """
        ### montar_tabela_de_itens

        Monta uma lista de dicionários para compor a tabela dos itens.

        #### Parâmetros:
        - :param: item_selecionado_id (int): o ID do item selecionado.
        - :param: incluir_item (bool): se um item está sendo incluído.

        #### Retorna:
        - Uma lista de dicionários com todos ou apenas o item selecionado.
        """

        # Conecta ao banco de dados
        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        # Se o id fornecido for 0, obtêm todos os itens, senão,
        # obtêm apenas o item com o id respectivo
        if item_selecionado_id == 0:
            sql = """
            SELECT      ItemID,
                        Item
            FROM        Item
            ORDER BY    Item
            """
        else:
            sql = f"""
            SELECT      ItemID,
                        Item
            FROM        Item
            WHERE       ItemID = {item_selecionado_id}
            ORDER BY    Item
            """
        cur.execute(sql)

        # Monta a lista de dicionários
        dict_itens = {
            "item_id"   : None,
            "item"      : None,
            "checked"   : None
        }

        lista_itens = []
        rows        = cur.fetchall()

        if incluir_item:
            lista_itens.append({
                "item_id": 0,
                "item": "",
                "checked": True
            })

        for row in rows:

            dict_itens = {
                "item_id"   : row[0],
                "item"      : row[1],
                "checked"   : False
            }

            lista_itens.append(dict_itens)

        return lista_itens

#-------------------------------------------------------------------------------#
#                        Função montar_tabela_de_consultas                      #
#-------------------------------------------------------------------------------#

    def montar_tabela_de_consultas(self, paciente_selecionado_id: int) -> "list[dict]":
        """
        ### montar_tabela_de_consultas

        Monta uma lista de dicionários para compor a tabela das consultas.

        #### Parâmetros:
        - :param: paciente_selecionado_id (int): o ID do paciente selecionado.

        #### Retorna:
        - Uma lista de dicionários com todas as consultas do paciente selecionado.
            - Contém:
                - Data da consulta;
                - IMC;
                - CC (circunferência da cintura);
                - G (percentual de gordura).
        """

        # Conecta ao banco de dados
        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        # Busca no banco de dados a data, o IMC, a CC, e o G% do paciente
        sql = f"""
        SELECT  Data,
                IMC,
                CC,
                G
        FROM    Consulta
        WHERE   PacienteID = {paciente_selecionado_id}
        """
        cur.execute(sql)

        # Cria a lista
        dict_consultas = {
            "data"  : None,
            "imc"   : None,
            "cc"    : None,
            "g"     : None
        }
        lista_consultas = []

        rows = cur.fetchall()

        for row in rows:
            dict_consultas = {
                "data"  : row[0],
                "imc"   : row[1],
                "cc"    : row[2],
                "g"     : row[3]
            }

            lista_consultas.append(dict_consultas)

        return lista_consultas

#-------------------------------------------------------------------------------#
#                     Função montar_tabela_do_plano_diario                      #
#-------------------------------------------------------------------------------#

    def montar_tabela_do_plano_diario(
        self,
        paciente_selecionado_id: int,
        data_dia_string_Ymd: str
    ) -> "list[dict]":
        """
        ### montar_tabela_do_plano_diario

        Monta uma lista de dicionários para compor a tabela do plano diário.

        #### Parâmetros:
        - :param: paciente_selecionado_id (int): o ID do paciente selecionado.
        - :param: data_dia_string_Ymd (str): a data do dia do plano diário, em ano-mês-dia.

        #### Retorna:
        - Uma lista de dicionários com o plano diário do dia especificado para o
        paciente especificado.
            - Contém:
                - Data do plano diário;
                - ID da refeição;
                - Refeição;
                - Horário;
                - Opcão;
                - ID do Item;
                - Item;
                - Quantidade;
                - ID da Unidade;
                - Unidade.
        """

        # Conecta ao banco de dados e faz uma query complexa
        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        sql = f"""
        SELECT      PD.Data,
                    CASE
                        WHEN R.RefeicaoID = 6
                        THEN 9
                        ELSE R.RefeicaoID
                    END AS RefeicaoID,
                    R.Refeicao,
                    R.Horario,
                    P.Opcao,
                    I.ItemID,
                    I.Item,
                    C.Quantidade,
                    U.UnidadeID,
                    U.Unidade
        FROM        PlanoDiario   AS PD
        INNER JOIN  Paciente      AS Pac ON PD.PacienteID = Pac.PacienteID
        INNER JOIN  Plano         AS P   ON PD.PlanoID    = P.PlanoID
        INNER JOIN  Refeicao      AS R   ON P.RefeicaoID  = R.RefeicaoID
        INNER JOIN  Cardapio      AS C   ON P.CardapioID  = C.CardapioID
        INNER JOIN  Item          AS I   ON C.ItemID      = I.ItemID
        INNER JOIN  Unidade       AS U   ON C.UnidadeID   = U.UnidadeID
        WHERE       PD.PacienteID = {paciente_selecionado_id}
        AND         PD.Data       = "{data_dia_string_Ymd}"
        """
        cur.execute(sql)

        # Monta a lista
        dict_plano_diario = {
            "Data"          : None,
            "RefeicaoID"    : None,
            "Refeicao"      : None,
            "Horario"       : None,
            "Opcao"         : None,
            "ItemID"        : None,
            "Item"          : None,
            "Quantidade"    : None,
            "UnidadeID"     : None,
            "Unidade"       : None
        }
        lista_plano_diario = []

        row = cur.fetchone()

        while row:
            dict_plano_diario = {
                "Data"          : row[0],
                "RefeicaoID"    : row[1],
                "Refeicao"      : row[2],
                "Horario"       : row[3],
                "Opcao"         : row[4],
                "ItemID"        : row[5],
                "Item"          : row[6],
                "Quantidade"    : row[7],
                "UnidadeID"     : row[8],
                "Unidade"       : row[9]
            }

            lista_plano_diario.append(dict_plano_diario)

            row = cur.fetchone()

        return lista_plano_diario
