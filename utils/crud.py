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
    - `caminho_do_banco` (str): o caminho do banco de dados.
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

    # def incluir_item():
        # Código a ser feito

#-------------------------------------------------------------------------------#
#                              Função salvar_item                               #
#-------------------------------------------------------------------------------#

    def salvar_item(self, formulario: dict) -> None:
        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        for campo in formulario:

            if campo[0:17] == "CheckboxSeleciona":

                sql = f"""
                UPDATE  Item
                SET     Item    = "{formulario["Item_" + campo[18:20]]}"
                WHERE   ItemID  = {campo[18:20]}
                """

                cur.execute(sql)
                conn.commit()

#-------------------------------------------------------------------------------#
#                             Função excluir_item                               #
#-------------------------------------------------------------------------------#


    def excluir_item(self, formulario: dict) -> None:

        conn = sqlite3.connect(self.db_path)
        cur  = conn.cursor()

        for campo in formulario:

            if campo[0:17] == "CheckboxSeleciona":

                sql = f"""
                DELETE
                FROM    Item
                WHERE   ItemID = {campo[18:20]}
                """

                cur.execute(sql)
                conn.commit()
