from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the author of a post to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author of the post
        return obj.author == request.user
