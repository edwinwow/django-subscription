from django import forms
from django.contrib import admin
from django.utils.html import conditional_escape as esc

from models import Subscription, UserSubscription, Transaction
from cartridge.shop.admin import ProductAdmin
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin

admin.site.register(Subscription, ProductAdmin)






class UserSubscriptionAdminForm(forms.ModelForm):
    class Meta:
        model = UserSubscription
    fix_group_membership = forms.fields.BooleanField(required=False)
    extend_subscription = forms.fields.BooleanField(required=False)


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'user', 'subscription', 'active', 'expires', 'valid')
    list_display_links = ('__unicode__',)
    list_filter = ('active', 'subscription', )
    date_hierarchy = 'expires'
    form = UserSubscriptionAdminForm
    fieldsets = (
        (None, {'fields': ('user', 'subscription', 'expires', 'active')}),
        ('Actions', {'fields': ('fix_group_membership', 'extend_subscription'),
                     'classes': ('collapse',)}),
        )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['extend_subscription']:
            obj.extend()
        if form.cleaned_data['fix_group_membership']:
            obj.fix()
        obj.save()

    # action for Django-SVN or django-batch-admin app
    actions = ('fix', 'extend',)

    def fix(self, request, queryset):
        for us in queryset.all():
            us.fix()
    fix.short_description = 'Fix group membership'

    def extend(self, request, queryset):
        for us in queryset.all():
            us.extend()
    extend.short_description = 'Extend subscription'

admin.site.register(UserSubscription, UserSubscriptionAdmin)


class TransactionAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('timestamp', 'id', 'event', 'subscription', 'user', 'ipn', 'amount', 'comment')
    list_display_links = ('timestamp', 'id')
    list_filter = ('subscription', 'user')
admin.site.register(Transaction, TransactionAdmin)
