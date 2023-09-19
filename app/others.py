import pandas as pd

def read_student_info():
  df = pd.read_excel("students.xlsx").dropna()
  a = df.iloc[:,:]
  data = a[['학번', '학번.1', '이름', '전화번호']]
  lis = []
  for i in range(len(data.iloc[:,0])):
    dd = dict(data.iloc[i,:])
    if len(str(dd["전화번호"]))==10:
      dd["전화번호"] = "0" + str(dd["전화번호"])
    else:
      dd["전화번호"] = str(dd["전화번호"]).replace("-","")
    lis.append(dd)
  return lis
