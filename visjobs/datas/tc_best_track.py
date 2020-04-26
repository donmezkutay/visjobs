import pandas as pd
import numpy as np

def wrap_tc_data(df):
    """returns adjusted NHC hurricane data
       input NHC hurricane best track data"""
    hur_dict = {}
    index = 0
    used_name = []
    name = 'init'
    count_i = 0
    for i in df['hour']:
        if i[1] == ' ':
            index = count_i
            name=i
            if name in used_name:
                name_extent = 1
                for k in used_name:
                    if name not in used_name:
                        break
                    else:
                        name=i
                        name = name + '{}'.format(name_extent)
                        name_extent+=1

            used_name.append(name)
            value_list = []
            for j in df.iloc[count_i+1:]['hour']:
                value_list.append(df.iloc[index].values)
                index+=1
                if j[1] == ' ' or index == 53217:
                    fill_name = 0
                    for nm in name:
                        if nm == ' ':
                            n = name[fill_name+1:]
                            fill_name+=1

                        else:
                            hur_dict[n] =  value_list 

                    break
        count_i+=1
    return hur_dict

def sep_tc_data(dict_data_w_name, stack = True):
    """input tc data name specified in the dictionary.
       returns seperated variables in time
       if stack = True ; stacked data returned"""
    #get matrix
    stacked = np.vstack(dict_data_w_name[1:])
    
    #check if matrix desired or not
    if stack == True:
        return stacked
    else:
        dates   = stacked[:,0]
        hours   = stacked[:,1]
        Ls      = stacked[:,2]
        types   = stacked[:,3]
        lats    = stacked[:,4]
        lons    = stacked[:,5]
        winds   = stacked[:,6]
        mslp    = stacked[:,7]

        return dates, hours, Ls, types, lats, lons, winds, mslp
    
def adjust_data_spaces(data_matris):
    copy_matris = np.copy(data_matris)
    count_i = 0
    for i in data_matris:
        count_j = 0
        for j in i:

            j_type = str(type(j))
            if j_type == "<class 'numpy.float64'>" or j_type == "<class 'int'>"  :
                break

            fill_name = 0
            count_nm = 0
            for nm in j:
                if nm == ' ':
                    n = j[fill_name+1:]
                    fill_name+=1
                elif fill_name == 0:
                    break
                else:
                    copy_matris[count_i][count_j] = n

                count_nm += 1
            count_j += 1
        count_i += 1
    return copy_matris

#adjusting lats and lons str to float
def coords_str_to_float(tc_matris):
    copy_tc_data = np.copy(tc_matris)
    count_i = 0
    #for longitude
    for i in copy_tc_data[5]:
        name = float(i[:-1])
        copy_tc_data[5][count_i] = name
        count_i += 1 

    #for latitude
    count_i = 0
    for i in copy_tc_data[4]:
        name = float(i[:-1])
        copy_tc_data[4][count_i] = name
        count_i += 1 
        
    return copy_tc_data


    
    
    