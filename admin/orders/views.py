import csv

from django.db import connection
from django.http import HttpResponse
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from admin.pagination import CustomPagination
from rest_framework.views import APIView
from users.authentication import JWTAuthentication
from .models import OrderItem, Order
from .serializers import OrderSerializer


class OrderGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get(self, req, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(req, pk).data
            })

        return self.list(req)


class ExportAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, req):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders.csv'

        orders = Order.objects.all()
        writer = csv.writer(response)

        writer.writerow(['ID', 'Name', 'Email', 'Product Title', 'Price', 'Quantity'])

        for order in orders:
            writer.writerow([order.id, order.name, order.email, '', '', ''])

            order_items = OrderItem.objects.all().filter(order_id=order.id)
            for item in order_items:
                writer.writerow(['', '', '', item.product_title, item.price, item.quantity])

        return response


class ChartAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    DATE_FORMAT(o.created_at, '%Y-%m-%d') as date, 
                    sum(i.quantity * i.price) as sum
                FROM orders_order as o
                JOIN orders_orderitem as i ON o.id = i.order_id
                GROUP BY date
            """)

            result = cursor.fetchall()

        data = [{
            'date': row[0],
            'sum': row[1]
        } for row in result]

        return Response({
            'data': data
        })
