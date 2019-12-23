"""brogress_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from api_crawler.models import Apidata
from rest_framework import routers, serializers, viewsets
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50

class DataSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Apidata
        fields = ['id','sex', 'height', 'start_weight', 'end_weight',
        'total_time', 'age', 'image_sources', 'post_id']

class DataViewSet(viewsets.ModelViewSet):
    serializer_class = DataSerializers
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Apidata.objects.all()

        sex = self.request.query_params.get('sex', None)
        if sex is not None:
            queryset = queryset.filter(sex=str(sex))

        start_weight = self.request.query_params.get('startweight', None)
        if start_weight is not None:
            queryset = queryset.filter(start_weight = str(start_weight))

        end_weight = self.request.query_params.get('endweight', None)
        if end_weight is not None:
            queryset = queryset.filter(end_weight = str(end_weight))

        age = self.request.query_params.get('age', None)
        if age is not None:
            queryset = queryset.filter(age = str(age))

        height = self.request.query_params.get('height', None)
        if height is not None:
            queryset = queryset.filter(height = str(height))

        return queryset


router = routers.DefaultRouter()
router.register('api', DataViewSet, basename='api',)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    
]
