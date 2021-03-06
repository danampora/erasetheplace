// ==UserScript==
// @name         EraseBot
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Erase the place!
// @author       mbarkhau, alex
// @updateurl    https://github.com/IncognitoJam/erasetheplace/blob/master/bot.user.js
// @downloadurl  https://github.com/IncognitoJam/erasetheplace/blob/master/bot.user.js
// @match        https://www.reddit.com/place*
// @match        https://www.reddit.com/place?webview=true
// @match        https://www.reddit.com/place?webview=true/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    var imageX = 474;
    var imageY = 402;
    var image = `xxxxxxxxxxxxxxxxxxxxxxbbxxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxxbbbbxxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxxbbwwbbxxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxxbbwwwwbbxxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxxbbwwwwwwbbxxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxxbbwwwwwwwwbbxxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxxbbwwwwwwwwwwbbxxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxxbbwwwwwwwwwwwwbbxxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxxbbwwwwwwwwwwwwwwbbxxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxxbbwwwwwwwwwwwwwwwwbbxxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxxbbwwwwwwwwwwwwwwwwwwbbxxxxxxxxxxxxxxxxxx
xxxxxxxxxxxbbwwwwwwwwwwwwwwwwwwwwbbxxxxxxxxxxxxxxxxx
xxxxxxxxxxbbwwwwwwwwwwwwwwwwwwwwwwbbxxxxxxxxxxxxxxxx
xxxxxxxxxbbwwwwwwwwwwwwwwwwwwwwwwwwbbxxxxxxxxxxxxxxx
xxxxxxxxbbwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxxxxxxxxxxxxx
xxxxxxxbbwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxxxxxxxxxxxx
xxxxxxbbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxxxxxxxxxxx
xxxxxbbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxxxxxxxxxx
xxxxbbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxxxxxxxxx
bbbbbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxxxxxxxx
bwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxxxxxxx
bwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxxxxxx
bwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxxxxx
bwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbxxxxxx
bwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxxx
bwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxxx
bwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbxx
bwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbbx
bwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbb
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`.split('\n');

    var colors = {
        "w": 0,   // white
        "b": 3,  // black
        "x": -1,   // null
    };

    var image_data = [];
    for (var relY = 0; relY < image.length; relY++) {
        var row = image[relY];
        for (var relX = 0; relX < row.length; relX++) {
            var color = colors[row[relX]];
            var absX = imageX + relX;
            var absY = imageY + relY;
            image_data.push(absX);
            image_data.push(absY);
            image_data.push(color);
        }
    }


    var p = r.place;

    r.placeModule("placePaintBot", function(loader) {
        var c = loader("canvasse");

        setInterval(function() {
            if (p.getCooldownTimeRemaining() > 200) {
                return;
            }
            for (var i = 0; i < image_data.length; i += 3) {
                var j = Math.floor((Math.random() * image_data.length) / 3) * 3;
                var x = image_data[j + 0];
                var y = image_data[j + 1];
                var color = image_data[j + 2];
                var currentColor = p.state[c.getIndexFromCoords(x, y)];

                if (currentColor != color && color > -1) {
                    console.log("set color for", x, y, "old", currentColor, "new", color);
                    p.setColor(color);
                    p.drawTile(x, y);
                    return;
                }
            }
            console.log("noop");
        }, 1500);
    });
})();
