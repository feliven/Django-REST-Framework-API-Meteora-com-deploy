from django.db import models
from django.core.validators import MinValueValidator, URLValidator

# Create your models here.

# nome: Nome da categoria. Campo obrigatório, com no máximo 100 caracteres.
# descricao: Descrição breve da categoria. Campo opcional, com no máximo 500 caracteres.
# criado_em: Data e hora de criação da categoria.
#       Campos automáticos gerados pelo sistema.
# atualizado_em: Data e hora da última atualização da categoria.
#       Campos automáticos gerados pelo sistema.


class Categoria(models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True,
    )
    descricao = models.TextField(
        max_length=500, blank=True, null=True, verbose_name="Descrição"
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    atualizado_em = models.DateTimeField(
        auto_now=True, verbose_name="Data de atualização"
    )

    def __str__(self) -> str:
        return self.nome


# nome: Nome do produto. Campo obrigatório, com no máximo 255 caracteres.
# descricao: Descrição detalhada do produto.
#       Campo opcional, com no máximo 1000 caracteres.
# preco: Preço do produto. Campo obrigatório, deve ser um número decimal positivo.
# quantidade_estoque: Quantidade disponível em estoque.
#       Campo obrigatório, deve ser um número inteiro positivo.
# categoria: Chave estrangeira para o modelo Categoria.
#       Campo obrigatório, deve ser uma categoria existente no sistema.
# imagem: Campo opcional para armazenar a URL da imagem do produto.
#       Campo opcional, deve ser uma URL válida para uma imagem.
# criado_em: Data e hora de criação do produto. Campos automáticos gerados pelo sistema.
# atualizado_em: Data e hora da última atualização do produto.
#       Campos automáticos gerados pelo sistema.


class Produto(models.Model):
    nome = models.CharField(
        max_length=255,
    )
    descricao = models.TextField(
        max_length=1000, blank=True, null=True, verbose_name="Descrição"
    )
    preco = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Preço",
    )
    quantidade_estoque = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name="Quantidade no estoque"
    )
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagem = models.CharField(blank=True, null=True, validators=[URLValidator()])
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de criação")
    atualizado_em = models.DateTimeField(
        auto_now=True, verbose_name="Data de atualização"
    )

    def __str__(self) -> str:
        return self.nome
