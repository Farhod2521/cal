import pandas as pd
from django.core.management.base import BaseCommand
from app_lightbulb.models import Room_Type_Category, Room_Type

class Command(BaseCommand):
    help = 'Import room types and categories from an Excel file'

    def handle(self, *args, **kwargs):
        # File path
        #file_path = r"D:\FASTAPI\cal\app_lightbulb\management\commands\x.xlsx"
        file_path = "/home/user/backend/cal/app_lightbulb/management/commands/x.xlsx"
        # Read the Excel file
        data = pd.read_excel(file_path)

        # Strip all column names to remove any extra spaces
        data.columns = data.columns.str.strip()

        # Function to safely convert values to integers
        def safe_int(value):
            """Convert value to integer, handling '-' and invalid formats, including floats."""
            if pd.isna(value) or value == "-" or str(value).strip() == "":
                return 0
            try:
                # Convert to float first to handle values like '80.0', then cast to int
                value = float(str(value).replace("*", "").strip())
                return int(value)
            except ValueError:
                print(f"Warning: Could not convert '{value}' to integer")
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
            razreyd = safe_str(row.get("razreyd"))
            ugr = safe_str(row.get("ugr"))
            recommended_lamps = safe_str(row.get("recommended_lamps"))

            # Debugging: Print the row details
            print(f"Processing row {index + 1}:")
            print(f"lk={safe_int(row.get('lk'))}, ra={safe_int(row.get('ra'))}, k={safe_int(row.get('k'))}, table_height={table_height}")

            # Create Room_Type instance
            try:
                Room_Type.objects.create(
                    category=category,
                    lk=safe_int(row.get('lk')),
                    ra=safe_int(row.get('ra')),
                    k=safe_int(row.get('k')),
                    table_height=table_height,
                    razreyd=razreyd,
                    ugr=ugr,
                    recommended_lamps=recommended_lamps
                )
            except Exception as e:
                print(f"Error processing row {index + 1}: {e}")

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
