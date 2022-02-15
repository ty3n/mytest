import os,time

def UpdateCaDate(path_file):
    fs = open(path_file).read()                                 
    a = time.gmtime()
    start_year = '%s'%str(a[0])[2:]
  
    start_month = '%02u'%a[1]    
    if a[1] == 1:
        end_month = '12' 
        end_year = '%s'%(int(str(a[0])[2:]) + 19)
         
    else:         
        end_month = '%02u'%(a[1]-1)  
        end_year = '%s'%(int(str(a[0])[2:]) + 20)
    chk_ok = 0
    f_chg = ""
    for i in fs.splitlines():
        #raw_input(i)   
        content_line = i + "\n"
        if "default_startdate" in i:
            t = i.split('=')[-1].strip()[:4]
            if (t[:2] == start_year) and (t[2:4] == start_month): chk_ok +=1  
            start_date = '%s%s01%s'%(start_year,start_month,i.split('=')[-1].strip()[6:])
            content_line = i.split('=')[0] + '= ' + start_date + '\n'
            print content_line
        if  "default_enddate" in i: 
            t = i.split('=')[-1].strip()[:4]
            if (t[:2] == end_year) and (t[2:4] == end_month): chk_ok +=1
            start_date = '%s%s28235959Z'%(end_year,end_month)
            content_line = i.split('=')[0] + '=   ' + start_date + '\n'
            print content_line
        if chk_ok == 2: break
        else: f_chg = f_chg + content_line
        #f_chg = f_chg + content_line
   
    if chk_ok < 2: 
        f = open(path_file,'w')
        f.write(f_chg)
        f.close()
        print "%s : Update CA Date OK..."%path_file
    else: print "%s : Check CA Date OK..."%path_file 
       
        
####  MAIN #####
UpdateCaDate('C:\\HtSignTools\\CA\\EuroHitron.CA\\ca.cfg')
UpdateCaDate('C:\\HtSignTools\\CA\\Hitron.CA\\ca.cfg')
    
    
    
