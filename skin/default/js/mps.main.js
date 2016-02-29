// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

//
// UX Debug Mode: Do Not Ship (well, it is ok to ship === false, just sloppy...)
//
var cvApp = cvApp || {};
cvApp.uxDebug = true;

//
// Shims, Polyfills, & Global Util Fns
//
if(typeof String.prototype.trim !== 'function') {
    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g, '');
    }
}

var validateDate = function (value, format) {
	if (value === undefined || value.trim() === '') return false;
	if (value.match(/^(\d{1,2})(\/|-)*(\d{1,2})(\/|-)*(\d{4})$/) == null) return false;

	try { return $.datepicker.parseDate(format, value); }
	catch (e) { return false; }
};

var closeDialog = function() {
	$(this).closest('.ui-dialog-content').dialog('close');
};

var showWarningDialog = function(dialogargs, successCallback, callbackargs) {
	var $warningdialog = $('#warningdialog');
	var $warntextspan = $warningdialog.find('.dialogwarntext');

	$warntextspan.text(dialogargs.dialogWarningText);
	$warningdialog.dialog({
		width: '300px', modal: true,
		buttons: [
			{ text: 'Yes', 'class': "btn", click: function() { successCallback(callbackargs); } },
			{ text: "Cancel", 'class': "cancel", click: closeDialog }
		]
	});
	$warningdialog.closest('.ui-dialog').find('.ui-dialog-title').text(dialogargs.dialogTitle);
};

var showAlertDialog = function(title, warntext) {
	var $warningdialog = $('#warningdialog');
	var $warntextspan = $warningdialog.find('.dialogwarntext');

	$warntextspan.text(warntext);
	$warningdialog.dialog({ width: '300px', modal: true, buttons: [ { text: 'OK', click: closeDialog } ] });
	$warningdialog.closest('.ui-dialog').find('.ui-dialog-title').text(title);
};

(function ($) {

    // Generic xsrf token include for all jQuery ajax reqs/responses:
    if(typeof ajaxPayload === 'object' && typeof ajaxPayload['_xsrf'] != null){
        $.ajaxSetup({
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-Xsrftoken', ajaxPayload['_xsrf']);
            }
        });
    };

    $.fn.serializeObject = function (periods) {
        "use strict";

        periods = typeof periods !== 'undefined' ? periods : true;

        var result = {};
        var extend = function (i, element) {
            var elemvalue = $.trim(element.value);
            if (periods) {
                if ('undefined' !== typeof result[element.name] && result[element.name] !== null) {
                    if ($.isArray(result[element.name])) result[element.name].push(elemvalue);
                    else result[element.name] = [result[element.name], elemvalue];
                } else
                    result[element.name] = elemvalue;
                return;
            }

            var node;
            var prev = result;
            var parts = element.name.split('.');

            if (parts.length > 1) {
                    for (i = 0; i < parts.length - 1; i++) {
                        node = prev[parts[i]];
                        if ('undefined' === typeof node || node === null) node = prev[parts[i]] = {};
                        prev = prev[parts[i]];
                }
            } else node = result;

            var lastpart = parts[parts.length-1];

            // If node with same name exists already, need to convert it to an array as it
            // is a multi-value field (i.e., checkboxes)
            if ('undefined' !== typeof node[lastpart] && node[lastpart] !== null) {
                if ($.isArray(node[lastpart])) node[lastpart].push(elemvalue);
                else node[lastpart] = [node[lastpart], elemvalue];
            } else  node[lastpart] = elemvalue;
        };

        $.each(this.serializeArray(), extend);
        return result;
    };

    // Generic url [url]# char-append scroll prevention
	$('body').on('click', 'a', function(ev){
		if($(ev.target).attr('href') == '#'){
			ev.preventDefault();
		}
	});

	// We do support Bootstrap Tooltips, which require initialization on selector:
	$('[data-toggle="tooltip"]').tooltip();

	// Header Menu Disabling:
	$('.mpsheader .navbar-nav').on('click', 'li a', function(event){
		// If the menu is disabled, stopProp & default...
		if( $(event.target).closest('ul').hasClass('mps-menu-disabled') ){
			event.stopPropagation();
			event.preventDefault();
		}
	});

	$('input.tbl-header-select-all').on('change', function(){
		var $this = $(this),
			nth = $this.data('nthCol') || false,
			tblId = $this.data('tblId') || false;
		if(nth === false || tblId === false){return false;}
		var $chks = $('table#'+tblId).find('tbody tr td:nth-child('+nth+') input[type=checkbox]');
		$chks.prop('checked', $(this).prop('checked'));
	});

})(jQuery);
