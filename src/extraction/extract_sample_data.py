import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker


# ============================================================
# Configurações iniciais
# ============================================================

# Faker em pt_BR para gerar nomes, empresas e textos com padrão brasileiro.
fake = Faker("pt_BR")
# Fixa as seeds para tornar a base reprodutível entre execuções.
random.seed(42)
Faker.seed(42)

# Caminhos absolutos da raiz do projeto e das pastas de dados.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, "data", "sample")

# Garante que as pastas existam antes de tentar salvar os CSVs.
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(SAMPLE_DATA_DIR, exist_ok=True)


# ============================================================
# Dados base simulados
# ============================================================

ORGAOS_PUBLICOS = [
    "Prefeitura Municipal de Fortaleza",
    "Prefeitura Municipal de Teresina",
    "Prefeitura Municipal de Recife",
    "Prefeitura Municipal de Salvador",
    "Prefeitura Municipal de São Luís",
    "Secretaria Estadual de Saúde",
    "Secretaria Estadual de Educação",
    "Secretaria Municipal de Infraestrutura",
    "Secretaria Municipal de Administração",
    "Secretaria Municipal de Assistência Social",
    "Departamento Estadual de Trânsito",
    "Instituto de Previdência Municipal",
    "Fundação Municipal de Cultura",
    "Câmara Municipal",
    "Tribunal de Contas do Estado",
]

# Lista de cidades, estados e regiões usadas para distribuir os registros.
CIDADES_ESTADOS = [
    ("Fortaleza", "CE", "Nordeste"),
    ("Teresina", "PI", "Nordeste"),
    ("Recife", "PE", "Nordeste"),
    ("Salvador", "BA", "Nordeste"),
    ("São Luís", "MA", "Nordeste"),
    ("Natal", "RN", "Nordeste"),
    ("João Pessoa", "PB", "Nordeste"),
    ("Maceió", "AL", "Nordeste"),
    ("Aracaju", "SE", "Nordeste"),
    ("São Paulo", "SP", "Sudeste"),
    ("Rio de Janeiro", "RJ", "Sudeste"),
    ("Belo Horizonte", "MG", "Sudeste"),
]

# Categorias e grupos analíticos para simular compras públicas variadas.
CATEGORIAS = [
    ("Material de escritório", "Bens de consumo"),
    ("Equipamentos de informática", "Tecnologia"),
    ("Serviços de limpeza", "Serviços terceirizados"),
    ("Serviços de vigilância", "Serviços terceirizados"),
    ("Medicamentos", "Saúde"),
    ("Equipamentos hospitalares", "Saúde"),
    ("Merenda escolar", "Educação"),
    ("Transporte escolar", "Educação"),
    ("Obras de pavimentação", "Infraestrutura"),
    ("Manutenção predial", "Infraestrutura"),
    ("Consultoria técnica", "Serviços especializados"),
    ("Software e sistemas", "Tecnologia"),
    ("Locação de veículos", "Transporte"),
    ("Combustíveis", "Transporte"),
]

# Modalidades de licitação presentes na base simulada.
MODALIDADES = [
    "Pregão Eletrônico",
    "Pregão Presencial",
    "Concorrência",
    "Tomada de Preços",
    "Dispensa de Licitação",
    "Inexigibilidade",
]

# Status possíveis do processo licitatório.
STATUS = [
    "Homologada",
    "Em andamento",
    "Cancelada",
    "Revogada",
    "Suspensa",
]

# Porte da empresa usado para variar o perfil dos fornecedores.
PORTES_EMPRESA = [
    "MEI",
    "Microempresa",
    "Empresa de Pequeno Porte",
    "Média Empresa",
    "Grande Empresa",
]


# ============================================================
# Funções auxiliares
# ============================================================

def gerar_cnpj_formatado() -> str:
    """
    Gera um CNPJ fictício formatado.
    Este CNPJ é apenas para fins de simulação de dados.
    """
    # Gera 14 dígitos aleatórios e monta o formato padrão de CNPJ.
    numeros = [random.randint(0, 9) for _ in range(14)]
    return (
        f"{numeros[0]}{numeros[1]}.{numeros[2]}{numeros[3]}{numeros[4]}."
        f"{numeros[5]}{numeros[6]}{numeros[7]}/"
        f"{numeros[8]}{numeros[9]}{numeros[10]}{numeros[11]}-"
        f"{numeros[12]}{numeros[13]}"
    )


