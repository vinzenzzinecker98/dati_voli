import pandas as pd
import urllib.request
data_departures = []
data_arrivals = []
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')
print("getting departures and arrivals for today: "+today)
for abfrage in [0,6,12,18]:
  print(f"timeslot {abfrage}")
  url = "https://www.roma-airport.com/fiumicino-fco-departures-airline-ita-airways?tp="+str(abfrage)
  with urllib.request.urlopen(url) as response:
    html = response.read()
  #<div class="flight-col flight-col__hour">

  #print(html)
  code = str(html)
  index = 0
  destindex = 0
  matches = code.count('<div class="flight-col flight-col__hour">')
  #print(f"{matches-1} matches from {abfrage}:00 to {abfrage+6}:00")
  for i in range(matches):
    destindex = code.find('<div class="flight-col flight-col__dest-term">', destindex)
    destanfang = code.find("<b>", destindex)+3
    destende = code.find("</span>", destindex)
    destindex = destindex + 10
    dest = code[destanfang:destende].replace("</b>\\n\\t\\t\\t\\t\\t\\t\\t<span>", " ")
    index = code.find('<div class="flight-col flight-col__hour">', index)
    nummer = code.find("/fiumicino-fco-flight-departure/",index)+32
    nummerende = code.find('"',nummer)
    id = code[nummer:nummerende]
    index = index+57
    time = code[index:index+5]
    if time =="rture": continue
    data_departures.append({"ID": id, "Time": time, "Destination": dest, "Date": today})
    #print(f"index: {index}-----time: {time}, Dest: {dest}, ID: {id}")



  url = "https://www.roma-airport.com/fiumicino-fco-arrivals-airline-ita-airways?tp="+str(abfrage)
  with urllib.request.urlopen(url) as response:
    html = response.read()
  #<div class="flight-col flight-col__hour">

  #print(html)
  code = str(html)
  index = 0
  destindex = 0
  matches = code.count('<div class="flight-col flight-col__hour">')
  #print(f"{matches-1} matches from {abfrage}:00 to {abfrage+6}:00")
  for i in range(matches):
    destindex = code.find('<div class="flight-col flight-col__dest-term">', destindex)
    destanfang = code.find("<b>", destindex)+3
    destende = code.find("</span>", destindex)
    destindex = destindex + 10
    dest = code[destanfang:destende].replace("</b>\\n\\t\\t\\t\\t\\t\\t\\t<span>", " ")
    index = code.find('<div class="flight-col flight-col__hour">', index)
    nummer = code.find("/fiumicino-fco-flight-arrival/",index)+30
    nummerende = code.find('"',nummer)
    id = code[nummer:nummerende]
    index = index+57
    time = code[index:index+5]
    if time =="val\\t": continue
    data_arrivals.append({"ID": id, "Time": time, "Origin": dest, "Date": today})
    #print(f"index: {index}-----time: {time}, Dest: {dest}, ID: {id}")






df_a = pd.DataFrame(data_arrivals)
df_d = pd.DataFrame(data_departures)

print("reading existing data...")
df_a_old = pd.read_excel("voli.xlsx", sheet_name="arrivals", index_col=0, )
df_d_old = pd.read_excel("voli.xlsx", sheet_name="departures", index_col=0)
print("writing...")
if not df_a_old.empty:
  if(df_a_old.iloc[-1]["Date"] == today):
    print("file already updated")
  else:
    df_a = pd.concat([df_a_old, df_a], ignore_index=True)
    df_d = pd.concat([df_d_old, df_d], ignore_index=True)

    with pd.ExcelWriter('voli.xlsx', engine="openpyxl", mode='a', if_sheet_exists="replace") as writer:  
        df_a.to_excel(writer, sheet_name="arrivals")
        df_d.to_excel(writer, sheet_name="departures")

    print("successfully updated file")
else:
  with pd.ExcelWriter('voli.xlsx', engine="openpyxl", mode='a', if_sheet_exists="replace") as writer:  
      df_a.to_excel(writer, sheet_name="arrivals")
      df_d.to_excel(writer, sheet_name="departures")

  print("successfully created file")