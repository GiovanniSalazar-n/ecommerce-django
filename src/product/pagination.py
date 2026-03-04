from rest_framework.pagination import PageNumberPagination


class ProductPageNumberPagination(PageNumberPagination):
    page_size = 2               
    page_query_param = "pagina" 
    page_size_query_param = "numero"
    max_page_size = 10