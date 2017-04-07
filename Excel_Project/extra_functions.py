from time import strftime,gmtime
import xlwt


def export_data(results):
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("Olx crawled results")
    counter = 0
    header(worksheet, counter)
    counter += 1
    for i in results:
        worksheet.write(counter, 0, i['Sector'])
        worksheet.write(counter, 1, i['Cluster'])
        worksheet.write(counter, 2, i['Sub_Cluster'])
        worksheet.write(counter, 3, i['Congested'])
        worksheet.write(counter, 4, i['Leakage'])
        worksheet.write(counter, 5, i['DCR'])
        worksheet.write(counter, 6, i['AFR'])
        worksheet.write(counter, 7, i['Misc'])
        worksheet.write(counter, 8, i['Analysis'])
        worksheet.write(counter, 9, i['Last_updated'])
        worksheet.write(counter, 10, i['Comments'])
        worksheet.write(counter, 11, i['Optimization_Completed'])
        worksheet.write(counter, 12, i['Status'])
        worksheet.write(counter, 13, i['Perm_Solution'])
        worksheet.write(counter, 14, i['Development_Priority'])
        worksheet.write(counter, 15, i['Cell_Split'])
        worksheet.write(counter, 16, i['Coverage Strategy'])
        worksheet.write(counter, 17, i['DART'])
        worksheet.write(counter, 18, i['Hardening_National'])
        worksheet.write(counter, 19, i['L1900_Capacity'])
        worksheet.write(counter, 20, i['L2100_Capacity'])
        worksheet.write(counter, 21, i['L700'])
        worksheet.write(counter, 22, i['Market_Infill'])
        worksheet.write(counter, 23, i['Modernization'])
        worksheet.write(counter, 24, i['New_Build_Infill'])
        worksheet.write(counter, 25, i['Replacement'])
        worksheet.write(counter, 26, i['ROB'])
        worksheet.write(counter, 27, i['Rural America'])
        worksheet.write(counter, 28, i['Sector_Add'])
        worksheet.write(counter, 29, i['Small_Cell_Strategy'])
        worksheet.write(counter, 30, i['T_Mobile_Store'])
        worksheet.write(counter, 31, i['Venue ACS'])
        worksheet.write(counter, 32, i['Cell_Split_ID'])
        counter += 1
    workbook.save("E:\\WebTracker.xls")
    print("created")


def header(worksheet, i):
    worksheet.write(i, 0, 'Sector')
    worksheet.write(i, 1, 'Cluster')
    worksheet.write(i, 2, 'Sub-Cluster')
    worksheet.write(i, 3, 'Congested')
    worksheet.write(i, 4, 'Leakage')
    worksheet.write(i, 5, 'DCR')
    worksheet.write(i, 6, 'AFR')
    worksheet.write(i, 7, 'Misc')
    worksheet.write(i, 8, 'Analysis(Why this site is on the list)')
    worksheet.write(i, 9, 'Last updated (Date)')
    worksheet.write(i, 10, 'Comments (What can be done short term)')

    worksheet.write(i, 11, 'Optimization Completed(Yes/No)')
    worksheet.write(i, 12, 'Status(Complete/In-progress)')
    worksheet.write(i, 13, 'Perm Solution (Describe the solution)')
    worksheet.write(i, 14, 'Development Priority')
    worksheet.write(i, 15, 'Cell Split')
    worksheet.write(i, 16, 'Coverage Strategy')
    worksheet.write(i, 17, 'DART')
    worksheet.write(i, 18, 'Hardening National')
    worksheet.write(i, 19, 'L1900 Capacity')
    worksheet.write(i, 20, 'L2100 Capacity')
    worksheet.write(i, 21, 'L700')
    worksheet.write(i, 22, 'Market Infill')
    worksheet.write(i, 23, 'Modernization')
    worksheet.write(i, 24, 'New Build Infill')
    worksheet.write(i, 25, 'Replacement')
    worksheet.write(i, 26, 'ROB')
    worksheet.write(i, 27, 'Rural America')
    worksheet.write(i, 28, 'Sector Add')
    worksheet.write(i, 29, 'Small Cell Strategy')
    worksheet.write(i, 30, 'T-Mobile Store')
    worksheet.write(i, 31, 'Venue ACS')
    worksheet.write(i, 32, 'Cell Split ID')


