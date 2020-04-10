class UrlProperty(object):
    def urls(self):
        """
        Gets all the URLs associated with the PersonController
        :param prefix: URL Prefix to prefix URLs with
        :return:
        """
        raise NotImplementedError('`urls()` must be implemented.')

    def __get_urls(self):
        raise NotImplementedError('`__get_urls()` must be implemented.')
