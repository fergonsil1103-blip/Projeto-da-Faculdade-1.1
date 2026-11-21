import csv


class Imovel:
    """Classe base para os imóveis da R.M Imóveis."""

    def __init__(self, categoria: str, aluguel_base: float):
        self.categoria = categoria
        self.aluguel_base = aluguel_base

    def calcular_adicional_quartos(self) -> float:
        return 0.0

    def calcular_adicional_estacionamento(self) -> float:
        return 0.0

    def calcular_desconto(self, subtotal: float) -> float:
        return 0.0

    def calcular_aluguel_mensal(self) -> float:
        subtotal = (
            self.aluguel_base
            + self.calcular_adicional_quartos()
            + self.calcular_adicional_estacionamento()
        )
        desconto = self.calcular_desconto(subtotal)
        return round(subtotal - desconto, 2)


class Apartamento(Imovel):
    """Apartamento: base R$ 700, +R$ 200 (2 quartos), +R$ 300 (garagem), -5% sem crianças."""

    def __init__(self, quartos: int, possui_garagem: bool, possui_criancas: bool):
        super().__init__("Apartamento", 700.00)
        self.quartos = quartos
        self.possui_garagem = possui_garagem
        self.possui_criancas = possui_criancas

    def calcular_adicional_quartos(self) -> float:
        return 200.00 if self.quartos == 2 else 0.0

    def calcular_adicional_estacionamento(self) -> float:
        return 300.00 if self.possui_garagem else 0.0

    def calcular_desconto(self, subtotal: float) -> float:
        if not self.possui_criancas:
            return round(subtotal * 0.05, 2)
        return 0.0


class Casa(Imovel):
    """Casa: base R$ 900, +R$ 250 (2 quartos), +R$ 300 (garagem)."""

    def __init__(self, quartos: int, possui_garagem: bool):
        super().__init__("Casa", 900.00)
        self.quartos = quartos
        self.possui_garagem = possui_garagem

    def calcular_adicional_quartos(self) -> float:
        return 250.00 if self.quartos == 2 else 0.0

    def calcular_adicional_estacionamento(self) -> float:
        return 300.00 if self.possui_garagem else 0.0


class Estudio(Imovel):
    """Estúdio: base R$ 1.200, pacote 2 vagas por R$ 250 + R$ 60 por vaga extra."""

    def __init__(self, vagas: int):
        super().__init__("Estúdio", 1200.00)
        self.vagas = vagas

    def calcular_adicional_estacionamento(self) -> float:
        if self.vagas == 0:
            return 0.0
        vagas_extras = self.vagas - 2
        return 250.00 + (vagas_extras * 60.00)


class OrcamentoLocacao:
    """Agrupa o imóvel escolhido, a taxa contratual e a projeção de 12 meses."""

    TAXA_CONTRATUAL = 2000.00

    def __init__(self, imovel: Imovel, parcelas_taxa: int):
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa

    def calcular_parcela_taxa(self) -> float:
        return round(self.TAXA_CONTRATUAL / self.parcelas_taxa, 2)

    def gerar_projecao_anual(self) -> list[dict]:
        aluguel_mensal = self.imovel.calcular_aluguel_mensal()
        valor_parcela = self.calcular_parcela_taxa()
        projecao = []

        for mes in range(1, 13):
            parcela_mes = valor_parcela if mes <= self.parcelas_taxa else 0.0
            total_mes = round(aluguel_mensal + parcela_mes, 2)
            projecao.append(
                {
                    "mes": mes,
                    "aluguel_mensal": f"{aluguel_mensal:.2f}",
                    "parcela_taxa_contratual": f"{parcela_mes:.2f}",
                    "total_mes": f"{total_mes:.2f}",
                }
            )
        return projecao

    def exibir_resumo(self) -> None:
        subtotal = (
            self.imovel.aluguel_base
            + self.imovel.calcular_adicional_quartos()
            + self.imovel.calcular_adicional_estacionamento()
        )
        desconto = self.imovel.calcular_desconto(subtotal)
        aluguel_final = self.imovel.calcular_aluguel_mensal()

        print("\n" + "=" * 52)
        print("RENTSMART - RESUMO DO ORÇAMENTO (R.M IMÓVEIS)")
        print("=" * 52)
        print(f"Categoria do imóvel       : {self.imovel.categoria}")

        if isinstance(self.imovel, (Apartamento, Casa)):
            print(f"Quantidade de quartos     : {self.imovel.quartos}")
            print(f"Vaga de garagem           : {'Sim' if self.imovel.possui_garagem else 'Não'}")
        if isinstance(self.imovel, Apartamento):
            print(f"Possui crianças           : {'Sim' if self.imovel.possui_criancas else 'Não'}")
        if isinstance(self.imovel, Estudio):
            print(f"Vagas de estacionamento   : {self.imovel.vagas}")

        print("-" * 52)
        print("VALORES MENSAIS DO ALUGUEL:")
        print(f"  Aluguel-base            : R$ {self.imovel.aluguel_base:>8.2f}")
        print(f"  Adicional de quartos    : R$ {self.imovel.calcular_adicional_quartos():>8.2f}")
        print(f"  Adicional estacionamento: R$ {self.imovel.calcular_adicional_estacionamento():>8.2f}")
        print(f"  Desconto aplicado       : -R$ {desconto:>7.2f}")
        print(f"  ALUGUEL MENSAL FINAL    : R$ {aluguel_final:>8.2f}")
        print("-" * 52)
        print("TAXA CONTRATUAL (SEPARADA DO ALUGUEL):")
        print(f"  Valor total da taxa     : R$ {self.TAXA_CONTRATUAL:>8.2f}")
        print(f"  Parcelamento escolhido  : {self.parcelas_taxa}x de R$ {self.calcular_parcela_taxa():.2f}")
        print("=" * 52)


