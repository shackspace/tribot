
var ongoingTouches = new Array();
var display;
var control;
var count;
function uiInit()
{
    display = $("#display");
    control = $("#control");
    count = 0;
    control.mousemove(function(e)
    {
        var currentOffset = $("#control").offset(); 
        var relX = e.pageX - currentOffset.left;
        var relY = e.pageY - currentOffset.top;
        var middleX = control.width()/2;
        var middleY = control.height()/2;
        var vecX = parseInt(relX - middleX);
        var vecY = -parseInt(relY - middleY);
        var len = Math.sqrt(vecX * vecX + vecY * vecY);
        var dir = Math.acos(vecY / len);
        if(vecX < 0)
        {
            dir = 2 * 3.1415 - dir;
        }
        dir = parseInt(dir * 360 / 2 / 3.1415);
        len = parseInt(len / 2);
        if (len > 50)
        {
            len = 50;
        }

        display.html("Direction:" + dir + " Velocity:"+ len+ "<br/> x" + vecX + " y:" + vecY )
    });
    $(document).keydown(function(eventObject)
    {
        switch (eventObject.keyCode)
        {
            case 81://Q
                query["rotation"] += 1;
                break;
            case 87://W
                query["speed"] += 1;
                break;
            case 69://E
                query["rotation"] -= 1;
                break;
            case 65://A
                query["direction"] += 1;
                break;
            case 83://S
                query["speed"] -= 1;
                break;
            case 68://D
                query["direction"] -= 1;
                break;
            case 32://Space
                //query["speed"]=0;
                //query["rotation"]=0;
                //query["direction"]=0;
                query["enable"]=false;
                break;
            case 13://Enter
                query["enable"]=true;  
        }
        if(query["rotation"] > 50)
            query["rotation"] = 50;
        if(query["rotation"] < -50)
            query["rotation"] = -50;
        if(query["speed"] > 50)
            query["speed"] = 50;
        if(query["speed"] < -50)
            query["speed"] = -50;
        if(query["direction"] > 180)
            query["direction"] = -179;
        if(query["direction"] < -179)
            query["direction"] = 180;
        display.html(
            "Speed:" + query["speed"] +
            "Roatation" + query["rotation"] +
            "Direction" + query["direction"] +
            "Enable" +  query["enable"]);
    })
}
