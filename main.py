from flask import Flask, request, jsonify
from scipy import stats
from flask_cors import CORS  
import numpy as np
import pandas as pd

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
                                     },
                     r"/get_nmf_immune_heatmap_data": {"origins": "http://127.0.0.1:5500",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_gene_heatmap_data": {"origins": "http://127.0.0.1:5500",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_protein_heatmap_data": {"origins": "http://127.0.0.1:5500",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_phospho_heatmap_data": {"origins": "http://127.0.0.1:5500",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_acetyl_heatmap_data": {"origins": "http://127.0.0.1:5500",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_comparison_and_survival_data": {"origins": "http://127.0.0.1:5500",
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
                     r"/get_gene_name_list": {"origins": "http://166.104.110.31:7000",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_nmf_immune_heatmap_data": {"origins": "http://166.104.110.31:7000",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_gene_heatmap_data": {"origins": "http://166.104.110.31:7000",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_protein_heatmap_data": {"origins": "http://166.104.110.31:7000",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_phospho_heatmap_data": {"origins": "http://166.104.110.31:7000",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_acetyl_heatmap_data": {"origins": "http://166.104.110.31:7000",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/get_comparison_and_survival_data": {"origins": "http://166.104.110.31:7000",
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     }
                     }) """

def get_prix_gene_name(geneNames):
    tmp = geneNames
    if '_' in tmp:
        return tmp.split('_')[0]
    else:
        return tmp
   
    
def get_heatmap_data():
    
    nmf_df = pd.read_csv('file/tumer_nmf_all.csv')
    #print(len(nmf_df))
    #print(nmf_df.head())
    nmf_df['search_gene_name'] = nmf_df.apply(lambda x:get_prix_gene_name(x['GeneName_Site']),axis=1)
    
    return nmf_df


def get_heatmap_gene_name_list(gene_type,gene_site,uniprot_site):
    tmp = gene_site
    if gene_type == 'RNA':
        return tmp +"_g"
    elif gene_type == 'PROTEIN':
        return tmp + "_p("+uniprot_site+")" 
    else:
        return tmp

                   
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


@app.route('/get_gene_name_list', methods=['POST'])
def get_gene_name_list():
    try:
        data = request.json
        #print(data)
        nmf_df = get_heatmap_data()
    
        #print(nmf_df['search_gene_name'])
        gene_name_vals = set(nmf_df['search_gene_name'].tolist())
        #print(len(list(gene_name_vals)))
        return jsonify({'geneName':list(gene_name_vals)})
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route('/get_nmf_immune_heatmap_data', methods=['POST'])
def get_nmf_immune_heatmap_data():
    try:
        data = request.json
        gene_name_list = data['geneNameList']
        print(gene_name_list)
        
        nmf_df = get_heatmap_data()

        sub_nmf_df = nmf_df[nmf_df['search_gene_name'].apply(lambda x: any(keyword == x for keyword in gene_name_list))] 
        sub_nmf_df['heatmap_gene_name'] = sub_nmf_df.apply(lambda x:get_heatmap_gene_name_list(x['Type'],x['GeneName_Site'],x['UniProt_Site']), axis=1)
        print(len(sub_nmf_df))
        
        sub_nmf_sort = sub_nmf_df.sort_values(by=['GeneName_Site'],ascending=[True])
        
        return jsonify(sub_nmf_sort.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route('/get_protein_heatmap_data', methods=['POST'])
def get_protein_heatmap_data():
    try:
        data = request.json
        #print(data)
        nmf_df = get_heatmap_data()
        
        protein_df = nmf_df[nmf_df['Type']=='PROTEIN'].copy()
        print("PROTEIN Total : "+str(len(protein_df)))

        protein_df['heatmap_gene_name'] =  protein_df.apply(lambda x:x['UniProt_Site'], axis=1)
        print(len(protein_df))
        
        protein_sort = protein_df.sort_values(by=['UniProt_Site'],ascending=[True])
        
        return jsonify(protein_sort.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route('/get_phospho_heatmap_data', methods=['POST'])
def get_phospho_heatmap_data():
    try:
        data = request.json
        #print(data)
        nmf_df = get_heatmap_data()
        
        phospho_df = nmf_df[nmf_df['Type']=='PHOSPHO'].copy()
        print("PHOSPHO Total : "+str(len(phospho_df)))

        phospho_df['heatmap_gene_name'] = phospho_df.apply(lambda x:x['UniProt_Site'], axis=1)
        print(len(phospho_df))
        
        phospho_sort = phospho_df.sort_values(by=['UniProt_Site'],ascending=[True])
        
        return jsonify(phospho_sort.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/get_acetyl_heatmap_data', methods=['POST'])
def get_acetyl_heatmap_data():
    try:
        data = request.json
        #print(data)
        nmf_df = get_heatmap_data()
        
        acetyl_df = nmf_df[nmf_df['Type']=='ACETYL'].copy()
        print("ACETYL Total : "+str(len(acetyl_df)))

        acetyl_df['heatmap_gene_name'] = acetyl_df.apply(lambda x:x['UniProt_Site'], axis=1)
        print(len(acetyl_df))
        
        acetyl_sort = acetyl_df.sort_values(by=['UniProt_Site'],ascending=[True])
        
        return jsonify(acetyl_sort.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route('/get_gene_heatmap_data', methods=['POST'])
def get_gene_heatmap_data():
    try:
        data = request.json
        print(data)
        nmf_df = get_heatmap_data()
        
        rna_df = nmf_df[nmf_df['Type']=='RNA']
        print("RNA Total : "+str(len(rna_df)))
        
        rna_df['heatmap_gene_name'] = rna_df.apply(lambda x:x['GeneName'], axis=1)
        print(len(rna_df))
        
        rna_sort = rna_df.sort_values(by=['GeneName'],ascending=[True])
        
        return jsonify(rna_sort.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/get_comparison_and_survival_data', methods=['POST'])
def get_comparison_and_survival_data():
    try:
        data = request.json
        print(data)
        
        geneName = data['geneName']
        #print(geneName)
        
        nmf_df = get_heatmap_data()
        
        sub_comparison_data = nmf_df[nmf_df['search_gene_name']==geneName]
        print(len(sub_comparison_data))
        
        return jsonify(sub_comparison_data.to_json(orient='split'))
    
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
      
    app.run(debug=True,host="0.0.0.0",port=5000)
