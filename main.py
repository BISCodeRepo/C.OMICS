from flask import Flask, request, jsonify
from scipy import stats
from flask_cors import CORS  
import numpy as np
import pandas as pd

app = Flask(__name__)
origins = ["https://comics.hanyang.ac.kr","http://comics.hanyang.ac.kr","http://166.104.110.31:7000"]
#origins = ["http://127.0.0.1:5500"]
CORS(app, resources={r"/api/kruskal_wallis": {"origins": origins,
                                          "methods": ["POST"],
                                          "allow_headers": ["Content-Type"]
                                          },
                     r"/api/rank_sums": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/api/get_gene_name_list": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/api/get_nmf_immune_heatmap_data": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/api/get_gene_heatmap_data": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/api/get_protein_heatmap_data": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/api/get_phospho_heatmap_data": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/api/get_acetyl_heatmap_data": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/api/get_comparison_and_survival_data": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/api/get_only_rna_heatmap_data": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/api/get_other_heatmap_data": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },      
                     r"/api/get_nmf_meta_columns": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     },
                     r"/api/get_survival_data": {"origins": origins,
                                     "methods": ["POST"],
                                     "allow_headers": ["Content-Type"]
                                     }       
                     })

def get_prix_gene_name(geneNames):
    tmp = geneNames
    if '_' in tmp:
        return tmp.split('_')[0]
    else:
        return tmp
   
    
def get_heatmap_data():
    
    nmf_df = pd.read_pickle('file/tumer_nmf_all.pkl')
    #print(len(nmf_df))
    #print(nmf_df.head())
    #nmf_df['search_gene_name'] = nmf_df.apply(lambda x:get_prix_gene_name(x['GeneName_Site']),axis=1)
    
    return nmf_df

def get_all_data():
    
    all_df = pd.read_pickle('file/all_df.pkl')
    
    return all_df



def get_only_rna_data():
    rna_df = pd.read_pickle('file/rna_sort.pkl')
    return rna_df


def get_other_data():
    other_df = pd.read_pickle('file/other_sort.pkl')
    return other_df


def get_heatmap_gene_name_list(gene_type,gene_site,uniprot_site):
    tmp = gene_site
    if gene_type == 'RNA':
        return tmp +"_g"
    elif gene_type == 'PROTEIN':
        return tmp + "_p("+uniprot_site+")" 
    else:
        return tmp

@app.route('/api/get_nmf_meta_columns', methods=['POST'])
def get_nmf_meta_columns():
    try:
        data = request.json
        meta_df = pd.read_pickle('file/nmf_meta_sort.pkl')
          
        return jsonify(meta_df.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})

                   
@app.route('/api/kruskal_wallis', methods=['POST'])
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


@app.route('/api/rank_sums', methods=['POST'])
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


@app.route('/api/get_gene_name_list', methods=['POST'])
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
    

@app.route('/api/get_only_rna_heatmap_data', methods=['POST'])
def get_only_rna_heatmap_data():
    try:
        data = request.json
        gene_name_list = data['geneNameList']
        print(gene_name_list)
        
        rna_df = get_only_rna_data()

        sub_rna_df = rna_df[rna_df['search_gene_name'].apply(lambda x: any(keyword == x for keyword in gene_name_list))] 
        sub_rna_df['heatmap_gene_name'] = sub_rna_df.apply(lambda x:get_heatmap_gene_name_list(x['Type'],x['GeneName_Site'],x['UniProt_Site']), axis=1)
        print(len(sub_rna_df))
        
        sub_rna_sort = sub_rna_df.sort_values(by=['GeneName_Site'],ascending=[True])
        
        return jsonify(sub_rna_sort.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/get_other_heatmap_data', methods=['POST'])
def get_other_heatmap_data():
    try:
        data = request.json
        gene_name_list = data['geneNameList']
        print(gene_name_list)
        
        other_df = get_other_data()

        sub_other_df = other_df[other_df['search_gene_name'].apply(lambda x: any(keyword == x for keyword in gene_name_list))] 
        sub_other_df['heatmap_gene_name'] = sub_other_df.apply(lambda x:get_heatmap_gene_name_list(x['Type'],x['GeneName_Site'],x['UniProt_Site']), axis=1)
        print(len(sub_other_df))
        
        sub_other_sort = sub_other_df.sort_values(by=['GeneName_Site'],ascending=[True])
        
        return jsonify(sub_other_sort.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})
    

    
@app.route('/api/get_nmf_immune_heatmap_data', methods=['POST'])
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
    
    
@app.route('/api/get_protein_heatmap_data', methods=['POST'])
def get_protein_heatmap_data():
    try:
        data = request.json
        #print(data)
        print(data)
        protein_sort = pd.read_pickle('file/protein_sort.pkl')
        print(len(protein_sort))
        
        return jsonify(protein_sort.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route('/api/get_phospho_heatmap_data', methods=['POST'])
def get_phospho_heatmap_data():
    try:
        data = request.json
        print(data)
        phospho_sort = pd.read_pickle('file/phospho_sort.pkl')
        print(len(phospho_sort))
        
        return jsonify(phospho_sort.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/api/get_acetyl_heatmap_data', methods=['POST'])
def get_acetyl_heatmap_data():
    try:
        data = request.json
        print(data)
        acetyl_sort = pd.read_pickle('file/acetyl_sort.pkl')
        
        print(len(acetyl_sort))
        
        return jsonify(acetyl_sort.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route('/api/get_gene_heatmap_data', methods=['POST'])
def get_gene_heatmap_data():
    try:
        data = request.json
        print(data)
        rna_df = pd.read_pickle('file/rna_sort.pkl')
        
        #rna_df['heatmap_gene_name'] = rna_df.apply(lambda x:x['GeneName'], axis=1)
        print(len(rna_df))
        
        #rna_sort = rna_df.sort_values(by=['GeneName'],ascending=[True])
        
        return jsonify(rna_df.to_json(orient='split'))
    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/api/get_comparison_and_survival_data', methods=['POST'])
def get_comparison_and_survival_data():
    try:
        data = request.json
        print(data)
        
        geneName = data['geneName']
        #print(geneName)
        
        all_df = get_all_data()
        
        sub_comparison_data = all_df[all_df['search_gene_name']==geneName]

        print(len(sub_comparison_data))
        
        return jsonify(sub_comparison_data.to_json(orient='split'))
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route('/api/get_survival_data', methods=['POST'])
def get_survival_data():
    try:
        data = request.json
        print(data)
        
        geneName = data['geneName']
        #print(geneName)
        
        all_df = get_heatmap_data()
        
        sub_comparison_data = all_df[all_df['search_gene_name']==geneName]

        print(len(sub_comparison_data))
        
        return jsonify(sub_comparison_data.to_json(orient='split'))
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
    
@app.route('/api/get_survival_overall_data', methods=['POST'])
def get_survival_overall_data():
    try:
        data = request.json
        print(data)
        
        geneName = data['geneName']
        #print(geneName)
        
        all_df = get_heatmap_data()
        
        sub_comparison_data = all_df[all_df['search_gene_name']==geneName]

        print(len(sub_comparison_data))
        
        return jsonify(sub_comparison_data.to_json(orient='split'))
    
    except Exception as e:
        return jsonify({"error": str(e)})
    


if __name__ == '__main__':
      
    app.run(debug=True,host="0.0.0.0",port=5000)
    #app.run(debug=True, host="0.0.0.0", port=5000, ssl_keyfile='/home/bis/PDIAMOND/key.pem', ssl_certfile='/home/bis/PDIAMOND/cert.pem', reload=True)
