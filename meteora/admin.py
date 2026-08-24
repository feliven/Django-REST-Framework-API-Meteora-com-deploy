from django.contrib import admin
from meteora.models import Produto, Categoria


# Register your models here.
class ListandoProdutos(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "preco",
        "quantidade_estoque",
        "categoria",
        "atualizado_em",
    )
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_editable = ("categoria",)
    list_per_page = 10


class ListandoCategorias(admin.ModelAdmin):
    list_display = ("id", "nome", "atualizado_em")
    list_display_links = ("id", "nome")
    search_fields = ("nome",)
    list_per_page = 10


admin.site.register(Produto, ListandoProdutos)
admin.site.register(Categoria, ListandoCategorias)
