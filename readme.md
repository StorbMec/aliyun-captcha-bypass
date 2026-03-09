# 🔐 Quebrador de Captcha Deslizante da Alibaba Cloud

Ferramenta automática para resolver captchas deslizantes da Alibaba Cloud (Aliyun) com detecção inteligente de distância.

## ⚖️ Aviso Legal

**IMPORTANTE:** Esta ferramenta é fornecida apenas para fins educacionais, pesquisa de segurança e testes autorizados.

- ✅ **Uso Permitido:** Pesquisa acadêmica, testes de segurança autorizados, aprendizado técnico
- ❌ **Uso Proibido:** Acesso não autorizado, lucro comercial, web scraping malicioso, qualquer atividade ilegal

Ao usar esta ferramenta, você concorda em:
1. Cumprir todas as leis e regulamentos aplicáveis
2. Usar apenas em sistemas que você tem permissão para testar
3. Assumir total responsabilidade pelo uso

## 📋 Requisitos

### Sistema Operacional
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)

### Software Necessário
- Python 3.8+
- Google Chrome (última versão)
- Git (opcional, para clonar repositório)

## 🚀 Instalação

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd quebrador-captcha-alibaba
```

### 2. Instale as Dependências

#### Windows:
```bash
pip install -r requirements.txt
```

#### Linux/macOS:
```bash
pip3 install -r requirements.txt
```

### Dependências Instaladas:
- `requests==2.31.0` - Para fazer requisições HTTP
- `ddddocr==1.4.11` - Motor OCR para detectar posição do captcha
- `undetected-chromedriver==3.5.5` - Driver Chrome não detectável
- `selenium==4.15.2` - Automação de navegador

## 📁 Estrutura de Arquivos

```
quebrador-captcha-alibaba/
│
├── pagina_captcha.html          # Página HTML com captcha de teste
├── calcular_distancia.py        # Script para calcular distância do slider
├── executar_quebrador_captcha.py # Script principal de automação
├── stealth.min.js               # Script anti-detecção para navegador
├── requirements.txt             # Dependências Python
└── LEIAME.md                    # Este arquivo
```

## 🔧 Configuração

### 1. Configure suas Credenciais

Edite o arquivo `pagina_captcha.html` e insira suas credenciais da Alibaba Cloud:

```javascript
// Linha ~76
window.AliyunCaptchaConfig = {
  region: 'cn',
  prefix: 'SEU_PREFIXO_AQUI'  // ✅ Substitua com seu prefixo
};

// Linha ~194
window.initAliyunCaptcha({
  SceneId: "SEU_SCENE_ID_AQUI",  // ✅ Substitua com seu Scene ID
  // ... resto da configuração
});
```

### 2. Verifique a Instalação do Chrome

O script detecta automaticamente a versão do Chrome. Se houver problemas:

1. Atualize o Chrome para a versão mais recente
2. Feche todas as janelas do Chrome antes de executar
3. Se persistir, edite `executar_quebrador_captcha.py` (linha ~80) e force uma versão específica

## 🎯 Uso

### Modo Automático (Recomendado)

Execute o script principal que automatiza todo o processo:

```bash
python executar_quebrador_captcha.py
```

O script irá:
1. ✓ Detectar automaticamente a versão do Chrome
2. ✓ Abrir a página com captcha
3. ✓ Capturar URLs das imagens
4. ✓ Calcular distância ideal com OCR
5. ✓ Construir tabela de mapeamento slider-shadow
6. ✓ Executar arrasto humanizado
7. ✓ Verificar o captcha

### Modo Manual

#### Passo 1: Abra a Página
```bash
# Abra pagina_captcha.html no navegador
# OU execute um servidor local:
python -m http.server 8000
# Acesse: http://localhost:8000/pagina_captcha.html
```

#### Passo 2: Clique em "Calcular Distância Automaticamente"
Isso irá capturar as URLs das imagens do captcha.

#### Passo 3: Execute o Calculador de Distância
```bash
python calcular_distancia.py "URL_IMAGEM_SLIDER" "URL_IMAGEM_FUNDO"
```

#### Passo 4: Use a Distância Calculada
1. Insira o valor no campo "Distância Shadow"
2. Clique em "Construir Tabela de Correspondência"
3. Clique em "Buscar Slider"
4. Clique em "Testar Arrasto do Slider"

## 🔍 Como Funciona

### 1. Detecção de Imagens
O script intercepta requisições de rede para capturar URLs das imagens:
- `shadow.png` - Imagem do slider/peça móvel
- `back.png` - Imagem de fundo com o espaço vazio

### 2. Cálculo de Distância
Usa a biblioteca `ddddocr` (OCR especializado) para:
- Analisar a imagem do slider
- Detectar a posição exata do encaixe na imagem de fundo
- Retornar coordenadas (x, y) precisas

### 3. Mapeamento Slider-Shadow
Constrói uma tabela que mapeia:
- Distância real do arrasto (pixels) → Posição visual da sombra
- Isso é necessário porque a distância física ≠ distância visual

### 4. Arrasto Humanizado
Simula movimento humano com:
- Curvas de aceleração (easing)
- Micro-variações aleatórias
- Timing natural
- Evita detecção de bot

## 🐛 Solução de Problemas

### Erro: "Chrome não foi possível iniciar"
**Solução:**
1. Atualize o Chrome: `chrome://settings/help`
2. Feche TODAS as janelas do Chrome
3. Execute novamente

