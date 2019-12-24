import os
import secrets
from flask import current_app

class Profil:
    def save_profil(form_profil):
        cls = secrets.token_hex(8)
        _,f_ext = os.path.splitext(form_profil.filename)
        filename = cls + f_ext
        path = os.path.join(current_app.root_path,'static/profil/' + filename)
        form_profil.save(path)
        return filename