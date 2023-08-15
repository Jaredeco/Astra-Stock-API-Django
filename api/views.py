from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from drf_spectacular.utils import extend_schema
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
from xml.etree import ElementTree as et
from rest_framework.decorators import api_view


def download_and_unzip(url, extract_to='.'):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)


class AstraZip:
    def __init__(self):
        file_url = 'https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip'
        file_path = 'export_full.xml'
        download_and_unzip(file_url)
        self.data = et.parse(file_path).getroot()
        self.products = self.data.find('items').findall('item')

    def get_products_number(self):
        return len(self.products)

    def get_products_names(self):
        return [p.attrib['name'] for p in self.products]

    def get_products_parts(self, product_code):
        for p in self.products:
            if p.attrib['code'] == product_code:
                parts = p.find('parts')
                if parts is not None:
                    return [pt.attrib['name'] for pt in parts.findall('part')]
        return []


astra_zip = AstraZip()


@extend_schema(description="Get number of products in Astra")
@api_view(('GET',))
def astra_products_number(request):
    products_number = astra_zip.get_products_number()
    return Response(data=products_number, status=HTTP_200_OK)


@extend_schema(description="Get all products names in Astra")
@api_view(('GET',))
def astra_products_names(request):
    products_names = astra_zip.get_products_names()
    return Response(data=products_names, status=HTTP_200_OK)


@extend_schema(description="Get parts of a specific product")
@api_view(('GET',))
def astra_product_parts(request, product_code):
    product_parts = astra_zip.get_products_parts(product_code)
    return Response(data=product_parts, status=HTTP_200_OK)
