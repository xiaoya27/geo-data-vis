import pandas as pd
import ast

from distance import cord_to_dis


class ShopGeoInfo:
    def __init__(self,shopcode):
        self.shopcode = shopcode

    def read_data(self):
        df = pd.read_excel('{}-surrounding.xlsx'.format(str(self.shopcode)))
        geo_ref= pd.read_excel('geo-info-full.xlsx').set_index('index')
        shop_lat,shop_lng,shop_name = geo_ref.loc[self.shopcode]['lat'],geo_ref.loc[self.shopcode]['lng'],geo_ref.loc[self.shopcode]['shopname']
        return df,shop_lat,shop_lng,shop_name

    def preprocessing(self):
        df,shop_lat,shop_lng,shop_name = self.read_data()
        df['lat'] = df.apply(lambda x: ast.literal_eval((x['geometry']))['location']['lat'],axis=1)
        df['lng'] = df.apply(lambda x: ast.literal_eval((x['geometry']))['location']['lng'],axis=1)
        df['distance'] = df.apply(lambda x: cord_to_dis(shop_lat,shop_lng,x['lat'],x['lng']),axis=1)
        short_df = df[['business_status','name','lat','lng','user_ratings_total','price_level','distance','types','permanently_closed','rating']]
        # preprocess
        print("before drop duplicates", len(short_df))
        short_df=short_df.drop_duplicates()
        print("after drop duplicates, {} left".format(len(short_df)))
        short_df=short_df[short_df['distance']<800]
        print("after set max distance to 800m, {} left".format(len(short_df)))
        return short_df,shop_lat,shop_lng,shop_name
    