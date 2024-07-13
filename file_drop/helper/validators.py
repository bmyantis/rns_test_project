from rest_framework.exceptions import ValidationError
import mimetypes


def validate_file_format(value):
    allowed_formats = ['image/jpeg', 'text/plain', 'image/png', 'application/pdf']
    mime_type, _ = mimetypes.guess_type(value.name)

    if mime_type not in allowed_formats:
        raise ValidationError(f'Unsupported file format: {mime_type}. Allowed formats are: {", ".join(allowed_formats)}')
