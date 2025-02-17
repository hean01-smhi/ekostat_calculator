# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 10:10:50 2018

@author: a002028
"""

import pandas as pd
import utils

"""
#==============================================================================
#==============================================================================
"""
def check_lists_in_dict(filter_dict, use_string=False):
    for key in filter_dict:
        if not utils.is_sequence(filter_dict[key]):
            if type(filter_dict[key]) == str and use_string:
                pass
            else:
                filter_dict[key] = [filter_dict[key]]
    return filter_dict

#==============================================================================
#==============================================================================
def get_boolean_from_interval(df=None, key='', interval=[]):
    """
    Assumes interval is a list of two float/int values and that lists in df are 
    of type float/int 
    """
    if type(interval)==str:
        interval = list(map(float, interval.split('-')))
        if len(interval)!=2:
            raise UserWarning('Filter interval is incorrect for key:',key,'interval:',interval)

    return (df[key] >= interval[0]) & (df[key] <= interval[1])

#==============================================================================
#==============================================================================
def get_ordered_list(dict_keys={}, list_keys=[]):
    ordered_list = [key for key in dict_keys if key not in list_keys]
    for key in list_keys:
        ordered_list.append(key)
    return ordered_list

#==============================================================================
#==============================================================================
def set_filter(df=None, filter_dict={}, interval_keys=[], logical_or_key=[], return_dataframe=False, use_string=False):
    """
    df: pandas.DataFrame
    filter_dict: { key1: [x], key2: [x,y,z] }
    interval_keys: keys with value list will be handled as intervals
                   filter_dict[key] = [value_from, value_to] or as string 'value_from-value_to'
    logical_key: if key in list, combined_boolean OR boolean from key is used.. (to be tested and evaluated / extended.. ).. sort order of loop ?
    return_dataframe: return as dataframe, else boolean
    """
    loop_list = get_ordered_list(dict_keys=filter_dict, 
                                 list_keys=logical_or_key)
    
    filter_dict = check_lists_in_dict(filter_dict, use_string=use_string)
    
    combined_boolean = ()
    
    for key in loop_list: 
        
#        key = key.upper()
        
        if key not in df: 
            continue
        
        if key in interval_keys:
            
            boolean = get_boolean_from_interval(df=df, 
                                                key=key, 
                                                interval=filter_dict.get(key))
        else:
            boolean = df[key].isin(filter_dict.get(key))
            
#        if not type(boolean) == pd.Series:
#            continue

        if type(combined_boolean) == pd.Series:
            if key in logical_or_key:
                combined_boolean = combined_boolean | boolean
            else:
                combined_boolean = combined_boolean & boolean
        else:
            combined_boolean = boolean 
 
    if return_dataframe:
        return df.loc[combined_boolean,:]
    else:
        return combined_boolean
    
#==============================================================================
#==============================================================================

if __name__ == '__main__':
    print('='*50)
    print('Running module "filter_dataframe.py"')
    print('-'*50)
    print('')
    
    df = pd.DataFrame({'a':range(10), 'b':range(10), 'c':range(10)})
    
    df = set_filter(df=df, 
                    filter_dict={'a':[2,3,4], 'c':'3-7', 'b':[5,9]}, 
                    use_string=True,
                    interval_keys=['b','c'],
                    logical_or_key=['a'],
                    return_dataframe=True)

    print(df)
    
    print('-'*50)
    print('done')
    print('-'*50)