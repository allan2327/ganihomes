# -*- coding: utf-8 -*-
from tinymce.widgets import TinyMCE

__author__ = 'Evren Esat Ozkan'
from django.contrib import admin
from utils.admin import admin_register
from website.models import *
#from mptt.admin import MPTTModelAdmin as mpttadmin

class IcerikInline(admin.StackedInline):
    model = Icerik
    #    formfield_overrides = {
    #        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 20}, )},
    #    }
    save_on_top = True
    save_as = True
    prepopulated_fields = {"slug": ("baslik",)}
    extra = 1

#class MedyaInline(admin.StackedInline):
#    model = Sayfa.medya.through

class SayfaAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'pul', 'menude', 'etkin')
    mptt_indent_field = "baslik"
    #    search_fields = ['', ]
    list_filter = ['menude', 'etkin']
    save_on_top = True
    filter_horizontal = ['medya']
    #    exclude = ('medya',)
    #raw_id_fields=('', )
    #readonly_fields=['',]
    #    save_as=True
    #ordering = ['',]
    #description=''
    actions = ['yer_degistir']
    #list_per_page=20
    #prepopulated_fields = {"slug": ("title",)}
    inlines = [IcerikInline, ]
    #list_display_links = ('','')
    date_hierarchy = 'pul'
    #list_select_related=False
    list_editable = ('menude', 'etkin')
    save_as = True

    #def save_model(self, request, obj, form, change):
    #    obj.save()

    #class FooInline(admin.TabularInline):
    #    model = Foo

    def yer_degistir(self, request, queryset):
        queryset[1].move_to(queryset[0], 'left')
        self.message_user(request, "İşlem başarılı.")

    yer_degistir.short_description = u'İşaretli **2** kaydın yerlerini değiştir.'


class MedyaAdmin(admin.ModelAdmin):
    readonly_fields = ('tip',)

#
#class DilAdmin(admin.ModelAdmin):
#    list_display = ('adi', 'kodu')
#    #    search_fields = ['', ]
#    #    list_filter = ['', ]
#    save_on_top = True


class CeviriInline(admin.TabularInline):
    model = Ceviriler
    extra = 1


class KelimeAdmin(admin.ModelAdmin):
    list_display = ('kelime', 'durum')
    #    search_fields = ['', ]
    #    list_filter = ['', ]
    readonly_fields = ['durum']
    save_on_top = True
    inlines = [CeviriInline, ]


class HaberAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'pul', 'dil_kodu', 'etkin', 'sabit')
    search_fields = ['baslik', 'icerik']
    list_filter = ['dil_kodu', 'etkin', 'etkin']
    list_editable = ['etkin', 'sabit']
    prepopulated_fields = {"slug": ("baslik",)}
    save_on_top = True
    filter_horizontal = ['medya']
    save_as = True

class VitrinAdmin(admin.ModelAdmin):
    list_display = ( 'pul', 'gorsel', 'dil_kodu', 'active', 'sira','tops','type')
    search_fields = ['baslik', 'icerik']
    list_filter = ['dil_kodu', 'active', 'type']
    list_editable = ['active', 'sira','tops']
    raw_id_fields = ['place_photo']
    save_on_top = True
    save_as = True


#admin.site.register(Sayfa, mpttadmin)
admin_register(admin, namespace=globals())
