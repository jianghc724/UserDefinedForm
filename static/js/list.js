/**
 * Created with PyCharm.
 * User: Epsirom
 * Date: 13-12-3
 * Time: 下午11:12
 */

var timeOffset = 0;

function wrapTwoDigit(num) {
    if (num < 10) {
        return '0' + num;
    } else {
        return num;
    }
}

function getChsDate(dt) {
    return wrapTwoDigit(dt.getDate()) + '日';
}

function getChsMonthDay(dt) {
    return wrapTwoDigit(dt.getMonth() + 1) + '月' + getChsDate(dt);
}

function getChsFullDate(dt) {
    return dt.getFullYear() + '年' + getChsMonthDay(dt);
}

function getChsDay(dt) {
    var dayMap = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    return dayMap[dt.getDay()];
}

function getTimeStr(dt) {
    return wrapTwoDigit(dt.getHours()) + ':' + wrapTwoDigit(dt.getMinutes());
}

function getTime(time) {
    var result = getChsFullDate(time) + ' ' + getChsDay(time) + ' ' + getTimeStr(time);
    return result;
}

function expand_long_text(dom) {
    var newhtml, par = $(dom).parent(), refdata = par.text().trim();
    dom = $(dom);
    refdata = refdata.substring(0, refdata.length - 3);
    newhtml = dom.attr('ref-data') + ' <a style="cursor:pointer;" ref-data="' + refdata + '" ref-hint="' + dom.text() + '" onclick="expand_long_text(this);">' + dom.attr('ref-hint') + '</a>';
    par.html(newhtml);
}

function getUpperName(id) {
    var result = ['CBD', 'CEX', 'DOPS', 'OOT', 'PAT'];
    return result[id - 1];
}

function getLowerName(id) {
    var result = ['cbd', 'cex', 'dops', 'oot', 'pat'];
    return result[id - 1];
}