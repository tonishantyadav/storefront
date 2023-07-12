from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb = 5000

    if file.size > max_size_kb:
        raise ValidationError(f"Image size cannot be larger then {max_size_kb} kb.")