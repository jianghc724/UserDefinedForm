/**
 * Created with PyCharm.
 * User: Epsirom
 * Date: 13-12-14
 * Time: 上午11:36
 */

function upmenu(count) {
    if (count > 0) {
        var menus = locals.usedSections;
        var menu = menus[count];
        menus[count] = menus[count - 1];
        menus[count - 1] = menu;
        render();
     }
}

function downmenu(count) {
    var menus = locals.usedSections;
    var len = menus.length;
    if (count < len - 1) {
        var menu = menus[count];
        menus[count] = menus[count + 1];
        menus[count + 1] = menu;
        render();
    }
}

function removemenu(count) {
    var menus = locals.usedSections;
    locals.unusedQuestions.push(menus.splice(count, 1)[0]);
    render();
}

function change_alter(i) {
    var alters = locals.unusedSections;
    var menus = locals.usedSections;
    menus.push(alters.splice(i, 1)[0]);
    render();
}
