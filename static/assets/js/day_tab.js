var tabs = document.getElementsByClassName('tab-head')[0].getElementsByClassName('selected');
tabs = tabs.concat(document.getElementsByClassName('tab-head')[0].getElementsByClassName('unselected'));
contents = document.getElementsByClassName('tab-content')[0].getElementsByClassName('show');
contents = contents.concat(document.getElementsByClassName('tab-content')[0].getElementsByClassName('hide'));

(function changeTab(tab) {
    for(var i = 0, len = tabs.length; i < len; i++) {
        tabs[i].onmouseover = showTab;
    }
})();

function showTab() {
    for(var i = 0, len = tabs.length; i < len; i++) {
        if(tabs[i] === this) {
            tabs[i].className = 'selected';
            contents[i].className = 'show';
        } else {
            tabs[i].className = 'unselected';
            contents[i].className = 'hide';
        }
    }
}