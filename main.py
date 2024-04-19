from flask import Flask, request, jsonify
from scipy import stats
from flask_cors import CORS  
import numpy as np
import pandas as pd


nmf_df = None

app = Flask(__name__)
CORS(app, resources={r"/kruskal_wallis": {"origins": "http://127.0.0.1:5500",
                                          "methods": ["POST"],
                                          "allow_headers": ["Content-Type"]
                                          },
                     r"/rank_sums": {"origins": "http://127.0.0.1:5500",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/getnmf": {"origins": "http://127.0.0.1:5500",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     }
                     }) 
"""CORS(app, resources={r"/kruskal_wallis": {"origins": "http://166.104.112.65",
                                          "methods": ["POST"],
                                          "allow_headers": ["Content-Type"]
                                          },
                     r"/rank_sums": {"origins": "http://166.104.112.65",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/getnmf": {"origins": "http://166.104.112.65",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     }
                     })  """
                     
@app.route('/kruskal_wallis', methods=['POST'])
def kruskal_wallis():
    data = request.json
    if 'allData' in data:
        samples = data['allData']
        print(samples)
        try:
            _, p_value = stats.kruskal(*samples)
            print(stats.kruskal(*samples))
            result = {
                "p_value": p_value
            }
            print("result"+str(result['p_value']))
            return jsonify(result)
        except Exception as e:
            print("error"+str(e))
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "no data"})


@app.route('/rank_sums', methods=['POST'])
def rankSums():
    data = request.json
    if 'allData' in data:
        samples = data['allData']    
        try:
            _, p_value = stats.ranksums(*samples)
            result = {
                "p_value": p_value
            }
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "no data"})

    
@app.route('/getnmf', methods=['POST'])
def requestNMF():
    data = request.json   
    try:
        condition_list = data['condition']
        return_df = None
        for con in condition_list:  
            sub_nmf_df1 = nmf_df[((nmf_df['Type'] =='RNA') | (nmf_df['Type'] =='PROTEIN')) & (nmf_df['GeneName_Site']==con)]
                
            sub_nmf_df2 = nmf_df[(nmf_df['Type'] !='RNA') & (nmf_df['Type'] !='PROTEIN') & (nmf_df['GeneName_Site'].str.split('_').str[0]==con)]
            
            if return_df is None:
                return_df = pd.concat([sub_nmf_df1,sub_nmf_df2])
            else:
                return_df = pd.concat([return_df,sub_nmf_df1,sub_nmf_df2])
        
        title_df = pd.DataFrame()
        title_df = title_df.append(pd.Series(nmf_df.columns.tolist(),index=nmf_df.columns), ignore_index = True)
        return_df1 = title_df.append(return_df,ignore_index=True)
        print(len(return_df1))
        return return_df1.to_json(orient="values")
    except Exception as e:
        return jsonify({"error": str(e)})


def read_file(path):
    lines = []
    r = open(path,'r')
    try:
        lines = r.readlines()
    finally:
        r.close()
    return lines
   
    
def getNMFData():
    return pd.read_csv('file/tumer_nmf_all.csv')


if __name__ == '__main__':
    
    #nmf_df = getNMFData()
    #print(len(nmf_df))
    #getProteinData()
    #getAcetylsite()
    #getGene()
    #getPhospho()
    app.run(debug=True,host="0.0.0.0",port=5000)
