from django.contrib import admin
from django.db.models import Min, Max
from .models import UserPhoto


class PriceRangeFilter(admin.SimpleListFilter):
    title = 'price range'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        # Get all prices from the UserPhoto model
        min_price = UserPhoto.objects.aggregate(Min('price'))['price__min']
        max_price = UserPhoto.objects.aggregate(Max('price'))['price__max']

        # Define the price ranges
        ranges = [
            (0, 50),
            (50, 100),
            (100, 500),
            (500, 1000),
            (1000, max_price + 1)
        ]

        # Only include ranges that have a photo in them
        valid_ranges = [(str(start), f"{start}-{end}") for start, end in ranges if
                        start < max_price and end > min_price]

        return valid_ranges

    def queryset(self, request, queryset):
        if self.value():
            start, end = map(int, self.value().split('-'))
            return queryset.filter(price__gte=start, price__lt=end)
        return queryset


class UserPhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo_name', 'author', 'created_at', 'updated_at', 'price', 'quantity', 'category')
    list_filter = (PriceRangeFilter, 'category', 'subcategory', 'location_taken', 'created_at')
    search_fields = ('photo_name', 'description', 'category', 'subcategory', 'location_taken')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


admin.site.register(UserPhoto, UserPhotoAdmin)
