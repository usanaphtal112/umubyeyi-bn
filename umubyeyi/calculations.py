from datetime import datetime, timedelta, date


class Pregnancy:
    @staticmethod
    def calculate_pregnancy_info(last_menstrual_period):
        dd = last_menstrual_period.day
        mm = last_menstrual_period.month
        yy = last_menstrual_period.year
        current_date = datetime.now().date()

        dd = dd + 7
        if dd <= 30 and mm >= 4:
            dd = dd
            mm = mm - 3
            yy = yy + 1
        elif dd > 30 and mm >= 4:
            dd = dd - 30
            mm = mm - 2
            yy = yy + 1

        elif dd <= 30 and mm <= 3:
            dd = dd
            mm = mm + 9
            yy = yy
        elif dd > 30 and mm < 3:
            dd = dd - 30
            mm = mm + 10
            yy = yy

        elif dd > 30 and mm == 3:
            dd = dd - 30
            mm = 1
            yy = yy + 1

        expected_date_delivery = date(yy, mm, dd)

        # Calculate number of weeks of pregnancy
        weeks_of_pregnancy = 42 - abs((current_date - expected_date_delivery).days // 7)

        # Calculate number of days of pregnancy
        days_of_pregnancy = (
            timedelta(280).days - abs((current_date - expected_date_delivery)).days
        )

        return expected_date_delivery, weeks_of_pregnancy, days_of_pregnancy
