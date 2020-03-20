function main(){
//Cards on the main screen:
//Profile, Journal, Finances, Reports
var thebigfour=document.querySelectorAll("table[onclick*='/Default.aspx']");



for (let i = 0; i < thebigfour.length; i++) {
    thebigfour[i].classList.add("theBigFour");
}


//Tabs on the top:
var topTabs=document.querySelector('td[style="background-position: center; background-repeat: repeat-x"]');
topTabs.classList.add("hidden");

var mainBody=document.querySelector('td[bgcolor="White"]');
mainBody.classList.add("blueBG");

//The menu
var rightSide=document.querySelector('td[style="font-family: Arial; font-size: 9pt;"][align="center"]');
rightSide.classList.add("grayBG")

//The sidebar
//moving the ribbon to the sidebar
var leftSide=document.querySelector('td[valign="top"][align="left"]');
ribbon=document.getElementById("ctl00_img_Badge");
ribbonLbl=document.getElementById("ctl00_lbl_Badge1");
var table=document.createElement('table');
var row=document.createElement('tr');
var col1=document.createElement('td');
var col2=document.createElement('td');
col1.appendChild(ribbon);
col2.appendChild(ribbonLbl);
row.appendChild(col1);
row.appendChild(col2);
table.appendChild(row);
leftSide.appendChild(table);

var advisorAlert=document.querySelector('th[scope="col"][style="color:#AD7A24;background-color:White;border-style:None;font-size:10px;"]')
if (advisorAlert){
advisorAlert.classList.add("advisorAlert");
}

//Other buttons
var otherBtns=document.querySelectorAll('tr[style*="cursor: pointer;"],td[style*="cursor: pointer;"],tr[style="height: 50px; vertical-align: top;"]');
console.log(otherBtns);
for (let i = 0; i < otherBtns.length; i++) {
    otherBtns[i].classList.add("otherBtns");
}
//Tabs
var tabs=document.querySelector('td[valign="bottom"][align="right"]');
var newTabs=tabs.children[0].children[0].children[1].children;
for (let i = 0; i < newTabs.length; i++) {
    newTabs[i].classList.add('noBgImage');
}
//Header
var header=document.querySelector('table[style="width: 100%;"][cellspacing="0"][cellpadding="0"]');
var headerChildren=header.children[0].children[0].children[1].children[0].children[0].children[0];

var tabsTD=document.createElement("td")
tabsTD.appendChild(tabs);
headerChildren.replaceChild(tabsTD,headerChildren.children[2]);


}
window.addEventListener('load', function (){
main()
});
