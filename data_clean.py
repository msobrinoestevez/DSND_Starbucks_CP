import pandas as pd
import numpy as np
import math

def portfolio_data_clean(portfolio):
    """
    INPUT: portfolio df provided
    
    OUTPUT: portfolio df cleaned:
        1. rename id column to offerid
        2. one hot encode the offer_type column
        3. one hot encode the channels column + previous channel column dropped
    """
    portfolio_clean = portfolio.copy()
    #rename id to offerid
    portfolio_clean = portfolio_clean.rename(columns={'id': 'offerid'})
    #ohe of offer_type and channels variable
    dummy_channels = pd.get_dummies(portfolio_clean.channels.apply(pd.Series).stack(),prefix="channel").sum(level=0)
    dummy_offer_type = pd.get_dummies(portfolio_clean.offer_type.apply(pd.Series).stack(),prefix="offer").sum(level=0)
    #concat dummy variables
    portfolio_clean = pd.concat([portfolio_clean,dummy_channels, dummy_offer_type], axis=1)
    #drops channels column
    portfolio_clean = portfolio_clean.drop('channels',axis=1)
    
    return portfolio_clean    


def profile_data_clean(profile):
    """
    INPUT: profile df provided
    
    OUTPUT: portfolio df cleaned:
        1. rename id column to customerid
        2. one hot encode the gender column
        3. drop rows with null values on income and gender variables (those with 118 in age variable)
        4. convert became_member_on to datetime values.
        5. one hot encode new year_became_member variable.
        6. one hot encode new weekday_became_member variable.
        7. split ages in 10 years bins and one hot encode it
    
    """
    profile_clean = profile.copy()
    #rename id to offerid
    profile_clean = profile_clean.rename(columns={'id': 'customerid'})
    #drop null income (and gender) null values
    profile_clean = profile_clean[profile.income.notnull()]
    #add datetime values
    profile_clean['became_member_on'] = pd.to_datetime(profile['became_member_on'].astype(str), format='%Y%m%d')
    profile_clean['year_became_member'] = profile_clean['became_member_on'].dt.year
    profile_clean['month_became_member'] = profile_clean['became_member_on'].dt.month
    profile_clean['weekday_became_member'] = profile_clean['became_member_on'].dt.weekday
    #add datetime categorical values
    profile_clean['weekday_became_member_cat'] = profile_clean['weekday_became_member'].map({0: 'Mon', 1 : 'Tue', 
                                                             2 : 'Wed', 3 : 'Thu', 
                                                             4 : 'Fri', 5 : 'Sat' , 6 : 'Sun'})

    profile_clean['month_became_member_cat'] = profile_clean['month_became_member'].map({1: 'Jan', 2 : 'Feb', 3: 'Mar', 
                                                     4: 'Apr', 5 : 'May',  6 : 'Jun',
                                                     7 : 'Jul', 8 : 'Aug' , 9 : 'Sep',
                                                     10 : 'Oct', 11 : 'Nov' , 12 : 'Dec'})

    profile_clean['weekday_became_member_cat'] = pd.Categorical(profile_clean['weekday_became_member_cat'], categories=['Mon','Tue','Wed','Thu','Fri','Sat', 'Sun'], ordered=True)
    profile_clean['month_became_member_cat'] = pd.Categorical(profile_clean['month_became_member_cat'], categories = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ordered=True)
    #split ages in 10 years bins and then ohe it
    labels = ['11-20','21-30','31-40','41-50','51-60','61-70','71-80','81-90','91-100','100-110']
    bins = np.arange(10, profile['age'].max(), 10)
    profile_clean['age_bins'] = pd.cut(profile_clean['age'], bins=bins, labels=labels)
    #ohe of gender
    dummy_gender = pd.get_dummies(profile_clean.gender.apply(pd.Series).stack(),prefix="gender").sum(level=0)
    #ohe of year become member new variable
    dummy_year = pd.get_dummies(profile_clean.year_became_member.apply(pd.Series).stack(),prefix="year_bm").sum(level=0)
    #ohe of age_bins variable
    dummy_age_bins = pd.get_dummies(profile_clean['age_bins'])
    #ohe of weekday_became_member variable
    dummy_weekday = pd.get_dummies(profile_clean['weekday_became_member_cat'], prefix="weekda_bm")   
    #concat dummy variables
    profile_clean = pd.concat([profile_clean, dummy_gender, dummy_year, dummy_age_bins, dummy_weekday], axis=1)
        
    return profile_clean  


def transcript_data_clean(transcript,profile_clean):
                
    """
    INPUT: transcript df provided
    
    OUTPUT: offer_data and transaction_data
        1. rename person column to customerid
        2. convert time variable units from hours to days to be consistent with portolio dataset
        3. drop rows of customers that are not contained in profile_clean df
        4. create offerid column (from value variable where events are not equal to transaction)
        5. create amount column (from value variable where events are not equal to transaction)
        6. ohe event
        7. Split transcript_clean dataset in two different datasets:
            7.1. offer_data: offerid|customerid|time|event(ohe)
            7.2. transaction_data customerid|time|amount            
    """
    transcript_clean = transcript.copy()
    cust_profile = list(profile_clean['customerid'])
    
    #rename person to customerid
    transcript_clean = transcript_clean.rename(columns={'person': 'customerid'})
    
    #convert time variable units from hours to days to be consistent with portolio dataset
    transcript_clean['time'] = transcript_clean['time']/24
    
    # drop rows of customers that are not contained in profile_clean df
    transcript_clean = transcript_clean[transcript_clean['customerid'].isin(cust_profile)==True]
    
    #offer_data
    offer_data = transcript_clean[transcript_clean['event'] != 'transaction']
    
    #create offerid column (from value variable where events are not equal to transaction)
    def offerid(x):
        for key,value in x.items():
            if key in ['offer id','offer_id']:
                return str(value)
    
    offer_data['offerid'] = offer_data['value'].apply(offerid)
    
    # ohe event
    dummy_event = pd.get_dummies(offer_data.event.apply(pd.Series).stack()).sum(level=0)
    
    #concat dummy variables
    offer_data = pd.concat([offer_data, dummy_event], axis=1)
    
    offer_data = offer_data[['offerid','customerid','time','offer received','offer viewed','offer completed']]
    
    #transaction_data
    transaction_data = transcript_clean[transcript_clean['event'] == 'transaction']
    
    #create amount column (from value variable where events are equal to transaction)
    
    def amount(x):
        for key,value in x.items():
            if key in ['amount']:
                return value
 
    transaction_data['amount'] = transaction_data['value'].apply(amount)
    
    transaction_data = transaction_data[['customerid','time','amount']]
   
    return offer_data, transaction_data   