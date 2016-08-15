import os.path

from . import settings
from sistema import helpers


# TODO: by default save extension from uploaded_file
def save_file(uploaded_file, category, extension=None, save_as=None):
    DEFAULT_EXTENSION = ''

    directory = os.path.join(settings.SISTEMA_UPLOAD_FILES_DIR, category)
    helpers.ensure_directory_exists(directory)

    if save_as is None:
        file_name = os.path.join(directory, helpers.generate_random_name())
    else:
        file_name = os.path.join(directory, save_as)
    if extension is None:
        extension = DEFAULT_EXTENSION
    if extension != '':
        file_name += '.' + extension

    with open(file_name, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return file_name
