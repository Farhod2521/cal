import pandas as pd
import re
from django.core.management.base import BaseCommand
from app_lightbulb.models import Room_Type_Category, Room_Type

class Command(BaseCommand):
    help = "Import data from xlsx file"

    def handle(self, *args, **kwargs):
        file_path = "/home/user/backend/cal/app_lightbulb/management/commands/x.xlsx"
        df = pd.read_excel(file_path, engine="openpyxl")
        df.columns = df.columns.str.replace(r"\s+", " ", regex=True).str.strip()

        print("Excel faylidagi ustunlar:", df.columns)  # Excel ustunlarini tekshirish uchun

        category_col = next((col for col in df.columns if "category" in col.lower()), None)
        room_col = next((col for col in df.columns if "room_type_category" in col.lower()), None)

        if not category_col or not room_col:
            raise ValueError(f"Excel faylida kerakli ustunlar topilmadi! Ustunlar: {df.columns}")

        for _, row in df.iterrows():
            main_category_name = str(row.get(room_col, "")).strip()
            subcategory_name = str(row.get(category_col, "")).strip() if pd.notna(row.get(category_col)) else ""
            room_name = str(row.get("Subcategory", "")).strip() if pd.notna(row.get("Subcategory")) else ""

            if not main_category_name:
                continue  # Kategoriya yo‘q bo‘lsa, o‘tkazib yuboramiz

            # Asosiy kategoriya mavjudligini tekshiramiz
            main_category, created = Room_Type_Category.objects.get_or_create(name=main_category_name, parent=None)

            category = main_category
            if subcategory_name:
                category, created = Room_Type_Category.objects.get_or_create(name=subcategory_name, parent=main_category)

            if not room_name:
                continue  # Subkategoriya yo‘q bo‘lsa, o'tkazib yuboramiz

            def clean_number(value, default=0):
                if pd.notna(value):
                    num = re.sub(r"\D", "", str(value))  # Faqat raqamlarni olish
                    return int(num) if num else default
                return default

            lk = clean_number(row["lk"])
            ra = clean_number(row["ra"])
            k = clean_number(row["k"])
            table_height = float(row["table_height"]) if pd.notna(row["table_height"]) and str(row["table_height"]).strip() != "-" else 0
            color_tem = row["color_tem"] if pd.notna(row["color_tem"]) and str(row["color_tem"]).strip() != "-" else ""
            light_type = row["light_type"] if pd.notna(row["light_type"]) and str(row["light_type"]).strip() != "-" else ""
            recommended_lamps = row["recommended_lamps"] if pd.notna(row["recommended_lamps"]) else ""

            # Mavjud Room_Type bor yoki yo‘qligini tekshiramiz
            if not Room_Type.objects.filter(
                category=category, lk=lk, ra=ra, k=k, table_height=table_height, color_tem=color_tem,
                light_type=light_type, recommended_lamps=recommended_lamps
            ).exists():
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
