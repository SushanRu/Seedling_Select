   
    # s: the dictionary of stages, skey: the list of keys in s
    # s['bpname']: breeding program name
    # s['sNo']: int. No. of all breeding stages
    # s['skey']: list. of all breeding stage names
    # s[breeding stage]['sdate']: str. starting date of a breeding stage
    # -----------------['smonth']: int. starting month of the breeding stage
    # -----------------['syear']: int. starting year of the breeding stage
    # -----------------['scode']: int. code of the starting date of the breeding stage
    # -----------------['edate']: str. ending date of a breeding stage
    # -----------------['emonth']: int. ending month of the breeding stage
    # -----------------['eyear']: int. ending year of the breeding stage
    # -----------------['ecode']: int. code of the ending date of the breeding stage
    # -----------------['lrNo']: int. number of loss reasons of a breeding stage
    # -----------------['lr'][n]: str. name of the nth loss
    # -----------------['rp'][n]: float. remaining proportion of the nth loss
    # -----------------['ld'][d]: str. loss date of the nth loss
    # -----------------['trp']: total remaining proportion of a stage
    # -----------------[family name]['Tfs']: TSS starting family size in a stage
    # ------------------------------['Tfe']: TSS ending family size in a stage
    # ------------------------------['Mfs']: MASS starting family size in a stage
    # ------------------------------['Mfe']: MASS ending family size in a stage
    # ------------------------------[n]['Dfs']: MASS family size in the beginning of nth DNA test
    # ------------------------------[n]['Dfe']: MASS family size in the end of nth DNA test
    # ------------------['total']['Ts']: TSS starting total size in a stage
    # ---------------------------['Te']: TSS ending total size in a stage
    # ---------------------------['Ms']: MASS starting total size in a stage
    # ---------------------------['Me']: MASS ending total size in a stage
    # s['ctype']: list of all cost types
    # s['smonthcode'] = s[tstage]['smonth'] + s[tstage]['syear'] * 12 - 1 # the base number of the first month
       
    # f: the dictionary of family information
    # f['fNo']: int. No. of families
    # f['fkey']: list. of all family names
    # f[family name]['fname']: father name of a family
    # --------------['mname']: mother name of a family
    # --------------['size']: original size of a family

    # tc: a dictionary for traditional cost information
    # tc['total']: total traditional cost for all stages and all families
    # tc[breeding stage]['tcost']: the total traditional cost in a breeding stage
    # ------------------['cost name']: a list of cost names in a breeding stage 
    # ------------------[cost name]['type']
    # -----------------------------['rangeNo']
    # -----------------------------['low']
    # -----------------------------['high']
    # -----------------------------['price']
    # -----------------------------['unit'] 
    # tc['typecost'] = {} # a dictionary for TSS cost in each type
    
    # tmcost = 0: total MASS cost for all families

    # mc: a dictionary for MASS cost
    # mc['typecost'] = {} # a dictionary for MASS cost in each type
        
    
    
    # mc['Dt_c']['DtNo']: int. No. of DNA tests
    # ----------['Dtkey']: list. of DNA test names
    # ----------[Dtname]['sourceNo']: No. of cost sources for a DNA test
    # ------------------['ckey']: list. of cost sources in a DNA test
    # ------------------[cost name]['rangeNo']: int. No. of price ranges for a cost
    # -----------------------------[n]['low']
    # -----------------------------[n]['high']
    # -----------------------------[n]['price']
    # -----------------------------[n]['unit']
    # mc['Dt_c']['cost']: DNA test cost for all stages, all families
    # ----------[family name]['cost']
    # ----------[family name][stage name]['cost']
    # ----------[family name][stage name][DNAtname]['cost']
    # mc['tradi']['total'] # total traditional cost in all breeding stages in MASS
    # ----------[breeding stage]['tcost'] # total traditional cost in a breeding stage in MASS
    # mc['DNAtesting'] # DNA testing cost in MASS
    
    # mc[tstage] = {}
    # ----------['Dt_c'] = 0 # DNA testing cost in each breeding stage
    # mc['save$'] # $ saving from MASS = tc['total'] - mc['total']
    # mc['save%'] # % saving from MASS = (tc['total'] - mc['total'])/tc['total'] * 100
    

    # Dt: a dictionary for DNA test information
    # Dt[family name][breeding stage]['Dt_No']: int. No. of DNA test in a stage in a family
    # -------------------------------[n]['Dt_name']: DNA test name of nth DNA test in a breeding stage in a family
    # -------------------------------[n]['rp']: remaining proportion of nth DNA test in a breeding stage in a family
    

######------------------------------------------------------------------------------------------------------------#####

def main():

    import csv
    
    
    infile = open("inputtemplate-051016.csv", "rt")
    outfile = open('output-051016.csv', 'wb')# use 'wb' but not 'w' for python2, so that there is no extra lines

    s = {}
    f = {}
    tc = {} # a dictionary for traditional cost information
    mc = {} # dictionary for MASS cost
    Dt = {} # dictionary for DNA test information
    
    
    # read data from input file
    s,f,tc,mc,Dt = read_csv(infile)
    
    # calculate family size in each stage, MASS & TSS
    s = cal_TSSsize(s, f, Dt)

    # calculate traditional cost in TSS and MASS
    tc, mc = cal_TSScost(s, f, tc, mc)

    # calculate DNA testing cost
    mc = cal_DANcost(tc, s, f, mc, Dt)
   

    print_csv(outfile, s, f, tc, mc, Dt)
    
    costcomp(s, f, tc, mc, Dt)
    populationsize(s, f, tc, mc, Dt)
    familysize(s, f, tc, mc, Dt)  
   
    # look for the most efficient stage
    
          
    infile.close
    outfile.close