class GeradorCSV:
    """Responsável por salvar a projeção dos 12 meses em arquivo CSV."""

    @staticmethod
    def salvar_projecao(orcamento: OrcamentoLocacao, nome_arquivo: str = "projecao_12_meses.csv") -> str:
        if not nome_arquivo.endswith(".csv"):
            nome_arquivo += ".csv"

        dados = orcamento.gerar_projecao_anual()
        colunas = ["mes", "aluguel_mensal", "parcela_taxa_contratual", "total_mes"]

        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=colunas, delimiter=";")
            escritor.writeheader()
            escritor.writerows(dados)

        return nome_arquivo


def ler_opcao_inteira(mensagem: str, opcoes_validas: list[int]) -> int:
    while True:
        try:
            valor = int(input(mensagem).strip())
            if valor in opcoes_validas:
                return valor
        except ValueError:
            pass
        print(f"Opção inválida! Escolha entre {opcoes_validas}.")


def ler_vagas_estudio() -> int:
    while True:
        try:
            vagas = int(input("Quantas vagas deseja? (0 para nenhuma, ou a partir de 2 vagas): ").strip())
            if vagas == 0 or vagas >= 2:
                return vagas
        except ValueError:
            pass
        print("Valor inválido! Para estúdio, informe 0 vagas ou no mínimo 2 vagas.")


def ler_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Resposta inválida! Digite 's' para sim ou 'n' para não.")


def main():
    print("=== Bem-vindo ao RentSmart - R.M Imóveis ===")
    print("1 - Apartamento (base R$ 700,00)")
    print("2 - Casa (base R$ 900,00)")
    print("3 - Estúdio (base R$ 1.200,00)")

    tipo = ler_opcao_inteira("Escolha o tipo de imóvel (1, 2 ou 3): ", [1, 2, 3])

    if tipo == 1:
        quartos = ler_opcao_inteira("Quantidade de quartos (1 ou 2): ", [1, 2])
        garagem = ler_sim_nao("Deseja vaga de garagem (+R$ 300,00/mês)? (s/n): ")
        criancas = ler_sim_nao("O cliente possui crianças? (s/n): ")
        imovel = Apartamento(quartos, garagem, criancas)
    elif tipo == 2:
        quartos = ler_opcao_inteira("Quantidade de quartos (1 ou 2): ", [1, 2])
        garagem = ler_sim_nao("Deseja vaga de garagem (+R$ 300,00/mês)? (s/n): ")
        imovel = Casa(quartos, garagem)
    else:
        vagas = ler_vagas_estudio()
        imovel = Estudio(vagas)

    parcelas = ler_opcao_inteira(
        "Em quantas parcelas deseja pagar a taxa contratual de R$ 2.000,00 (1 a 5)? ",
        [1, 2, 3, 4, 5],
    )

    orcamento = OrcamentoLocacao(imovel, parcelas)
    orcamento.exibir_resumo()

    nome_csv = input("\nDigite o nome do arquivo CSV (ou Enter para 'projecao_12_meses.csv'): ").strip()
    if not nome_csv:
        nome_csv = "projecao_12_meses.csv"

    arquivo_salvo = GeradorCSV.salvar_projecao(orcamento, nome_csv)
    print(f"\nArquivo '{arquivo_salvo}' gerado com sucesso!")


if __name__ == "__main__":
    main()
