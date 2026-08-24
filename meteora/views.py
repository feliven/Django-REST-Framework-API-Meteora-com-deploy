from rest_framework import viewsets
from meteora.models import Produto, Categoria
from meteora.serializers import ProdutoSerializer, CategoriaSerializer


# Create your views here.
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