#--------------------------------------------------------------------------------------------------------------------    
#--------------------------------------------------------------------------------------------------------------------
def read_csv(infile):
    s = {} # dictionary for all information in each stage
    s['bpname'] = () # the name of the breeding program
    s['sNo'] = 0# read the number of breeding stages: s['sNo']
    s['skey'] = [] # a list of stage names
    s['ctype'] = [] # a lit of all cost types
    f = {} # dictionary for family information
    tc = {} # a dictionary for traditional cost information
    tc['ctype'] = {} # a dictionary for TSS cost in each type
    mc = {} # dictionary for MASS cost
    mc['ctype'] = {} # a dictionary for MASS cost in each type
    Dt = {} # dictionary for DNA test information
    
    with infile as csvfile:
        lit = csvfile.readline() # read the notation line for the name of the breeding program
        lit = csvfile.readline().rstrip('\n')
        lit = lit.split(',')
        s['bpname'] = lit[0]# read the name of the breeding program

        csvfile.readline()# read the notation line for the number of breeding stages
        lit = csvfile.readline().rstrip('\n')
        lit = lit.split(',')
        s['sNo'] = int(lit[0])# read the number of breeding stages: s['sNo']

        csvfile.readline() # read the notation line for breeding stages
        for i in range(s['sNo']):
            lit = csvfile.readline().rstrip('\n')
            lit = lit.split(',')
            tstage = lit[0] # temporary stage name
            s[tstage] = {} # define dictionary for breeding stages using stage name as the key
            s[tstage]['sdate'] = lit[1] # s[breeding stage name]['sdate']: starting date 
            s[tstage]['smonth'] = int(s[tstage]['sdate'].split('|')[0])
            s[tstage]['syear'] = int(s[tstage]['sdate'].split('|')[1])
            if i == 0:
                s['smonthcode'] = s[tstage]['smonth'] + s[tstage]['syear'] * 12 - 1 # the base number of the first month
            
            s[tstage]['scode'] = s[tstage]['smonth'] + s[tstage]['syear'] * 12 - s['smonthcode']
           
            
            s[tstage]['edate'] = lit[2] # s[breeding stage name]['edate']: ending date
            s[tstage]['emonth'] = int(s[tstage]['edate'].split('|')[0])
            s[tstage]['eyear'] = int(s[tstage]['edate'].split('|')[1])
            s[tstage]['ecode'] = s[tstage]['emonth'] + s[tstage]['eyear'] * 12 - s['smonthcode']
            
            
            s[tstage]['lrNo'] = int(lit[3]) # the number of loss reasons in a stage 

            # define dictionarys under s[breeding stage]
            s[tstage]['lr'] = {} # dictionary for loss reasons in a stage
            s[tstage]['rp'] = {} # dictionary for remaining proportions after losses in a stage
            s[tstage]['ld'] = {} # dictionary for loss date in a stage
            s[tstage]['trp'] = 1 # remaining proportion after all TSS losses in a stage

            # get infor for each loss reason
            m = 4 # m counts the index of the list, now it is the first loss reason
            for j in range(s[tstage]['lrNo']): # j is from 6 to the total number of loss reasons-1
                s[tstage]['lr'][j] = lit[m] #s[breeding stage]['lr'][jth loss reason]
                s[tstage]['rp'][j] = float(lit[m + 1]) # remaining proportion of jth loss reason
                s[tstage]['ld'][j] = lit[m + 2] # loss date of jth loss reason
                s[tstage]['trp'] = s[tstage]['trp'] * s[tstage]['rp'][j] # calculate total remaining proportion
                m +=3

            s['skey'].append(lit[0]) # the list of stage names
            
        
        # read the line for family structure
        csvfile.readline()
        csvfile.readline() # read the notation line for family structure
        lit = csvfile.readline().rstrip('\n')
        lit = lit.split(',') # lit: temporary list for family structure list
        f['fNo'] = int(lit[0]) # No. of families
        f['fkey'] = [] # a list of family names
        s['ctype'] = [] # a list of cost types
        

        # read family infor
        m = 1 # the index in the list, now it is the first family name
        for i in range(f['fNo']):
            tfname = lit[m] # temp family name
            f[tfname] = {}
            f[tfname]['fname'] = lit[m + 1]
            f[tfname]['mname'] = lit[m + 2]
            f[tfname]['size'] = int(lit[m + 3])
            f['fkey'].append(tfname)
            m += 4

        
        # read TSS cost info from the file
        csvfile.readline()
        csvfile.readline()
        
        for i in range(s['sNo']): # go through all breeding stages one by one
            lit = csvfile.readline().rstrip('\n')
            lit = lit.split(',')
            tc[lit[0]] = {} # lit[0] is breeding stage name
            tc[lit[0]]['tcost'] = 0 # c[breeding stage name]['tcost'] = the total traditional cost in a breeding stage
            tc[lit[0]]['cost name'] = [] # c[breeding stage name]['cost name']: a list of cost names in a breeding stage
            cNo = int(lit[1]) # No. of cost sources in stage lit[0]
        
            j = 0 # count the number of cost source
            m = 1 # count the index number in the list, it reads to index 1 (the second string in the list) ("cNo")
            t = 0 # a temporary value to look for new cost type. If the type is already exist, t = 1, otherwise t = 0
            
            while j < cNo:
                
                m += 1
                Tcname = lit[m] # Tsnam: temporary cost name, only works in this loop
                tc[lit[0]]['cost name'].append(Tcname)
                tc[lit[0]][Tcname] = {} # lit[m + 1]: cost name
                m += 1
                tc[lit[0]][Tcname]['type'] = lit[m]
                # collect all cost types into the list ctype
                if s['ctype'] == []:
                    s['ctype'].append(lit[m])
                else:
                    for k in s['ctype']:
                        if k == lit[m]:
                            t = 1 # if the type is already in the list, t = 1
                            break
                    if t == 0: s['ctype'].append(lit[m]) # if t = 0, the type is new and add it to the list
                    
                
                m += 1 # m is now the index for rangeNo
                tc[lit[0]][Tcname]['rangeNo'] = int(lit[m])

                for k in range(tc[lit[0]][Tcname]['rangeNo']): # k is the rangeNo. - 1. c[breeding stage][cost name][rangeNo][]
                    tc[lit[0]][Tcname][k]={}
                    m += 1 # m is the index for the lower boundry of the range
                    tc[lit[0]][Tcname][k]['low'] = int(lit[m])
                    m += 1 # m is now the higher boundry of range k
                    tc[lit[0]][Tcname][k]['high'] = int(lit[m])
                    m += 1 # m is now the price of range k
                    tc[lit[0]][Tcname][k]['price'] = float(lit[m])
                    m += 1 # m is now the unit of range k
                    tc[lit[0]][Tcname][k]['unit'] = lit[m]

                j += 1 # j goes to the next cost source
        
        # read DNA test cost -----------------------------

        #read DNA testing cost information
        csvfile.readline()
        mc['Dt_c'] = {}
        lit = csvfile.readline().rstrip('\n')
        lit = lit.split(',')
        
        mc['Dt_c']['DtNo'] = int(lit[0]) # read the number of different DNA tests
        mc['Dt_c']['Dtkey'] = [] # a list of DNA test names
        csvfile.readline()
        csvfile.readline()
        for i in range(mc['Dt_c']['DtNo']):
            lit = csvfile.readline().rstrip('\n')
            lit = lit.split(',')
            Dtname = lit[0] # temporary DNA test name
            mc['Dt_c']['Dtkey'].append(Dtname)
        
            mc['Dt_c'][Dtname] = {} # mc['DNAt_cost_info'][DNA test name]
            mc['Dt_c'][Dtname]['sourceNo'] = int(lit[1]) #No. of cost sources for a DNA test
            mc['Dt_c'][Dtname]['ckey'] = [] # a list of cost sources in a DNA test
        
            m = 1 # index in the list
            for j in range(mc['Dt_c'][Dtname]['sourceNo']):
                m += 1 # index in the list, now cost name 
                cost_name = lit[m]
                mc['Dt_c'][Dtname]['ckey'].append(cost_name)

                mc['Dt_c'][Dtname][cost_name] = {}
                m += 1 # m is now the index of the range number
                mc['Dt_c'][Dtname][cost_name]['rangeNo'] = int(lit[m])
                for k in range(mc['Dt_c'][Dtname][cost_name]['rangeNo']):
                    mc['Dt_c'][Dtname][cost_name][k] = {}
                    m += 1
                    mc['Dt_c'][Dtname][cost_name][k]['low'] = int(lit[m])
                    m += 1
                    mc['Dt_c'][Dtname][cost_name][k]['high'] = int(lit[m])
                    m += 1
                    mc['Dt_c'][Dtname][cost_name][k]['price'] = float(lit[m])
                    m += 1
                    mc['Dt_c'][Dtname][cost_name][k]['unit'] = lit[m]
    

    # read DNA test information---------------------------

        csvfile.readline()
        #read DNA test in each family
        for i in f['fkey']:
            Dt[i] = {} # dictionary Dt[family name]
            for j in s['skey']:
                Dt[i][j] = {} # Dt[family name][breeding stage]
                Dt[i][j]['Dt_No'] = 0 # Dt[family name][stage name]['Dt_No'] = 0 if there is no DNA test in that stage
        lit = csvfile.readline().rstrip('\n')
        lit = lit.split(',')       
        tfNo = int(lit[0]) # No. of families using DNA tests
        csvfile.readline()
        for i in range(tfNo):
              lit = csvfile.readline().split(',')
              tsNo = int(lit[1]) # No. of breeding stages using DNA tests (temp)
              m = 1 # list index
              for j in range(tsNo):
                  tfname = lit[0] # family name using DNA tests (temp)
                  m += 1 # breeding stage
                  tbs = lit[m] # breeding stage name (temp)
                  m += 1 # m is the index of No. of DNA tests 
                  Dt[tfname][tbs]['Dt_No'] = int(lit[m])# Dt[family name][breeding stage]['Dt_No']: No. of DNA tests used in family, stage
                  for k in range(Dt[tfname][tbs]['Dt_No']):
                      Dt[tfname][tbs][k] = {} # Dt[family name][breeding stage][kth DNA test]
                      m += 1 # the index of DNA test name
                      Dt[tfname][tbs][k]['Dt_name'] = lit[m] # Dt[family name][breeding stage][kth DNA test]['Dt_name']
                      m += 1 # the index of culling ratio
                      Dt[tfname][tbs][k]['rp'] = float(lit[m]) # Dt[family name][breeding stage][kth DNA test]['rp']: remaining proportion                   

    return s,f,tc,mc,Dt 


