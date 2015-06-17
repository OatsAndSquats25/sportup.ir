function popupwindow(url, title, w, h) {
    var left = (screen.width/2)-(w/2);
    var top = (screen.height/2)-(h/2);
    popupWindow =  window.open(url, title, 'toolbar=no, location=no, directories=no, status=no, menubar=no, addressbars=no, resizable=no, copyhistory=no, width='+w+', height='+h+', top='+top+', left='+left);
     return popupWindow
}

function refreshParent() {
    window.opener.location.reload();
}
