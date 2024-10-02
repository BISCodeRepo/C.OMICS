var baseURL = "http://127.0.0.1:5000/api/";
//var baseURL = "https://comics.hanyang.ac.kr/api/";

var nmfMetaSortData = ['Subtype','Subtype Core','Subtype Membership','Histology','Age','Sex','Smoking','TNM stage','Pathologic-N',
'Adjuvant Treatment','Recurrence Status','TIL pattern','Immune Cluster','Whole Genome Doubling','TP53','Other Tumor Suppressor genes',
'EGFR','Other Oncogene Alteration']

var nmfMetaData = ['Subtype','Subtype Core','Histology','Sex','Smoking','TNM stage','Pathologic-N','Adjuvant Treatment',
'Recurrence Status','TIL pattern','Immune Cluster','Whole Genome Doubling','TP53','Other Tumor Suppressor genes',
'EGFR','Other Oncogene Alteration']

var nmfMetaOrder = {
    "Subtype":1,
    "Subtype Core":2,
    "Subtype Membership":3,
    "Histology":4,
    "Age":5,
    "Sex":6,
    "Smoking":7,
    "TNM stage":8,
    "Pathologic-N":9,
    "Adjuvant Treatment":10,
    "Recurrence Status":11,
    "TIL pattern":12,
    "Immune Cluster":13,
    "Whole Genome Doubling":14,
    "TP53":15,
    "Other Tumor Suppressor genes":16,
    "EGFR":17,
    "Other Oncogene Alteration":18
}

var nmfMetaDataJson = {
    "Subtype":[],
    "Subtype Core":[],
    "Subtype Membership":[],
    "Histology":[],
    "Age":[],
    "Sex":[],
    "Smoking":[],
    "TNM stage":[],
    "Pathologic-N":[],
    "Adjuvant Treatment":[],
    "Recurrence Status":[],
    "TIL pattern":[],
    "Immune Cluster":[],
    "Whole Genome Doubling":[],
    "TP53":[],
    "Other Tumor Suppressor genes":[],
    "EGFR":[],
    "Other Oncogene Alteration":[]
}


var allData = []
var myPopup = null;

var toolbarMenu = {
    File: [
      //'Open', 
      //null, 
      'Save Image', 'Save Dataset', 'Save Session', 
      //null, 
      //'Close Tab', null, 
      'Rename Tab'],
    Tools: [
      //'New Heat Map',
      //null,
      //'Hierarchical Clustering',
      //'KMeans Clustering',
      //null,
      //'Marker Selection',
      //'Nearest Neighbors',
      //'Create Calculated Annotation',
      //null,
      //null,
      //'Adjust',
      //'Collapse',
      //'Similarity Matrix',
      //'Transpose',
      //null,
      'Chart',
      null,
      't-SNE',
      null,
      'Sort/Group',
      'Filter',
      //null,
      //'API'
      //null
      ],
    View: [
      'Zoom In', 'Zoom Out', null, 'Fit To Window', 'Fit Rows To Window', 'Fit Columns To Window', null, '100%', null,
      'Options'],
    Edit: [
      //'Copy Image',
      //'Copy Selected Dataset',
      //null,
      'Move Selected Rows To Top',
      'Annotate Selected Rows',
      'Copy Selected Rows',
      'Invert' +
      ' Selected Rows',
      'Select All Rows',
      'Clear Selected Rows',
      null,
      'Move Selected Columns To Top',
      'Annotate Selected Columns',
      'Copy Selected Columns',
      'Invert' +
      ' Selected Columns',
      'Select All Columns',
      'Clear Selected Columns']
      /*Help: [
        'Find Action', null, 'Contact', 'Configuration', 'Tutorial', 'Source Code', null, 'Keyboard' +
        ' Shortcuts']*/
  }


var metaArray=[];

var color = [
  "#70DB93",
  "#5C3317",
  "#9F5F9F",
  "#B5A642",
  "#8C7853",
  "#A67D3D",
  "#5F9F9F",
  "#D98719",
  "#B87333",
];


class PatientMetaData {
  constructor() {
  }
}

