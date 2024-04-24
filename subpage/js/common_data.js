var baseURL = "http://127.0.0.1:5000/";
//var baseURL = "http://166.104.112.65:5000/";

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

var nmfMetaObj = {
    "vectors" :[]
  }

var allData = []
var myPopup = null;

var toolbarMenu = {
    File: [
      'Open', null, 'Save Image', 'Save Dataset', 'Save Session', null, 'Close Tab', null, 'Rename' +
      ' Tab'],
    Tools: [
      'New Heat Map',
      null,
      'Hierarchical Clustering',
      'KMeans Clustering',
      null,
      'Marker Selection',
      'Nearest Neighbors',
      'Create Calculated Annotation',
      null,
      'Adjust',
      'Collapse',
      'Similarity Matrix',
      'Transpose',
      null,
      'Chart',
      null,
      't-SNE',
      null,
      'Sort/Group',
      'Filter',
      null,
      //'API'
      null],
    View: [
      'Zoom In', 'Zoom Out', null, 'Fit To Window', 'Fit Rows To Window', 'Fit Columns To Window', null, '100%', null,
      'Options'],
    Edit: [
      'Copy Image',
      'Copy Selected Dataset',
      null,
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


var immuneMetaGradientName = {
  'CD8 T cells':'yellow',
  'CD4 T cells':'yellow',
  'Tregs':'yellow',
  'B cells':'yellow',
  'NK cells':'yellow',
  'Neutrophils':'yellow',
  'DC':'yellow',
  'Monocytes':'yellow',
  'Macrophages':'yellow',
  'Epithelial cells':'yellow',
  'Recognition of tumor cells':'green',
  'Trafficking and infiltration':'green',
  'Checkpoint expression':'green',
  'Inhibitor cells':'green',
  'Priming and activation':'green',
  'T cell immunity':'green',
  'Inhibitory molecules':'green'
}

const Pi = 3.141592

