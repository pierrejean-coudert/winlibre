from django.contrib import admin
from repository.winrepo.models import *

class ReplacesOperatorInline(admin.TabularInline):
    model = ReplacesOperator
    extra = 1

class ReplacesListAdmin(admin.ModelAdmin):
    inlines = (ReplacesOperatorInline,)

class Pre_dependsOperatorInline(admin.TabularInline):
    model = Pre_dependsOperator
    extra = 1

class Pre_dependsListAdmin(admin.ModelAdmin):
    inlines = (Pre_dependsOperatorInline,)

class DependsOperatorInline(admin.TabularInline):
    model = DependsOperator
    extra = 1

class DependsListAdmin(admin.ModelAdmin):
    inlines = (DependsOperatorInline,)

class ProvidesOperatorInline(admin.TabularInline):
    model = ProvidesOperator
    extra = 1

class ProvidesListAdmin(admin.ModelAdmin):
    inlines = (ProvidesOperatorInline,)

class RecommendsOperatorInline(admin.TabularInline):
    model = RecommendsOperator
    extra = 1

class RecommendsListAdmin(admin.ModelAdmin):
    inlines = (RecommendsOperatorInline,)

class SuggestsOperatorInline(admin.TabularInline):
    model = SuggestsOperator
    extra = 1

class SuggestsListAdmin(admin.ModelAdmin):
    inlines = (SuggestsOperatorInline,)

admin.site.register(Package)
admin.site.register(Section)
admin.site.register(Supported)
admin.site.register(Language)
admin.site.register(Url)
admin.site.register(ReplacesList, ReplacesListAdmin)
admin.site.register(Pre_dependsList, Pre_dependsListAdmin)
admin.site.register(DependsList, DependsListAdmin)
admin.site.register(ProvidesList, ProvidesListAdmin)
admin.site.register(RecommendsList, RecommendsListAdmin)
admin.site.register(SuggestsList, SuggestsListAdmin)
admin.site.register(ReplacesOperator)
admin.site.register(Pre_dependsOperator)
admin.site.register(DependsOperator)
admin.site.register(ProvidesOperator)
admin.site.register(RecommendsOperator)
admin.site.register(SuggestsOperator)

