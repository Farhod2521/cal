import pandas as pd
import re
from django.core.management.base import BaseCommand
from app_lightbulb.models import Room_Type_Category, Room_Type

class Command(BaseCommand):
    help = "Import data from xlsx file"

    def handle(self, *args, **kwargs):
        file_path = "/home/user/backend/cal/app_lightbulb/management/commands/x.xlsx"

        df = pd.read_excel(file_path, engine="openpyxl")
        df.columns = df.columns.str.strip()  # Ustun nomlaridan bo‘sh joylarni olib tashlash

        category_col = "category"
        subcategory_col = "Subcategory"
        room_col = "Room_Type_Category name"

        if category_col not in df.columns or room_col not in df.columns:
            raise ValueError("Excel faylida kerakli ustunlar topilmadi!")

        for index, row in df.iterrows():
            main_category_name = str(row.get(room_col, "")).strip()
            subcategory_name = str(row.get(category_col, "")).strip() if pd.notna(row.get(category_col)) else ""
            room_name = str(row.get(subcategory_col, "")).strip() if pd.notna(row.get(subcategory_col)) else ""

            if not main_category_name:
                continue  # Agar asosiy kategoriya bo'lmasa, bu qatordan o'tib ketamiz

            # Asosiy kategoriyani yoki mavjudini olish
            main_category, _ = Room_Type_Category.objects.get_or_create(name=main_category_name, parent=None)

            category = main_category
            if subcategory_name:
                # Agar subkategoriya mavjud bo‘lsa, uni asosiy kategoriyaga bog‘laymiz
                category, _ = Room_Type_Category.objects.get_or_create(name=subcategory_name, parent=main_category)

            if not room_name:
                continue  # Agar xona nomi bo‘lmasa, bu qatordan o‘tib ketamiz

            # Faqat raqamlarni olish uchun yordamchi funksiya
            def clean_number(value, default=0):
                if pd.notna(value):
                    num = re.sub(r"\D", "", str(value))  # Raqam bo'lmaganlarni olib tashlash
                    return int(num) if num else default
                return default

            lk = clean_number(row["lk"])
            ra = clean_number(row["ra"])
            k = clean_number(row["k"])
            table_height = float(row["table_height"]) if pd.notna(row["table_height"]) and str(row["table_height"]).strip() != "-" else 0
            color_tem = row["color_tem"] if pd.notna(row["color_tem"]) and str(row["color_tem"]).strip() != "-" else ""
            light_type = row["light_type"] if pd.notna(row["light_type"]) and str(row["light_type"]).strip() != "-" else ""
            recommended_lamps = row["recommended_lamps"] if pd.notna(row["recommended_lamps"]) else ""

            Room_Type.objects.create(
                category=category,
                lk=lk,
                ra=ra,
                k=k,
                table_height=table_height,
                color_tem=color_tem,
                light_type=light_type,
                recommended_lamps=recommended_lamps
            )

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
