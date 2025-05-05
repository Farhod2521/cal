import os
import django
from django.core.files import File

# Django sozlamalarini yuklash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app_lightbulb.models import LEDPanel

# Rasm papkasi (loyiha asosidan nisbiy yo‘l)
IMAGE_DIR = os.path.join('led_image')  # yoki to‘liq yo‘l yozing, masalan: '/home/user/project/led_image'

# Barcha LEDPanel obyektlaridan o'tamiz
for panel in LEDPanel.objects.all():
    # Rasm nomini yasaymiz: "name.png"
    image_name = f"{panel.name}.png"
    image_path = os.path.join(IMAGE_DIR, image_name)

    # Fayl mavjudligini tekshiramiz
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            panel.image.save(image_name, File(img_file), save=True)
        print(f"{panel.name} uchun rasm yuklandi.")
    else:
        print(f"{panel.name} uchun rasm topilmadi.")
