from django.core.paginator import InvalidPage
from rest_framework.pagination import PageNumberPagination
from rest_framework.utils.urls import replace_query_param
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'first': self.get_first_link(),
                'second_previous': self.get_second_previous_link(),
                'previous': self.get_previous_link(),
                'next': self.get_next_link(),
                'second_next': self.get_second_next_link(),
                'last': self.get_last_link(),
            },
            'total': self.page.paginator.count,
            'page_size': self.page_size,
            'current': self.page.number,
            'results': data

        })

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)
        try:
            self.next_page = paginator.page(int(page_number) + 1)
        except InvalidPage:
            self.next_page = None
        try:
            self.previous_page = paginator.page(int(page_number) - 1)
        except InvalidPage:
            self.previous_page = None
        return super(CustomPagination, self).paginate_queryset(queryset, request, view=None)

    def get_second_next_link(self):
        if not self.get_next_link() or not self.next_page.has_next():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.next_page.next_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_second_previous_link(self):
        if not self.get_previous_link() or not self.previous_page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        page_number = self.previous_page.previous_page_number()
        return replace_query_param(url, self.page_query_param, page_number)

    def get_first_link(self):
        if not self.page.has_previous():
            return None
        url = self.request.build_absolute_uri()
        return replace_query_param(url, self.page_query_param, 1)

    def get_last_link(self):
        if not self.page.has_next():
            return None
        url = self.request.build_absolute_uri()
        return replace_query_param(url, self.page_query_param, self.page.paginator.num_pages)
