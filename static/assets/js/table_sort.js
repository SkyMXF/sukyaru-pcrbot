$(document).on('click','th',function(){
    var table = $(this).parents('table').eq(0);

    
    var index_in_html = $(this).index()
    var col_name_in_html = $(this).text()
    var real_index = index_in_html

    var head_row_num = table.find("thead").find("tr").toArray().length
    if (head_row_num > 1){
        // 是复合表头，需要计算实际排序依据列号
        switch(index_in_html){
            case 0:
                if (col_name_in_html === "昵称") real_index = 0;    // 昵称
                else if (col_name_in_html === "伤害") real_index = 1; // 第一刀伤害
                break;
            case 1:
                if (col_name_in_html === "第一刀") real_index = 1;    // 第一刀伤害
                else if (col_name_in_html === "补偿刀") real_index = 2; // 第一刀补偿刀
                break;
            case 2:
                real_index = 3; // 第二刀伤害
                break;
            case 3:
                if (col_name_in_html === "第三刀") real_index = 5;    // 第三刀伤害
                else if (col_name_in_html === "补偿刀") real_index = 4; // 第二刀补偿刀
                break;
            case 4:
                if (col_name_in_html === "积分") real_index = 7;    // 积分
                else if (col_name_in_html === "伤害") real_index = 5; // 第三刀伤害
                break;
            case 5:
                real_index = 6; // 第三刀补偿刀
                break;
        }
    }
    console.log("选择和实际排序: ",index_in_html,col_name_in_html,real_index)

    // 排序
    var rows = table.find("tbody").find('tr').toArray().sort(comparer(real_index));
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
var name_damage_re = /^.*?\(\d\-\d\)\s(\d+)$/;
var only_number_re = /^(\d+)(\.\d+)?$/;
function getCellValue(row, index){
    var text_value = $(row).children('td').eq(index).text()
    var value = 0
    if (text_value !== ""){
        // 非空字符串，尝试匹配boss名+伤害的re
        var match_array = text_value.match(name_damage_re)
        if (match_array !== null){
            // 匹配成功，伤害部分转int
            value = parseFloat(match_array[0])
            console.log("匹配字符", match_array[0], match_array)
        }
        else{
            // 匹配boss名+伤害的re失败, 尝试匹配纯数字
            if (text_value.match(only_number_re)){
                value = parseFloat(text_value)
            }
            else{
                // 匹配纯数字失败，认为是无需转换的字符串
                value = text_value
            }
        }
    }
    return value;
}