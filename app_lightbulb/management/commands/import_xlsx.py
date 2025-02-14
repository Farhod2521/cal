import pandas as pd
from django.core.management.base import BaseCommand
from app_lightbulb.models import Room_Type_Category, Room_Type

class Command(BaseCommand):
    help = 'Import room types and categories from an Excel file'

    def handle(self, *args, **kwargs):
        # File path
        file_path = "/home/user/backend/cal/app_lightbulb/management/commands/x.xlsx"

        # Read the Excel file
        data = pd.read_excel(file_path)

        # Strip all column names to remove any extra spaces
        data.columns = data.columns.str.strip()

        # Function to safely convert values to integers
        def safe_int(value):
            """Convert value to integer, handling '-' and invalid formats."""
            if pd.isna(value) or value == "-" or str(value).strip() == "":
                return 0
            try:
                # Remove any extra symbols like '*'
                value = str(value).replace("*", "").strip()
                return int(value)
            except ValueError:
                return 0

        # Function to safely handle string values
        def safe_str(value):
            return str(value).strip() if pd.notna(value) else ""

        # Iterate through each row in the Excel file
        for index, row in data.iterrows():
            # Handle Room_Type_Category (parent)
            root_category_name = safe_str(row.get('Room_Type_Category  name'))
            if not root_category_name:
                print(f"Error processing row {index + 1}: Missing Room_Type_Category name")
                continue

            root_category, _ = Room_Type_Category.objects.get_or_create(name=root_category_name, parent=None)

            # Handle category (child of the root category)
            category_name = safe_str(row.get('category'))
            category = root_category
            if category_name:
                category, _ = Room_Type_Category.objects.get_or_create(name=category_name, parent=root_category)

            # Safely handle all fields
            table_height = (
                float(row["table_height"]) if pd.notna(row["table_height"]) and str(row["table_height"]).strip() != "-"
                else 0
            )
            color_tem = safe_str(row.get("color_tem"))
            light_type = safe_str(row.get("light_type"))
            recommended_lamps = safe_str(row.get("recommended_lamps"))

            # Create Room_Type instance
            try:
                Room_Type.objects.create(
                    category=category,
                    lk=safe_int(row.get('lk')),
                    ra=safe_int(row.get('ra')),
                    k=safe_int(row.get('k')),
                    table_height=table_height,
                    color_tem=color_tem,
                    light_type=light_type,
                    recommended_lamps=recommended_lamps
                )
            except Exception as e:
                print(f"Error processing row {index + 1}: {e}")

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
