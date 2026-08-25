"""
Management command para popular o banco de dados com categorias e produtos
de um e-commerce de roupas, usando Faker.

Uso:
    python manage.py popular_dados
    python manage.py popular_dados --limpar
    # apaga os dados existentes antes de popular
"""

import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

# Ajuste este import para o caminho real da sua app
from meteora.models import Categoria, Produto

fake = Faker("pt_BR")

# Categorias fixas de um e-commerce de roupas (nomes controlados,
# já que "nome" é unique=True e não faz sentido gerar aleatoriamente)
CATEGORIAS = [
    {
        "nome": "Camisetas",
        "descricao": "Camisetas casuais e estampadas para o dia a dia.",
    },
    {
        "nome": "Calças",
        "descricao": "Calças jeans, sarja e moletom para todos os estilos.",
    },
    {
        "nome": "Vestidos",
        "descricao": "Vestidos casuais, festa e trabalho.",
    },
    {
        "nome": "Jaquetas",
        "descricao": "Jaquetas e casacos para dias frios.",
    },
    {
        "nome": "Moletons",
        "descricao": "Moletons e blusas de frio confortáveis.",
    },
    {
        "nome": "Shorts",
        "descricao": "Shorts e bermudas para o verão.",
    },
    {
        "nome": "Saias",
        "descricao": "Saias em diversos comprimentos e tecidos.",
    },
    {
        "nome": "Blusas",
        "descricao": "Blusas femininas para diferentes ocasiões.",
    },
    {
        "nome": "Calçados",
        "descricao": "Tênis, sapatos e sandálias.",
    },
    {
        "nome": "Acessórios",
        "descricao": "Bonés, cintos, bolsas e outros acessórios.",
    },
]

# Palavras usadas para montar nomes de produtos plausíveis por categoria
PRODUTOS_POR_CATEGORIA = {
    "Camisetas": [
        "Camiseta Básica",
        "Camiseta Estampada",
        "Camiseta Gola V",
        "Camiseta Oversized",
    ],
    "Calças": [
        "Calça Jeans Skinny",
        "Calça Sarja",
        "Calça Moletom",
        "Calça Alfaiataria",
    ],
    "Vestidos": ["Vestido Midi", "Vestido Longo", "Vestido Casual", "Vestido de Festa"],
    "Jaquetas": [
        "Jaqueta Jeans",
        "Jaqueta Corta-Vento",
        "Jaqueta de Couro",
        "Jaqueta Bomber",
    ],
    "Moletons": ["Moletom Canguru", "Moletom Careca", "Moletom com Capuz"],
    "Shorts": ["Short Jeans", "Short Moletom", "Bermuda Cargo"],
    "Saias": ["Saia Midi", "Saia Jeans", "Saia Plissada"],
    "Blusas": ["Blusa de Tricô", "Blusa Cropped", "Blusa Social"],
    "Calçados": ["Tênis Casual", "Sapatênis", "Sandália Rasteira", "Bota Coturno"],
    "Acessórios": [
        "Boné Aba Reta",
        "Cinto de Couro",
        "Bolsa Transversal",
        "Mochila Casual",
    ],
}

CORES = ["Preto", "Branco", "Azul", "Vermelho", "Cinza", "Bege", "Verde", "Rosa"]


class Command(BaseCommand):
    help = "Popula o banco de dados com categorias "
    "e produtos de exemplo (e-commerce de roupas)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limpar",
            action="store_true",
            help="Apaga todas as categorias e produtos existentes antes de popular",
        )
        parser.add_argument(
            "--qtd-produtos",
            type=int,
            default=30,
            help="Quantidade de produtos a serem criados (padrão: 30)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["limpar"]:
            self.stdout.write("Apagando dados existentes...")
            Produto.objects.all().delete()
            Categoria.objects.all().delete()

        categorias_criadas = self._criar_categorias()
        self._criar_produtos(categorias_criadas, options["qtd_produtos"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Concluído: {Categoria.objects.count()} categorias e "
                f"{Produto.objects.count()} produtos no banco de dados."
            )
        )

    def _criar_categorias(self):
        self.stdout.write("Criando categorias...")
        categorias = []
        for dados in CATEGORIAS:
            categoria, criada = Categoria.objects.get_or_create(
                nome=dados["nome"],
                defaults={"descricao": dados["descricao"]},
            )
            categorias.append(categoria)
            status = "criada" if criada else "já existia"
            self.stdout.write(f"  - {categoria.nome} ({status})")
        return categorias

    def _criar_produtos(self, categorias, quantidade):
        self.stdout.write(f"Criando {quantidade} produtos...")

        produtos_a_criar = []
        for _ in range(quantidade):
            categoria = random.choice(categorias)
            nomes_possiveis = PRODUTOS_POR_CATEGORIA.get(categoria.nome, ["Produto"])
            nome_base = random.choice(nomes_possiveis)
            cor = random.choice(CORES)
            nome = f"{nome_base} {cor}"

            # max_digits=5, decimal_places=2 => valor máximo permitido é 999.99
            preco = Decimal(
                str(
                    fake.pydecimal(
                        left_digits=3,
                        right_digits=2,
                        positive=True,
                        min_value=19,
                        max_value=999,
                    )
                )
            )

            produto = Produto(
                nome=nome,
                descricao=fake.text(max_nb_chars=300),
                preco=preco,
                quantidade_estoque=random.randint(0, 200),
                categoria=categoria,
                imagem=fake.image_url(width=600, height=800),
            )
            produtos_a_criar.append(produto)

        Produto.objects.bulk_create(produtos_a_criar)
        self.stdout.write(f"  {len(produtos_a_criar)} produtos criados.")
