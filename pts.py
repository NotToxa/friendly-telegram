#by: @Not_Toxa
from .. import loader, utils
import logging
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)


@loader.tds
class PTSMod(loader.Module):
    """Photo to Sticker | Фото в стикер. Модуль позволяет превращать фото в стикер.\n.pts <replay>"""
    strings = {"name":"PTS"}
    
    async def get_img_from_msg(self, reply, message):
        if message.file and "image" in message.file.mime_type:
            return BytesIO(await message.download_media(bytes))
        if reply and reply.file and "image" in reply.file.mime_type:
            return BytesIO(await reply.download_media(bytes))
  
            
    async def ptscmd(self, message):
        """Превращает фото в стикер"""
        logger.debug("Logging.")
        reply = await message.get_reply_message()
        im = await self.get_img_from_msg(reply, message)
        if not im:
            await message.edit("Требуется реплай на медиа")
            return
        im2 = Image.open(im)
        output = BytesIO()
        output.name = "photo.webp"
        im2.save(output)
        output.seek(0)
        await message.delete()
        await message.client.send_file(message.to_id, output)
        return

    