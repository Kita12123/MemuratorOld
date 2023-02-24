//#######################################################################################
//    データ種類　選択
//#######################################################################################
/*
### Function ###
*/
//選択済み
function Selected(id, id2){
    document.querySelector(id2).style.backgroundColor = "#FFF";
    var obj = document.querySelector(id);
    obj.style.color = "#000000";
    obj.style.backgroundColor = "#FFF";
}
//選択可能
function CanSelect(id, id2){
    document.querySelector(id2).style.backgroundColor = "#AFAFAF";
    var obj = document.querySelector(id);
    obj.style.color = "#FFF";
    obj.style.backgroundColor = "#AFAFAF";
}
/*
### Main ###
*/
//明細データ
function showTable(){
    document.querySelector('#table').style.display    = '';
    document.querySelector('#totall1').style.display  = 'none';
    document.querySelector('#totall2').style.display  = 'none';
    document.querySelector('#totall3').style.display  = 'none';
    Selected(id='#tab1', id2='#tab1b');
    CanSelect(id='#tab2', id2='#tab2b');
    CanSelect(id='#tab3', id2='#tab3b');
    CanSelect(id='#tab4', id2='#tab4b');
}
//集計1
function showTotall1(){
    document.querySelector('#table').style.display    = 'none';
    document.querySelector('#totall1').style.display  = '';
    document.querySelector('#totall2').style.display  = 'none';
    document.querySelector('#totall3').style.display  = 'none';
    CanSelect(id='#tab1', id2='#tab1b');
    Selected(id='#tab2', id2='#tab2b');
    CanSelect(id='#tab3', id2='#tab3b');
    CanSelect(id='#tab4', id2='#tab4b');
}
//集計2
function showTotall2(){
    document.querySelector('#table').style.display    = 'none';
    document.querySelector('#totall1').style.display  = 'none';
    document.querySelector('#totall2').style.display  = '';
    document.querySelector('#totall3').style.display  = 'none';
    CanSelect(id='#tab1', id2='#tab1b');
    CanSelect(id='#tab2', id2='#tab2b');
    Selected(id='#tab3', id2='#tab3b');
    CanSelect(id='#tab4', id2='#tab4b');
}
//集計3
function showTotall3(){
    document.querySelector('#table').style.display    = 'none';
    document.querySelector('#totall1').style.display  = 'none';
    document.querySelector('#totall2').style.display  = 'none';
    document.querySelector('#totall3').style.display  = '';
    CanSelect(id='#tab1', id2='#tab1b');
    CanSelect(id='#tab2', id2='#tab2b');
    CanSelect(id='#tab3', id2='#tab3b');
    Selected(id='#tab4', id2='#tab4b');
}

//チェックボックス
let checkBox = document.getElementsByClassName("checkBox");

//全てのチェックボックスをON/OFFする
function checkBoxChecked(){
    bool = document.getElementById("checkBoxAll").checked;
    for (let i = 0; i < checkBox.length; i++) {
        checkBox[i].checked = bool;
    }
}