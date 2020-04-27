from medical_peek_scrapper.services.serializers import JObjectSerializer


class MckessonProduct(JObjectSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = ''
        self.invoice_title = ''
        self.manufacturer_id = ''
        self.description = ''
        self.product_id = ''
        self.features = []
        self.specifications = []
        self.more_information = []
