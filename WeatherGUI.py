from tkinter import *
import requests
import bs4

#replace each space with a plus
def replace(name, lookFor, replaceWith):
    name = list(name)
    out = name
    for i in range(0, len(name)):
        if name[i] == lookFor:
            out[i] = replaceWith
    return "".join(out)

#make window
root = Tk()
root.title("Weather")
root.eval("tk::PlaceWindow %s center" % root.winfo_pathname(root.winfo_id()))

#make frame
app = Frame(root)
app.grid()

#label
label = Label(app, text = "Weather for City: ", font = 24)
label.grid(row = 0, column = 0, sticky = W)

#entry
entry = Entry(app, font = 24)
entry.grid(row = 0, column = 1)
entry.focus_set()

#location label
location = StringVar()
locationLabel = Label(app, textvariable = location, font = "-weight bold")
locationLabel.grid(row = 1, columnspan = 3, sticky = W)

#temp label
temp = StringVar()
tempLabel = Label(app, textvariable = temp, font = 24)
tempLabel.grid(row = 2, columnspan = 3, sticky = W)

#precip label
precip = StringVar()
precipLabel = Label(app, textvariable = precip, font = 24)
precipLabel.grid(row = 3, columnspan = 3, sticky = W)

#humidity label
humidity = StringVar()
humidityLabel = Label(app, textvariable = humidity, font = 24)
humidityLabel.grid(row = 4, columnspan = 3, sticky = W)

#wind label
wind = StringVar()
windLabel = Label(app, textvariable = wind, font = 24)
windLabel.grid(row = 5, columnspan = 3, sticky = W)

#forecast label
forecast = StringVar()
forecastLabel = Label(app, textvariable = forecast, font = "-weight bold")
forecastLabel.grid(row = 6, columnspan = 3, sticky = W)

#day labels
days = []
dayLabels = []
for i in range(0, 8):
    days.append(StringVar())
    dayLabels.append(Label(app, textvariable = days[i], font = 24))
    dayLabels[i].grid(row = 7 + i, columnspan = 3, sticky = W)

#button
def callback():
    #format name
    loc = entry.get()
    loc2 = replace(loc, " ", "+")
    #make url
    url = "https://www.google.com/search?hl=en&site=webhp&q=weather+in+" + loc2
    #get page
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"}
    page = requests.get(url, headers = headers)
    page.raise_for_status()
    #format page
    fPage = bs4.BeautifulSoup(page.text, "html.parser")
    #get values
    pageLoc = fPage.find("div", attrs = {"id": "wob_loc"})
    pageTime = fPage.find("div", attrs = {"id": "wob_dts"})
    pageTemp = fPage.find("span", attrs = {"id": "wob_tm"})
    pageTemp2 = fPage.find("span", attrs = {"id": "wob_ttm"})
    pagePrecip = fPage.find("span", attrs = {"id": "wob_pp"})
    pageHumidity = fPage.find("span", attrs = {"id": "wob_hm"})
    pageWind = fPage.find("span", attrs = {"id": "wob_ws"})
    pageWind2 = fPage.find("span", attrs = {"id": "wob_tws"})
    pageDays = []
    
    if pageLoc:
        for i in range(0, 8):
            pageDay = fPage.find("div", attrs = {"wob_di": i})
            pageDayStrs = list([])
            for string in pageDay.strings:
                newStr = replace(repr(string), "'", "")
                pageDayStrs.append(newStr)
            pageDays.append(pageDayStrs)
        
        #update values
        location.set("Current Weather in " + pageLoc.text + " (" + pageTime.text + ")")
        temp.set("Temperature:\t" + pageTemp.text + "°F / " + pageTemp2.text + "°C")
        precip.set("Precipitation:\t" + pagePrecip.text)
        humidity.set("Humidity:\t\t" + pageHumidity.text)
        wind.set("Wind:\t\t" + pageWind.text + " / " + pageWind2.text)
        forecast.set("Forecast")
        for i in range(0, 8):
            days[i].set(pageDays[i][0] + ":\thigh: " + pageDays[i][1] + "°F / " + pageDays[i][2] + "°C" +
                ",\tlow: " + pageDays[i][4] + "°F / " + pageDays[i][5] + "°C")
    else:
        #clear values
        location.set("")
        temp.set("")
        precip.set("")
        humidity.set("")
        wind.set("")
        forecast.set("")
        for i in range(0, 8):
            days[i].set("")
    
    #clear entry
    entry.delete(0, END)
    
button = Button(app, text = "Submit", font = 24, command = callback)
button.grid(row = 0, column = 2, columnspan = 2)

root.mainloop()
