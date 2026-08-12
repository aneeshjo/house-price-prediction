import sys


class HousePricePredictionException(Exception):

    def __init__(self, error_message, error_detail: sys):

        super().__init__(error_message)

        self.error_message = self._get_detailed_error_message(
            error_message,
            error_detail
        )

    @staticmethod
    def _get_detailed_error_message(
        error_message,
        error_detail
    ):

        _, _, exc_tb = error_detail.exc_info()

        if exc_tb is None:
            return error_message

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        return (
            f"Error occurred in file "
            f"[{file_name}] at line "
            f"[{line_number}]: "
            f"{error_message}"
        )

    def __str__(self):
        return self.error_message