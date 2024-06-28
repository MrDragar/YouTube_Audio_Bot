import logging
from typing import Optional

from .models import Media, MediaType, Platform


async def get_media(link_id: str, type: MediaType,
                    resolution: Optional[str],
                    platform: Platform = Platform.YOUTUBE) -> Optional[Media]:
    media = await Media.get_or_none(link_id=link_id, type=type,
                                    resolution=resolution, platform=platform)
    return media


async def get_file_id(link_id: str, type: MediaType,
                      resolution: Optional[str],
                      platform: Platform = Platform.YOUTUBE) -> Optional[str]:
    media = await Media.get_or_none(link_id=link_id, type=type,
                                    resolution=resolution, platform=platform)
    return media.file_id if media else None


async def create_media(link_id: str, type: MediaType,
                       resolution: Optional[str],
                       platform: Platform = Platform.YOUTUBE) -> Media:
    media = (await Media.get_or_create(link_id=link_id, type=type,
                                      resolution=resolution, platform=platform))[0]
    await media.save()
    return media


async def delete_media(file_unique_id: str) -> bool:
    logging.debug(f"Delete media {file_unique_id}")
    media = await Media.get_or_none(file_unique_id=file_unique_id)
    if media is None:
        return True

    await media.delete()
    return False