#--------------------------------------------------------------------------------------------------------------------
def cal_TSSsize(s, f, Dt):
    
    # calculate number of seedlings in each stage of TSS
    # assign original family size to the firs breeding stage
    ts1 = s['skey'][0] # temp name of the first stage
    s[ts1]['total'] = {}
    s[ts1]['total']['Ts'] = 0 # TSS start total size in stage 0
    s[ts1]['total']['Te'] = 0 # TSS end total size in stage 0
    s[ts1]['total']['Ms'] = 0 # MASS start total size in stage 0
    s[ts1]['total']['Me'] = 0 # MASS end total size in stage 0
    for i in range(f['fNo']):
        s[ts1][f['fkey'][i]] = {} # s[breeding stage][family name], lit[ 1 + i] is the family name
        s[ts1][f['fkey'][i]]['Tfs'] = f[f['fkey'][i]]['size'] # start family size in the first stage
        s[ts1][f['fkey'][i]]['Tfe'] = s[ts1][f['fkey'][i]]['Tfs'] * s[ts1]['trp'] # edning family size in the first stage
        s[ts1][f['fkey'][i]]['Mfs'] = s[ts1][f['fkey'][i]]['Tfs'] # MASS starting family size for the first stage equals to TSS  
        s[ts1][f['fkey'][i]]['Mfe'] = s[ts1][f['fkey'][i]]['Tfe'] # MASS ending family size for the first stage equals to TSS
        
        s[ts1]['total']['Ts'] = s[ts1]['total']['Ts'] + s[ts1][f['fkey'][i]]['Tfs']
        s[ts1]['total']['Te'] = s[ts1]['total']['Te'] + s[ts1][f['fkey'][i]]['Tfe']
        s[ts1]['total']['Ms'] = s[ts1]['total']['Ms'] + s[ts1][f['fkey'][i]]['Mfs']
        s[ts1]['total']['Me'] = s[ts1]['total']['Me'] + s[ts1][f['fkey'][i]]['Mfe']
    # calculate number of seedlings in each stage of TSS
    m = 1 # count the index in skey
    for stage in s['skey'][1:]:
        # define dictionaries s[breeding stage name]['total']['stsize'],['etsize']
        s[stage]['total'] = {}
        s[stage]['total']['Ts'] = 0 # TSS total size in the beginning of a breeding stage  
        s[stage]['total']['Te'] = 0 # TSS total size in the end of a breeding stage
        s[stage]['total']['Ms'] = 0 # MASS total size in the beginning of a breeding stage  
        s[stage]['total']['Me'] = 0 # MASS total size in the end of a breeding stage
        for family in f['fkey']: # m takes on family names in order
            s[stage][family] = {} # define dictionaries s[breeding stage name][family name]
            s[stage][family]['Tfs'] = 0 # TSS family size in the beginning of breeding stage skey[i]
            s[stage][family]['Tfe'] = 0 # TSS family size in the end of breeding stage skey[i]
            s[stage][family]['Mfs'] = 0 # MASS family size in the beginning of breeding stage skey[i]
            s[stage][family]['Mfe'] = 0 # MASS family size in the end of breeding stage skey[i]            

            # calculate TSS start, end family size
            s[stage][family]['Tfs'] = s[s['skey'][m-1]][family]['Tfe']
            s[stage][family]['Tfe'] = round(s[stage][family]['Tfs'] * s[stage]['trp'])
            
            # caluculate MASS start, end family size
            s[stage][family]['Mfs'] = s[s['skey'][m-1]][family]['Mfe']
            
            if Dt[family][stage]['Dt_No'] == 0: # there is no DNA test in the stage, family
                s[stage][family]['Mfe'] = round(s[stage][family]['Mfs'] * s[stage]['trp'])
            else: # there is DNA test in the stage, family
                s[stage][family][0] = {}
                s[stage][family][0]['Dfs'] = s[stage][family]['Mfs'] # MASS family size in the beginning of kth DNA test
                s[stage][family][0]['Dfe'] = round(s[stage][family][0]['Dfs'] * Dt[family][stage][0]['rp'])
                endDsize = s[stage][family][0]['Dfe'] # endDsize: family size in the end of DNA tests in a stage
                
                for k in range(1,Dt[family][stage]['Dt_No']):
                    s[stage][family][k] = {}
                    s[stage][family][k]['Dfs'] = round(s[stage][family][k-1]['Dfe'])
                    s[stage][family][k]['Dfe'] = round(s[stage][family][k]['Dfs'] * Dt[family][stage][k]['rp'])# MASS family size in the beginning of kth DNA test
                    endDsize = s[stage][family][k]['Dfe']
                 

                s[stage][family]['Mfe'] = round(endDsize * s[stage]['trp'])
                    
            
            # calculate start, end total size
            s[stage]['total']['Ts'] = s[stage]['total']['Ts'] + s[stage][family]['Tfs']
            s[stage]['total']['Te'] = s[stage]['total']['Te'] + s[stage][family]['Tfe']
            s[stage]['total']['Ms'] = s[stage]['total']['Ms'] + s[stage][family]['Mfs']
            s[stage]['total']['Me'] = s[stage]['total']['Me'] + s[stage][family]['Mfe']
        m += 1
    return s
