from basis.managers import PersistentModelManager
from django.db.models import Q


class DirectoryManager(PersistentModelManager):

    def permitted(self, user):
        if user.is_superuser:
            return self
        query = Q(id=-1)
        query |= Q(users_with_access=user)
        for group in user.groups.all():
            query |= Q(groups_with_access=group)
        return self.filter(query).distinct()


class FileManager(PersistentModelManager):

    def permitted(self, user):
        if user.is_superuser:
            return self
        query = Q(id=-1)
        query |= Q(parent_folder__users_with_access=user)
        for group in user.groups.all():
            query |= Q(parent_folder__groups_with_access=group)
        return self.filter(query).distinct()
