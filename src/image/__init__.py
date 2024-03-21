from ..database import database
from .service import ImageService
from .scraper import ImageScraper
from .repository import ImageRepository
from .router import ImageRouter

scraper = ImageScraper()
repository = ImageRepository(database=database)
service = ImageService(scraper=scraper, repository=repository)
router = ImageRouter(service=service)