#--------------------------------------------------------------------------------------------------------------------
def cal_TSScost(s, f, tc, mc):
    tc['total'] = 0 # total TSS cost
    mc['tradi'] = {} # traditional cost in MASS
    mc['tradi']['total'] = 0 # total traditional cost in all breeding stages in MASS
    mc['DNAtesting'] = 0 # DNA testing cost in MASS
    
    # calculate traditional cost
    for i in s['skey']: # skey is the list of breeding stage names, i will take on different breeding stage names in order
        mc['tradi'][i] = {}
        mc['tradi'][i]['tcost'] = 0 # total traditional cost in a breeding stage in MASS
        for j in tc[i]['cost name']: # c[breeding stage name].keys = cost names in each breeding stage. j will take on different cost names in one breeding stage
            for k in range(tc[i][j]['rangeNo']): # k is from 0 to range number in that cost name-1, the loop cycles for 'range number' times
                if s[i]['total']['Ts'] >= tc[i][j][k]['low'] and (tc[i][j][k]['high'] < 0 or s[i]['total']['Ts'] <= tc[i][j][k]['high']):
                    if tc[i][j][k]['unit'] == '$':
                        tc[i]['tcost'] = tc[i]['tcost'] + tc[i][j][k]['price']
                    else:
                        tc[i]['tcost'] = tc[i]['tcost'] + s[i]['total']['Ts'] * tc[i][j][k]['price']
                if s[i]['total']['Ms'] >= tc[i][j][k]['low'] and (tc[i][j][k]['high'] < 0 or s[i]['total']['Ms'] <= tc[i][j][k]['high']):
                    if tc[i][j][k]['unit'] == '$':
                        mc['tradi'][i]['tcost'] = mc['tradi'][i]['tcost'] + tc[i][j][k]['price']
                    else:
                        mc['tradi'][i]['tcost'] = mc['tradi'][i]['tcost'] + s[i]['total']['Ms'] * tc[i][j][k]['price']
                                           
        
        tc['total'] = tc['total'] + tc[i]['tcost']
        mc['tradi']['total'] = mc['tradi']['total'] + mc['tradi'][i]['tcost']
    
    # Calculate cost composition
    for ttype in s['ctype']: # ttype: temporary variable for a cost type
        tc['ctype'][ttype] = 0
        mc['ctype'][ttype] = 0
    
    for stage in s['skey']: # skey is the list of breeding stage names, i will take on different breeding stage names in order
        for costname in tc[stage]['cost name']: # c[breeding stage name].keys = cost names in each breeding stage. j will take on different cost names in one breeding stage
            ttype = tc[stage][costname]['type'] # a temporaty variable to record the cost type for a cost name, in one stage of a family
            for k in range(tc[stage][costname]['rangeNo']): # k is from 0 to range number in that cost name-1, the loop cycles for 'range number' times
                if s[stage]['total']['Ts'] >= tc[stage][costname][k]['low'] and (tc[stage][costname][k]['high'] < 0 or s[stage]['total']['Ts'] <= tc[stage][costname][k]['high']):
                    
                    if tc[stage][costname][k]['unit'] == '$':
                        tc['ctype'][ttype] = tc['ctype'][ttype] + tc[stage][costname][k]['price']
                        
                    else:
                        tc['ctype'][ttype] = tc['ctype'][ttype] + s[stage]['total']['Ts'] * tc[stage][costname][k]['price']
                        
                if s[stage]['total']['Ms'] >= tc[stage][costname][k]['low'] and (tc[stage][costname][k]['high'] < 0 or s[stage]['total']['Ms'] <= tc[stage][costname][k]['high']):
                    if tc[stage][costname][k]['unit'] == '$':
                        mc['ctype'][ttype] = mc['ctype'][ttype] + tc[stage][costname][k]['price']
                        
                    else:
                        mc['ctype'][ttype] = mc['ctype'][ttype] + s[stage]['total']['Ms'] * tc[stage][costname][k]['price']

    return tc, mc
