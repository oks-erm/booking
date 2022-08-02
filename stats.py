import csv
from datetime import date, datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from spreadsheet import get_worksheet


def age(birthdate):
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
        item[3] = age(datetime.strptime(item[3], "%d-%m-%Y").date())
    with open("stats.csv", "w", newline="") as f:
        f.truncate()
        writer = csv.writer(f)
        writer.writerows(data)


def customers_stats():
    """
    Writes customers stats in pdf file.
    """
    df = pd.read_csv('stats.csv')
    plt.figure()
    plt.hist(df["BD"], bins=20, color="blue", edgecolor="black")
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter('{}%'.format))
    plt.xlabel('Age')

    plt.figure()
    plt.pie([(df['NUM OF BOOKINGS'].sum()-df['CANCELLED'].sum()),
            df['CANCELLED'].sum()], autopct='%1.1f%%',
            labels=["Total number of bookings", "Cancelled"])
    plt.xlabel('Bookings vs cancelled')

    plt.figure()
    plt.hist(df['NUM OF BOOKINGS'], bins=20, color="green", edgecolor="black")
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter('{}%'.format))
    plt.xlabel('Number of bookings per customer')

    plt.figure()
    x = pd.DataFrame(df)
    bins = [0, 20, 30, 40, 50, 60, 120]
    labels = ["below 20", "20-30", "30-40", "40-50", "50-60", "60+"]
    x["Age groups"] = pd.cut(x["BD"], bins=bins, labels=labels, right=False)
    pie_data = (x.groupby("Age groups")["BD"].count()).to_frame()
    pie_data["Age groups"] = round((pie_data.BD/sum(pie_data.BD))*100, 2)
    pie_data["Age groups"].plot.pie(autopct='%1.1f%%')

    pdf_pgs = PdfPages("stats.pdf")
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs:
        fig.savefig(pdf_pgs, format='pdf')
    pdf_pgs.close()