var nmfMetaColorNameMap = {
  'Subtype':{'1':'#FF6666','2':'#99CCFF','3':'#FFCC33','4':'#00FF99','5':'#00CCFF'},
  'Subtype Core':{'Y':'#000000','N':'#f5f5dc'},
  'Subtype Membership':{'start':'#f5f5dc','end':'#FF6600'},
  'Histology':{'AD':'#99FF99','SC':'#FF9900','NC':'#FF66CC','MA':'#6600CC','Others':'#003300'},
  'Age':{'start':'#f5f5dc','end':'#333333'},
  'Sex':{'F':'#3399FF','M':'#660099'},
  'Smoking':{'Cr':'#660033','Ex':'#FF9900','N':'#CCCCCC','NA':'#666666'},
  'TNM Stage':{'IA1':'#FFFF66','IA2':'#CCFF33','IA3':'#99FF66','IB':'#33FF00',
  'IIA':'#33CC66','IIB':'#009933','IIIA':'#009966','IIIB':'#006633','IVA':'#660099'},
  'Pathologic N':{'N0':'#CCCCCC','N1':'#CCCC00','N2':'#CC66CC'},
  'Adjuvant Treatment':{'None':'#999999','CTx':'#0033FF','RTx':'#CC0000','CTx & RTX':'#9900CC'},
  'Recurrence Status':{'NA':'#CCCCCC','0':'#666666','1':'#CC3399'},
  'TIL Pattern':{'Unknown':'#CCCCCC','absent':'#FFFFCC','non−brisk multifocal':'#CCCC99','brisk band-Like':'#666633','brisk diffuse':'#333300'},
  'Immune Cluster':{'Cold':'#3333FF','Hot':'#FF66CC'},
  'Whole Genome Doubling':{'Y':'#000000','N':'#f5f5dc'},
  'TP53':{'Not altered':'#f5f5dc','CNV.loss':'#CC6699','Mutation':'#FFCC66','Mut+CNV.loss':'#663300'},
  'Other Tumor Suppressor genes':{'Not altered':'#f5f5dc','CNV.loss':'#CC6699','Mutation':'#FFCC66','Mut+CNV.loss':'#663300'},
  'EGFR':{'None':'#f5f5dc','Others_Indel':'#FF9900','Others_SNV':'#0033FF','L858R':'#CCFF99','exon19_del':'#990033'},
  'Other Oncogene Alteration':{'ERBB2':'#660099','KRAS':'#003300','PIK3CA':'#FF6600','KRAS_PIK3CA':'#993300',
  'MET':'#333333','ALK':'#663333','ROS1':'#003399','RET':'#333300'}
}


var immuneMetaColorNameMap = {
  'Pathway Based IC':{'HTE':'#CC0000','CTE':'#0033CC'},
  'TIL Pattern':{'unknown':'#CCCCCC','absent':'#FFFFCC','non-brisk multifocal':'#CCCC66','brisk band-diffuse':'#CC9933','brisk diffuse':'#663300'},
  'Histology':{'AD':'#99FF99','SC':'#FF9900','NC':'#FF66CC','MA':'#6600CC','Others':'#003300'},
  'Multi Omics Subtype':{'1':'#FF6666','2':'#99CCFF','3':'#FFCC33','4':'#00FF99','5':'#00CCFF'},
  'Stage':{'1':'#FFFF66','2':'#CCFF33','3':'#99FF66','4':'#33FF00'},
  'Tissue':{'Tumor':'#FF0000','Normal':'#FF9999'},
  'Cell Type Based IC':{'HTE':'#CC0000','CTE':'#0033CC','NAT-enriched':'#339900'},
  'CD8 T Cells':{'start':'#0033FF','end':'#FF0000'},
  'CD4 T Cells':{'start':'#0033FF','end':'#FF0000'},
  'Tregs':{'start':'#0033FF','end':'#FF0000'},
  'B Cells':{'start':'#0033FF','end':'#FF0000'},
  'NK Cells':{'start':'#0033FF','end':'#FF0000'},
  'Neutrophils':{'start':'#0033FF','end':'#FF0000'},
  'DC':{'start':'#0033FF','end':'#FF0000'},
  'Monocytes':{'start':'#0033FF','end':'#FF0000'},
  'Macrophages':{'start':'#0033FF','end':'#FF0000'},
  'Epithelial Cells':{'start':'#0033FF','end':'#FF0000'},
  'Recognition of Tumor Cells':{'start':'#0033FF','end':'#FF0000'},
  'Trafficking and Infiltration':{'start':'#0033FF','end':'#FF0000'},
  'Checkpoint Expression':{'start':'#0033FF','end':'#FF0000'},
  'Inhibitor Cells':{'start':'#0033FF','end':'#FF0000'},
  'Priming and Activation':{'start':'#0033FF','end':'#FF0000'},
  'T Cell Immunity':{'start':'#0033FF','end':'#FF0000'},
  'Inhibitory Molecules':{'start':'#0033FF','end':'#FF0000'}
}

const Pi = 3.141592

