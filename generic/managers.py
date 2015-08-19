from django.db.models import Manager, Q
from django.utils.timezone import now

class DisplayableManager(Manager):
    """
    Provides filter for restricting items returned by status and
    publish date when the given user is not a staff member.
    """

    def active(self, for_user=None):
        """
        For non-staff users, return items with a published status and
        whose publish and expiry dates fall before and after the
        current date when specified.
        """
        from models import Displayable
        if for_user is not None:
            self.filter(user = for_user)
        return self.filter(
            Q(publish_date__lte=now()),
            Q(expiry_date__gte=now()),
            Q(status=Displayable.CONTENT_STATUS_ACTIVE))
            # Q(status=2))