def gerar_fornecedores(qtd_fornecedores: int = 120) -> list[dict]:
    """
    Gera uma lista de fornecedores simulados.
    Alguns fornecedores serão usados de forma recorrente para criar padrões analíticos.
    """
    # Começa com uma lista vazia e adiciona fornecedores fixos para repetição.
    fornecedores = []

    nomes_fixos = [
        "Alpha Serviços Integrados Ltda",
        "Nordeste Tecnologia e Sistemas Ltda",
        "Global Med Distribuidora Ltda",
        "Prime Construções e Engenharia Ltda",
        "Sigma Segurança Patrimonial Ltda",
        "Delta Soluções Administrativas Ltda",
        "Omega Comércio de Equipamentos Ltda",
        "Maximus Transportes e Logística Ltda",
        "DataGov Sistemas Públicos Ltda",
        "Conecta Saúde Distribuidora Ltda",
    ]

    for nome in nomes_fixos:
        # Fornecedores recorrentes ajudam a simular concentração de compras.
        fornecedores.append(
            {
                "nome_fornecedor": nome,
                "cnpj_fornecedor": gerar_cnpj_formatado(),
                "porte_empresa": random.choice(PORTES_EMPRESA),
                "fornecedor_recorrente": True,
            }
        )

    for _ in range(qtd_fornecedores - len(nomes_fixos)):
        # Completa a base com fornecedores aleatórios para diversificar os dados.
        fornecedores.append(
            {
                "nome_fornecedor": fake.company(),
                "cnpj_fornecedor": gerar_cnpj_formatado(),
                "porte_empresa": random.choice(PORTES_EMPRESA),
                "fornecedor_recorrente": False,
            }
        )

    return fornecedores


def gerar_valor_por_categoria(categoria: str) -> float:
    """
    Gera valores estimados com faixas diferentes por categoria.
    Isso deixa a base mais realista.
    """
    # Cada categoria recebe uma faixa de valores coerente com o tipo de compra.
    faixas = {
        "Material de escritório": (5_000, 80_000),
        "Equipamentos de informática": (20_000, 600_000),
        "Serviços de limpeza": (30_000, 900_000),
        "Serviços de vigilância": (50_000, 1_200_000),
        "Medicamentos": (30_000, 2_000_000),
        "Equipamentos hospitalares": (80_000, 3_500_000),
        "Merenda escolar": (40_000, 1_800_000),
        "Transporte escolar": (60_000, 2_500_000),
        "Obras de pavimentação": (150_000, 8_000_000),
        "Manutenção predial": (40_000, 1_500_000),
        "Consultoria técnica": (20_000, 700_000),
        "Software e sistemas": (30_000, 1_200_000),
        "Locação de veículos": (40_000, 1_000_000),
        "Combustíveis": (50_000, 2_000_000),
    }

    minimo, maximo = faixas.get(categoria, (10_000, 500_000))
    return round(random.uniform(minimo, maximo), 2)


def calcular_valor_contratado(valor_estimado: float, gerar_outlier: bool = False) -> float:
    """
    Gera o valor contratado.
    Em casos normais, ele fica próximo ao valor estimado.
    Em casos suspeitos, fica muito acima da média.
    """
    # Outliers simulam sobrepreço ou contratos muito acima do esperado.
    if gerar_outlier:
        fator = random.uniform(1.45, 2.80)
    else:
        fator = random.uniform(0.75, 1.18)

    return round(valor_estimado * fator, 2)


def calcular_score_risco(
    valor_estimado: float,
    valor_contratado: float,
    fornecedor_recorrente: bool,
    modalidade: str,
    status: str,
    gerar_outlier: bool,
) -> tuple[float, str]:
    """
    Cria um score inicial de risco baseado em regras simples.
    Depois, nas próximas etapas, vamos evoluir isso com Machine Learning.
    """
    # Começa com score neutro e soma pontos conforme sinais de risco aparecem.
    score = 0

    percentual_diferenca = ((valor_contratado - valor_estimado) / valor_estimado) * 100

    if percentual_diferenca > 15:
        score += 20

    if percentual_diferenca > 40:
        score += 25

    if fornecedor_recorrente:
        score += 15

    if modalidade in ["Dispensa de Licitação", "Inexigibilidade"]:
        score += 20

    if status in ["Cancelada", "Revogada", "Suspensa"]:
        score += 10

    if gerar_outlier:
        score += 30

    score = min(score, 100)

    # Converte o score num nível qualitativo fácil de interpretar no dashboard.
    if score < 25:
        nivel = "Baixo"
    elif score < 50:
        nivel = "Médio"
    elif score < 75:
        nivel = "Alto"
    else:
        nivel = "Crítico"

    return round(score, 2), nivel


# ============================================================
# Geração da base
# ============================================================

