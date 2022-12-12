from banksampah.views import create_bank, show_bank, delete_bank, show_banksampah_json, flutter_createbank, show_bank_flutter, show_banksampah_json_flutter, delete_bankflutter
from django.urls import path

app_name = 'banksampah'

urlpatterns = [
    path('', create_bank, name='create'),
    path('contents/', show_bank, name='show'),
    path('delete/<int:id>/', delete_bank, name='delete'),
    path('json/', show_banksampah_json, name='show_json'),
    path('createbank_flutter/', flutter_createbank, name='createbankflutter'),
    path('contents_flutter/', show_bank_flutter, name='show_flutter'),
    path('json_flutter/', show_banksampah_json_flutter, name='show_json_flutter'),
    path('delete_flutter/<int:id>/', delete_bankflutter, name='delete_flutter'),
]