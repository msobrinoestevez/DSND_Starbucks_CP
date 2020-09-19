
import pandas as pd
import numpy as np

def combine_data(profile_clean, portfolio_clean, offer_data, transaction_data):
   
    """
    For each customer, apply the following algorithm:

    1. Select a customer's profile
    2. Select offer data for a specific customer
    3. Select transactions for a specific customer
    4. Select received, completed, viewed offer data from customer offersr
    5. Iterate over each offer a customer receives
    6. Initialize the current offer id
    7. Look-up a description of the current offer (duration_days)
    8. Select the time when offer was received (start_time)
    9. Calculate time when the offer ends (start_time + duration days)
    10. Initialize boolean arrays that determine if the customer completed an offer between offer period, taking into account view and completed times.
    11. Initialize a boolean array that select customer transactions that fall within the valid offer time window
    12. Sum transactions amount per customer for all those transactions that within the valid offer time window
    13. Convert combined data lists to dataframe
    
    """
    
    data = []
    customers_id = offer_data['customerid'].unique()
    
    
    for ind in range(len(customers_id)):
        
        cust_id = customers_id[ind]
        
        customer = profile_clean[profile_clean['customerid']==cust_id]
        
        cust_offer_data = offer_data[offer_data['customerid']==cust_id]
        
        cust_transaction_data = transaction_data[transaction_data['customerid']==cust_id]
        
        offer_received_data = cust_offer_data[cust_offer_data['offer received'] == 1]
        offer_completed_data = cust_offer_data[cust_offer_data['offer completed'] == 1]
        offer_viewed_data = cust_offer_data[cust_offer_data['offer viewed'] == 1]
        
        rows = []
        for i in range(offer_received_data.shape[0]):
            
            offer_id = offer_received_data.iloc[i]['offerid']
            
            offer_row = portfolio_clean.loc[portfolio_clean['offerid'] == offer_id]
            
            duration_days = offer_row['duration'].values[0]
            
            start_time = offer_received_data.iloc[i]['time']
            end_time = start_time + duration_days
        
            off_completed_withintime = np.logical_and(
                offer_completed_data['time'] >= start_time, offer_completed_data['time'] <= end_time)
            
            off_viewed_withintime = np.logical_and(
                offer_viewed_data['time'] >= start_time, offer_viewed_data['time'] <=end_time)

            offer_successful = off_completed_withintime.sum() > 0 and off_viewed_withintime.sum() > 0
            
            transaction_withintime = np.logical_and(
                cust_transaction_data['time'] >= start_time, cust_transaction_data['time'] <= end_time)
        
            transaction_data = cust_transaction_data[transaction_withintime]
            
            transaction_total_amount = transaction_data['amount'].sum()
            
            row = {
                
                'time': start_time,
                'total_amount': transaction_total_amount,
                'offer_successful': int(offer_successful),
            }
                
            row.update(offer_row.iloc[0,0:].to_dict())

            row.update(customer.iloc[0,:].to_dict())

            rows.append(row)
        
        data.extend(rows)
    
    data = pd.DataFrame(data)
    return data



