// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

var cvApp = cvApp || {};
cvApp.ubiquitousModalFormLoad = function(options){
	//
	// An abstracted version of the ubiquitous click handling AJAX code used for EDIT and ADD Modals
	//

	// Safety: options should be an object...
	if (typeof options !== "object") {
	    console.log('Uh oh - a call is not working as desired: ', options);
	}
	else{
	    // Required: We must have unique url - other things are optional over-writes...
	    if (options.url.length <= 0 || typeof options.url !== "string") {
			console.log('Uh oh - a call is missing a URL: ', options);
	    }
	    else{

			// Now using a shared _wrap func with ubiquitousLoadModalForm...
			var request = {};
			request = cvApp._wrapRequestVarsFromOptions(options);
			request.data.response_type = options.response_type;

			//
			// This version doesn't always follow redirects in window... ;)
			//
			var $modal = $(options.modal.modal_element),
				$errorMsg = $modal.find(options.modal.modal_element),
				$body = $modal.find('.modal-body');

			request.success = options.success || function(data, textStatus, xhr) {
				if(!cvApp._checkSessionValidity(data, textStatus, xhr)){return false;};

				// We expect a server side redirect to state enabled form HTML at this point...
				$body.empty();
				$body.prepend($errorMsg);
				$body.append(data);

				// Load Repeating Field '+' & '-' buttons...
				cvApp._handleRepeatingFields();

				$body.find('[data-toggle="tooltip"]').tooltip(); // Instantiate tooltips on new DOM elements...

				var $pops = $body.find('.cvFieldHelpBtn');
				$pops.each(function(i, el){
				    var $el = $(el),
				        shelp = $el.parent().find('.cvFieldHelpContent').html(),
				        stitle = $el.closest('.form-row').find('label:first').text().replace('*','').replace(':', '') + ' Help:';

				    $el.click(function(e){
				        $(e).focus(); // Dumb Safari Bootstrap Popover fix
				    });

				    $(el).popover({
                        content: function(){
                            return shelp;
                        },
                        html: true,
                        placement: 'left',
                        title: function(){
                            return stitle;
                        },
                        container: '#editModal .modal-body'
                    });
				});

				// The Form is going to have it's own button, we will replace (hide & rebind on another El):
				$modal.find(options.modal.modal_button_replaces).hide();

				// New: Author Etc Widget fields need Init:
				$body.find('.mps-json-enums-widget').each(function(){

				});

				// New: Date-Pickers in CV Forms
				$body.find('.cv-date-picker').each(function(){
				    $(this).addClass('mps-date-picker');
				});
				window.setTimeout(function(){
				    mpsApp.mpsDatePickerizeDom($body);
				},0);



				// Bind the specified modal UX button to the Save callback():
				$modal.off('click', options.modal.modal_button)
				      .on('click', options.modal.modal_button, options.modal.modal_callback);

				$modal.off('keydown', '.modal-dialog select')
                    .on('keydown', '.modal-dialog select', function(ev){
                    if (ev.keyCode == 27) {
                        ev.stopPropagation();
                        ev.preventDefault();
                    }
                });

				// focus() on first :visible :input...
				window.setTimeout(function(){
					$body.find('input[type=text]:visible, select:visible, textarea:visible, input[type=radio]:visible').first().focus();
				}, 333);

			};
			request.error = function(jqXHR, textStatus, errorThrown) {
				cvApp.showPageMessage(textStatus, cvApp.ERROR, $errorMsg);
			}

			// Clear the modal error message HTML before continuing?
			if (typeof options.clearErrors === "undefined" || options.clearErrors === true) {
				cvApp.hideHeaderMessage($errorMsg);
			}

			//
			// The ajax() call - now it is trivial & generic
			// BUGBUG: add ajax abort handling?
			//
			$.ajax({
				url: request.url,
				type: request.type,
				data: request.data,
				headers: request.headers,
				success: request.success,
				error: request.error
			});
	    }
	}
};