#--------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------
def cal_DANcost(tc, s, f, mc, Dt): # calculate DNA testing cost
    mc['Dt_c']['cost'] = 0 # DNA test cost for all stages, all families
    # ----------[family name][stage name]['cost']
    # ----------[family name][stage name][DNAtname]['cost']
    for tstage in s['skey']:
            mc[tstage] = {}
            mc[tstage]['Dt_c'] = 0 # DNA testing cost in each breeding stage
            
    for tfamily in f['fkey']:
        mc['Dt_c'][tfamily] = {}
        mc['Dt_c'][tfamily]['cost'] = 0 # DNA test cost for a family, all stages
        for tstage in s['skey']:
            mc['Dt_c'][tfamily][tstage] = {}
            mc['Dt_c'][tfamily][tstage]['cost'] = 0 # DNA test cost for a family in a stage
            
            for i in range(Dt[tfamily][tstage]['Dt_No']): # ith DNA test in a stage, family
                tDname = Dt[tfamily][tstage][i]['Dt_name'] # DNA test name in a stage, family
                
                for j in range(mc['Dt_c'][tDname]['sourceNo']): # jth cost source of a DNA test
                    tcost_name = mc['Dt_c'][tDname]['ckey'][j] # jth cost name
                    
                    for k in range(mc['Dt_c'][tDname][tcost_name]['rangeNo']): # kth range in a cost
                        tsize = s[tstage][tfamily][i]['Dfs']
                        tlow = mc['Dt_c'][tDname][tcost_name][k]['low']
                        thigh = mc['Dt_c'][tDname][tcost_name][k]['high']
                        
                        if tsize >= tlow and(tsize <= thigh or thigh < 0):
                            if mc['Dt_c'][tDname][tcost_name][k]['unit'] == '$':
                                mc['Dt_c'][tfamily][tstage]['cost']= mc['Dt_c'][tfamily][tstage]['cost'] + mc['Dt_c'][tDname][tcost_name][k]['price']
                                
                                
                            else:
                                mc['Dt_c'][tfamily][tstage]['cost']= mc['Dt_c'][tfamily][tstage]['cost'] + mc['Dt_c'][tDname][tcost_name][k]['price'] * s[tstage][tfamily][i]['Dfs']
            
            mc[tstage]['Dt_c'] += mc['Dt_c'][tfamily][tstage]['cost']
                                         

                                
            
            mc['Dt_c'][tfamily]['cost'] = mc['Dt_c'][tfamily]['cost'] + mc['Dt_c'][tfamily][tstage]['cost']
   
        mc['Dt_c']['cost'] = mc['Dt_c']['cost'] + mc['Dt_c'][tfamily]['cost']
    
     # calculate total MASS cost
    mc['DNAtesting'] = mc['Dt_c']['cost']
    mc['total'] = mc['tradi']['total'] + mc['DNAtesting']
    mc['save$'] = tc['total'] - mc['total']
    mc['save%'] = (tc['total'] - mc['total'])/tc['total'] * 100
    
    return mc                   
                        
    
