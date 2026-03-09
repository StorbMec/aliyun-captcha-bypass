#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ferramenta de Cálculo de Distância para Captcha Deslizante
Calcula automaticamente a distância que o slider precisa ser arrastado através de URLs de imagens

⚖️ Aviso Legal:
Esta ferramenta destina-se apenas a testes de segurança autorizados, pesquisa acadêmica e aprendizado técnico.
É estritamente proibido o uso para acesso não autorizado, lucro comercial, web scraping malicioso ou outros fins ilegais.
Ao usar esta ferramenta, você concorda em cumprir todas as leis e regulamentos aplicáveis e assumir os riscos de uso.
"""

import sys
import io

# CORREÇÃO PARA WINDOWS: Forçar UTF-8 no stdout
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import requests
import ddddocr


def calcular_distancia_de_urls(url_shadow, url_fundo):
    """
    Baixa imagens de URLs e calcula a distância do slider

    Args:
        url_shadow (str): URL da imagem do slider
        url_fundo (str): URL da imagem de fundo

    Returns:
        dict: Dicionário contendo informações de distância
    """
    try:
        # Baixar imagem do slider
        print(f"Baixando imagem do slider: {url_shadow[:60]}...")
        resposta_shadow = requests.get(url_shadow, timeout=10)
        resposta_shadow.raise_for_status()
        bytes_shadow = resposta_shadow.content

        # Baixar imagem de fundo
        print(f"Baixando imagem de fundo: {url_fundo[:60]}...")
        resposta_fundo = requests.get(url_fundo, timeout=10)
        resposta_fundo.raise_for_status()
        bytes_fundo = resposta_fundo.content

        # Usar ddddocr para calcular distância
        print("Calculando distância do slider...")
        det = ddddocr.DdddOcr(det=False, ocr=False)
        resultado = det.slide_match(bytes_shadow, bytes_fundo)

        return resultado

    except requests.RequestException as e:
        print(f"Falha no download da imagem: {e}")
        return None
    except Exception as e:
        print(f"Falha no cálculo da distância: {e}")
        return None

def main():
    if len(sys.argv) != 3:
        print("Uso incorreto!")
        print("Uso: python calcular_distancia.py <url_shadow> <url_fundo>")
        sys.exit(1)

    url_shadow = sys.argv[1]
    url_fundo = sys.argv[2]

    print("=" * 50)
    print("Calculadora de Distância do Slider")
    print("=" * 50)
    
    # Validar URLs
    if not url_shadow.startswith('http'):
        print(f"URL do shadow inválida: {url_shadow[:50]}...")
        sys.exit(1)
    
    if not url_fundo.startswith('http'):
        print(f"URL do fundo inválida: {url_fundo[:50]}...")
        sys.exit(1)

    resultado = calcular_distancia_de_urls(url_shadow, url_fundo)

    if resultado:
        print("\nResultado do Cálculo:")
        
        # ddddocr retorna um dicionário com 'target' que é uma tupla (x, y)
        # Também pode retornar apenas a coordenada x diretamente
        if isinstance(resultado, dict):
            if 'target' in resultado:
                # Formato: {'target': (x, y)}
                distancia = resultado['target'][0]
                print(f"Posição encontrada: x={resultado['target'][0]}, y={resultado['target'][1]}")
            else:
                # Tentar outras possíveis chaves
                print(f"Resultado completo: {resultado}")
                # Tentar extrair distância de qualquer forma
                for chave in resultado:
                    if isinstance(resultado[chave], (list, tuple)) and len(resultado[chave]) >= 1:
                        distancia = resultado[chave][0]
                        break
                else:
                    distancia = list(resultado.values())[0] if resultado.values() else 0
        elif isinstance(resultado, (int, float)):
            # Retorno direto da distância
            distancia = int(resultado)
        else:
            print(f"Formato inesperado: {resultado}")
            distancia = 0
        
        print(f"\nDistância de arrasto recomendada: {distancia} pixels")
        print("=" * 50)
    else:
        print("\nCálculo falhou!")
        print("Possíveis causas:")
        print("  1. ddddocr não instalado corretamente")
        print("  2. Falha no download da imagem")
        print("  3. Problema de conexão de rede")
        print("\nTente:")
        print("  pip install --upgrade ddddocr")
        sys.exit(1)

if __name__ == "__main__":
    main()