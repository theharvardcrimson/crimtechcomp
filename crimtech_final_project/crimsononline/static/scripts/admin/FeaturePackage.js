var baseIdvar = "";

$(document).ready(function() {
    //alert($("div.add-row").children("a").length);
    $('div.add-row').children('a').click(function(){
        addRowClick(baseIdvar);
    });
    //window.setTimeout("$('div.add-row').children('a').click(function(){addRowClick",1000);
});

function addRowClick(baseId) {
    var counter = 1;
    var newId = baseId.replace("__prefix__","1");
    //alert(newId);
    while($("#"+newId).length>0){
        newId = newId.replace("-"+(counter).toString()+"-","-"+(counter+1).toString()+"-");
        counter++;
    }

    counter--;
    newId = newId.replace("-"+(counter+1).toString()+"-","-"+(counter).toString()+"-");
    set_related_content(newId,['Image', 'Gallery', 'Article', 'Map', 'FlashGraphic', 'Video']);
}
