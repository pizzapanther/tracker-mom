from django.contrib import admin

from tmom.exchange.models import Follow, FollowRequest, LocationShare


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
  list_display = ("owner", "following", "active", "created")
  date_hierarchy = "created"
  list_filter = ("active",)
  search_fields = ("owner__email", "following__email")
  raw_id_fields = ("owner", "following")


@admin.register(FollowRequest)
class FollowRequestAdmin(admin.ModelAdmin):
  list_display = ("owner", "used_by", "used_on", "created")
  date_hierarchy = "created"
  search_fields = ("owner__email", "following__email")
  raw_id_fields = ("owner", "used_by")


@admin.register(LocationShare)
class ShareAdmin(admin.ModelAdmin):
  list_display = ("follow", "created")
  date_hierarchy = "created"
  list_filter = ("created",)
  search_fields = ("follow__email",)
  raw_id_fields = ("follow",)
