import os
import uuid
import base64
import datetime
from io import BytesIO
from PIL import Image as PilImage
from src.helpers.s3images import S3Images
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import generic_relationship

from src.core import settings
from src.core.databse import Basemodel


class ImageModel(Basemodel):
    __tablename__ = "images"

    object_type = Column(Unicode(255))
    object_id = Column(Integer)
    object = generic_relationship(object_type, object_id)

    __filename = Column(String(36), unique=True, nullable=False)
    __created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return self.filename

    @property
    def filename(self):
        return self.__filename

    @filename.setter
    def filename(self, name):
        self.__filename = f"{str(uuid.uuid4())}.{name.split('.')[-1]}"

    @property
    def base64_image(self):
        return getattr(self, "__base64_image", "")

    @base64_image.setter
    def base64_image(self, string):
        setattr(self, "__base64_image", string)

    @hybrid_property
    def created_at(self):
        return self.__created_at.isoformat()

    @property
    def url(self):
        return f"{settings.MEDIA_URL}{self.filename}"

    @property
    def path(self):
        return os.path.join(settings.MEDIA_ROOT, self.filename)

    @staticmethod
    def base64_to_image(base64_string):
        if not base64_string:
            return None

        img_format, img_str = base64_string.split(";base64,")
        img_bytes = BytesIO(base64.b64decode(img_str))
        ext = img_format.split("/")[-1]

        return img_bytes, ext


    async def delete(self, session):

        if os.path.exists(self.path):
            if settings.DEBUG:
                os.remove(self.path)
            else:
                await S3Images(**settings.S3_CONFIGS).delete_s3(self.filename)

        session.delete(self)
        session.commit()

        return True

    async def save(self, session):

        data_bytes, _ = self.base64_to_image(self.base64_image)
        image = PilImage.open(data_bytes)

        if settings.DEBUG:
            image.save(self.path)
        else:
            await S3Images(**settings.S3_CONFIGS).to_s3(image, self.filename)

        session.add(self)
        session.commit()

        return True
