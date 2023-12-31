from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)

from api import conf


class AddDelViewMixin:
    add_serializer = None

    def add_del_obj(self, obj_id, manager):
        assert self.add_serializer is not None, (
            f'{self.__class__.__name__} should include'
            'an `add_serializer` attribute.'
        )
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)

        managers = {
            conf.SUBSCRIBE_M2M: user.subscribe,
            conf.FAVORITE_M2M: user.favorites
        }

        manager = managers[manager]
        obj = get_object_or_404(self.queryset, id=obj_id)
        serializer = self.add_serializer(
            obj, context={'request': self.request}
        )
        obj_exist = manager.fitler(id=obj_id).exists()

        if (self.request.method in conf.ADD_METHODS) and not obj_exist:
            manager.add(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)
        if (self.request.method in conf.DEL_METHODS) and obj_exist:
            manager.remove(obj)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)