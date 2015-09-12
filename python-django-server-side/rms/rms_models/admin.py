from django.contrib import admin
from rms.rms_models.models import Users,FoodItem,BasicFoodItem,FoodContent,UserRatings,Deficiency,BasicFoodQuality,Allergic,Quality,Restaurant,Transaction
from rms.GameOfDenomination.models import Game,GameRecord
# Register your models here.

admin.site.register(Users)
admin.site.register(FoodItem)
admin.site.register(BasicFoodItem)
admin.site.register(FoodContent)
admin.site.register(Quality)
admin.site.register(Restaurant)
admin.site.register(BasicFoodQuality)
admin.site.register(Game)
admin.site.register(GameRecord)
admin.site.register(Transaction)
admin.site.register(Allergic)
admin.site.register(Deficiency)
admin.site.register(UserRatings)