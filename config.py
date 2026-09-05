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

# ID interno da extensão (browser_specific_settings.gecko.id no manifest.json).
# A extensão Good Block não declara um ID fixo no manifest, então o Firefox
# gera um ID temporário a cada instalação (ex.: "abc123@temporary-addon").
# Deixe None para descobrir automaticamente via about:debugging.
EXTENSION_ID = None

# Timeouts padrão (em segundos) usados pelos waits explícitos do BasePage.
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 3