cvApp._wrapRequestVarsFromOptions = function(options){
	// IN: options{}
	// OUT: request obj{} for ajax calls

	var payload = ajaxPayload; // ajaxPayload is global js loaded base set of app state values (3 now)
	var request = {url: options.url};

	// POST or ???
	request.type = options.type || "POST";

	var $errorEl = options.errorMessage ? $(options.errorMessage) :  $('#errorMessage');

	// BUGBUG: consider better if needed, but these work:
	request.headers = options.headers || { 'Content-Type': 'application/json' };

	//console.log('_wrapRequestVarsFromOptions:', options);

	request.success = options.success || function(data, textStatus, xhr) {

		if (typeof data.exception != 'undefined') {

		    //console.log('_wrapRequestVarsFromOptions data.exception:', data, textStatus);

		    cvApp.showPageMessage(data.exceptionMessage, cvApp.ERROR, $errorEl);
		    //$errorEl.text(data.exceptionMessage);
		    return true;
		}
		if (typeof data.error != 'undefined') {

		    //console.log('_wrapRequestVarsFromOptions data.error:', data, textStatus);

		    if(typeof options.success_error === "function"){
		        options.success_error(data, textStatus, xhr);
		    }
		    else{
		        cvApp.showHeaderMessage(data.error, cvApp.ERROR, $errorEl);
		        //$errorEl.text(data.error);
		    }
	    }
	    if (typeof data.errors != 'undefined') {

			//console.log('_wrapRequestVarsFromOptions data.errors:', data, textStatus);
            var msg = (typeof data.errors.message != 'undefined') ? data.errors.message : data.errors;
			cvApp.showHeaderMessage(msg, cvApp.ERROR, $errorEl);
			//$errorEl.text(data.errors.message);
			return;
		}

		if (typeof data.message != 'undefined') {

		    //console.log('_wrapRequestVarsFromOptions data.message:', data, textStatus);

		    cvApp.showHeaderMessage(data.message, cvApp.WARN, $errorEl);
		    //$errorEl.text(data.message);
		    return;
		}
		if (typeof data.msgid != 'undefined') {$.cookie('msgid', data.msgid, { path: '/'});}

		// Special Modal Redirect Handling...
		var $btn = $('#editModal #modalSaveButton');
		if (typeof data.redirect != 'undefined') {

            //console.log('_wrapRequestVarsFromOptions data.redirect:', data, textStatus);

            $btn.prop('disabled', true);
            $('#editModal').modal('hide');

            if(typeof options.success_redirect === "function"){
		        // Do the specified custom redirect
		        options.success_redirect(data, textStatus, xhr);
		    }
		    else{
                // Redirect (safe wrapper for Hash changes vs. browser behavior expecting in-page-links)
                cvApp.postRedirect(data.redirect);
            }
		}else{
		    // Enable the modal Save button after response
            $btn.prop('disabled', false);
		}


	};
	request.error = options.error || function(jqXHR, textStatus, errorThrown) {
        // Enable the modal Save button after response
        $btn = $('#editModal #modalSaveButton');
        $btn.prop('disabled', false);

        //console.log('_wrapRequestVarsFromOptions AJAX .error:', jqXHR, textStatus, errorThrown);

        cvApp.showHeaderMessage(textStatus, cvApp.ERROR, $('#errormessage'));
        //$('#errormessage').text(textStatus);
	}


	// Sometimes there will be other data (e.g. category_code), if so we add them to the payload
	if (typeof options.data === "undefined") {
		var reservedProps = ['url','clearErrors','type','headers','success','error','data','modal','redirect','success_error','success_redirect'];
		$.each(options, function(key,value) {
			if ($.inArray(key, reservedProps) < 0){payload[key] = value;}
		});
		request.data = JSON.stringify(payload);
	}
	else{
		request.data = options.data; // Some triggers push a serialized Form...
		$.extend(request.data, ajaxPayload); // Friendly extend with global payload vars...
	}

	return request;

};

