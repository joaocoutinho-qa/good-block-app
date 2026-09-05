"""
Configuração central do projeto: caminhos, ID da extensão e timeouts.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACTION_SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots", "actions")
VIDEOS_DIR = os.path.join(BASE_DIR, "videos")

# XPI oficial e assinado da extensão Good Block. Usá-lo diretamente evita que
# o Selenium crie um ZIP temporário ao instalar o diretório extraído no CI.
EXTENSION_PATH = os.path.join(BASE_DIR, "extensions", "good_block-1.0.3.xpi")

# Deixe como None para descobrir o UUID no perfil descartável do teste em
# about:debugging. O Firefox gera esse UUID a cada sessão.
EXTENSION_ID = None

# Timeouts padrão (em segundos) usados pelos waits explícitos do BasePage.
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 5
BLOCKED_PAGE_TIMEOUT = 20
