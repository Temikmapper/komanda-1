from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response 

from expenses.models import UsualExpenses, Categories
from api.serializers import UsualExpensesSerializer, CategoriesSerializer

class UsualExpensesViewSet(viewsets.ModelViewSet):
    queryset = UsualExpenses.objects.all()
    serializer_class = UsualExpensesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Создание объектов, если на вход подан список
        """
        data = request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
                serializer.data,
                headers=headers
        )

class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Создание объектов, если на вход подан список
        """
        data = request.data
        many = isinstance(data, list)
        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
                serializer.data,
                headers=headers
        )