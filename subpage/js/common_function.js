///////////////////////새로고침 화면 로드//////////////////////////////
function showSpinner() {
  var lastIndex = document.getElementsByClassName('layerPopup').length-1;
  document.getElementsByClassName('layerPopup')[lastIndex].style.display='block';
}

function hideSpinner() {
  var lastIndex = document.getElementsByClassName('layerPopup').length-1;
  document.getElementsByClassName('layerPopup')[lastIndex].style.display='none';
}

/////////////////////// HeatMap 그리기//////////////////////////////
////uniprotIdArray : 행  gene/ protein 명 배열
////patientsArray : 열 환자 id 배열
////dataArray : 데이터 [[]] 2차원 배열
////heatMapDiv : headmap div id 
////metaArray : meta data 배열 
function paintHeatMap(uniprotIdArray,patientsArray,dataArray,heatMapDiv,metaArray,linkArray){

  var patientTmp = []
  var subPatient = []

  //debugger;

  for(var i=0; i<metaArray.length; i++){
    var tmp = metaArray[i].substr(0,metaArray[i].length-1);
    var tmpArray = tmp.split(',').slice(1,tmp.split(',').length)
    
    for(var j=0; j<patientsArray.length;j++){
      var paiTmp = patientsArray[j].substr(0,patientsArray[j].length-1)+'T';
      if(tmpArray.indexOf(paiTmp)>-1){
        patientTmp.push(tmpArray.indexOf(paiTmp));
        subPatient.push(patientsArray[j])
      }
    }
  }

  var finalDataArray = [];
  for(var i = 0; i<dataArray.length;i++){
    var tmp = dataArray[i];
    var fArray = []
    for(var j=0;j<patientTmp.length;j++){
      fArray.push(tmp[patientTmp[j]])
    }
    finalDataArray.push(fArray)
  }


  var metaList = []
  if(metaArray !=null && metaArray.length > 0){
      for(var i=0; i<metaArray.length; i++){
          var tmp = metaArray[i].substr(0,metaArray[i].length-1);
          var colValue = tmp.split(',')[0];
          var tmpArray = tmp.split(',').slice(1,tmp.split(',').length)
          var putArray =[];
          for(var j=0;j<patientTmp.length;j++){
            putArray.push(tmpArray[patientTmp[j]]);
          }
          if(colValue=='Sample.ID'){
            metaList.push({
              'name':colValue,
              'array':subPatient
            })
          } else{
            metaList.push({
              'name':colValue,
              'array':putArray
            })
          }
        }
  }
  
  nmfMetaObj['vectors'] = metaList

  $('#'+heatMapDiv).empty();

  var json = {
    "rows": uniprotIdArray.length,
    "columns": subPatient.length,
    "seriesArrays": [finalDataArray],
    "seriesDataTypes": ["Float32"],
    "seriesNames": ["NMF"],
    "rowMetadataModel": {
      "vectors": [{
        "name": "Gene",
        "array": uniprotIdArray
      },{
        "name": "Link",
        "array": linkArray
      }]
    },
    "columnMetadataModel": nmfMetaObj
  }

  var columnColorMap = getColumnColorModel(metaList);
  //debugger

  var comMorpheus = new morpheus.HeatMap({
    el: $('#'+heatMapDiv),
    dataset: morpheus.Dataset.fromJSON(json),
    colorScheme: { // optional color scheme. default is relative
      type: 'fixed',
      /*map: [{
        value: -12,
        color: '#0000ff'
      }, {
        value: 0,
        color: '#ffffff'
      }, {
        value: 12,
        color: '#ff0000'
      }]*/
    },
    //showRowNumber: true,
    tools: [{ // optional tools to run at load time
      //name: 'Hierarchical Clustering',
      //params: {cluster: 'Rows and columns'}
    }],
    menu:toolbarMenu,
    columnColorModel:columnColorMap
  });

  return comMorpheus;

}



/////////////////////// Legend popup//////////////////////////////

function DrawLegendPopup(colorMap){
  
  if(myPopup!=null){
    myPopup.close();
  }
  
  myPopup = window.open('', 'Legend', 'height=600, width=1200, scrollbars=yes');
  var htmlStr="<div><table><tr>";
  var substr="";
  var i = 1;
  $.map(colorMap, function(k, v){
      htmlStr += "<td style='text-align: center;'>"+k.key+"</td>";
      var newArr = $.map(k.value,function(key,value){return key});
      var subArr = $.map(newArr[0],function(key,value){return key});
      substr += "<td style='height: fit-content;'><table border='1px solid #ccc' cellspacing='0' cellpadding='0' style='margin: auto;'>";
      $.map(subArr,function(key,value){
        substr += "<tr><td bgcolor='"+key.value+"' height='15' width='15'></td>"+
          "<td>"+key.key+"</td></tr>";
      });
      substr += "</table></td>";
      if(i%8==0){
        htmlStr +="</tr><tr>";
        htmlStr += substr;
        substr = "";
        htmlStr +="</tr><tr>";
      }
      i++;
  });
  htmlStr += substr;
  htmlStr += "</tr><tr></table></div>";

  myPopup.document.write(htmlStr);
  myPopup.focus()   
}

