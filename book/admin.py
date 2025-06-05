from django.contrib import admin
from book.models import *

admin.site.register(Category)
admin.site.register(Kitob)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Cart)
admin.site.register(CartItem)
