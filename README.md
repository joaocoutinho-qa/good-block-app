# Good Block Automation (Selenium + Python)

Automação da extensão Firefox **Good Block** (bloqueio de sites, Manifest V2)
usando Selenium WebDriver + geckodriver, com Page Object Model (POM).

## Por que Selenium (e não Playwright)?

O Playwright usa o protocolo Juggler para controlar o Firefox, que **não
permite navegar para páginas `moz-extension://`** (o popup da extensão
trava em `about:blank` e nunca carrega). O Selenium usa o geckodriver
real, que não tem essa limitação — `driver.get("moz-extension://...")`
funciona normalmente.

## Instalação

1. Crie e ative um ambiente virtual:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

3. O arquivo assinado da extensão já está incluído em
   [`extensions/good_block-1.0.3.xpi`](./extensions/good_block-1.0.3.xpi).
   O diretório [`good-block-extension-src/`](./good-block-extension-src)
   permanece disponível apenas para consulta do código-fonte extraído.

### Descobrindo o UUID da extensão

Cada perfil descartável de teste recebe um UUID `moz-extension://` novo. O
projeto o descobre automaticamente em `about:debugging` antes de abrir o popup.

## Ajustando os seletores reais

Os seletores em [`pages/good_block_popup_page.py`](./pages/good_block_popup_page.py)
e [`pages/blocked_page.py`](./pages/blocked_page.py) são **placeholders**
(o `popup.js` real é um bundle Webpack minificado, então não dá pra
adivinhar os seletores certos sem inspecionar o DOM renderizado).

Para descobrir os seletores reais:

```powershell
python explore.py
```

Isso abre o Firefox com a extensão instalada, navega até o popup, e
pausa a execução. Abra o DevTools (F12) na janela do Firefox, inspecione
os elementos reais (botão "Add group", campos de nome/sites, lista de
grupos, toggle liga/desliga, modal de bloqueio) e atualize os locators
nos Page Objects correspondentes.

## Rodando os testes

```powershell
pytest -v
```

Os testes em [`tests/test_good_block.py`](./tests/test_good_block.py) usam
uma instância limpa do Firefox por teste (fixture `driver` em
[`conftest.py`](./conftest.py), escopo `function`).

Na pipeline, o artifact `test-evidence` inclui screenshots em
`screenshots/actions/`, numerados pela ordem de execução. Há uma captura após
cada clique, preenchimento e seleção, além da configuração imediatamente antes
da navegação para o Facebook. Ele também inclui um MP4 por teste em `videos/`;
o vídeo do cenário de bloqueio mostra a configuração do grupo, o carregamento
do Facebook e o modal do Good Block.

## Estrutura do projeto

```
project/
├── requirements.txt
├── config.py              # caminhos, EXTENSION_PATH, timeouts
├── conftest.py             # fixture do driver com a extensão instalada
├── explore.py              # script exploratório para inspecionar o popup
├── extensions/             # XPI oficial assinado usado pelos testes
├── good-block-extension-src/  # código-fonte da extensão já extraído
├── pages/
│   ├── base_page.py
│   ├── good_block_popup_page.py
│   └── blocked_page.py
└── tests/
    └── test_good_block.py
```

## Troubleshooting

| Problema | Causa provável | Solução |
|---|---|---|
| `install_addon` falha com erro de assinatura | XPI ausente ou corrompido | Restaure `extensions/good_block-1.0.3.xpi` e execute os testes novamente |
| Página `moz-extension://...` fica em branco | UUID errado ou extensão ainda não terminou de instalar | Use `BasePage.discover_extension_uuid()` para obter o UUID atual em vez de fixar um valor |
| `NoSuchElementException` / elemento não encontrado | Seletor placeholder ainda não foi ajustado | Rode `python explore.py` e atualize o locator correspondente no Page Object |
| `geckodriver` não encontrado / versão incompatível | Driver desatualizado | O projeto usa `webdriver-manager`, que baixa a versão correta automaticamente; se persistir, delete o cache em `~/.wdm` e rode de novo |
| Extensão não aparece em `about:debugging` | Caminho em `EXTENSION_PATH` incorreto | Confirme em `config.py` que o caminho aponta para uma pasta com `manifest.json` na raiz, ou para um `.xpi` válido |
| Testes muito lentos ou instáveis no CI | Ambiente gráfico do runner pode afetar o Firefox | A pipeline executa Firefox no Xvfb; localmente o navegador continua visível |