function ImmuneDrawLegendPopup(colorMap){
  
  
  if(myPopup!=null){
    myPopup.close();
  }
  
  myPopup = window.open('', 'Legend', 'height=600, width=1200, scrollbars=yes');
  var htmlStr="<div><table><tr>";
  var substr="";
  var i = 1;
  $.map(colorMap, function(k, v){
      htmlStr += "<td style='text-align: center;'>"+k.key+"</td>";
      var colo = immuneMetaGradientName[k.key];
      var newArr = $.map(k.value,function(key,value){return key});
      var subArr = $.map(newArr[0],function(key,value){return key});
      if(colo!=null && colo!="" && colo!=undefined){
        substr += "<td style='height: fit-content;'><table border='1px solid #ccc' cellspacing='0' cellpadding='0' style='margin: auto;width:83%'>";
        substr += "<tr><td style='height: fit-content;'>"
        switch(colo){
          case "green":
            substr += "<div style='height:20px;margin:auto; background : linear-gradient(to right,#FFFFFF,#006030);'></div></tr>";
            break;
          case "yellow":
            substr += "<div style='height:20px;margin:auto; background : linear-gradient(to right,#FFFFFF,#fbc504);'></div></tr>";
            break
            case "red":
            substr += "<div style='height:20px;margin:auto; background : linear-gradient(to right,#FFFFFF,#be0202);'></div></tr>";
            break;
          case "orange":
            substr += "<div style='height:20px;margin:auto; background : linear-gradient(to right,#FFFFFF,#fb9804);'></div></tr>";
            break;
          case "blue":
            substr += "<div style='height:20px;margin:auto; background : linear-gradient(to right,#FFFFFF,#0202f7);'></div></tr>";
            break;
        }
        substr += "<tr><td><span style='font-size:13px;float:left'>"+subArr[0].key+"</span><span style='font-size:13px;float:right'>"+subArr[subArr.length-1].key+"</span></td></tr>";
        substr += "</table></td>";

      } else{       
        substr += "<td style='height: fit-content;'><table border='1px solid #ccc' cellspacing='0' cellpadding='0' style='margin: auto;'>";
        $.map(subArr,function(key,value){        
            substr += "<tr><td bgcolor='"+key.value+"' height='15' width='15'></td>"+
            "<td>"+key.key+"</td></tr>";
        });
        substr += "</table></td>";
      }
      
      if(i%8==0||i==23){
        htmlStr +="</tr><tr>";
        htmlStr += substr;
        substr = "";
        htmlStr +="</tr><tr>";
      }
      i++;
  });
  htmlStr += substr;
  htmlStr += "</tr><tr></table></div>";

  myPopup.document.write(htmlStr);
  myPopup.focus()   
}


/////////////////////// Sample(Patient)리스트 가져오기//////////////////////////////
function getConcatSampleList(){
  
  var patientsArray = []
  //Patients
  var nmfPat = nmfData[0].substr(0,nmfData[0].length-1);
  patientsArray = patientsArray.concat(nmfPat.split(',').slice(4,nmfPat.split(',').length));

  return patientsArray

}


function getConcatGeneList(){

  var geneList = []

  //Genens
  for(var i = 1; i<nmfData.length-1;i++) {
      var tmp = nmfData[i]
      geneList.push(tmp.split(',')[3].split("_")[0])
  }

  let patSet = new Set(geneList);
  geneList = Array.from(patSet).sort();

  return geneList

}


function getDataArray(){

  var dataList = []

  for(var i = 1; i<nmfData.length-1;i++) {
      var tmp = nmfData[i]
      dataList.push(tmp.split(',').slice(4, tmp.split(',').length))
  }

  return dataList

}


function getGeneIDList(){


  var uniprotIdArray = []

  for(var i = 1; i<nmfData.length-1;i++) {
      var tmp = nmfData[i]
      uniprotIdArray.push(tmp.split(',')[3])
  }

  return uniprotIdArray

}


