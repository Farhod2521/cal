import json
import os
import django

# Django loyihangizning nomi (settings.py joylashgan papka)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app_lightbulb.models  import LEDPanel

def load_json_data():
    with open('lampo.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            LEDPanel.objects.create(
                name=item.get("name", ""),
                power=item.get("power", 0),
                color_temperature=item.get("color_temperature", ""),
                voltage=item.get("voltage", ""),
                current=item.get("current", ""),
                protection_rating=None if item.get("protection_rating") == "-" else item.get("protection_rating"),
                frequency=item.get("frequency", ""),
                luminous_flux_min=item.get("luminous_flux_min", 0),
                luminous_flux=item.get("luminous_flux", ""),
                efficiency=item.get("efficiency", ""),
                color_rendering_index=None if item.get("color_rendering_index") == "-" else item.get("color_rendering_index"),
                dimensions=item.get("dimensions", ""),
                mounting_size=None if item.get("mounting_size") == "-" else item.get("mounting_size"),
                beam_angle=None if item.get("beam_angle") == "-" else item.get("beam_angle"),
            )
        print("Barcha ma'lumotlar saqlandi.")

if __name__ == '__main__':
    load_json_data()
