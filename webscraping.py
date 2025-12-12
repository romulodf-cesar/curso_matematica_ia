from pathlib import Path
import pandas as pd
# ========= CONFIGURAÇÕES GERAIS ========= #
# Página com a tabela do Brasileirão Série A 2024 (HTML estável)
URL_TABELA = "https://www.futexcel.com.br/brasileirao/index.html"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
ARQUIVO_SAIDA = DATA_DIR / "brasileirao_serie_a_2025.csv"
# ========= 1) LER A TABELA DIRETO COM PANDAS.READ_HTML ========= #


def extrair_tabela_brasileirao() -> pd.DataFrame:
    """
    Usa pandas.read_html para ler as tabelas da página e
    retorna a tabela de classificação do Brasileirão.
    """

    print(f"[PANDAS] Lendo tabelas com read_html a partir de: {URL_TABELA}")
    # pandas faz o request HTTP internamente
    tabelas = pd.read_html(URL_TABELA)
    print(f"[PANDAS] Quantidade de tabelas encontradas: {len(tabelas)}")

    # Olhar rapidamente o shape de cada tabela (para debug/estudo)
    for i, t in enumerate(tabelas):
        print(f"  - Tabela {i}: shape = {t.shape}")

    # Na futexcel, a primeira tabela geralmente é a de classificação
    df = tabelas[0].copy()

    print("\n[PANDAS] Colunas originais:")
    print(df.columns)

    # Caso o cabeçalho venha meio estranho / multi-index, vamos "achatar"
    novas_colunas = []
    for col in df.columns:
        if isinstance(col, tuple):
            partes = [str(c) for c in col if not pd.isna(c)]
            nome = " ".join(partes)
        else:
            nome = str(col)
        novas_colunas.append(nome)

    df.columns = novas_colunas

    print("\n[PANDAS] Colunas após ajuste:")
    print(df.columns)

    # Renomear colunas para nomes mais amigáveis (ajusta conforme necessário)
    mapa_cols = {
        "Pos": "posicao",
        "Time": "time",
        "P": "pontos",
        "Pts": "pontos",
        "J": "jogos",
        "V": "vitorias",
        "E": "empates",
        "D": "derrotas",
        "GP": "gols_pro",
        "GC": "gols_contra",
        "SG": "saldo_gols",
        "S": "saldo_gols",
        "%": "aproveitamento",
    }

    df = df.rename(columns=lambda c: mapa_cols.get(c, c))

    print("\n[PANDAS] Colunas finais:")
    print(df.columns)

    print("\n[PANDAS] Primeiras linhas da tabela:")
    print(df.head())

    return df


# ========= 2) SALVAR EM CSV ========= #

def salvar_tabela_csv(df: pd.DataFrame, caminho: Path) -> None:
    """
    Salva o DataFrame em um arquivo CSV na pasta data/.
    """
    df.to_csv(caminho, index=False, encoding="utf-8")
    print(f"\n[CSV] Arquivo salvo em: {caminho.resolve()}")


# ========= 3) MAIN ========= #

def main():
    print("=== Scraper da Tabela do Brasileirão Série A 2024 ===\n")

    df_tabela = extrair_tabela_brasileirao()
    salvar_tabela_csv(df_tabela, ARQUIVO_SAIDA)

    print("\nTudo pronto! Abra o arquivo:")
    print(f" -> {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()
