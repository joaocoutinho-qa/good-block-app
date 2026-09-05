"""
Configuração central do projeto: caminhos, ID da extensão e timeouts.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho para a extensão Good Block. Pode ser:
#  - uma pasta com o código-fonte extraído (manifest.json na raiz), ou
#  - um arquivo .xpi dentro de extensions/
# O método driver.install_addon() do Selenium aceita ambos os formatos.
EXTENSION_PATH = os.path.join(BASE_DIR, "good-block-extension-src")

# Alternativa: se você baixar o .xpi da AMO e colocar em extensions/,
# descomente a linha abaixo e ajuste o nome do arquivo.
# EXTENSION_PATH = os.path.join(BASE_DIR, "extensions", "good_block-1.0.3.xpi")

# ID declarado no manifest e UUID estável usado pela origem moz-extension://.
# Definir o mapeamento no perfil antes de iniciar o Firefox evita depender de
# about:debugging, que o Selenium Grid não permite abrir.
EXTENSION_ID = "good-block@lucasandrade.com"
EXTENSION_UUID = "c069f0cb-7bb2-4ed4-b136-64e634f5eb51"

# Timeouts padrão (em segundos) usados pelos waits explícitos do BasePage.
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 3
BLOCKED_PAGE_TIMEOUT = 20
