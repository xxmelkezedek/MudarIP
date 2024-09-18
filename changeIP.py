import subprocess
import ctypes
import re
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def validar_ip(ip):
    pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    return re.match(pattern, ip) is not None

def alterar_ip(interface, novo_ip, mascara="255.255.255.0"):
    '''
    Altera o endereço de IP de uma Interface de Rede no Windows.

    Args:
    interface (str): Nome da interface de rede (tipo camada Ethernet)
    novo_ip (str): Novo endereço de IP.
    mascara (str): Máscara de sub-rede (padrão: 255.255.255.0)
    '''

    if not is_admin():
        print('Você precisa ter privilégios de ADMIN para rodar esse script.')
        return

    if not validar_ip(novo_ip):
        print('Endereço IP inválido.')
        return

    comando = f'netsh interface ip set address name="{interface}" static {novo_ip} {mascara}'
    try:
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        print(f'O IP da interface {interface} foi alterado com sucesso para {novo_ip}')
        print('Saída do comando:', resultado.stdout)
    except subprocess.CalledProcessError as e:
        print(f'Erro ao alterar o IP: {e}')
        print('Saída de erro:', e.stderr)

controle = input('Deseja alterar o IP? S/N: ').lower()
if controle == 's':
    if __name__ == "__main__":
        if len(sys.argv) < 3:
            print("Uso: python script.py <interface> <novo_ip> [mascara]")
            sys.exit(1)
        
        interface = sys.argv[1]
        novo_ip = sys.argv[2]
        mascara = sys.argv[3] if len(sys.argv) > 3 else "255.255.255.0"

        alterar_ip(interface, novo_ip, mascara)
else:
    print('Que pena, até a próxima!')