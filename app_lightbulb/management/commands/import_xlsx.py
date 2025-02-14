import pandas as pd
from django.core.management.base import BaseCommand
from app_lightbulb.models import Room_Type_Category, Room_Type  # Modelingizning aniq joylashuvini tekshiring

class Command(BaseCommand):
    help = "Import data from xlsx file"

    def handle(self, *args, **kwargs):
        file_path = "x.xlsx"  # Faylning to'liq joylashuvi

        df = pd.read_excel(file_path, engine="openpyxl")

        category = None  # Hozirgi kategoriya
        for index, row in df.iterrows():
            # Agar `Room_Type_Category name` to'ldirilgan bo'lsa, yangi kategoriya yaratamiz
            if pd.notna(row["Room_Type_Category name"]):
                category, _ = Room_Type_Category.objects.get_or_create(name=row["Room_Type_Category name"])

            # Agar `Room_Type name` bo'sh bo'lsa, uni o'tkazib yuboramiz
            if pd.isna(row["Room_Type name"]):
                continue

            # Bo'sh kataklarga 0 qiymatini berish
            lk = int(row["lk"]) if pd.notna(row["lk"]) else 0
            ra = int(row["ra"]) if pd.notna(row["ra"]) else 0
            k = int(row["k"]) if pd.notna(row["k"]) else 0
            table_height = float(row["table_height"]) if pd.notna(row["table_height"]) else 0
            color_tem = row["color_tem"] if pd.notna(row["color_tem"]) else ""
            light_type = row["light_type"] if pd.notna(row["light_type"]) else ""

            # Room_Type obyektini yaratish
            Room_Type.objects.create(
                category=category,
                name=row["Room_Type name"],
                lk=lk,
                ra=ra,
                k=k,
                table_height=table_height,
                color_tem=color_tem,
                light_type=light_type
            )

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
