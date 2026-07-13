from django.core.cache import cache
from rest_framework.response import Response

class CacheMixin:
    def list(self, request, *args, **kwargs):
        # 1. So'rov parametrlarini olamiz (search, ordering, filters)
        # Bu bilan har bir filtr uchun alohida kesh kaliti yaratiladi
        query_params = request.query_params.urlencode()
        
        # 2. Kalit: class nomi + user ID + query params
        key = f"{self.__class__.__name__}-list-{request.user.id}-{query_params}"
        
        data = cache.get(key)
        if not data:
            response = super().list(request, *args, **kwargs)
            data = response.data
            cache.set(key, data, 60*15)
            return response
            
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        # Detail (retrieve) uchun ham xuddi shunday
        lookup_val = kwargs.get(self.lookup_field or 'pk')
        key = f"{self.__class__.__name__}-detail-{request.user.id}-{lookup_val}"
        
        data = cache.get(key)
        if not data:
            response = super().retrieve(request, *args, **kwargs)
            data = response.data
            cache.set(key, data, 60*15)
            return response
        return Response(data)