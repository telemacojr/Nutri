"""
Operações CRUD do aplicativo "Nutri".

Instancie a classe `CRUD` com o caminho do banco de dados.
"""

#-------------------------------------------------------------------------------#
#                            Configuração Inicial                               #
#-------------------------------------------------------------------------------#

# Importações
import sqlite3

#-------------------------------------------------------------------------------#
#                            Criação da classe CRUD                             #
#-------------------------------------------------------------------------------#

class CRUD:
    """
    Operações CRUD do aplicativo "Nutri".

    Parâmetro:
    - :param: caminho_do_banco (str): o caminho do banco de dados.
    """

    def __init__(self, caminho_do_banco: str):
        self.db_path = caminho_do_banco

#-------------------------------------------------------------------------------#
#                              Função ler_formulario                            #
#-------------------------------------------------------------------------------#

    def ler_formulario(self, formulario: dict) -> None:
        for campo in formulario:
            if campo[0:17] == "CheckboxSeleciona":
                print(
                    campo[0:17], ':', campo[18:20],
                    formulario['Item_' + campo[18:20]]
                )

#-------------------------------------------------------------------------------#
#                              Função incluir_item                              #
#-------------------------------------------------------------------------------#

    def incluir_item(self, nome_do_item: str) -> None:
        """
        ### incluir_item

        Inclui o item especificado no banco de dados.

        #### Parâmetros:
        - :param: nome_do_item (str): o nome do item a ser criado.
        """

        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        sql = f"""
        INSERT
        INTO    Item
        (Item)
        VALUES  ("{nome_do_item}")
        """

        cur.execute(sql)
        conn.commit()

#-------------------------------------------------------------------------------#
#                           Função atualizar_item                               #
#-------------------------------------------------------------------------------#

    def atualizar_item(self, item_id: int, novo_nome: str) -> None:
        """
        ### atualizar_item

        Exclui os itens selecionados.

        #### Parâmetros:
        - :param: item_id (int): o id do item a ser atualizado.
        - :param: novo_nome (str): o novo nome do item.
        """

        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        sql = f"""
        UPDATE  Item
        SET     Item    = "{novo_nome}"
        WHERE   ItemID  = {item_id}
        """

        cur.execute(sql)
        conn.commit()

#-------------------------------------------------------------------------------#
#                             Função excluir_item                               #
#-------------------------------------------------------------------------------#

    def excluir_item(self, item_id: int) -> None:
        """
        ### excluir_item

        Exclui os itens selecionados.

        #### Parâmetros:
        - :param: item_id (int): o id do item a ser excluído.
        """

        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        sql = f"""
        DELETE
        FROM    Item
        WHERE   ItemID = {item_id}
        """

        cur.execute(sql)
        conn.commit()
