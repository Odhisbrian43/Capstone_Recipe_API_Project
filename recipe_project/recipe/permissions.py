from rest_framework import permissions

#Custom permission to only allow owner of a recipe to edit and delete options.
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        #Allow read permissions for request GET, READ or OPRIONS.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user
