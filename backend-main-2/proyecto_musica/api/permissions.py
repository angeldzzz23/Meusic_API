from rest_framework import permissions

# making custom permissions
class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit own profile  """

    # returns true or a false if we want to allow the user to edit
    # gets called when we try to update a user
    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            print("also here")
            return True
            # returns true if the user is trying to update their own profile
            print("here", obj.id == request.user.id)
        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """ Allow users to update their own status"""

    def has_object_permission(self, request, view, objc):
        """ Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        # if the user is trying to put or patch
        # returns true if they have the same user_profile_id
        return obj.user_profile.id == request.user.id
