<html>

<head>
<script src="http://www.google.com/jsapi" type="text/javascript"></script> 
<script type="text/javascript">google.load("jquery", "1.6.4");</script>
<script type="text/javascript">
function get_XPath(elt)
{
    var path = '';
    for (; elt && elt.nodeType==1; elt=elt.parentNode)
    {     
        var idx=$(elt.parentNode).children(elt.tagName).index(elt)+1;
        idx>1 ? (idx='['+idx+']') : (idx='');
        path='/'+elt.tagName.toLowerCase()+idx+path;
    }
    return path;
}
</script>
<style>
.%(css_class)s {
    background-color : #FFA500;
}
</style>
</head>

<body>
%(content)s
</body>

<script type="text/javascript">
$('body').click(function(event) 
{    
    xpath = get_XPath(event.target)    
    className = "%(css_class)s"
    element = $(event.target)    
    
    if (element.hasClass(className))
        element.removeClass(className)
    else
        element.addClass(className)
    
    element[0].id = xpath    
});
</script>

</html>
