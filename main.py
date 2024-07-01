from flask import Flask, request, jsonify
from scipy import stats
from flask_cors import CORS  
import numpy as np
import pandas as pd
import json

app = Flask(__name__)
CORS(app, resources={r"/kruskal_wallis": {"origins": "http://127.0.0.1:5500",
                                          "methods": ["POST"],
                                          "allow_headers": ["Content-Type"]
                                          },
                     r"/rank_sums": {"origins": "http://127.0.0.1:5500",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_gene_name_list": {"origins": "http://127.0.0.1:5500",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     }
                     }) 
"""CORS(app, resources={r"/kruskal_wallis": {"origins": "http://166.104.110.31:7000",
                                          "methods": ["POST"],
                                          "allow_headers": ["Content-Type"]
                                          },
                     r"/rank_sums": {"origins": "http://166.104.110.31:7000",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/getGeneName": {"origins": "http://166.104.110.31:7000",
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


def read_file(path):
    lines = []
    r = open(path,'r')
    try:
        lines = r.readlines()
    finally:
        r.close()
    return lines


def get_prix_gene_name(geneNames):
    tmp = geneNames
    if '_' in tmp:
        return tmp.split('_')[0]
    else:
        return tmp
   
    
def get_heatmap_data():
    
    nmf_df = pd.read_csv('file/tumer_nmf_all.csv')
    print(len(nmf_df))
    #print(nmf_df.head())
    nmf_df['search_gene_name'] = nmf_df.apply(lambda x:get_prix_gene_name(x['GeneName_Site']),axis=1)
    
    #protein_df = nmf_df[nmf_df['Type']=='PROTEIN']
    #print("PROTEIN Total : "+str(len(protein_df)))
    #rna_df = nmf_df[nmf_df['Type']=='RNA']
    #print("RNA Total : "+str(len(rna_df)))
    #acetyl_df = nmf_df[nmf_df['Type']=='ACETYL']
    #print("ACETYL Total : "+str(len(acetyl_df)))
    #phospho_df = nmf_df[nmf_df['Type']=='PHOSPHO']
    #print("PHOSPHO Total : "+str(len(phospho_df)))
    
    return nmf_df


@app.route('/get_gene_name_list', methods=['POST'])
def get_gene_name_list():
    try:
        data = request.json
        print(data)
        nmf_df = get_heatmap_data()
    
        #print(nmf_df['search_gene_name'])
        gene_name_vals = set(nmf_df['search_gene_name'].tolist())
        print(len(list(gene_name_vals)))
        return jsonify({'geneName':list(gene_name_vals)})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    
    get_heatmap_data()
    
    app.run(debug=True,host="0.0.0.0",port=5000)