cvApp.ubiquitousPageRequest = function(options){
	//
	// An abstracted version of the ubiquitous click handling AJAX code used for most navigation & submits/requests in the app
	// IN: a {} object with any one or more of URL, headers, cat_code, and callback Funcs pointers
	// OUT: an AJAX POST with rolled up data that will result in the desired POST and redirect with minimal local instance code.
	//

	// Safety: options should be an object...
	if (typeof options !== "object") {
	    console.log('Uh oh - a call is not working as desired: ', options);
	}
	else{
	    // Required: We must have unique url - other things are optional over-writes...
	    if (options.url.length <= 0 || typeof options.url !== "string") {
			console.log('Uh oh - a call is missing a URL: ', options);
	    }
	    else{
			// Everything other than .url will have defaults we can use 90%+ of the time...

			var $error = (options.errorMessage) ? $(options.errorMessage) : $('#errormessage');

			// Clear the error message HTML before continuing?
			if (typeof options.clearErrors === "undefined" || options.clearErrors === true) {
				$error.text('').fadeOut();
			}

			// Now using a shared _wrap func with ubiquitousLoadModalForm...
			var request = cvApp._wrapRequestVarsFromOptions(options);

			//
			// BUGBUG: add ajax abort handling?
			//
			$.ajax({
				url: request.url,
				type: request.type,
				data: request.data,
				headers: request.headers,
				success: request.success,
				error: request.error
			});
	    }
	}
};

cvApp._ubiquitousModalFormCallback = function(event){
    //
    // NOTE: This function is very specifically used for Modal Edit & Add dialogs, and should be passed back to ONLY
    //       ubiquitousModalFormLoad() calls...
    //

    // Disable the button so we don't spam-submit
    $btn = $(event.target);
    $btn.prop('disabled', true);

    cvApp.ubiquitousPageRequest({
        url: '/cv/save',
        data: JSON.stringify($('#editdetailform').serializeObject()),
        errorMessage: '#modalerrormessage',
        success: function(data, textStatus, xhr){

            if(!cvApp._checkSessionValidity(data, textStatus, xhr)){return false;};

            var $modal = $('#editModal'),
                $body = $modal.find('.modal-body'),
                $errorEl = $('#modalerrormessage'),
                $btn = $modal.find('#modalSaveButton');

            if(typeof data.error != "undefined"){
                // Insert the error msg
                $errorEl.text(data.error).show();

                // Scroll to top of modal:
                $body.scrollTop(1);
            }
            if(typeof data.errors != 'undefined'){
                // Toggle unSavedWork state.
                cvApp.isUnsavedModalWork = true;

                // Handle special Invalid Session ID:
                //console.log('ModalFormCallback:', data.errors);

                var sErr = '';

                // Clear Red UXs (if previously altered)
                $body.find('.errWrap').removeClass('has-error');
                $body.find('.errWrap *').removeClass('has-error');

                // Build & gild UXs
                for(k=data.errors.length-1; k >= 0; k--){

                    // Build error message
                    sErr = data.errors[k].message + '<br/>';

                    // Turn UXs red:
                    var $errEl = $body.find('[name='+data.errors[k].code+']:first');
                    $errEl.parent().addClass('has-error');

                    var iNit = $body.scrollTop();
                    $errEl.focus();

                    cvApp._showPopoverErrorOnElement({
                        target: '[name='+data.errors[k].code+']:first',
                        title: '',
                        body: data.errors[k].message,
                        code: data.errors[k].code
                    });

                    /* if(k == 0){
                        $errEl = $body.find('input[name='+data.errors[k].code+']:first');
                        window.setTimeout(function($errEl){
                            var iY = $errEl.offset().top;
                            if($body.scrollTop() >= iNit){
                                $body.scrollTop($body.scrollTop() + 30)
                            }
                            else if(iNit > $body.scrollTop()){
                                $body.scrollTop($body.scrollTop() - 50)
                            }
                        },100);
                    } */
                };

            }
            if (typeof data.exception != 'undefined') {$errorEl.text(data.exceptionMessage);}
            if (typeof data.message != 'undefined') {$errorEl.text(data.message);}
            if (typeof data.msgid != 'undefined') {$.cookie('msgid', data.msgid, { path: '/'});}
            if (typeof data.redirect != 'undefined') {

                // Disable the button after response
                $btn.prop('disabled', true);
                $('#editModal').modal('hide');

                // Put the background Grid UXs in a Loading state
                cvApp.triggerLoadingStates();

                // Toggle unSavedWork state.
                cvApp.isUnsavedModalWork = false;

                // Success!  Send an event to GA:
                if (typeof ga != "undefined") {
	                var eType = ($btn.closest('form').find('input[name=mode]').val() == 'edit') ? 'edit_item' : 'add_item',
	                    eLabel = cvApp.getSectionName();
	                ga('send', 'event', 'cv_item', eType, eLabel, {useBeacon: true});
	            };

                // Redirect (safe wrapper for Hash changes vs. browser behavior expecting in-page-links)
                cvApp.postRedirect(data.redirect);

            }
            else{
                // Enable the button after response
                $btn.prop('disabled', false);
            }
        }
    });
};