def get_excel_data(i, time, sheet, request):
    print("----------")
    print(sheet.cell_value(i,2))
    return {
                    'timestamp': time,
                    'username': request.session['username'],
                    'Sector':sheet.cell_value(i,0),
                    'Cluster':sheet.cell_value(i,1),
                    'Sub_Cluster':sheet.cell_value(i,2),
                    'Congested':sheet.cell_value(i,3),
                    'Leakage':sheet.cell_value(i,4),
                    'DCR':sheet.cell_value(i,5),
                    'AFR':sheet.cell_value(i,6),
                    'Misc':sheet.cell_value(i,7),
                    'Analysis':sheet.cell_value(i,8),
                    'Last_updated':sheet.cell_value(i,9),
                    'Comments':sheet.cell_value(i,10),

                    'Optimization_Completed':sheet.cell_value(i,11),
                    'Status':sheet.cell_value(i,12),
                    'Perm_Solution':sheet.cell_value(i,13),
                    'Development_Priority':sheet.cell_value(i,14),
                    'Cell_Split':sheet.cell_value(i,15),
                    'Coverage Strategy':sheet.cell_value(i,16),
                    'DART':sheet.cell_value(i,17),
                    'Hardening_National':sheet.cell_value(i,18),
                    'L1900_Capacity':sheet.cell_value(i,19),
                    'L2100_Capacity':sheet.cell_value(i,20),
                    'L700':sheet.cell_value(i,21),
                    'Market_Infill':sheet.cell_value(i,22),
                    'Modernization':sheet.cell_value(i,23),
                    'New_Build_Infill':sheet.cell_value(i,24),
                    'Replacement':sheet.cell_value(i,25),
                    'ROB':sheet.cell_value(i,26),
                    'Rural America':sheet.cell_value(i,27),
                    'Sector_Add':sheet.cell_value(i,28),
                    'Small_Cell_Strategy':sheet.cell_value(i,29),
                    'T_Mobile_Store':sheet.cell_value(i,30),
                    'Venue ACS':sheet.cell_value(i,31),
                    'Cell_Split_ID':sheet.cell_value(i,32),
            }

def get_post_data(request):
    return {
        'username': request.session['username'],
        'timestamp': strftime("%a, %d %b %Y %H:%M:%S", gmtime()),
        'Sector': request.POST['0'],
        'Cluster': request.POST['1'],
        'Sub_Cluster': request.POST['2'],
        'Congested':request.POST['3'],
        'Leakage':request.POST['4'],
        'DCR': request.POST['5'],
        'AFR': request.POST['6'],
        'Misc': request.POST['7'],
        'Analysis': request.POST['8'],
        'Last_updated': request.POST['9'],
        'Comments': request.POST['10'],
        'Optimization_Completed': request.POST['11'],
        'Status': request.POST['12'],
        'Perm_Solution': request.POST['13'],
        'Development_Priority': request.POST['14'],
        'Cell_Split': request.POST['15'],
        'Coverage_Strategy': request.POST['16'],
        'DART': request.POST['17'],
        'Hardening_National': request.POST['18'],
        'L1900_Capacity': request.POST['19'],
        'L2100_Capacity': request.POST['20'],
        'L700': request.POST['21'],
        'Market_Infill': request.POST['22'],
        'Modernization': request.POST['23'],
        'New_Build_Infill': request.POST['24'],
        'Replacement': request.POST['25'],
        'ROB': request.POST['26'],
        'Rural_America': request.POST['27'],
        'Sector_Add': request.POST['28'],
        'Small_Cell_Strategy': request.POST['29'],
        'T_Mobile_Store': request.POST['30'],
        'Venue_ACS': request.POST['31'],
        'Cell_Split_ID': request.POST['32'],
        }
