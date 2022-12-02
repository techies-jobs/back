import re


def validate_email(email):
    try:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, email):
            return True
        return False
    except (TypeError, Exception) as err:
        # Log error
        return False


def validate_url(url: str) -> bool:
    if not str(url).startswith("https://"):
        return False
    return True


# def image_upload(request, **kwargs):
#     try:
#         user = request.user
#         image = request.data.get('image', None)
#
#         if not image:
#             return Response({"detail": f"image is required"}, status=status.HTTP_400_BAD_REQUEST)
#
#         if str(image.name).split(".")[-1] not in ['jpeg', 'png', 'jpg']:
#             return Response({"detail": f"Invalid image extension, only accept 'png', 'jpeg' and 'jpg' image."},
#                             status=status.HTTP_403_FORBIDDEN)
#
#         if image.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
#             return Response({"detail": "Image type is not supported for upload."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         user.image = image
#         user.save()
#     except (Exception, ) as err:
#         ...