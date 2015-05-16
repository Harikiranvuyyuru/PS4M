var button = new Array(100);
var LESS = 'less';
var MORE = 'more';

var curVoteId = null;
var curButtonNum = null;
var curVoteType = null;

function createAccount() {
    var userName = $('input:text[name=newAccount-username]').val();
    var password1 = $('input:password[name=newAccount-password]').val();
    var password2 = $('input:password[name=newAccount-password2]').val();

    if(userName == '') {
        $('#createAccountErrorMsg').text("Enter user name");
    } else if (password1 == '') {
        $('#createAccountErrorMsg').text("Enter password");
    } else if(password2 == '') {
        $('#createAccountErrorMsg').text("Confirm password");
    } else if(password1 != password2) {
        $('#createAccountErrorMsg').text("Passwords do not match");
    } else {
	// Everything checks out on this side, request a new account
	$.post("/signUp", {'userName': userName, 'password': password1},
               function() {
                   updateUiForLogIn(userName);
               }
	  ).fail(function(data) { 
	      $('#createAccountErrorMsg').text(data.responseText); 
	  });
    }
}

function getFilteredItems() {
    var filterStr = $.cookie("filterList");
    if(filterStr == null) {
        return {};
    }

    var result = {};
    var filterArr = unescape(filterStr).split(",");
    for (var i = 0; i < filterArr.length; i++) {
        result[filterArr[i]] = 1;
    }
    return result;
}

function hideItems(cssClass) {
    var items = $('.item');
    for(var i = 0; i < items.length; i++) {
        var curItem = $('#item-' + i);
        if(curItem.hasClass(cssClass)) {
            curItem.addClass("hide");
        }
    }
}

function setFilterList(filteredHash) {
    var filtered = [];
    for (var i in filteredHash) {
        filtered.push(i);
    }
    filtered = filtered.join(",");
    $.cookie("filterList", filtered);
}

function unHideItems(cssClass) {
    var items = $('.item');
    for(var i = 0; i < items.length; i++) {
        var curItem = $('#item-' + i);
        if(curItem.hasClass(cssClass)) {
            curItem.removeClass("hide");
        }
    }
}

function updateItems(changedValue) {
    var filtered = getFilteredItems();
    if(changedValue in filtered) {
        delete filtered[changedValue];
        unHideItems(changedValue);
    } else {
        filtered[changedValue] = 1;
        hideItems(changedValue);
    }
    setFilterList(filtered);
}


function init() {
    var filtered = getFilteredItems();
    for(var i in filtered) {
        $('#filter-' + i)[0].checked = false;
        hideItems(i);
    }
}

function logIn() {
    var userName = $('input:text[name=logIn-userName]').val();
    var password = $('input:password[name=logIn-password]').val();

    $.post("/logIn", {'userName': userName, 'password': password},
           function() {
               updateUiForLogIn(userName);
           }
	  ).fail(function(data) { 
	      $('#loginErrorMsg').text(data.responseText); 
	  });
}

function buttonMouseOver(num, type) {
    if(!isButtonSet(num, type)) {
        colorButton(num, type)
    } else {
        uncolorButton(num, type)
    }
}

function buttonMouseOut(num, type) {
    if(!isButtonSet(num, type)) {
        uncolorButton(num, type)
    } else {
        colorButton(num, type)
    }
}

function isButtonSet(num, type) {
    return button[num] == type;
}

function lightbox() {
    $('.lightboxBackdrop, .lightbox').animate({'opacity':'.50'}, 300, 'linear');
    $('.lightbox').animate({'opacity':'1.00'}, 300, 'linear');
    $('.lightboxBackdrop, .lightbox').css('display', 'block');
    $('input:text[name=logIn-userName]').focus()
}

function lightboxClose() {
    $('.lightboxBackdrop, .lightbox').animate({'opacity':'0'}, 300, 'linear', function(){
        $('.lightboxBackdrop, .lightbox').css('display', 'none');
    });
}

function colorButton(num, type) {
    if(type == LESS) {
        $('#l' + num).addClass("less-clicked");
    } else if (type == MORE) {
        $('#m' + num).addClass("more-clicked");
    }
}

function uncolorButton(num, type) {
    if(type == MORE) {
        $('#m' + num).removeClass("more-clicked");
    } else if (type == LESS) {
        $('#l' + num).removeClass("less-clicked");
    }
}

function updateUiForLogIn(userName) {
    $('#userBox').html(userName + " (<a href='/logOut'>logout</a>)&nbsp&nbsp|&nbsp&nbsp<a href='/liked'>Liked</a>");
    if(curVoteId != null) {
	vote(curVoteId, curButtonNum, curVoteType);
        curVoteId = null;
        curButtonNum = null;
        curVoteType = null;
    }
    lightboxClose();
}

function vote(itemId, buttonNum, voteType) {
    // Is the user logged in? 
    if($.cookie("sessionData") == null) {
        lightbox();

        // Save this for after they complete the form.
        curVoteId = itemId;
        curVoteType = voteType;
        curButtonNum = buttonNum;

        return;
    }

    var postParams = {itemId: itemId, voteType: voteType};
    var savedType = button[buttonNum];

    if(savedType == undefined) {
        // Standard vote
        postParams["action"] = "vote";
        colorButton(buttonNum, voteType);
        button[buttonNum] = voteType;
    } else if (savedType == voteType) {
        // Undo vote
        postParams["action"] = "undo";
        uncolorButton(buttonNum, voteType);
        button[buttonNum] = undefined;
    } else { 
        // Toggle vote (savedType == undefinded && savedType == voteType)
        postParams["action"] = "toggle";
        var reverseType = (voteType == MORE) ? LESS : MORE;
        uncolorButton(buttonNum, reverseType);
        colorButton(buttonNum, voteType);
        button[buttonNum] = voteType;
    }
    
    $.post("/vote", postParams);
}

$(document).ready(function(){
    $('.lightboxClose').click(function(){
        lightboxClose();
    });
    
    $('.lightboxBackdrop').click(function(){
        lightboxClose();
    });

});

