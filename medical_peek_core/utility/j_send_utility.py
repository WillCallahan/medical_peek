from medical_peek_core.model.j_send import JSend


class JSendUtility(object):
    @classmethod
    def is_j_send_object(cls, obj):
        """

        :param obj:
        :type obj: dict
        :return:
        :rtype:
        """
        j_send = JSend()
        for key in obj:
            if not j_send.__dict__.__contains__(key):
                return False
        return True

    @classmethod
    def get_status_by_status_code(cls, status_code):
        """
        Gets the JSend object Status based on the HTTP Response Status Code
        :param status_code: HTTP Response Status Code (i.e 200, 201, 403, 500)
        :type status_code: int
        :return: String JSend Status string
        :rtype: str
        """
        from medical_peek_core.utility.exception_utility import ExceptionUtility
        return JSend.Status.error if ExceptionUtility.is_error(status_code) else JSend.Status.success
