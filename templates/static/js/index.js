
// 选项卡
function tabClick(tabChil,tabColor,tabBox){
    $(tabChil ).click(function () {
        $(this).addClass(tabColor).siblings(tabChil).removeClass(tabColor);
        var num = $(this).index();
        $(tabBox).eq(num).show().siblings(tabBox).hide();
    });
}
function activeColor(actBox,actCololr){
    $(actBox).click(function(){
        $(this).stop().addClass(actCololr).siblings().removeClass(actCololr);
    });
}