#--------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------
# write output into a csv file
def print_csv(outfile2, s, f, tc, mc, Dt):
    import csv

    with outfile2 as csvfile:
        output = csv.writer(csvfile, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)
        output.writerow(['Name of the breeding program', s['bpname']])
        output.writerow([])
        # print summary of breeding stages
        output.writerow(['Summary of breeding stages'])
        output.writerow(['Breeding stage','Starting month','Ending month', 'potential loss reason', 'potential loss percentage'])
        wstring = [] # temporary row string
        for i in range(s['sNo']):
            wstring = [s['skey'][i]]
            wstring.append(s[s['skey'][i]]['sdate'])
            wstring.append(s[s['skey'][i]]['edate'])

            for j in range(len(s[s['skey'][i]]['lr'])):
                wstring.append(s[s['skey'][i]]['lr'][j])
                wstring.append(s[s['skey'][i]]['rp'][j])
            output.writerow(wstring)                                 
                             
        # print the summary of family structure
        output.writerow([])
        output.writerow(['Summary of family structure'])
        output.writerow(['Number of families', f['fNo']])
        output.writerow(['Family name', 'Father', 'Mother', 'Original seedling number'])

        for i in range(f['fNo']):
            output.writerow([f['fkey'][i], f[f['fkey'][i]]['fname'], f[f['fkey'][i]]['mname'], f[f['fkey'][i]]['size']])

        # print TSS cost information
        output.writerow([])
        output.writerow(['Summary of TSS cost structure'])
        output.writerow(['Breeding stage', 'Cost reason', 'Lower bound', 'Higher bound', 'Cost', 'Cost unit'])
        for i in range(s['sNo']):
            wstring = [s['skey'][i]] # temporary array to write in one row of the csv file
            for j in tc[s['skey'][i]]['cost name']: # j is a list of cost names
                wstring.append(j)
                for k in range(tc[s['skey'][i]][j]['rangeNo']):
                    if tc[s['skey'][i]][j][k]['high'] > 0:
                        wstring.append(tc[s['skey'][i]][j][k]['low'])
                        wstring.append(tc[s['skey'][i]][j][k]['high'])
                        wstring.append(tc[s['skey'][i]][j][k]['price'])
                        wstring.append(tc[s['skey'][i]][j][k]['unit'])
                    else:
                        wstring.append(tc[s['skey'][i]][j][k]['low'])
                        wstring.append('Inf')
                        wstring.append(tc[s['skey'][i]][j][k]['price'])
                        wstring.append(tc[s['skey'][i]][j][k]['unit'])                         

            output.writerow(wstring)

            
        #print DNA test cost information
        output.writerow([])
        output.writerow(['Summary of DNA test cost information'])
        for i in mc['Dt_c']['Dtkey']: # i takes on every DNA test name
            wstring = ([i])
            for j in mc['Dt_c'][i]['ckey']: # j takes on every cost name in a DNA test
                wstring.append(j)
                for k in range(mc['Dt_c'][i][j]['rangeNo']):
                    if mc['Dt_c'][i][j][k]['high'] >= 0:
                        wstring.append(mc['Dt_c'][i][j][k]['low'])
                        wstring.append(mc['Dt_c'][i][j][k]['high'])
                        wstring.append(mc['Dt_c'][i][j][k]['price'])
                        wstring.append(mc['Dt_c'][i][j][k]['unit'])
                    else:
                        wstring.append(mc['Dt_c'][i][j][k]['low'])
                        wstring.append('Inf')
                        wstring.append(mc['Dt_c'][i][j][k]['price'])
                        wstring.append(mc['Dt_c'][i][j][k]['unit'])
                output.writerow(wstring)

        # print DNA test information
        output.writerow([])
        output.writerow(['Summary of DNA test information'])
        output.writerow(['Family name', 'Stage name', 'DNA test name','Remaining ratio', 'Starting size'])
             
        for i in f['fkey']:
            wstring = []
            for j in s['skey']:
                if Dt[i][j]['Dt_No'] != 0:
                    #wstring = ([i])
                    wstring.append(i)
                    wstring.append(j)
                for k in range(Dt[i][j]['Dt_No']):
                    wstring.append(Dt[i][j][k]['Dt_name'])
                    wstring.append(Dt[i][j][k]['rp'])
                    wstring.append(s[j][i][k]['Dfs'])
            if wstring:
                output.writerow(wstring)

        # print results
        output.writerow([])
        output.writerow(['Output I: population size in each stage'])
        # print title row
        wstring =['TSS']
        for i in f['fkey']:
            
            tstageT = i
            wstring.append(tstageT)
        wstring.append('Total')
        
        wstring.append(' ')
        wstring.append('MASS')
        for i in f['fkey']:
            
            tstageM = i
            wstring.append(tstageM)
        wstring.append('Total')
        
        wstring.append(' ')
        wstring.append('Decrease in MASS')
        for i in f['fkey']:
            
            tstageM = i
            wstring.append(tstageM)
        wstring.append('Total')
                
        output.writerow(wstring)
        
        #print population size in each stage
        for j in range(s['sNo']):
            wstring = ([s['skey'][j]])
            for m in f['fkey']:
                wstring.append(int((s[s['skey'][j]][m]['Tfs']))) # print family TSS size, MASS size in that stage
                                
            wstring.append(int(s[s['skey'][j]]['total']['Ts'])) # print total TSS size in that stage
            wstring.append(' ')
            wstring.append(s['skey'][j])
            
            for m in f['fkey']:
                wstring.append(int((s[s['skey'][j]][m]['Mfs']))) # print family MASS size in that stage
                
            wstring.append(int(s[s['skey'][j]]['total']['Ms'])) # print total MASS size in that stage
            wstring.append(' ')
            wstring.append(s['skey'][j])
            
            for m in f['fkey']:
                wstring.append(int((s[s['skey'][j]][m]['Mfs'])) - int((s[s['skey'][j]][m]['Tfs']))) # print decrease in MASS compared to TSS
                
            wstring.append(int(s[s['skey'][j]]['total']['Ms']) - int(s[s['skey'][j]]['total']['Ts'])) # print total size decrease in MASS in that stage
            
            output.writerow(wstring)
            
        # print cost information in each stage
        output.writerow('')
        wstring = (['Output II: costs in each stage'])
        output.writerow(wstring)
        
        # print the title row
        wstring = ([' '])
        wstring.append('TSS costs($)')
        wstring.append('MASS non-DNA testing costs($)')
        wstring.append('MASS DNA testing costs($)')
        wstring.append('MASS costs($)')
        output.writerow(wstring)
        
        # print cost numbers
        for j in range(s['sNo']):
            wstring = ([s['skey'][j]])
            wstring.append(round(tc[s['skey'][j]]['tcost'])) # print total TSS cost in that stage
            wstring.append(round(mc['tradi'][s['skey'][j]]['tcost'])) # print MASS non-DNA testing cost in that stage
            wstring.append(round(mc[s['skey'][j]]['Dt_c']))
            wstring.append(round(mc['tradi'][s['skey'][j]]['tcost']) + round(mc[s['skey'][j]]['Dt_c']))
            output.writerow(wstring)
        
        wstring = ['Total TSS cost']
        wstring.append(round(tc['total']))
        wstring.append(' ')
        wstring.append('Total MASS costs')
        wstring.append(round(mc['tradi']['total']))
        
        output.writerow(wstring)
        
       
        # print cost composition of TSS and MASS
        output.writerow([''])
        output.writerow(['Cost composition'])
        wstring = (['Cost type','TSS cost ($)', 'MASS cost ($)'])
        output.writerow(wstring)
        for ttype in s['ctype']:
            wstring = ([ttype,round(tc['ctype'][ttype]), round(mc['ctype'][ttype])])
            output.writerow(wstring)
        
        wstring = ['DNA testing', '0', round(mc['Dt_c']['cost'])]
        output.writerow(wstring)
                        
        wstring = ['Total cost', round(tc['total']), round(mc['total'])]
        output.writerow(wstring)
        
        output.writerow(' ')
        
        # print cost saving from MASS
        #tsaving = tc['total'] - mc['total']
        #tsavingp = tsaving/tc['total'] * 100
        output.writerow('')
        output.writerow(['Total saving'])
        wstring = ['Saving from using MASS ($)', mc['save$']]
        output.writerow(wstring)
        wstring = ['Saving from using MASS (%)', int(mc['save%'])]
        output.writerow(wstring)
        