### Erro: "ddddocr não instalado"
**Solução:**
```bash
pip install --upgrade ddddocr
```

### Erro: "Timeout aguardando elemento"
**Solução:**
1. Verifique sua conexão com internet
2. Verifique se o Scene ID está correto
3. Tente recarregar a página

### Captcha Falha Mesmo com Distância Correta
**Possíveis Causas:**
1. IP bloqueado (muitas tentativas)
2. Detecção de automação
3. Variações no captcha
4. Ajuste fino necessário (+/- 1-2 pixels)

### Erro: "Formato inesperado" ao calcular distância
**Solução:**
1. Verifique se as URLs das imagens são válidas
2. Teste o download manual das imagens
3. Reinstale ddddocr: `pip install --upgrade --force-reinstall ddddocr`

## 📊 Saída Esperada

### Sucesso:
```
==================================================
   PROCESSO CONCLUÍDO
==================================================

📋 VERIFICANDO RESULTADO:
   1. Olhe para a janela do Chrome
   2. Se aparecer 'verificação bem-sucedida' = SUCESSO ✓
   3. Se aparecer erro ou nada acontecer = Falhou

💡 PARA VER O TOKEN:
   1. Na janela do Chrome, pressione F12
   2. Vá na aba 'Console'
   3. Procure por: Verificação aprovada! Parâmetros:
   4. O token estará após essa mensagem
```

### Token de Verificação:
O token de verificação será exibido no console do navegador em formato JSON:
```javascript
{
  captchaVerifyParam: "...",
  sessionId: "...",
  token: "..."
}
```

## 🔒 Segurança e Privacidade

- ✅ Todo código é executado localmente
- ✅ Nenhum dado é enviado para servidores externos
- ✅ URLs das imagens são temporárias
- ✅ Credenciais ficam apenas no seu arquivo HTML

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto é fornecido "como está", sem garantias. Use por sua conta e risco.

## ⚠️ Aviso Final

**Esta ferramenta é apenas para fins educacionais e de pesquisa.**

O uso indevido desta ferramenta pode:
- Violar termos de serviço
- Resultar em bloqueio de IP/conta
- Ter consequências legais

O autor não se responsabiliza por qualquer uso indevido ou danos causados pelo uso desta ferramenta.

---

## 📞 Suporte

Para problemas ou dúvidas:
1. Verifique a seção "Solução de Problemas"
2. Revise os logs de erro
3. Abra uma issue no repositório com:
   - Descrição do problema
   - Passos para reproduzir
   - Logs de erro completos
   - Versão do Python e Chrome

---

**Desenvolvido com 💙 para pesquisa de segurança**