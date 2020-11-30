from rest_framework import permissions

class IsLiker (permissions.BasePermission) :

    def has_object_permission (self, request, view, obj) :
        return obj.liked_people == request.user

class IsOwner (permissions.BasePermission) :

    def has_object_permission (self, request, view, obj) :
        return obj.owner == request.user

class IsOwnerOrReadOnly (permissions.BasePermission) :
    SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

    def has_object_permission (self, request, view, obj) :
        if request.method in self.SAFE_METHODS or obj.owner == request.user :
            return True
        return False