######------------------------------------------------------------------------------------------------------------#####
def costcomp(s, f, tc, mc, Dt): # the graph of cost comparison
    # graph cost composition of TSS and MASS
    import numpy as np
    import numpy
    import matplotlib.pyplot as plt
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Pring cost comparison between MASS and TSS
    # creat the data matrix
    i = 0
    for ttype in s['ctype']:
        if i == 0:
            data = [round(tc['ctype'][ttype]), round(mc['ctype'][ttype])]
            
        else:
            data = numpy.vstack([data, [round(tc['ctype'][ttype]), round(mc['ctype'][ttype])]])
        i += 1
    data = numpy.vstack([data, [0, round(mc['DNAtesting'])]])
    
               
    columns = ('TSS', 'MASS')
    rows = s['ctype'] + ['DNA testing']
    
    tvalue = max(tc['total'], mc['total']) # temporary maximum value of tc and mc total cost, to estimate the y axis range
    
    # Get some pastel shades for the colors
    
    colors = plt.cm.Pastel1(np.linspace(0, 0.5, len(rows)))
    n_rows = len(data)

    index = np.arange(len(columns)) + 0.3
    bar_width = 0.4

    # Initialize the vertical-offset for the stacked bar chart.
    y_offset = np.array([0.0] * len(columns))
    # Plot bars and create text labels for the table
    cell_text = []
    for row in range(n_rows):
        
        plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
        y_offset = y_offset + data[row]
        
        cell_text.append(['%d' % (x) for x in data[row]])
        
    # Reverse colors and text labels to display the last value at the top.
    colors = colors[::-1]
    cell_text.reverse()
    rows.reverse()

    # Add a table at the bottom of the axes
    the_table = plt.table(cellText= cell_text,
                      rowLabels=rows,
                      rowColours=colors,
                      colLabels=columns,
                      loc='bottom')
    cellDict = the_table.get_celld()
    tlength = len(cellDict)
    trow = (tlength + 1 )/3
    
    cellDict[(0,0)].set_height(0.08)
    cellDict[(0,1)].set_height(0.08)
    for i in range(1, trow):
        cellDict[(i, -1)].set_height(0.05)
        cellDict[(i, 0)].set_height(0.05)
        cellDict[(i, 1)].set_height(0.05)
        #print(i)
        #i.set_height(0.05)
        
    # Adjust layout to make room for the table:
    plt.subplots_adjust(left=0.2, bottom=0.25)

    plt.ylabel("Costs ($)")
    plt.ylim(ymax = tvalue + round(tvalue/500) * 100)
    
    plt.text(index[0], tc['total'] * 21/20, 'Total: %d $'%int(tc['total']), fontdict = None, withdash = False)
    plt.text(index[1], mc['total'] * 21/20, 'Total: %d $'%int(mc['total']), fontdict = None, withdash = False)
    
    plt.text(0.5,0.99, 'Cost saving: %d $ (%d %s)'%(int(mc['save$']),int(mc['save%']), '%'), horizontalalignment = 'center', verticalalignment = 'top', transform = ax.transAxes)
    
    #plt.text(index[0.5], tvalue, 'Cost saving: %d $'% int(mc['save$']))
    plt.xticks([])
    plt.legend()
    plt.title('Cost comparison between TSS and MASS')
    
    #plt.show()
    plt.savefig('Cost_Comparison.png')
    plt.close()
