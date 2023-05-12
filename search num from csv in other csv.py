import csv

dannye=csv.reader(open('dannye.csv'), delimiter=';') #read data from csv
rosreestr=csv.reader(open('csv/ros3xx.csv'), delimiter=';')

next(dannye, None) #skip header
next(rosreestr, None)

for row_d in dannye: # looking each row from csv file f1
    #print(row_d[0])
    for row_r in rosreestr: # looking for each row from csv file f2
        #print(row_r[0])
        if row_d[0]==row_r[0]: #checking the condition; worse case Time complexity o(n2)
            print(row_r)
            break