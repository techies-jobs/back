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


def validate_image(image):
    try:
        if not image:
            return False, "image is required"

        if str(image.name).split(".")[-1] not in ['jpeg', 'png', 'jpg']:
            return False, "Invalid image extension, only accept 'png', 'jpeg' and 'jpg' image."

        if image.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
            return False, "Image type is not supported for upload."

    except (Exception, ) as err:
        return False, str(err)

    else:
        return True, "Success"

def send_email(**kwargs):
    """
        This function should contain logics for send mail to any user.
        It receives 'named' parameters as **kwargs.
    """
    try:

        return True, f""
    except (Exception, ) as err:
        return False, f"{err}"