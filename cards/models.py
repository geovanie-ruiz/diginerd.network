from django.db import models
from django.db.models import Q
from django_enumfield import enum
from network.models import Article, ArticleType

MAX_LEVEL = 7


class CardType(enum.Enum):
    DIGITAMA = 0
    DIGIMON = 1
    OPTION = 2
    TAMER = 3

    __labels__ = {
        DIGITAMA: 'Digitama',
        DIGIMON: 'Digimon',
        OPTION: 'Option',
        TAMER: 'Tamer'
    }


class EffectType(enum.Enum):
    MAIN = 0
    SOURCE = 1
    SECURITY = 2

    __labels__ = {
        MAIN: 'Main Effect',
        SOURCE: 'Source Effect',
        SECURITY: 'Security Effect'
    }


class CardColor(enum.Enum):
    RED = 0
    YELLOW = 1
    BLUE = 2
    GREEN = 3
    BLACK = 4
    PURPLE = 5
    WHITE = 6

    __labels__ = {
        RED: 'Red',
        YELLOW: 'Yellow',
        BLUE: 'Blue',
        GREEN: 'Green',
        BLACK: 'Black',
        PURPLE: 'Purple',
        WHITE: 'White'
    }


class DigimonStage(enum.Enum):
    NONE = 0
    IN_TRAINING = 1
    ROOKIE = 2
    CHAMPION = 3
    ULIMATE = 4
    MEGA = 5

    __labels__ = {
        NONE: 'None',
        IN_TRAINING: 'In Training',
        ROOKIE: 'Rookie',
        CHAMPION: 'Champion',
        ULIMATE: 'Ultimate',
        MEGA: 'Mega'
    }


class CardRarity(enum.Enum):
    COMMON = 0
    UNCOMMON = 1
    RARE = 2
    SUPER_RARE = 3
    SECRET_RARE = 4
    PROMO = 5

    __labels__ = {
        COMMON: 'Common',
        UNCOMMON: 'Uncommon',
        RARE: 'Rare',
        SUPER_RARE: 'Super Rare',
        SECRET_RARE: 'Secret Rare',
        PROMO: 'Promo'
    }


class ReleaseSet(models.Model):
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    card_types = models.IntegerField(default=0)
    set_art = models.ImageField(upload_to='art/set/', default='art/no-img.png')

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return f'{self.code}: {self.name}'


class CardKeyword(models.Model):
    name = models.CharField(max_length=64)
    reminder_text = models.TextField()

    def __str__(self):
        return f'{self.name}'


class Card(Article):
    number = models.CharField(max_length=16)
    release_set = models.ForeignKey(
        ReleaseSet, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    card_type = enum.EnumField(CardType)
    color = enum.EnumField(CardColor)
    play_cost = models.IntegerField(default=0)
    level = models.IntegerField(null=True, blank=True)
    stage = enum.EnumField(DigimonStage, default=DigimonStage.NONE)
    digimon_power = models.IntegerField(null=True, blank=True)
    flavor_type = models.CharField(max_length=255, null=True, blank=True)
    flavor_attribute = models.CharField(max_length=255, null=True, blank=True)
    rarity = enum.EnumField(CardRarity)
    card_of_the_day = models.DateField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f'{self.number}: {self.name}'

    def save(self, *args, **kwargs):
        self.title = str(self)
        self.article_type = ArticleType.CARD
        super().save(*args, **kwargs)


class DigivolveCost(models.Model):
    color = enum.EnumField(CardColor)
    cost = models.IntegerField(default=0)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='evo')


class CardArt(models.Model):
    artist = models.CharField(max_length=255)
    card_art = models.ImageField(
        upload_to='art/card/', default='art/no-img.png')
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='art')
    release_set = models.ForeignKey(
        ReleaseSet, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f' {self.release_set}: {self.card} by {self.artist}'


class CardEffect(models.Model):
    effect_type = enum.EnumField(EffectType)
    effect_text = models.TextField(null=True, blank=True)
    card_keyword = models.ForeignKey(
        CardKeyword, on_delete=models.PROTECT, null=True, blank=True, related_name='keyword')
    card = models.ForeignKey(
        Card, on_delete=models.CASCADE, related_name='effect')

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(effect_text__isnull=False) | Q(
                    card_keyword__isnull=False),
                name='effect_or_keyword_needed'
            )
        ]

    def __str__(self):
        return f' {self.card} {EffectType.get_label(self.effect_type)}'
