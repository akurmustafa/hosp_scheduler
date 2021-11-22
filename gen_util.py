
import datetime


def get_weekday(date_str):
    yy, mm, dd = date_str.split('_')
    return datetime.datetime(int(yy), int(mm), int(dd)).weekday()


def main():
    print(get_weekday("2021_10_01"))


if __name__ == '__main__':
    main()
