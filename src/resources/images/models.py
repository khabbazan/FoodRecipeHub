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
from src.core.database import Basemodel


class ImageModel(Basemodel):
    """
    Represents an image model in the database.

    Attributes:
        object_type (str): The type of object associated with the image.
        object_id (int): The ID of the object associated with the image.
        object (object): A generic relationship to associate the image with various object types.
        filename (str): The unique filename of the image.
        base64_image (str): The base64-encoded image data.
        created_at (str): The creation timestamp in ISO format.
        url (str): The URL for accessing the image.
        path (str): The local file path to the image.

    Methods:
        base64_to_image(base64_string): Convert a base64-encoded image string to an image object.
        delete(session): Delete the image.
        save(session): Save the image.
    """

    __tablename__ = "images"

    object_type = Column(Unicode(255))
    object_id = Column(Integer)
    object = generic_relationship(object_type, object_id)  # noqa VNE003

    __filename = Column(String(36), unique=True, nullable=False)
    __created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        """Returns a string representation of the image."""
        return self.filename

    @property
    def filename(self):
        """Property: Get the filename of the image."""
        return self.__filename

    @filename.setter
    def filename(self, name):
        """Property: Set the filename of the image based on input name."""
        self.__filename = f"{str(uuid.uuid4())}.{name.split('.')[-1]}"

    @property
    def base64_image(self):
        """Property: Get the base64-encoded image data."""
        return getattr(self, "__base64_image", "")

    @base64_image.setter
    def base64_image(self, string):
        """Property: Set the base64-encoded image data."""
        setattr(self, "__base64_image", string)  # noqa B010

    @hybrid_property
    def created_at(self):
        """Hybrid Property: Get the creation timestamp in ISO format."""
        return self.__created_at.isoformat()

    @property
    def url(self):
        """Property: Get the URL for accessing the image."""
        return f"{settings.MEDIA_URL}{self.filename}"

    @property
    def path(self):
        """Property: Get the local file path to the image."""
        return os.path.join(settings.MEDIA_ROOT, self.filename)

    @staticmethod
    def base64_to_image(base64_string):
        """
        Convert a base64-encoded image string to an image object.

        Args:
            base64_string (str): Base64-encoded image data.

        Returns:
            tuple: A tuple containing the image bytes and extension.
        """
        if not base64_string:
            return None

        img_format, img_str = base64_string.split(";base64,")
        img_bytes = BytesIO(base64.b64decode(img_str))
        ext = img_format.split("/")[-1]

        return img_bytes, ext

    async def delete(self, session):
        """
        Delete the image.

        Args:
            session (Session): SQLAlchemy session.

        Returns:
            bool: True if deletion was successful.
        """
        if os.path.exists(self.path):
            if settings.DEBUG:
                os.remove(self.path)
            else:
                await S3Images(**settings.S3_CONFIGS).delete_s3(self.filename)

        session.delete(self)
        session.commit()

        return True

    async def save(self, session):
        """
        Save the image.

        Args:
            session (Session): SQLAlchemy session.

        Returns:
            bool: True if saving was successful.
        """
        data_bytes, _ = self.base64_to_image(self.base64_image)
        image = PilImage.open(data_bytes)

        if settings.DEBUG:
            image.save(self.path)
        else:
            await S3Images(**settings.S3_CONFIGS).to_s3(image, self.filename)

        session.add(self)
        session.commit()

        return True
