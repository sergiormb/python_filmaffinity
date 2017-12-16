"""Page type: images."""
import re
from .page import Page
pattern_thumbnail = re.compile(r'\((.*?)\)', re.IGNORECASE)


class ImagesPage(Page):
    """Page type: images."""

    def _get_list_of_images(self, imgs_soup):
        """:returns List of dicts containing two keys for each dict:
                - image (full resolution image)
                - thumbnail (low resolution image)
                """
        if not imgs_soup:
            return []
        all_imgs = imgs_soup.find_all("div", {"class": 'colorbox-image'})
        imgs = []
        for i in all_imgs:
            if hasattr(i, 'a'):
                im = i.a['href']
                th = None
                if hasattr(i.a, 'div'):
                    re_th = pattern_thumbnail.search(
                        i.a.div['style'])
                    if re_th:
                        th = re_th.group(1)
                imgs.append({'image': im,
                             'thumbnail': th})
        return imgs

    def get_posters(self):
        """Get images of type posters."""
        imgs_cells = self.soup.find("div", {"id": 'type_imgs_2'})
        return self._get_list_of_images(imgs_cells)

    def get_stills(self):
        """Get images of type stills."""
        imgs_cells = self.soup.find("div", {"id": 'type_imgs_9'})
        return self._get_list_of_images(imgs_cells)

    def get_promos(self):
        """Get images of type promos."""
        imgs_cells = self.soup.find("div", {"id": 'type_imgs_8'})
        return self._get_list_of_images(imgs_cells)

    def get_events(self):
        """Get images of type events/red carpet."""
        imgs_cells = self.soup.find("div", {"id": 'type_imgs_11'})
        return self._get_list_of_images(imgs_cells)

    def get_shootings(self):
        """Get images of type shootings/making of."""
        imgs_cells = self.soup.find("div", {"id": 'type_imgs_13'})
        return self._get_list_of_images(imgs_cells)
