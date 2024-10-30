from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from tmom.exchange.models import Follow


@admin.register(Follow)
class FollowAdmin(SimpleHistoryAdmin):
  list_display = ('owner', 'following', 'approved', 'active', 'created')
  date_hierarchy = 'created'
  list_filter = ('approved', 'active')
  search_fields = ('owner__email', 'following__email')
  raw_id_fields = ('owner', 'following')
