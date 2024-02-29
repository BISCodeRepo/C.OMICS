///////////////////////새로고침 화면 로드//////////////////////////////
function showSpinner(nameConent) {
    //debugger
    $('#'+nameConent+' .layerPopup').css('display','block');
  }
  
  function hideSpinner(nameConent) {
    $('#'+nameConent+' .layerPopup').css('display','none');
  }