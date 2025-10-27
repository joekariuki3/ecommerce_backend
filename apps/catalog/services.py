import csv
import io
import logging

from .serializers import CategorySerializer

logger = logging.getLogger(__name__)


def process_category_csv(file_obj):
    """
    Process a CSV file to bulk-create categories.

    Args:
        file_obj: An in-memory file object containing the CSV data.

    Returns:
        A dictionary containing the results of the operation, including
        success count, error count, and a list of detailed errors.
    """
    try:
        # The file is opened in binary mode, so we need to decode it.
        csv_text = file_obj.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(csv_text))
    except (UnicodeDecodeError, csv.Error) as e:
        logger.error(f"CSV processing failed: {e}")
        return {
            "status": "Error",
            "success_count": 0,
            "error_count": 1,
            "errors": [
                {
                    "row_number": 1,
                    "data": {},
                    "errors": {"file": f"Invalid CSV file format: {e}"},
                }
            ],
        }

    success_count = 0
    error_count = 0
    errors = []

    required_columns = {"name"}
    if not required_columns.issubset(reader.fieldnames or []):
        missing = required_columns - set(reader.fieldnames or [])
        errors.append(
            {
                "row_number": None,
                "data": {},
                "errors": {
                    "headers": f"Missing required columns: {', '.join(missing)}"
                },
            }
        )
        return {
            "status": "Error",
            "success_count": 0,
            "error_count": 1,
            "errors": errors,
        }

    # Row 1 is the header, so start numbering data rows from 2 for user-friendly error reporting
    for i, row in enumerate(reader, start=2):
        serializer = CategorySerializer(data=row)
        if serializer.is_valid():
            serializer.save()
            success_count += 1
        else:
            error_count += 1
            errors.append({"row_number": i, "data": row, "errors": serializer.errors})

    status = "Upload completed successfully."
    if error_count > 0:
        status = f"Upload completed with {error_count} errors."

    return {
        "status": status,
        "success_count": success_count,
        "error_count": error_count,
        "errors": errors,
    }