def gerar_base_licitacoes(qtd_registros: int = 1500) -> pd.DataFrame:
    """
    Gera uma base simulada de licitações públicas.
    """
    # Gera o catálogo de fornecedores uma vez e reutiliza ao longo dos registros.
    fornecedores = gerar_fornecedores()
    registros = []

    # Define o intervalo temporal da simulação.
    data_inicio = datetime(2021, 1, 1)
    data_fim = datetime(2025, 12, 31)
    intervalo_dias = (data_fim - data_inicio).days

    for i in range(1, qtd_registros + 1):
        # Sorteia as dimensões principais do registro.
        orgao = random.choice(ORGAOS_PUBLICOS)
        cidade, estado, regiao = random.choice(CIDADES_ESTADOS)
        categoria, grupo_categoria = random.choice(CATEGORIAS)
        modalidade = random.choice(MODALIDADES)

        # Força fornecedores recorrentes a aparecerem mais vezes.
        if random.random() < 0.35:
            fornecedor = random.choice([f for f in fornecedores if f["fornecedor_recorrente"]])
        else:
            fornecedor = random.choice(fornecedores)

        # Estima o valor com base na categoria escolhida.
        valor_estimado = gerar_valor_por_categoria(categoria)

        # Cria anomalias em uma pequena parte da base.
        gerar_outlier = random.random() < 0.08
        valor_contratado = calcular_valor_contratado(valor_estimado, gerar_outlier)

        # Datas simuladas de publicação e homologação.
        data_publicacao = data_inicio + timedelta(days=random.randint(0, intervalo_dias))
        data_homologacao = data_publicacao + timedelta(days=random.randint(10, 120))

        # Status com distribuição enviesada para refletir cenário realista.
        status = random.choices(
            STATUS,
            weights=[0.72, 0.12, 0.06, 0.05, 0.05],
            k=1
        )[0]

        # Métricas derivadas do contrato.
        diferenca_valor = round(valor_contratado - valor_estimado, 2)
        percentual_diferenca = round((diferenca_valor / valor_estimado) * 100, 2)

        # Calcula score e nível de risco para cada licitação.
        score_risco, nivel_risco = calcular_score_risco(
            valor_estimado=valor_estimado,
            valor_contratado=valor_contratado,
            fornecedor_recorrente=fornecedor["fornecedor_recorrente"],
            modalidade=modalidade,
            status=status,
            gerar_outlier=gerar_outlier,
        )

        # Consolida o registro final que será exportado para CSV.
        registros.append(
            {
                "id_licitacao": i,
                "numero_processo": f"{random.randint(1000, 9999)}/{data_publicacao.year}",
                "orgao": orgao,
                "cidade": cidade,
                "estado": estado,
                "regiao": regiao,
                "categoria": categoria,
                "grupo_categoria": grupo_categoria,
                "descricao": f"Contratação referente a {categoria.lower()} para atendimento de demandas públicas.",
                "fornecedor": fornecedor["nome_fornecedor"],
                "cnpj_fornecedor": fornecedor["cnpj_fornecedor"],
                "porte_empresa": fornecedor["porte_empresa"],
                "valor_estimado": valor_estimado,
                "valor_contratado": valor_contratado,
                "diferenca_valor": diferenca_valor,
                "percentual_diferenca": percentual_diferenca,
                "data_publicacao": data_publicacao.date(),
                "data_homologacao": data_homologacao.date(),
                "ano": data_publicacao.year,
                "mes": data_publicacao.month,
                "trimestre": ((data_publicacao.month - 1) // 3) + 1,
                "modalidade": modalidade,
                "status": status,
                "fornecedor_recorrente": fornecedor["fornecedor_recorrente"],
                "possivel_outlier": gerar_outlier,
                "score_risco": score_risco,
                "nivel_risco": nivel_risco,
            }
        )

    # Transforma a lista de dicionários em DataFrame para salvar e analisar.
    df = pd.DataFrame(registros)
    return df


def salvar_dados(df: pd.DataFrame) -> None:
    """
    Salva os dados gerados nas pastas raw e sample.
    """
    # Define os destinos dos arquivos gerados.
    raw_path = os.path.join(RAW_DATA_DIR, "licitacoes_raw.csv")
    sample_path = os.path.join(SAMPLE_DATA_DIR, "licitacoes_sample.csv")

    # Salva a base completa e uma amostra reduzida para uso rápido.
    df.to_csv(raw_path, index=False, encoding="utf-8-sig")
    df.head(100).to_csv(sample_path, index=False, encoding="utf-8-sig")

    # Exibe um resumo simples da execução no terminal.
    print("Base de dados gerada com sucesso!")
    print(f"Total de registros: {len(df)}")
    print(f"Arquivo raw salvo em: {raw_path}")
    print(f"Arquivo sample salvo em: {sample_path}")

    print("\nPrévia dos dados:")
    print(df.head())

    print("\nDistribuição por nível de risco:")
    print(df["nivel_risco"].value_counts())

    print("\nValor total contratado:")
    print(f"R$ {df['valor_contratado'].sum():,.2f}")


if __name__ == "__main__":
    # Executa a geração da base quando o arquivo é chamado diretamente.
    df_licitacoes = gerar_base_licitacoes(qtd_registros=1500)
    salvar_dados(df_licitacoes)
