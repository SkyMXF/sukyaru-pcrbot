var tabs = document.getElementsByClassName('tab-head')[0].getElementsByTagName('h3'),
contents = document.getElementsByClassName('tab-content')[0].getElementsByTagName('div');

(function changeTab(tab) {
    for(var i = 0, len = tabs.length; i < len; i++) {
        tabs[i].onmousedown = showTab;
    }
})();

function showTab() {
    var content_pos = 0
    for(var i = 0, len = tabs.length; i < len; i++) {
        while (contents[content_pos].className === "table-wrapper" || contents[content_pos].className === "damage_chart") {
            content_pos += 1;
        }
        if(tabs[i] === this) {
            tabs[i].className = 'selected';
            contents[content_pos].className = 'show';
        } else {
            tabs[i].className = '';
            contents[content_pos].className = 'hide';
        }
        content_pos++;
    }
}