###--------------------------------------------------------------------------------------------------    
def populationsize(s, f, tc, mc, Dt): # graph of family sizes in MASS and TSS
    import numpy as np
    import numpy
    import matplotlib.pyplot as plt
    #from matplotlib.backends.backend_pdf import PdfPages
       
    
    # Pring family size in TSS and MASS
    # creat the data matrix
    tno = [] # a list of TSS family size in each month
    mno = [] # a list of MASS family size in each month
    month = [] # a list of months throughout seedling selection
    colors = plt.cm.jet(np.linspace(0, 0.5, len(s['skey'])))
    arrowstage = []# the stage with DNA test
   
    
    for i in range(len(s['skey'])):
        
        tstage = s['skey'][i]
        if i == 0:
            plt.ylim(ymax = s[tstage]['total']['Ts'], ymin = 0)
            tnextstage = s['skey'][i + 1]
            p1a, = plt.plot([s[tstage]['scode'], s[tnextstage]['scode']],[s[tstage]['total']['Ts'], s[tnextstage]['total']['Ts']],color = colors[i], lw = 3)
            p1b, = plt.plot([s[tstage]['scode'], s[tnextstage]['scode']],[s[tstage]['total']['Ms'], s[tnextstage]['total']['Ms']],'--', color = colors[i], lw = 3)
                    
        if i < len(s['skey']) - 1:
            tnextstage = s['skey'][i + 1]
            
            plt.plot([s[tstage]['scode'], s[tnextstage]['scode']],[s[tstage]['total']['Ts'], s[tnextstage]['total']['Ts']],color = colors[i], lw = 3)
            plt.plot([s[tstage]['scode'], s[tnextstage]['scode']],[s[tstage]['total']['Ms'], s[tnextstage]['total']['Ms']],'--', color = colors[i], lw = 3)
        if i == len(s['skey']) - 1:
            plt.plot([s[tstage]['scode'], s[tstage]['ecode']],[s[tstage]['total']['Ts'], s[tstage]['total']['Te']], color = colors[i], lw = 3)
            plt.plot([s[tstage]['scode'], s[tstage]['ecode']],[s[tstage]['total']['Ms'], s[tstage]['total']['Me']], '--', color = colors[i], lw = 3)
            
        for tfamily in (f['fkey']):
            if Dt[tfamily][tstage]['Dt_No'] != 0:
                arrowstage.append(tstage)
                                            
        plt.axvline(x = s[tstage]['scode'], color = (0,0,0,0.2))
    
    xmin = plt.axis()[0]
    ymax = plt.axis()[3] 
    ymin = plt.axis()[2] # the minimum value on the y axis
    
    
    plt.text(xmin,(ymax * 101 / 100),r'$\uparrow DNA test$', color = 'r')
    
    for tstage in arrowstage:
        plt.text(s[tstage]['scode'], ymin -100, r'$\uparrow$', fontsize = 30, color = 'r')
        #print ymin
        
    for tstage in s['skey']:
        plt.text(s[tstage]['scode'], ymin, tstage[0:3], verticalalignment='bottom',rotation = 45)
    
    plt.title('Seedling population size in TSS and MASS')
    plt.ylabel("Seedling population size")
    plt.xlabel("Time(month)")
    
    plt.legend([p1a, p1b], ['TSS','MASS'])
      
    #plt.show()
    plt.savefig('Population_Size.png')
    plt.close()
    
###-------------------------------------------------------------------
def familysize(s, f, tc, mc, Dt): # graph of family size
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.collections import PolyCollection
    from matplotlib.colors import colorConverter
    import matplotlib.pyplot as plt
    import numpy as np
    #import numpy
    
    maxy = s[s['skey'][0]][f['fkey'][0]]['Tfs'] # calculate the maximum family size for the y axis
    
    for tfamily in f['fkey']:
        tmaxy = s[s['skey'][0]][tfamily]['Tfs']
        if tmaxy >= maxy:
            maxy = tmaxy
             
        
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)
    tmonth = s[s['skey'][-1]]['ecode']
    
    
    verts = []
    verts2 = []
    zs = []
    zs2 = []
    
    for i in range(1, f['fNo'] + 1):
        zs.append(i- 0.0001)
        zs2.append(i)
    
     
    #colors = plt.cm.gist_rainbow(np.linspace(0, 0.5, (len(s['skey']))))
    #colors = [cc('k'), cc('r'), cc('k'), cc('g'), cc('k'), cc('b'), cc('k'), cc('y'),  cc('k'), cc('c'), cc('k'), cc('m'), cc('k'), cc('r'), cc('k'), cc('g'), cc('k'), cc('b'), cc('k'), cc('y'),  cc('k'), cc('c'), cc('k'), cc('m')]
    colors = ['#FF0000', '#40FF00', '#00FFFF', '#0101DF', '#FFFF00', '#FF00FF', '#6E6E6E']
    colors2 = ['#F6CECE', '#FBFBEF', '#FBFBEF', '#FBFBEF', '#FBFBEF', '#FBFBEF', '#FBFBEF']
    
    for tfamily in f['fkey']:
        xs = [0.999999] 
        ys = [0]
        for i in range(len(s['skey'])):
            tstage = s['skey'][i]
            xs.append(s[tstage]['scode'])
            ys.append(s[tstage][tfamily]['Mfs'])
            
            if i == len(s['skey']):
                xs.append(s[tstage]['ecode'])
                ys.append(s[tstage][tfamily]['Mfe'])
           
        xs.append(s[tstage]['ecode']+0.0000001)
        ys.append(0)
              
        verts.append(list(zip(xs, ys)))
        
        xs2 = [0.999999] 
        ys2 = [0]
        for i in range(len(s['skey'])):
            tstage = s['skey'][i]
            xs2.append(s[tstage]['scode'])
            ys2.append(s[tstage][tfamily]['Tfs'])
            
            
            if i == len(s['skey']):
                xs2.append(s[tstage]['ecode'])
                ys2.append(s[tstage][tfamily]['Tfe'])  
        
        xs2.append(s[tstage]['ecode']+0.0000001)
        ys2.append(0)
        
        verts2.append(list(zip(xs2, ys2)))
    
    poly = PolyCollection(verts, edgecolors = colors[0: f['fNo']], facecolors = colors[0: f['fNo']])
    #poly.set_alpha(0.9)
    
    poly2 = PolyCollection(verts2, facecolors = colors2[0: f['fNo']])
    poly2.set_alpha(0.3)
    
    ax.add_collection3d(poly, zs=zs, zdir='y')
    ax.add_collection3d(poly2, zs=zs2, zdir='y')
    
    ax.set_xlabel('Time (month)')
    txtick = (int(tmonth/20)) * 20
    ax.set_xticks(range(0, tmonth, int(txtick/4)))
    
    ax.set_xlim3d(0, tmonth)
    
    ax.set_ylabel('Families')
    ax.set_ylim3d(0, f['fNo'])
    ax.set_zlabel('Population size')
    ax.set_zlim3d(0, maxy)
    ax.view_init(elev = 10, azim = -20)
    ax.set_yticks(zs2)
    
    plt.title('Family size in MASS and TSS')

    #plt.show()
    plt.savefig('Family_Size.png')
    plt.close()   

#--------------------------------------------------------------------------------
        
    
# execute main() function
main()














        
    
        