function getRowGeneList(){

  var uniprotIdArray = []
  for(var i = 1; i<nmfData.length-1;i++) {
      var tmp = nmfData[i].split(",");
      if(tmp[0] == 'RNA'){
        uniprotIdArray.push(tmp[3] +"_g")
      } else if(tmp[0] == 'PROTEIN'){
        uniprotIdArray.push(tmp[3] +"_p ("+ tmp[1]+")")
      } else {
        uniprotIdArray.push(tmp[3])
      }
      
  }
  return uniprotIdArray

}


function getUniprotIDList(geneList){

  var uniprotIdArray = []
  for(var i= 0 ; i<geneList.length ; i++){
    var tmp = nmfData[i+1].split(',');
    uniprotIdArray.push(geneList[i]+"="+tmp[1].split('_')[0])
  }

  return uniprotIdArray
}



//////////////// 색상 gradient ////////////////
function getColumnColorModel(metaList){

  //debugger
  let returnMap = {};

  var yelloList = []
  var greenList = []

  for(var i =0;i<metaList.length;i++){
    var tmp = metaList[i];
    var colo = immuneMetaGradientName[tmp['name']];

    if(colo == 'yellow'){
      yelloList = yelloList.concat(tmp['array'])
    } else if(colo == 'green'){
      greenList = greenList.concat(tmp['array'])
    }
  }

  var yellowSortList = yelloList.map(x => parseFloat(x.trim()).toFixed(3)).sort(ascOrder);
  var greenSortList = greenList.map(x => parseFloat(x.trim()).toFixed(3)).sort(ascOrder);

  var yellowColorList = gradient_two('#0000ff','#ff0000',yellowSortList);
  var greenColorList = gradient('#FFFFFF','#ff0000',greenSortList.length);

  for(var i =0;i<metaList.length;i++){
    var tmp = metaList[i];
    var tmpMap = {};
    var colo = immuneMetaGradientName[tmp['name']];
    if(colo == 'yellow'){
      $.each(tmp['array'],function(i,v){
        var index = yellowSortList.indexOf(v);
        tmpMap[v]=yellowColorList[index]
      })
    } else if(colo == 'green'){
      $.each(tmp['array'],function(i,v){
        var index = greenSortList.indexOf(v);
        tmpMap[v]=greenColorList[index]
      })
    }

    if(tmp['name'] == "Cell type-based IC"){
      returnMap[tmp['name']]={'NAT-enriched':'#d8b365','CTE':'#2ca02c','HTE':'#1f77b4'};
    } else if(tmp['name'] == 'Other Oncogene Alteration'){
      returnMap[tmp['name']]={'None':'#ffffff','KRAS':'#aec7e8','RET':'#ff7f0e','ALK':'#ffbb78',
                            'ERBB2':'#2ca02c','PIK3CA':'#98df8a','MET':'#d62728','KRAS_PIK3CA':'#ff9896'};
    } else if(tmp['name'] == "Recurrence Status"){
      returnMap[tmp['name']]={'0':'#d8b365','1':'#2ca02c','':'#ffffff'};
    }else{
      returnMap[tmp['name']]=tmpMap;
    }

  }

  return returnMap;
}

function ascOrder (a, b) {
  return a - b
}

function rgbToHex(r, g, b){
  var hex = ((r << 16) | (g << 8) | b).toString(16);
  return "#" + new Array(Math.abs(hex.length - 7)).join("0") + hex;
}
// hex to rgb
function hexToRgb(hex){
   var rgb = [];
   for (var i = 1; i < 7; i += 2){
      rgb.push(parseInt("0x" + hex.slice(i, i + 2)));
   }
   return rgb;
}

function gradient(startColor, endColor, step){
  
   var sColor = hexToRgb(startColor),
   eColor = hexToRgb(endColor);

  
  var rStep = (eColor[0] - sColor[0]) / step,
      gStep = (eColor[1] - sColor[1]) / step,
      bStep = (eColor[2] - sColor[2]) / step;

  var gradientColorArr = [];
  for (var i = 0;i < step;i++){
      gradientColorArr.push(rgbToHex(parseInt(rStep * i + sColor[0]), parseInt(gStep * i + sColor[1]), parseInt(bStep * i + sColor[2])));
  }
  return gradientColorArr;
}

function gradient_two(startColor, endColor, sortList){

  var upZeroList = []
  var downZeroList = []
  var k = 0
  var j = 0

  $.each(sortList,function(i,v){
    if(v>=0){
      upZeroList[k] = v;
      k++;
    }else{
      downZeroList[j] = v;
      j++
    }
  });

  upZeroColorArr = gradient('#FFFFFF',endColor,upZeroList.length);
  downZeroColorArr = gradient(startColor,'#FFFFFF',downZeroList.length);

 var gradientColorArr = $.merge(downZeroColorArr, upZeroColorArr)
 
 return gradientColorArr;
}