from rest_framework import generics, mixins, views
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.response import Response


class ProductView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        user = request.user
        query = Product.objects.all()
        serializers = ProductSerializers(query, many=True)
        data = []
        for prod in serializers.data:
            fab_query = Favorit.objects.filter(
                user=user).filter(product_id=prod["id"])
            if fab_query:
                prod['favorit'] = fab_query[0].isFavorit
            else:
                prod['favorit'] = False
            data.append(prod)
        return Response(data)


class FavoritView(views.APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        data = request.data["id"]
        user = request.user
        single_product = Favorit.objects.filter(user=user).filter(id=data)
        if single_product:
            fab = single_product[0].isFavorit
            prod = Favorit.objects.get(id=single_product[0].id)
            prod.isFavorit = not fab
            prod.save()
        else:
            Favorit.objects.create(product_id=data, user=user, isFavorit=True)
        return Response({"message": "response is Get Successfully"})


class UserView(views.APIView):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]

    def get(self, request):
        user = request.user
        user_obj = User.objects.get(username=user.username)
        serializer = UserSerializers(user_obj)
        return Response(serializer.data)


class Register(views.APIView):
    def post(self, request):
        serializers = UserSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"error": False, "message": "User was Created!"})
        return Response({"error": True, "message": "User Not Created!"})