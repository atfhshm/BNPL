from drf_spectacular.utils import OpenApiExample
from rest_framework import serializers

__all__ = [
    'get_serializer_validation_errors',
    'DetailSerializer',
]

MESSAGES = {
    serializers.CharField: [
        'This field may not be blank.',
        'Invalid character value.',
        'Ensure this field has no more than {max_length} characters.',
        'Ensure this field has at least {min_length} characters.',
    ],
    serializers.EmailField: [
        'Enter a valid email address.',
    ],
    serializers.URLField: [
        'Enter a valid URL.',
    ],
    serializers.UUIDField: [
        'Must be a valid UUID.',
    ],
    serializers.IPAddressField: [
        'Enter a valid IPv4 or IPv6 address.',
    ],
    serializers.RegexField: [
        'This value does not match the required pattern.',
    ],
    serializers.SlugField: [
        "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.",
    ],
    serializers.IntegerField: [
        'A valid integer is required.',
        'Ensure this value is less than or equal to {max_value}.',
        'Ensure this value is greater than or equal to {min_value}.',
    ],
    serializers.FloatField: [
        'A valid number is required.',
        'Ensure this value is less than or equal to {max_value}.',
        'Ensure this value is greater than or equal to {min_value}.',
    ],
    serializers.DecimalField: [
        'A valid number is required.',
        'Ensure this value is less than or equal to {max_value}.',
        'Ensure this value is greater than or equal to {min_value}.',
        'Ensure that there are no more than {max_decimal_places} decimal places.',
        'Ensure that there are no more than {max_digits} digits in total.',
    ],
    serializers.DateTimeField: [
        'Datetime has wrong format. Use one of these formats instead: YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]',
        'Date has wrong format. Use one of these formats instead: YYYY-MM-DD',
        'Invalid datetime for the timezone "{timezone}".',
        'Datetime value out of range.',
    ],
    serializers.DateField: [
        'Date has wrong format. Use one of these formats instead: YYYY-MM-DD',
        'Expected a date but got a datetime.',
    ],
    serializers.TimeField: [
        'Time has wrong format. Use one of these formats instead: HH:MM[:ss[.uuuuuu]]',
    ],
    serializers.DurationField: [
        'Duration has wrong format. Use one of these formats instead: [DD] [HH:[MM:]]ss[.uuuuuu]',
    ],
    serializers.ChoiceField: [
        '"{input}" is not a valid choice.',
        'This field is required.',
    ],
    serializers.MultipleChoiceField: [
        '"{input}" is not a valid choice.',
        'Expected a list of items but got type "{input_type}".',
    ],
    serializers.FileField: [
        'No file was submitted.',
        'The submitted data was not a file.',
        'The submitted file is empty.',
        'Ensure this filename has at most {max_length} characters.',
    ],
    serializers.ImageField: [
        'Upload a valid image. The file you uploaded was either not an image or a corrupted image.',
    ],
    serializers.ListField: [
        'Expected a list of items but got type "{input_type}".',
        'This list may not be empty.',
        'Ensure this field has at least {min_length} elements.',
        'Ensure this field has no more than {max_length} elements.',
    ],
    serializers.DictField: [
        'Expected a dictionary of items but got type "{input_type}".',
        'This dictionary may not be empty.',
    ],
    serializers.JSONField: [
        'Value must be valid JSON.',
    ],
    serializers.BooleanField: [
        'Must be a valid boolean.',
    ],
}


def get_serializer_validation_errors(serializer: serializers.BaseSerializer):
    instance = serializer()
    validation_errors = {}
    for field_name, field in instance.fields.items():
        # Check if the field is not read-only
        if not field.read_only:
            field_type = type(field)
            # Map the field to its respective error messages
            if field_type in MESSAGES:
                validation_errors[field_name] = MESSAGES[field_type]
    return OpenApiExample(
        '400 Validation Error Example',
        value=validation_errors,
        status_codes=[400],
        description=f'400 Bad Request validation error responses for {serializer.__name__}.',
        response_only=True,
    )


class DetailSerializer(serializers.Serializer):
    detail = serializers.CharField()
