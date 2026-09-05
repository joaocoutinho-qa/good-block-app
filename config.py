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

# Deixe como None para descobrir o UUID da extensão instalada temporariamente
# em about:debugging. O Firefox gera esse UUID a cada sessão.
EXTENSION_ID = None

# Timeouts padrão (em segundos) usados pelos waits explícitos do BasePage.
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 3
BLOCKED_PAGE_TIMEOUT = 20
