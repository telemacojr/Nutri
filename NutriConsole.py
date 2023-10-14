#-------------------------------------------------------------------------------------------#
# Nome do programa: Nutri.py                                                                #
# Autor...........: Telêmaco Queiroz Júnior                                                 #
# Data de criação.: 2023-09-16                                                              #
# Interface.......: console                                                                 #
# Descrição.......: aplicativo para montagem de plano diário de cardápios para nutrição     #
#-------------------------------------------------------------------------------------------#

import os
import pyodbc

from datetime import datetime
from colorama import Fore, Back, Style

#-------------------------------------------------------------------------------------------#
#                                     Monta o cabeçalho                                     #
#-------------------------------------------------------------------------------------------#

def monta_cabecalho():

    os.system("cls")

    print(Back.LIGHTBLUE_EX + "+--------------------------------------------------------------------------------------------------+")
    print(Back.LIGHTBLUE_EX + "|                                              Nutri                                               |")
    print(Back.LIGHTBLUE_EX + "+--------------------------------------------------------------------------------------------------+")
    print(Back.LIGHTBLUE_EX + "| ENTER: Consulta   F: Fim   I: Tela inicial                                                       |")
    print(Back.LIGHTBLUE_EX + "+--------------------------------------------------------------------------------------------------+")
    print(Back.BLACK + " ")

#-------------------------------------------------------------------------------------------#
#                                     Obtem o paciente                                      #
#-------------------------------------------------------------------------------------------#

def obtem_paciente():

    PacientID = input(Fore.MAGENTA + "Paciente ID: ")
    
    return PacientID

#-------------------------------------------------------------------------------------------#
#                               Obtem uma lista de pacientes                                #
#-------------------------------------------------------------------------------------------#

def obtem_pacientes():

    line = ""
    line = line + "PacienteID" + " "
    line = line + "Paciente"   + " "*43
    line = line + "Data"       + " "*7
    line = line + "IMC"        + " "*3
    line = line + "CC"         + " "
    line = line + "G%"

    print(Fore.CYAN + line)

    line = ""
    line = line + "-"*10 + " "
    line = line + "-"*50 + " "
    line = line + "-"*10 + " "
    line = line + "-"*5  + " "
    line = line + "-"*2  + " "
    line = line + "-"*5

    print(Fore.CYAN + line)

    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=TELEMACO201609\SQLEXPRESS;'
                          'Database=Loterias;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()

    sql = ""
    sql = sql + " SELECT	    P.PacienteID, "                                                     + "\n"
    sql = sql + " 		        P.Paciente, "                                                       + "\n"
    sql = sql + " 		        CONVERT(VARCHAR(10), C.Data, 103) AS Data, "                        + "\n"
    sql = sql + " 	        	C.IMC, "                                                            + "\n"
    sql = sql + "   	    	C.CC, "                                                             + "\n"
    sql = sql + "	        	C.G "                                                               + "\n"
    sql = sql + " FROM		    Nutri.dbo.Paciente	AS P "                                          + "\n"
    sql = sql + " INNER JOIN	Nutri.dbo.Consulta	AS C	ON	P.PacienteID	= C.PacienteID "    + "\n"

    cursor.execute(sql)

    row = cursor.fetchone()

    while row:

        line = ""
        line = line + str(row[0])             + " "*10
        line = line + row[1]                  + " "*(51-len(row[1]))
        line = line + row[2]                  + " "
        line = line + "{:.2f}".format(row[3]) + " "
        line = line + str(row[4])             + " "
        line = line + "{:.2f}".format(row[5])

        print(Fore.WHITE + line)

        row = cursor.fetchone()

    print(" ")

#-------------------------------------------------------------------------------------------#
#                                Obtem dados de um paciente                                 #
#-------------------------------------------------------------------------------------------#

def obtem_dados_paciente(PacienteID):

    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=TELEMACO201609\SQLEXPRESS;'
                          'Database=Loterias;'
                          'Trusted_Connection=yes;')

    cursor = conn.cursor()

    sql = ""
    sql = sql + " SELECT	    P.PacienteID, "
    sql = sql + " 		        P.Paciente, "
    sql = sql + " 		        C.Data, "
    sql = sql + " 	        	C.IMC, "
    sql = sql + "   	    	C.CC, "
    sql = sql + "	        	C.G "
    sql = sql + " FROM		    Nutri.dbo.Paciente	AS P "
    sql = sql + " INNER JOIN	Nutri.dbo.Consulta	AS C	ON	P.PacienteID	= C.PacienteID "
    sql = sql + " WHERE         P.PacienteID = " + PacienteID

    cursor.execute(sql)

    row = cursor.fetchone()

    while row:

        print(Fore.RED + 'Paciente ID..............:', Fore.WHITE + str(row[0]))
        print(Fore.RED + 'Nome do Paciente.........:', Fore.WHITE + row[1])
        print(Fore.RED + 'Data da Consulta.........:', Fore.WHITE + row[2])
        print(Fore.RED + 'Índice de Massa Corporal.:', Fore.WHITE + "{:.2f}".format(row[3]))
        print(Fore.RED + 'Circunferência da Cintura:', Fore.WHITE + str(row[4]))
        print(Fore.RED + 'Percentual de Gordura....:', Fore.WHITE + "{:.2f}".format(row[5]) + "%")
        print(" ")

        row = cursor.fetchone()

#-------------------------------------------------------------------------------------------#
#                                         Principal                                         #
#-------------------------------------------------------------------------------------------#

monta_cabecalho()
obtem_pacientes()

while True:

    PacienteID = obtem_paciente()

    if   PacienteID.upper() == 'F':
         monta_cabecalho()
         print(Fore.GREEN + "Obrigado por usar o aplicativo Nutri!")
         print(" ")
         break
    elif PacienteID.upper() == 'I':
         monta_cabecalho()
         obtem_pacientes()
    elif PacienteID.isnumeric():
         monta_cabecalho()
         obtem_dados_paciente(PacienteID)
    else:
         print(Fore.RED + "Opção inválida. Por favor, tente novamente...")
         print(" ")
