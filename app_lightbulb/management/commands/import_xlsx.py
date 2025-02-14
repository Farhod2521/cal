import pandas as pd
from django.core.management.base import BaseCommand
from app_lightbulb.models import Room_Type_Category, Room_Type

class Command(BaseCommand):
    help = "Import data from xlsx file"

    def handle(self, *args, **kwargs):
        file_path = "/home/user/backend/cal/app_lightbulb/management/commands/x.xlsx"

        df = pd.read_excel(file_path, engine="openpyxl")
        df.columns = df.columns.str.strip()  # Ustun nomlaridan bo‘sh joylarni olib tashlash

        # Ustun nomlarini avtomatik aniqlash
        category_col = next((col for col in df.columns if "Category" in col), None)
        room_col = next((col for col in df.columns if "Room_Type" in col), None)

        if not category_col or not room_col:
            raise ValueError("Room_Type_Category name yoki Room_Type name ustuni topilmadi! Excel ustunlarini tekshiring.")

        category = None
        for index, row in df.iterrows():
            category_name = str(row.get(category_col, "")).strip() if pd.notna(row.get(category_col)) else ""
            room_name = str(row.get(room_col, "")).strip() if pd.notna(row.get(room_col)) else ""

            if category_name:
                category, _ = Room_Type_Category.objects.get_or_create(name=category_name)

            if not room_name:
                continue

            # Bo'sh yoki "-" bo'lgan qiymatlar uchun default qiymat
            lk = int(row["lk"]) if pd.notna(row["lk"]) and str(row["lk"]).strip() != "-" else 0
            ra = int(row["ra"]) if pd.notna(row["ra"]) and str(row["ra"]).strip() != "-" else 0
            k = int(row["k"]) if pd.notna(row["k"]) and str(row["k"]).strip() != "-" else 0
            table_height = float(row["table_height"]) if pd.notna(row["table_height"]) and str(row["table_height"]).strip() != "-" else 0
            color_tem = row["color_tem"] if pd.notna(row["color_tem"]) and str(row["color_tem"]).strip() != "-" else ""
            light_type = row["light_type"] if pd.notna(row["light_type"]) and str(row["light_type"]).strip() != "-" else ""

            # Ma'lumotlarni saqlash
            Room_Type.objects.create(
                category=category,
                name=room_name,
                lk=lk,
                ra=ra,
                k=k,
                table_height=table_height,
                color_tem=color_tem,
                light_type=light_type
            )

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
