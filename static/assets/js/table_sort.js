$(document).on('click','th',function(){
    var table = $(this).parents('table').eq(0);
    var rows = table.find('tr:gt(1)').toArray().sort(comparer($(this).index()));
    this.asc = !this.asc;
    if (!this.asc){rows = rows.reverse();}
    table.children('tbody').empty().html(rows);
});
function comparer(index) {
    return function(a, b) {
        var valA = getCellValue(a, index), valB = getCellValue(b, index);
        return $.isNumeric(valA) && $.isNumeric(valB) ?
            valA - valB : valA.localeCompare(valB);
    };
}
var name_damage_re = /\(\d\-\d\)(\d+)/;
function getCellValue(row, index){
    console.log(row)
    var text_value = $(row).children('td').eq(index).text()
    console.log("元素", text_value)
    var value = 0
    if (text_value !== ""){
        // 非空字符串，尝试匹配boss名+伤害的re
        var match_array = text_value.match(name_damage_re)
        if (match_array !== null){
            // 匹配成功，伤害部分转int
            value = parseFloat(match_array[0])
            console.log("匹配成功", value)
        }
        else{
            // 匹配失败，直接转int
            value = parseFloat(text_value)
            console.log("匹配失败", value)
        }
    }
    else{
        console.log("空字符", value)
    }
    console.log(value)
    return value;
}