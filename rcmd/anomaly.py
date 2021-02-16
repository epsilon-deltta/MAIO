class anomaly:
    def __init__(self):
        pass

    def strip_iqr(self,df,cols,strength=1):
                
        for col in cols :
            q75 = df[col].quantile(q=0.75)
            q25 = df[col].quantile(q=0.25)
            iqr = q75 - q25
            rbound = q75 + 1.5*strength
            lbound = q25 - 1.5*strength
            
            df = df.drop(index = df[ ( lbound > tkwd[col]) | (tkwd[col] > rbound) ].index)
            
        return df

    def test(self):
        print("this is for testing")