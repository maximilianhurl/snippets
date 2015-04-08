import uuid
from django.db import models
from markupfield.fields import MarkupField


class Snippet(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)
    text = MarkupField(markup_type='markdown')
