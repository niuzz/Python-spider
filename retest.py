import re


str = '{"contacthtml":"\n    <div class=\"pop-ups-bg\"><\/div>\n    <div class=\"orderpackage\">\n    <h3><span onclick=\"return closebox()\"><\/span>\u5a92\u4f53\u8be6\u60c5<\/h3>\n\t<dl class=\"account_details\">\n\t<dt><img src=\"\/api\/files\/20161203150450643.png\" class=\"mtimg\"><\/dt>\n\t<dd><h4>\u4e2d\u534e\u7f51\u79d1\u6280<span class=\"m_price\">\uffe5105.00<\/span><\/h4><div class=\"news_p\">\u5b98\u7f51:http:\/\/tech.china.com\/<\/div><\/dd><\/dl>\n    <div class=\"mediabody\"><span class=\"tip_bg\"><\/span><span class=\"tip_fg\"><\/span>\n\t<table class=\"tab01-batchdetail\">\n\t<tbody>\n\t<tr>\n\t<th>\u539f\u4ef7<\/th><td><em class=\"red\">150.00<\/em><\/td><th>\u5730\u533a<\/th><td><em class=\"red\">\u5168\u56fd<\/em><\/td><\/tr>\n\t<tr><th>\u5a92\u4f53\u7c7b\u578b<\/th><td><em>IT-\u79d1\u6280<\/em><\/td><th>\u7efc\u5408\u95e8\u6237<\/th><td><em>\u7efc\u5408\u95e8\u6237<\/em><\/td><\/tr>\n\t<tr><th>\u6848\u4f8b<\/th><td><em><a href=\"http:\/\/tech.china.com\/data\/11022462\/20160725\/23144779.html\" target=\"_blank\">\u67e5\u770b\u6848\u4f8b<\/a><\/em><\/td><th>\u5165\u53e3<\/th><td><em><a href=\"\/api\/files\/1509103394447.jpg\" target=\"_blank\">\u67e5\u770b\u5165\u53e3<\/a><\/em><\/td><\/tr>\n\t<tr><th>\u6536\u5f55\u53c2\u8003<\/th><td><em>\u65b0\u95fb\u6536\u5f55<\/em><\/td><th>\u94fe\u63a5\u7c7b\u578b<\/th><td><em>\u5a92\u4f53\u5b89\u6392;<\/em><\/td><\/tr>\n\t<tr><th>\u53ef\u53d1\u5a92\u4f53<\/th><td colspan=\"3\"><em>\u51fa\u7a3f\u5feb;\u7406\u8d22;\u53ef\u5e26\u7f72\u540d;\u6613\u4e0a\u76f8\u5173;\u6839\u636e\u5a92\u4f53\u5c5e\u6027<\/em><\/td><\/tr>\n\t<tr><th>\u4e0b\u5355\u5907\u6ce8<\/th><td colspan=\"3\"><em>\u6807\u989818\u5b57\u5185\uff0c\u7f51\u8d37\u4e0d\u53d1\uff0c\u65e0\u53e3<\/em><\/td><\/tr>\n\t<\/tbody>\n\t<\/table>\n\t<\/div>\n    <\/div>\n","status":"true"}'
str = str.replace("\n", "")
str = str.replace("\\", "")
print(str)
s = re.match('{(.*?)}', str)


astr = '<br />'
s = re.match('.*?<br />.*?', astr)
print(s)