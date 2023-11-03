"""
Outras funções utilitárias do aplicativo "Nutri".
"""

#-------------------------------------------------------------------------------#
#                            Configuração Inicial                               #
#-------------------------------------------------------------------------------#

# Importações
from datetime  import datetime, timedelta, date
from xml.etree import ElementTree as ET

#-------------------------------------------------------------------------------#
#                         Função calcula_segunda_feira                          #
#-------------------------------------------------------------------------------#

def calcula_segunda_feira() -> date:
    """
    ### calcula_segunda_feira

    Calcula quando foi a última segunda-feira.

    #### Retorna:
    - Um objeto `date`, com o dia da última segunda-feira, em ano-mês-dia.
    """

    hoje = date.today()

    if hoje.weekday() == 0:
        return hoje
    else:
        return hoje - timedelta(hoje.weekday())

#-------------------------------------------------------------------------------#
#                            Função soma_dia_data                               #
#-------------------------------------------------------------------------------#

def soma_dia_data(data: date, dias: int) -> datetime:
    """
    ### soma_dia_data

    Realiza a soma entre a data inicial e o número de dias fornecidos.

    #### Parâmetros:
    :param: data (date): data inicial, em ano-mês-dia.
    :param: dias (int): número de dias a ser somado.

    #### Retorna:
    - Um objeto `datetime` com a data resultante.
    """

    data_date = datetime.strptime(str(data), "%Y-%m-%d")
    data_soma = data_date + timedelta(dias)

    return data_soma

#-------------------------------------------------------------------------------#
#                                Função dia_semana                              #
#-------------------------------------------------------------------------------#

def dia_semana(data: date) -> str:
    """
    ### dia_semana

    Recebe um objeto `date` e determina qual o dia da semana.

    #### Parâmetros:
    :param: data (date): data a ser analisada.

    #### Retorna:
    - Uma string com o dia da semana, em português.
    """

    if data.weekday() == 0:
        return "segunda-feira"
    elif data.weekday() == 1:
        return "terça-feira"
    elif data.weekday() == 2:
        return "quarta-feira"
    elif data.weekday() == 3:
        return "quinta-feira"
    elif data.weekday() == 4:
        return "sexta-feira"
    elif data.weekday() == 5:
        return "sábado"
    elif data.weekday() == 6:
        return "domingo"

    return ""

#-------------------------------------------------------------------------------#
#                           Função obter_configuracoes                          #
#-------------------------------------------------------------------------------#

def obter_configuracoes(caminho_do_arquivo: str) -> dict:
    """
    ### obter_configuracoes

    Obtêm as configurações do arquivo XML de configurações.

    #### Parâmetros:
    :param: caminho_do_arquivo (str): o caminho do arquivo XML de configurações.

    #### Retorna:
    - Um dicionário com as configurações.
        - Contém:
            - BancoDeDados: o caminho do banco de dados.
    """

    tree        = ET.parse(caminho_do_arquivo)
    root        = tree.getroot()
    config_dict = {}

    for el in root:
        config_dict[el.tag] = el.text

    return config_dict
