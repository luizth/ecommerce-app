from rest_framework import permissions

from .serializers import UserSerializer


class ViewPermissions(permissions.BasePermission):

    def has_permissions(self, req, view):
        data = UserSerializer(req.data).data

        view_access = any(p['name'] == 'view_' + view.permissions_object for p in data['role']['permissions'])
        edit_access = any(p['name'] == 'edit_' + view.permissions_object for p in data['role']['permissions'])

        if req.method == 'GET':
            return view_access or edit_access

        return edit_access
