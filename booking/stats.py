"""
Functions related to statistics report.
"""
import csv
from datetime import date, datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from booking.spreadsheet import get_worksheet, SCOPED_CRED


def upload(my_file, folder):
    """
    Uploads file to Goggle Drive.
    """
    try:
        # Authenticate and construct service.
        service = build('drive', 'v3', credentials=SCOPED_CRED)

        file_metadata = {'name': str(date.today())+'_stats.pdf',
                         'parents': [folder]}
        media = MediaFileUpload(my_file, mimetype='application/pdf')
        file = service.files().create(body=file_metadata,  # pylint: disable=maybe-no-member
                                      media_body=media,
                                      fields='id').execute()
    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None
    return file.get('id')


def calculate_age(birthdate):
    """
    Calculates age based on birthdate.
    """
    today = date.today()
    age = (today.year - birthdate.year
           - ((today.month, today.day) < (birthdate.month, birthdate.day)))
    return str(age)


def data_for_stats():
    """
    Prepares data for stats and writes it to csv
    """
    data = get_worksheet("customers")
    for item in data[1:]:
        item[3] = calculate_age(datetime.strptime(item[3], "%d-%m-%Y").date())
    with open("stats.csv", "w", newline="") as file:
        file.truncate()
        writer = csv.writer(file)
        writer.writerows(data)


def customers_stats():
    """
    Writes customers stats in pdf file.
    """
    dataframe = pd.read_csv('stats.csv')

    # histogram with age
    plt.figure()
    plt.hist(dataframe["BD"], bins=20, color="#4285f4", edgecolor="black")
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter('{}%'.format))  # pylint: disable=consider-using-f-string
    plt.xlabel('Age')

    # pie chart with age groups
    plt.figure()
    my_data = pd.DataFrame(dataframe)
    bins = [0, 20, 30, 40, 50, 60, 120]
    labels = ["below 20", "20-30", "30-40", "40-50", "50-60", "60+"]
    my_data["Age groups"] = pd.cut(my_data["BD"], bins=bins,
                                   labels=labels, right=False)
    pie_data = (my_data.groupby("Age groups")["BD"].count()).to_frame()
    pie_data["Age groups"] = round((pie_data.BD/sum(pie_data.BD))*100, 2)
    pie_data["Age groups"].plot.pie(colors=["#bbe0e7", "#fce782", "#2a7acc",
                                    "#a755f4", "#74e387", "#ffa25e"],
                                    autopct='%1.1f%%', startangle=35)

    # rate of cancelled bookings
    plt.figure()
    plt.pie([(dataframe['NUM OF BOOKINGS'].sum()-dataframe['CANCELLED'].sum()),
            dataframe['CANCELLED'].sum()],
            colors=["#7ada61", "#f07a9a"],
            autopct='%1.1f%%',
            labels=["Total number of bookings", "Cancelled"])
    plt.xlabel('Bookings vs cancelled')

    # histogram number of bookings per customer
    plt.figure()
    plt.hist(dataframe['NUM OF BOOKINGS'], bins=20,
             color="#a6ceef", edgecolor="black")
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter('{}%'.format))  # pylint: disable=consider-using-f-string
    plt.xlabel('Number of bookings per customer')

    # save multiple figures to one pdf file
    pdf_pgs = PdfPages("stats.pdf")
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs:
        fig.savefig(pdf_pgs, format='pdf')
    pdf_pgs.close()
    upload("stats.pdf", '1RMQBmiL3ATEkIAtPFmQypM5rcYfzXsD-')
