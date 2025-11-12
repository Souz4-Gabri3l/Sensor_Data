import json
import random
from datetime import datetime, timedelta
from statistics import mean

# GERADOR DE DADOS FICTÍCIOS
def gerar_dados_sensores(qtd_registros: int = 10):
    dados = []
    tempo_base = datetime.now()

    for i in range(qtd_registros):
        leitura = {
            "horário": (tempo_base - timedelta(minutes=i)).isoformat(),
            "temperatura": round(random.uniform(18.0, 35.0), 2),
            "umidade": round(random.uniform(40.0, 90.0), 2),
        }
        dados.append(leitura)
    
    # Retorna os dados em ordem cronológica
    return list(reversed(dados))

# FUNÇÕES DE ARMAZENAMENTO
def salvar_em_json(dados, arquivo="dados_sensores.json"):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print(f"Dados salvos em {arquivo}")

def carregar_de_json(arquivo="dados_sensores.json"):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return []

# FUNÇÕES DE ANÁLISE E FILTRAGEM
def filtrar_por_temperatura(dados, temp_min=None, temp_max=None):
    return [
        d for d in dados
        if (temp_min is None or d["temperatura"] >= temp_min)
        and (temp_max is None or d["temperatura"] <= temp_max)
    ]

def calcular_medias(dados):
    if not dados:
        return None

    return {
        "média_temperatura": round(mean(d["temperatura"] for d in dados), 2),
        "média_umidade": round(mean(d["umidade"] for d in dados), 2),
    }


def exibir_resumo(dados):
    print("\n RESUMO DAS LEITURAS")
    print(f"Total de registros: {len(dados)}")

    medias = calcular_medias(dados)
    if medias:
        print(f"Temperatura média: {medias['média_temperatura']}°C")
        print(f"Umidade média: {medias['média_umidade']}%")

# NOVA FUNÇÃO — ALERTA DE TEMPERATURA
def verificar_alertas_temperatura(dados):
    print("\n VERIFICAÇÃO DE ALERTAS DE TEMPERATURA")

    for leitura in dados:
        temp = leitura["temperatura"]
        horario = leitura["horário"]

        if temp > 30:
            print(f"🔥 ALERTA DE CALOR: {temp}°C em {horario}")
        elif temp < 20:
            print(f"❄️  ALERTA DE FRIO: {temp}°C em {horario}")
    
    print("Verificação concluída.")

# EXECUÇÃO PRINCIPAL (TESTE)
if __name__ == "__main__":
    # Gerar dados simulados
    dados_sensores = gerar_dados_sensores(15)

    # Salvar em JSON
    salvar_em_json(dados_sensores)

    # Carregar os dados do arquivo
    dados_carregados = carregar_de_json()

    # Filtrar temperaturas acima de 30°C e abaixo de 20°C
    baixas_temperaturas = filtrar_por_temperatura(dados_carregados, temp_max=20.0)
    altas_temperaturas = filtrar_por_temperatura(dados_carregados, temp_min=30.0)

    # Exibir resumo das leituras
    exibir_resumo(dados_carregados)

    # Verificar alertas automáticos de temperatura
    verificar_alertas_temperatura(dados_carregados)

    # Mostrar quantas leituras estão acima de 30°C
    print(f"\n Leituras acima de 30°C: {len(altas_temperaturas)}")

    # Mostrar quantas leituras estão abaixo de 20°C
    print(f"\n Leituras abaixo de 20ºC: {len(baixas_temperaturas)}")

    # Finalização
    print("\nPrograma concluído.")