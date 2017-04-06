from time import strftime,gmtime




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
