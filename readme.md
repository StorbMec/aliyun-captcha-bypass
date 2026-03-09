# Alibaba Cloud Slider Captcha Solver

Ferramenta em Python para **resolver captchas deslizantes (slider captcha) da Alibaba Cloud / Aliyun** usando análise de imagem e automação de navegador.

O projeto pode ser usado **de forma standalone** ou integrado em outros scripts.


---

# Requisitos

Sistema:

- Windows 10/11
- Linux
- macOS

Software necessário:

- Python 3.8+
- Google Chrome (versão recente)

Bibliotecas Python utilizadas:

- selenium
- undetected-chromedriver
- requests
- ddddocr
- opencv-python
- numpy
- pillow

---

# Instalação

Clone o repositório:

```bash
git clone [<repo-url>](https://github.com/StorbMec/aliyun-captcha-bypass)
cd aliyun-captcha-solver
```

Instale as dependências:

```bash
pip install -r requirements.txt
pip install selenium requests undetected-chromedriver ddddocr opencv-python numpy pillow
```
---

# Estrutura do Projeto

```
aliyun-captcha-solver/

run_captcha_solver.py
calculate_distance.py
captcha_test_page.html
stealth.min.js
requirements.txt
README.md
```

# Configuração

Antes de executar o solver, é necessário obter dois parâmetros do captcha:

- `prefix`
- `SceneId`

Eles podem ser encontrados no **Network tab do DevTools**.

Passos:

1. Abrir o site alvo
2. Pressionar **F12**
3. Ir em **Network**
4. Filtrar por `captcha`
5. Encontrar requisição para:

```
https://<prefix>.captcha-open.aliyuncs.com/
```

Exemplo:

```
https://no8xfe.captcha-open.aliyuncs.com/
```

Parâmetros extraídos:

```
prefix = no8xfe
SceneId = 36qgs6xb
```

Depois atualize no HTML:

```javascript
window.AliyunCaptchaConfig = {
  region: 'cn',
  prefix: 'SEU_PREFIX'
}
```

E:

```javascript
SceneId: "SEU_SCENE_ID"
```

---

# Uso

Execute o script principal:

```bash
python run_captcha_solver.py
```

Se o captcha for resolvido com sucesso, será retornado:

```
captchaVerifyParam: xxxxxxxxxxxxx
```

---

# Como Funciona

O processo segue basicamente estes passos:

1. Abrir página com captcha
2. Capturar URLs das imagens do captcha
3. Baixar as imagens (slider + background)
4. Detectar a posição do gap usando OpenCV
5. Calcular distância de arrasto
6. Simular movimento humano do mouse
7. Capturar o token de verificação

---

# Calcular Distância Manualmente

Também é possível rodar apenas o script de análise de imagem:

```bash
python calculate_distance.py <slider_url> <background_url>
```

Ele irá:

- baixar as imagens
- detectar o gap
- retornar a distância recomendada de arrasto

---

# Ajustes de Movimento

O movimento do slider utiliza:

- easing function (easeInOut)
- pequenas variações aleatórias
- tempo de arrasto aproximado de usuário real

Isso ajuda a reduzir detecção de automação.

---

# Problemas Comuns

Captcha falha mesmo com distância correta.

Possíveis causas:

- IP bloqueado
- detecção de automação
- pequena variação na distância

Solução comum:

```
ajustar +-1 a 3 pixels
```

---

Erro ao iniciar Chrome:

- atualizar Chrome
- fechar todas instâncias abertas
- reinstalar `undetected-chromedriver`

---

Erro em análise de imagem:

Ajustar parâmetros do OpenCV:

```python
cv2.Canny(gray, 50, 150)
```

---

# Integração em Outros Scripts

Exemplo simples usando subprocess:

```python
import subprocess
import re

result = subprocess.run(
    ["python", "run_captcha_solver.py"],
    capture_output=True,
    text=True
)

match = re.search(r'captchaVerifyParam:(.+)', result.stdout)

if match:
    captcha_param = match.group(1).strip()
```

---

# Contribuição

Pull requests são bem-vindos.

Fluxo sugerido:

```
fork
create branch
commit
push
open pull request
```

---

# Agradecimentos

Este projeto foi parcialmente inspirado por:

https://github.com/mucsbr/aliyun-captcha-fake

Agradecimentos ao autor pelo trabalho relacionado ao captcha da Aliyun.
