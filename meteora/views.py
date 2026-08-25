from django.db.models.functions import Lower
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from meteora.models import Produto, Categoria
from meteora.serializers import ProdutoSerializer, CategoriaSerializer

# Create your views here.


class CaseInsensitiveOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        # If no ordering was specified, do not modify the queryset's ordering.
        # Previously the filter always called queryset.order_by(*ordering).
        # When no ordering was supplied, it cleared any ordering
        # and produced an unordered QuerySet.
        if not ordering:
            return queryset
        ordering = [
            Lower(f[1:]).desc() if f.startswith("-") else Lower(f) for f in ordering
        ]
        return queryset.order_by(*ordering)


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend, CaseInsensitiveOrderingFilter, SearchFilter]
    ordering_fields = ["nome"]
    search_fields = ["nome", "descricao"]


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, CaseInsensitiveOrderingFilter, SearchFilter]
    ordering_fields = ["nome", "criado_em", "atualizado_em"]
    search_fields = ["nome", "descricao"]
