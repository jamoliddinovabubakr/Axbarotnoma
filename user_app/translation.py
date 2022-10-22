from modeltranslation.translator import register, TranslationOptions
from user_app.models import Region, Gender, Role, State, Menu


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Gender)
class GenderTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Role)
class RoleTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(State)
class StateTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = ('name',)