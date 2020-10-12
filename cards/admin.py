from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.db.models import ImageField
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import (Card, CardArt, CardEffect, CardKeyword, DivivolveCost,
                     ReleaseSet)


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []

        if value and getattr(value, 'url', None):
            output.append(f'<img src="{value.url}" width="240" height="336" style="object-fit: cover;" />')

        output.append(
            super(AdminImageWidget, self).render(
                name,
                value,
                attrs,
                renderer
            )
        )
        return mark_safe(u''.join(output))

class CardEffectInline(admin.StackedInline):
    model = CardEffect
    extra = 0

class CardArtInLine(admin.StackedInline):
    verbose_name = 'Card Art'
    verbose_name_plural = 'Card Art'
    model = CardArt
    extra = 0
    fields = ('artist', 'card_art', 'release_set')
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget}
    }

class DivivolveCostInLine(admin.TabularInline):
    model = DivivolveCost
    extra = 0

@admin.register(ReleaseSet)
class ReleaseSetAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'release_date', 'card_types')
    formfield_overrides = {
        ImageField: {'widget': AdminImageWidget}
    }

@admin.register(CardKeyword)
class CardKeyword(admin.ModelAdmin):
    list_display = ('name', 'reminder_text')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'card_type', 'release_set', 'rarity')
    list_filter = ('color', 'release_set', 'rarity', 'card_type', 'flavor_type', 'flavor_attribute')
    fieldsets = [
        ('Card ID',         {'fields': ['number', 'release_set', 'rarity', 'card_of_the_day']}),
        ('Details',         {'fields': ['name', 'card_type']}),
        ('Play',            {'fields': ['color', 'play_cost', 'level', 'stage', 'digimon_power']}),
        ('Flavor',          {'fields': ['flavor_type', 'flavor_attribute']}),
        ('Discussion',      {'fields': ['content']}),
    ]
    inlines = [DivivolveCostInLine, CardArtInLine, CardEffectInline]
