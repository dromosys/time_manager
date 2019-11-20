from rest_framework import permissions

# https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
 
class IsAccountAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS and request.user and request.user.is_staff):
            return True
        return False
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user_id == request.user