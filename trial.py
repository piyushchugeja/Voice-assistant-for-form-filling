data = "0212 2003"
date = data.split()
date = date[0][0:2] + "/" + date[0][2:] + "/" + date[1]
print(date)