cvApp._checkSessionValidity = function(data, textStatus, xhr){
    // There are a couple things that could go wrong, so look for Errors
    var doSessionLogout = false;
    if(typeof data['errors'] == "string"){
        if(data['errors'] == "Invalid Session identifier" || data['errors'] == "This session has been idle. As a safety measure you have been logged out."){
            doSessionLogout = true;
        }
    }
    else if(typeof data == 'string' && data.indexOf('class="cvLoginPage') >= 0){
        // Certain actions, eg loading a modal edit dialog, can result in nested Login pages if session expired:
        doSessionLogout = true;
    }
    if (doSessionLogout){
        $('#editModal').modal('hide');
        cvApp.showHeaderMessage("This session has been idle. As a safety measure you have been logged out.", cvApp.ERROR, true);
        window.setTimeout(function(){window.location.href = "/admin/logout#ESI";}, 2000);
        return false;
    }
    return !doSessionLogout;
}

cvApp._commonErrorHandler = function($dom, data, textStatus, xhr){
    // Server often Responds with Success msg but with Error, Errors, or Redirect to show/do:
    if(typeof data.errors == 'object'){
        var sErr = '';

        // Clear Red UXs (if previously altered)
        $dom.find('.errWrap').removeClass('has-error');
        $dom.find('.errWrap *').removeClass('has-error');

        // Build & gild UXs
        for(k=data.errors.length-1; k >= 0; k--){

            // Build error message
            sErr = data.errors[k].message + '<br/>';

            // Turn UXs red:
            var $errEl = $dom.find('#'+data.errors[k].code);
            if(!$errEl.parent().hasClass('errWrap')){
                $errEl.wrap('<div class="has-error errWrap"></div>');
            }
            else if(!$errEl.parent().hasClass('has-error')){
                $errEl.parent().addClass('has-error');
            }

            var iNit = $dom.scrollTop();
            $errEl.focus();

            cvApp._showPopoverErrorOnElement({
                target: '#'+data.errors[k].code,
                title: '',
                body: data.errors[k].message,
                placement: 'left',
                code: data.errors[k].code
            });

            if(k == 0){
                $errEl = $dom.find('#'+data.errors[k].code);
                window.setTimeout(function(){
                    var iY = $errEl.offset().top;
                    if($dom.scrollTop() >= iNit){
                        $dom.scrollTop($dom.scrollTop() + 30)
                    }
                    else if(iNit > $dom.scrollTop()){
                        $dom.scrollTop($dom.scrollTop() - 50)
                    }
                },100);
            }
        };
    }
    if(typeof data.errors === 'string'){
        cvApp.showHeaderMessage(data.errors, cvApp.ERROR);
    }
    if(typeof data.msgid === 'string'){
        $.cookie('msgid', data.msgid, { path: '/'});
    }
    if(typeof data.redirect === "string"){
        cvApp.postRedirect(data.redirect);
    }
};