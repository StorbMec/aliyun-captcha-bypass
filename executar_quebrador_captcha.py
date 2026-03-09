#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ferramenta Automática de Quebra de Captcha Deslizante da Alibaba Cloud
Detecta automaticamente a versão do Chrome
"""

import os
import subprocess
import re
import time
import sys

# Verificar dependências
try:
    import undetected_chromedriver as uc
    print("✓ undetected_chromedriver encontrado")
except ImportError:
    print("❌ ERRO: undetected_chromedriver não instalado")
    print("Execute: pip install undetected-chromedriver")
    sys.exit(1)

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def obter_versao_chrome():
    """Detecta a versão do Chrome instalado"""
    try:
        # Windows
        if sys.platform == 'win32':
            import winreg
            try:
                # Tentar registro do Chrome
                chave = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
                versao, _ = winreg.QueryValueEx(chave, 'version')
                winreg.CloseKey(chave)
                versao_principal = int(versao.split('.')[0])
                print(f"✓ Chrome detectado: versão {versao} (principal: {versao_principal})")
                return versao_principal
            except:
                pass
            
            # Tentar via comando
            try:
                caminho_chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
                if not os.path.exists(caminho_chrome):
                    caminho_chrome = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
                
                resultado = subprocess.run([caminho_chrome, '--version'], capture_output=True, text=True)
                versao = resultado.stdout.strip().split()[-1]
                versao_principal = int(versao.split('.')[0])
                print(f"✓ Chrome detectado: versão {versao} (principal: {versao_principal})")
                return versao_principal
            except:
                pass
        
        # Se não conseguiu detectar, retornar None
        print("⚠ Não foi possível detectar a versão do Chrome automaticamente")
        return None
        
    except Exception as e:
        print(f"⚠ Erro ao detectar versão do Chrome: {e}")
        return None


def main():
    print("\n" + "=" * 60)
    print("   Ferramenta de Quebra de Captcha Deslizante da Alibaba Cloud")
    print("=" * 60 + "\n")

    # --- DETECTAR VERSÃO DO CHROME ---
    versao_chrome = obter_versao_chrome()
    
    # --- INICIAR CHROME ---
    print("⏳ Iniciando Chrome...")
    
    driver = None
    erros = []
    
    # Tentar com versão detectada
    if versao_chrome:
        try:
            print(f"   Tentando com versão {versao_chrome}...")
            driver = uc.Chrome(
                headless=False,
                use_subprocess=False,
                version_main=versao_chrome
            )
            print(f"✓ Chrome iniciado com versão {versao_chrome}\n")
        except Exception as e:
            erros.append(f"Versão {versao_chrome}: {str(e)[:100]}")
            print(f"   ✗ Falhou com versão {versao_chrome}")
    
    # Se falhou, tentar versões comuns
    if not driver:
        versoes_comuns = [145, 144, 146, 143, 147]  # Versões mais comuns
        
        for ver in versoes_comuns:
            if ver == versao_chrome:  # Já tentamos
                continue
            
            try:
                print(f"   Tentando versão {ver}...")
                driver = uc.Chrome(
                    headless=False,
                    use_subprocess=False,
                    version_main=ver
                )
                print(f"✓ Chrome iniciado com versão {ver}\n")
                break
            except Exception as e:
                erros.append(f"Versão {ver}: {str(e)[:100]}")
                continue
    
    # Se ainda não conseguiu
    if not driver:
        print("\n" + "=" * 60)
        print("❌ NÃO FOI POSSÍVEL INICIAR O CHROME")
        print("=" * 60)
        print("\nTentativas feitas:")
        for erro in erros[:3]:  # Mostrar só as 3 primeiras
            print(f"  - {erro}")
        
        print("\n🔧 SOLUÇÕES:")
        print("\n1. ATUALIZE O CHROME:")
        print("   - Abra o Chrome manualmente")
        print("   - Vá em: Configurações → Sobre o Chrome")
        print("   - Aguarde atualizar para a versão mais recente")
        print("   - Feche TODAS as janelas do Chrome")
        print("   - Execute este script novamente")
        
        print("\n2. OU force uma versão específica:")
        print("   - Edite o arquivo executar_quebrador_captcha.py")
        print("   - Linha ~80, mude para:")
        print("     driver = uc.Chrome(version_main=145)  # Use SUA versão")
        
        print("\n3. OU reinstale o driver:")
        print("   pip uninstall undetected-chromedriver -y")
        print("   pip install undetected-chromedriver")
        
        return

    try:
        # --- INJETAR ANTI-DETECÇÃO ---
        if os.path.exists('stealth.min.js'):
            with open('stealth.min.js', 'r', encoding='utf-8') as f:
                driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': f.read()})
            print("✓ Anti-detecção ativado")
        else:
            print("⚠ stealth.min.js não encontrado (opcional)")

        # --- ABRIR PÁGINA ---
        print("⏳ Carregando página...\n")
        caminho_html = os.path.abspath("pagina_captcha.html")
        
        if not os.path.exists(caminho_html):
            print(f"❌ Arquivo não encontrado: {caminho_html}")
            print(f"   Procurado em: {os.getcwd()}")
            return
        
        driver.get(f"file://{caminho_html}")
        time.sleep(5)
        print("✓ Página carregada")

        # --- PASSO 1: CAPTURAR URLS ---
        print("\n" + "-" * 60)
        print("PASSO 1: Capturando URLs das imagens")
        print("-" * 60)
        
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "calcular-auto"))
        )
        btn.click()
        
        WebDriverWait(driver, 10).until(
            lambda d: "python calcular_distancia.py" in d.find_element(By.ID, "exibicao-urls-imagens").text
        )
        
        comando = driver.find_element(By.CSS_SELECTOR, "span[style*='monospace']").text
        print(f"✓ Comando: {comando[:70]}...")

        # --- PASSO 2: CALCULAR DISTÂNCIA ---
        print("\n" + "-" * 60)
        print("PASSO 2: Calculando distância com Python")
        print("-" * 60)
        
        # Pegar URLs diretamente do JavaScript ao invés do comando
        import shlex
        
        url_shadow = driver.execute_script("return window.obterUrlImagemSlider();")
        url_fundo = driver.execute_script("return window.obterUrlImagemFundo();")
        
        print(f"URL Shadow: {url_shadow[:80]}...")
        print(f"URL Fundo: {url_fundo[:80]}...")
        
        # Executar Python diretamente ao invés de via shell
        import sys
        resultado = subprocess.run(
            [sys.executable, "calcular_distancia.py", url_shadow, url_fundo],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # Mostrar saída completa
        if resultado.stdout:
            print("\n" + resultado.stdout)
        if resultado.stderr:
            print("STDERR:")
            print(resultado.stderr)
        
        # Verificar se houve erro
        if resultado.returncode != 0:
            print(f"\n❌ O script falhou com código de erro: {resultado.returncode}")
            print("\n🔧 TESTE MANUAL:")
            print(f'   python calcular_distancia.py "{url_shadow}" "{url_fundo}"')
            print("\n💡 DICA: Copie o comando acima e execute manualmente para ver o erro")
            return
        
        match = re.search(r"Distância de arrasto recomendada: (\d+)", resultado.stdout)
        if not match:
            print("\n❌ Não foi possível extrair a distância da saída")
            print("   Saída recebida:")
            print(f"   {resultado.stdout[:200]}")
            return
        
        dist_shadow = int(match.group(1))
        print(f"✓ Distância calculada: {dist_shadow}px")

        # --- PASSO 3: CONSTRUIR MAPEAMENTO ---
        print("\n" + "-" * 60)
        print("PASSO 3: Construindo tabela de mapeamento (~10 segundos)")
        print("-" * 60)
        
        driver.find_element(By.ID, "construir-mapeamento").click()
        
        WebDriverWait(driver, 25).until(
            lambda d: "Total de" in d.find_element(By.ID, "exibicao-urls-imagens").text
        )
        print("✓ Tabela construída")
        time.sleep(1)

        # --- PASSO 4: ENCONTRAR DISTÂNCIA IDEAL ---
        print("\n" + "-" * 60)
        print("PASSO 4: Calculando distância ideal do slider")
        print("-" * 60)
        
        input_shadow = driver.find_element(By.ID, "distancia-shadow")
        input_shadow.clear()
        input_shadow.send_keys(str(dist_shadow))
        
        driver.find_element(By.ID, "buscar-slider").click()
        time.sleep(1)
        
        dist_slider = driver.find_element(By.ID, "distancia-arrasto").get_attribute("value")
        print(f"✓ Distância do slider: {dist_slider}px")

        # --- PASSO 5: ARRASTAR ---
        print("\n" + "-" * 60)
        print("PASSO 5: Executando arrasto humanizado")
        print("-" * 60)
        print("   (Observe o Chrome - o slider vai se mover)")
        
        driver.find_element(By.ID, "testar-arrasto").click()
        
        print("\n⏳ Aguardando verificação (20 segundos)...")
        time.sleep(5)

        # --- RESULTADO ---
        print("\n" + "=" * 60)
        print("   PROCESSO CONCLUÍDO")
        print("=" * 60)
        print("\n📋 VERIFICANDO RESULTADO:")
        print("   1. Olhe para a janela do Chrome")
        print("   2. Se aparecer 'verificação bem-sucedida' = SUCESSO ✓")
        print("   3. Se aparecer erro ou nada acontecer = Falhou")
        
        print("\n💡 PARA VER O TOKEN:")
        print("   1. Na janela do Chrome, pressione F12")
        print("   2. Vá na aba 'Console'")
        print("   3. Procure por: Verificação aprovada! Parâmetros:")
        print("   4. O token estará após essa mensagem")
        print("=" * 60 + "\n")
        
        input("⏸ Pressione ENTER para fechar o navegador...")

    except KeyboardInterrupt:
        print("\n\n⏹ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione ENTER para fechar...")
    finally:
        try:
            driver.quit()
            print("✓ Navegador fechado")
        except:
            pass


if __name__ == "__main__":
    main()