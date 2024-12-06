
# Importação de bibliotecas para uso no código

from pyModbusTCP.server import ModbusServer
from camera import captura_frame
from time import sleep
from Centros import centro_circulos

#Create an instance of ModbusServer

SERVER_ADDRESS = '10.103.16.110'
SERVER_PORT = 502

# Configuração da comunicação MODBUS

server = ModbusServer(SERVER_ADDRESS, SERVER_PORT, no_block = True)
# Parâmetros de entrada
img_path = "images/foto_superior.png"
#num_pieces = funcao_principal()  # Número de divisões desejadas

# Variáveis de controle
continuar = 1
var_frame_1 = False
var_frame_2 = False
camera_pos_1=True
camera_pos_2=True

# Tentativa de conexão 

try:

    # Estabelecimento da conexão entre robô e PC

    print('Starting server...')
    server.start()
    print('Server is online')

    # Loop para enquanto o programa ainda estiver rodando

    while True:
       # Coleta do Frame Superior ---------------------------------------------------------------------------------------
       var_camera_superior=server.data_bank.get_coils(0)[0] # Coleta do sinal oriundo do robô
       var_camera_inferior=server.data_bank.get_coils(2)[0] # Coleta do sinal oriundo do robô
       if (var_camera_superior == True) and (camera_pos_1==True):
            while var_frame_1 !=True:
                sleep(3)
                var_Main =True
                var_frame_1=captura_frame(img_path) # Realização do salvamento da imagem
                cx,cy= centro_circulos(img_path)
                server.data_bank.set_input_registers(4, [cx])
                server.data_bank.set_input_registers(5, [cy])
                server.data_bank.set_input_registers(6, [1]) # Adicionar entrada no robô
                print('superior')
                sleep(1)
            server.data_bank.set_discrete_inputs(1, [True])  # Envio do valor True para o robô
            camera_pos_1=False # Quebra do if 
        # Coleta do frame lateral ----------------------------------------------------------------------------------------
       if var_camera_inferior == True and camera_pos_2==False:
           while var_frame_2 !=True:
                var_frame_2=captura_frame('foto_lateral.png') # Realização do salvamento da imagem
                print('lateral')
                sleep(1)
           server.data_bank.set_discrete_inputs(3, [True]) # Envio do valor True para o robô
           camera_pos_2=False # Quebra do if 
        # -------------------------------------------------------------------------------------------------------------------
       

except:
    print('Shutting down server...')
    server.stop()
    print('Server is offline')