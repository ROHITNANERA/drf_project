from rest_framework.pagination import CursorPagination,PageNumberPagination
from rest_framework.response import Response

class MyPagination(CursorPagination):
    page_size=2
    page_size_query_param = 'page_size'
    ordering='id'
    max_page_size=10
#page_query_param is used to define a pagenumber parameters name to be accepted.
    page_query_param='page'
#page_size_query_param is used to define a page_size parameter name to be accepted.
    page_size_query_param = 'size'
#last_page_strings is used to define the keyword which is used as a query parameter to get the last page.
    last_page_strings = 'last'
    

class MyCustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })