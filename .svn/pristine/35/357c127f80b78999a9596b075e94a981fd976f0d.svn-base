// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$(function() {
    $.widget( "wfWidgets.itemWidget", {
        options: {},
        _create: function(){
            var $this = this;
        },

        $wfWidget: false,

        ajaxPostFormForValidation: function(e, $form, cb){
            var $this = this,
                isDraftBtn = $(e.target).text().indexOf('Draft') > -1;

            // Prevent Form Submit to server from submit/click event bubbling:
            e.preventDefault();
            e.stopPropagation();

            // Do not reload to the same item
            window.location.hash = '';

            // New: Generic support for Confirm msgs on any button
            var bConfirm = $(e.target).data('confirm-msg');
            if(bConfirm !== undefined && bConfirm.length > 0){
                var isConfirmed = window.confirm(bConfirm);
                if(!isConfirmed){ return false;}
            }

            // Serialize Form...
            // BUGFIX: Disabled Inputs not read (in FF at least):
            var $dEls = $form.find('input:disabled, select:disabled, textarea:disabled');
            $dEls.prop('disabled', false);
            var $data = JSON.stringify($form.serializeObject()),
                $url = $form.attr('action');
            $dEls.prop('disabled', true);

            // Submit form via AJAX POST...
            $.ajax({
				url: $url,
				type: 'POST',
				data: $data,
				dataType: 'json'
			})
            .done(function(data, textStatus, jqXHR){
                // New: FLRR Candidate View needs to track Submitted rev_reqd items...
                if($form.hasClass('wfHasFLRR') && data.success === true && mpsApp._isCandidateView){
                    var $workflowWidget = $('#workflow-content').data('wfWidgets-workFlowPage');
                    $workflowWidget.completedFLRRs = $workflowWidget.completedFLRRs || [];
                    $workflowWidget.completedFLRRs.push($form.closest('.wf-itemWidgetWrapper').data('code'));
                    if(!isDraftBtn){window.location.hash = '';} // Give the page a chance to select next FLRR or TBD...
                }
                // Also Attest could lead to hidden Thank You - the logic for that exists, but we need to clear the URL hash that perhaps brought the user to Attest:
                if($form.hasClass('wf-clear-hash-on-success')){
                    window.location.hash = '';
                }

                $this._globalResponseHandler(data, textStatus, jqXHR, $url, cb);
                $this._triggerFlrrButtonCheck();
            })
            .fail(function( jqXHR, textStatus, errorThrown ){
                // Errors Exist:
                console.log('AJAX post received error response.', jqXHR);
            });
        },

        _globalResponseHandler: function(data, textStatus, jqXHR, $url, cb){
            var $this = this;

            if(wfApp._sessionExpiryLogoutRequired(data)){return false;} // Just in case we get a Success response...of the Login form

            // callback() is optional param
            if(typeof cb === 'function'){
                cb(data, $this);
            }

            // IF the server side wants to reload current page, we do this instead:
            if($this.$wfWidget === false){$this.$wfWidget = $('#workflow-content').data('wfWidgets-workFlowPage');}
            if(data.reloadForm === true){$this.$wfWidget.uxStates.forceDetailsView = $this.element.data('code');}


            // There are possibly errors in the success response:
            if(typeof data.errors !== 'undefined'){
                $this.renderFormErrors(data.errors);
            }
            // FE should get new Workflow payload (AJAX) and reload
            else if (data.success === true){
                // console.log('Success on Form Post, see console for details');
                var $workflowWidget = $('#workflow-content').data('wfWidgets-workFlowPage');
                $workflowWidget.refreshWorkflowPage(data);
            }
            // LDAP & other future features may wish to 'replace' form values after client<->server chat:
            else if(typeof data.replacements !== 'undefined'){
                $this._fillFormFromServer(data.replacements);
            }
            // There is possibly a redirect in the response data
            else if(typeof data.redirect === 'string'){
                window.location.hash = ''; // Do not reload to the same item (in hash) when server says not to
                window.location = data.redirect;
            }
            else if(typeof data.error === 'string'){
                // This is for Failed Uploads or similar cases where we wish to use the Global Curtain for a server-provided message that is not errors{fields/codes}:
                var $link = $('<div><a href="#" style="float:right;"><span class="glyphicon glyphicon-remove"></span></a><span class="glyphicon glyphicon-warning-sign"></span> '+data.error+'</div>');
                $link.on('click', function(e){
                    cvApp.hideHeaderMessage('', true);
                });
                cvApp.showHeaderMessage($link, 'danger', true);
            }
            else{
                // BUGBUG: should this ever happen?  The HTML LOAD should be below from load() only?
                console.log('Unexpected response: expecting errors, success, or redirect. See console for details\n'+data.exceptionMessage);
                console.log('Unexpected POST response data:', data);
            }
        },

        getAjaxFormData: function(){
            var $this = this,
                item = $this.options.item;

            // Makes sur we don't show a stale form while AJAX gets a new one
            $this.formDestroy();

            // Show Loading... spinner in inner content
            $('#wf-workflow-loading-inner, #wf-workflow-loading-inner *').show();

            // Submit form via AJAX GET...
            $.ajax({
				url: $this.options.item.data.url,
				type: 'GET',
				dataType: 'html'
			})
            .done(function(data, textStatus, jqXHR){
                if(wfApp._sessionExpiryLogoutRequired(data)){return false;} // Just in case we get a Success response...of the Login form

                $('#wf-workflow-loading-inner, #wf-workflow-loading, .wf-workflow-loading').hide();

                // There are possibly errors in the success response:
                if(typeof data.errors !== 'undefined'){
                    //alert('errors!  see console...');
                    console.log('errors!',data);
                }
                // There is possibly a redirect in the response data
                else if(typeof data.redirect === 'string'){
                    window.location.hash = ''; // Do not reload to the same item (in hash) when server says not to
                    window.location = data.redirect;
                }
                else{
                    // Trigger formLoad() on the widget with the response data...expecting a Form of HTML
                    $this.element.trigger('formLoad', data);
                }
                $this._triggerFlrrButtonCheck();

            })
            .fail(function( jqXHR, textStatus, errorThrown ){
                $('#wf-workflow-loading-inner').show();
                // Errors Exist:
                console.log('AJAX post received error response.', jqXHR);
            });
        },

        setWidgetToAjaxFormInterfaces: function(){
            var $this = this;

            // Bind triggered events from Overview UX & super itemWidget:
            $this.element.on('_showItemWidget', function(e, params){
                //console.log('element _showItemWidget triggered');
                $this.element.show().removeClass('starthidden');
                if(mpsApp._isCandidateView){
                    $('#workflow-content').data('wfWidgets-workFlowPage')._highlightCandidateNav($('a[data-section="'+$this.element.attr('id')+'"]'));
                }
                $this.getAjaxFormData();
            });
            $this.element.on('formLoad', function(e, params){
                $this.formLoad(params);
            });
            $this.element.on('click', 'form button[type=submit], .btn-group .dropdown-menu li a, form a.btn', function(e){
                // Some things just don't want to follow patterns...
                if($(e.target).hasClass('wf-irregular-trigger')){
                    return false;
                }

                e.stopPropagation();

                // AJAX POST the form to the server, get [TBD Something?!?] back...
                var $me = $(this),
                    $btn = $me,
                    $form = $btn.closest('form'),
                    sName = $btn.text(),
                    cb = false;

                //
                // New Candidate View Non-FLRR input disabling results in Webkit not sending Disabled Select values...so fix them:
                //

                if(mpsApp._isCandidateView && $form.find('.wf-flrr-note').length > 0){
                    // $form.closest('form').find('input:disabled, select:disabled, textarea:disabled').addClass('wf-post-ajax-disabled').prop('disabled', false);
                }
                //
                // BUGBUG: Maybe instead serialize the form with them enabled then put back BEFORE the POST?
                //

                // NEW: Academic Evals (others?) might want to render an item from JSON instead of from a server side form (see below)
                if(typeof $btn.data('wfSubUploadItem') != 'undefined'){
                    $.ajax({
                        url: $btn.data('wfSubUploadItem'),
                        type: 'GET',
                        dataType: 'json'
                    })
                        .done(function(data, textStatus, jqXHR){
                            // console.log('Acad Eval File Upload item back from server: ', data, textStatus, jqXHR);

                            if(wfApp._sessionExpiryLogoutRequired(data)){return false;} // Just in case we get a Success response...of the Login form

                            var $item = data;
                            $this._renderSoloSubItemFromJSON($item);
                            $this._triggerFlrrButtonCheck();
                        })
                        .fail(function( jqXHR, textStatus, errorThrown ){
                            // Errors Exist:
                            console.log('AJAX post received error response.', jqXHR);
                        });

                    $("html, body").animate({ scrollTop: 0 }, "fast");
                    return true;
                }

                // NEW: Academic Eval et al: sometimes we want to load another form from a button click
                if(typeof $btn.data('wfSubPage') != 'undefined'){
                    // This is 'Load another Form instead of Submitting current Form' scenario:
                    var jItem = {
                        common:{
                            descr: sName,
                            class_name: 'PacketDownload'
                        },
                        data:{
                            url: $btn.data('wfSubPage')
                        },
                        jAuth: {},
                        guid: wfApp._createUniqueID('subPage')
                    };

                    $this._renderSoloSubItemFromJSON(jItem);
                    $("html, body").animate({ scrollTop: 0 }, "fast");
                    return true;
                }

                if($btn.data('wfUrl')){
                    $form.attr('action', $btn.data('wfUrl'));
                }

                // Some UXs have messages to show during AJAX or LDAP or such
                if($btn.hasClass('wf-ldap-btn')){
                    cvApp.showHeaderMessage('Looking up user...', 'info', true);
                    $('#wf-modal-backdrop').show();
                    cb = function(data){
                        var $form = $btn.closest('form'),
                            $submit = $form.find('.wf-details-form-btn-bar button');
                        if(typeof data.errors != 'undefined'){
                            // Errors will appear in UX, get out of the way
                            $('.cv-global-message, #wf-modal-backdrop').hide();
                            $submit.prop('disabled', true);
                        }
                        else{
                            cvApp.hideHeaderMessage('User found');
                            $('#wf-modal-backdrop').hide();
                            $btn.closest('form').find('input, button').prop('disabled', false); // BUGBUG: Why did this change?  Should entire LDAP form enable & submit?
                        }
                    };
                }

                // Generic Support for Buttons causing a RELOAD OF THEIR ITEM instead of Back-to-Overview
                if($btn.hasClass('wf-reload-current-item')){
                    $this.$wfWidget = $('#workflow-content').data('wfWidgets-workFlowPage');
                    cb = function(data, widget){
                        //console.log('cb fired:', data, widget, $this.element.data('code'));
                        widget.$wfWidget.uxStates.forceDetailsView = $this.element.data('code');

                        // If we Enabled some Disabled items for Candidate FLRR mode, put them back...
                        // $('form .wf-post-ajax-disabled').prop('disabled', true).removeClass('wf-post-ajax-disabled');
                    };
                }

                // Generic Support for Buttons causing a RELOAD TO ANOTHER ITEM instead of Back-to-Overview
                if($btn.hasClass('wf-redirect-to-item')){
                    $this.$wfWidget = $('#workflow-content').data('wfWidgets-workFlowPage');
                    cb = function(data, widget){
                        console.log('cb fired:', data, widget, $btn.data('redirectToItem'));
                        widget.$wfWidget.uxStates.forceDetailsView = $btn.data('redirectToItem');
                    };
                }

                // We have View PDF which cannot submit form
                if($btn.prop('tagName') != 'A' || ($btn.prop('tagName') == 'A' && $btn.hasClass('btn'))){
                    $this.ajaxPostFormForValidation(e, $form, cb);
                }

            });

            /*
            $this.element.on('blur', 'form .mps-validate-email', function(e){
                var $mail = $(this),
                    str = $mail.val();
                if(str.length > 0 && !mpsApp._isValidEmailAddy(str.substring(0, str.lastIndexOf('.')).toLowerCase()+str.substring(str.lastIndexOf('.')))){
                    $this.renderFormErrors([{message:'A valid email address is required', code:$mail.attr('name')}], $mail.closest('form'));
                }
            });
            */

        },

        _renderSoloSubItemFromJSON: function(jItem){
            var $this = this,
                $guid = (typeof jItem.guid != 'undefined') ? jItem.guid : wfApp._createUniqueID(jItem.common.code),
                $wrapper = $('<div id="'+$guid+'" class="wf-itemWidgetWrapper clearfix" data-code="'+$guid+'" data-breadcrumbtwo="'+jItem.common.descr+'"></div>');

            $this.$wfWidget = $('#workflow-content').data('wfWidgets-workFlowPage');

            // Append it to item collection already in page...
            $('#wf-details-content-body').append($wrapper);
            $this.$wfWidget._renderItem(jItem, $wrapper, $guid);

            // Tell wfWidget to go back to Academic Evals on submit/reload rather than Overview:
            $this.$wfWidget.uxStates.forceDetailsView = $this.element.data('code');

            // Trigger showing our new subPage:
            $this.$wfWidget._showSectionById($guid);

            // TBD: Cancel Links back to this form
            // TBD: Item Title?  Maybe just add to form?
        },

        formLoad: function(form){
            var $this = this;
            $this.$form = $(form);
            $this.formDestroy();
            $this.element.find('.wf-widget-serverside-form').append($this.$form);

            // Handles Repeaters etc
            $this.$form.trigger('safeInitFormWidgets');

            // Global Disable safety.  BUGBUG: server side forms should also either not render things or add disabled to tags?
            if($this.options.item.data.disabled === true){
                $this.$form.addClass('wf-item-is-disabled');
                $this.$form.find('input, textarea, button, select').not('#saved_set_name, .wf-validate-non-empty-button, .wf-save-template, .wf-print-item').attr('disabled', 'disabled');
                $this.$form.find('.btn-primary').not('#saved_set_name, .wf-validate-non-empty-button, .wf-save-template, .wf-print-item').addClass('btn-default').removeClass('btn-primary');
                $this.$form.find('.wf-details-footer-cancel span').not('.glyphicon').text('Overview');
            }
            else{
                $this.$form.find('.wf-details-footer-cancel span').not('.glyphicon').text('Cancel');
                $this.$form.find('select, input, textarea').eq(0).focus();
            }

            // Special wf-item-magic-list-item support
            $this.$form.find('.wf-item-magic-list-item').each(function(iI, tagInput){
                var $widget = $(tagInput),
                    $btn = $(tagInput).find('button'),
                    $new = $('<span class="wf-tag-wrapper"><input class="tag_input" type="text" value="" name="'+$(this).data('fieldname')+'"/><span class="glyphicon glyphicon-remove-circle"></span></span>    ');

                    // Button needs to be first el in parent for this UX approach...
                    $(tagInput).prepend($btn);

                    if($widget.hasClass('wf-item-magic-list-item-select')){
                        var $select = $widget.find('select')
                        sNoun = $btn.text().substr(4);

                        // Add Select a [noun]:
                        var $opt = $('<option class="DNC" value="-1">Select a '+sNoun+'...</option>');
                        $select.prepend($opt);
                        $opt.prop('selected', true);

                        // Reveal a select on button click...
                        $btn.on('click', function(e){
                            $select = $(e.target).closest('.wf-item-magic-list-item-select').find('select');
                            $select.prop('disabled', false).show().toggleClass('starthidden');
                        });

                        $widget.on('change', function(e){
                            var $select = $(e.target);
                            if ($select.find('option:selected').hasClass('DNC')){
                                return false;
                            }
                            var $wrap = $new.clone();
                            $wrap.insertAfter($select);
                            var sVal = $select.val();
                            $wrap.find('input').val(sVal).prop('disabled', true);
                            $select.hide().toggleClass('starthidden').insertAfter($wrap);
                            $select.find('option:first').prop('selected', true);
                        });
                    }
                    else{
                        // Reveal a new input on button click
                        $btn.on('click', function(e){
                            var $temp = $new.clone();
                            $temp.insertAfter($btn);
                            $temp.delay(250).focus();
                        });
                    }

                    // REMOVE blah on (x) clicks:
                    if($this.options.item.data.disabled !== true){
                        $(tagInput).on('click', '.glyphicon', function(e){
                            $(e.target).closest('.wf-tag-wrapper').remove();
                        });
                    }
                    else{
                        $(tagInput).find('.glyphicon').hide();
                    }
            });

            //
            // NEW: Forms can have associated JSON data
            // BUGBUG: Are there any needs for MULTIPLE forms/items to exist?  Maybe Acad Eval type items?  Multiple Uploads?
            //
            $this._processFormForFieldLevelRevisionsRequired();

            // Newer Print button in header:
            mpsApp._copyPrintBtnToHeader($this.$form);

            $this.element.trigger('fixPaneHeights');

        },

        _processFormForFieldLevelRevisionsRequired: function(){
            var $this = this;

            //console.log('_processFormForFieldLevelRevisionsRequired...')

            // If there is JSON data for the form it will be currentItem with taskCode = value of the data-json-load attr:
            var sTK = (typeof itemJSON != 'undefined' && itemJSON .currentItem.taskCode) ? itemJSON.currentItem.taskCode : false,
                $jForm = (sTK !== false) ? $this.element.find('form[data-json-load="'+sTK+'"]') : false,
                jData = (sTK !== false && $jForm !== false) ? itemJSON.currentItem : false;

            if(jData !== false){
                //console.log('Item/Form loaded has associated json data: ', $jForm, jData);

                //
                // There are TWO modes possible for FLRR:
                //      1) OFA type user Marking Entire Items/Pages FLRR
                //      2) Candidate/Consumer Editing things marked FLRR
                //

                // BOTH Modes Display FLRR on items that have them...
                if(jData.canSeeFieldLevelRevisions){
                    var isCandidateFLRRAddRemoveAllowed = false;

                    //
                    // New: Candidate View DISABLES all but FLRR inputs...
                    //
                    if(mpsApp._isCandidateView && jData.RevisionsRequiredFieldNames.length > 0){
                        $jForm.find('input, select, textarea, .cv-add-group-btn, .cv-remove-group-btn').prop('disabled', true);
                    }

                    $.each(jData.RevisionsRequiredFieldNames, function(i, jRRFN){
                        //console.log('Existing Note flrr:', jRRFN);
                        $this._displayFLRevReqdData(jRRFN, $jForm);
                        if(i==0){
                            $jForm.addClass('wfHasFLRR');
                        }

                        //
                        // New: FLRR can either turn Repeating Group editing by Candidate on or off, so we have to set that up too
                        //
                        if(jRRFN.name == 'repeater_addremove'){
                            // console.log('Trapped?', jRRFN);
                            isCandidateFLRRAddRemoveAllowed = true;
                            $jForm.attr('data-flrr-groupactionsdenied', ((jRRFN.comment == 'false') ? 'true' : 'false') );
                        }

                    });

                    //
                    // New: Candidate View DISABLES all but FLRR inputs...
                    //
                    if(mpsApp._isCandidateView && jData.RevisionsRequiredFieldNames.length > 0){
                        // UNLESS Field Level Revisions Required allow the user to add/remove items...
                        // console.log('isCandidateFLRRAddRemoveAllowed here is:', isCandidateFLRRAddRemoveAllowed)
                        if(isCandidateFLRRAddRemoveAllowed){
                            // Enable it for user...
                            $jForm.find('.cv-add-group-btn, .cv-remove-group-btn').prop('disabled', false);
                        }
                        else{
                            $jForm.find('.cv-add-group-btn, .cv-remove-group-btn').prop('disabled', true);
                        }
                    }


                    // Put Global Comment at top of Item in Non-Editor View modes:
                    if(jData.isFieldLevelRevisable !== true && jData.RevisionsRequiredFieldNames.length > 0){
                        var isGlobalComment = false;
                        $.each(jData.RevisionsRequiredFieldNames, function(i,o){
                            if(o.name == 'global_comment'){
                                isGlobalComment = o.comment;
                            }
                        });
                        var $note = $('<div role="alert" class="alert alert-warning wf-flrr-global-header" id="wf-revisions-required-note"></div>'),
                            $content = $('<span class="glyphicon glyphicon-warning-sign wf-item-before"></span><span class="wf-flrr-global-note">&nbsp; Specific Revisions are Required - please review the highlighted notes in the form below.</span>'),
                            $link = $('<a data-toggle-text="Show Notes" class="wf-rr-toggle" href="#"><span class="wf-rr-text">Hide Notes</span><span data-toggle-classes="glyphicon-chevron-up glyphicon-chevron-down" class="glyphicon glyphicon-chevron-up"></span></a>'),
                            $pre = $('<pre class="wf-rr-target" style="display: block;">'+((isGlobalComment !== false) ? isGlobalComment : '')+'</pre>');
                        $note.append($content);
                        if(isGlobalComment != false){
                            $note.append($link).append($pre);
                        }
                        $jForm.find('.wf-flrr-global-header').remove();
                        $jForm.prepend($note);
                    }
                }

                if(jData.isFieldLevelRevisable){
                    // Credentialing Dept Type User, allowed to Toggle FLRR Mode & Mark things FLRR and provide FLRR Notes
                    // Put Giant Button on Item:
                    $this.element.find('.wf-flrr-super-button').remove();
                    $this._addFLRevReqdItemSuperButton($jForm, jData);

                    // Put Enter Require Revisions buttons on each row in the FLRR list:
                    var zFields = $jForm.find('input, textarea, select').not('.wf-flrr-enabled, input[type="hidden"]');
                    $.each(zFields, function(i, oIn){
                        //console.log('Entry Button flrr:', oIn);
                        $this._addFLRevReqdItemEntryButton(oIn, jData);
                    });
                }
                else{
                    // Candidate/Consumer Type User?
                    // BUGBUG: May Edit things marked FLRR (nothing else) and Sees the FLRR Notes - need to do anytyhing?

                    // Put FLRR Notes on each item in the FLRR list:
                }

                // We made changes, must give the Repeaters a chance to respect them...
                $this.$form.trigger('safeInitFormWidgets');

            }
        },

        _addFLRevReqdItemSuperButton: function($jForm, jData){
            var $this = this,
                $btn = $('<button class="btn btn-warning wf-flrr-super-button" data-flrr-mode="read">Enter Revisions Required...</button>'),
                $globalComment = $('<div class="wf-flrr-global-comment wf-flrr-edit-form wf-form-right"><textarea class="global_comment" style="display:none !important;" data-code="global_comment" name="global_comment" placeholder="Optional general notes that will appear to users - also see below for Revisions Required buttons on specific fields in this form."></textarea></div>'),
                $form = $jForm;

            $btn.on('click', function(e){
                // Toggle Button Text & form's FLRR buttons
                var $row = $btn.closest('.wf-form-right'),
                    gcHide = {};
                $btn.data('flrrMode', (($btn.data('flrrMode') == 'read') ? 'edit' : 'read'));
                $btn.text((($btn.data('flrrMode') == 'edit') ? 'Done Entering Revisions Required' : 'Enter Revisions Required...'));

                // Global Comment is Special
                var $gMsg = $jForm.find('.wf-flrr-global-comment');
                if($btn.data('flrrMode') == 'edit'){
                    $gMsg.show().removeClass('starthidden');
                    $gMsg.find('.wf-flrr-item-button').click().hide();
                }
                else{
                    $gMsg.addClass('starthidden').hide();
                }

                $jForm.find('.wf-flrr-item-button, .wf-flrr-repeater-checkbox').toggleClass('starthidden');
                $jForm.find('.wf-flrr-btn-border-needed').toggleClass('wf-flrr-border-on').css('padding-left', '5px !important');
            });
            $jForm.prepend($globalComment);
            $jForm.prepend($btn);

            // Form Repeating Forms, we have to insert a Add/Remove vs. Fields Only box
            var zRepeats = $jForm.find('.Repeating-Form-Wrapper'); // NOTE: .Repeating-Form-Wrapper.data('form') == credWorkExpGroup GUID
            if(zRepeats.length > 0){
                $.each(zRepeats, function(i,r){
                    // console.log('zRepeats i:', r);
                    var $wrap = $('<div class="wf-flrr-repeater-checkbox starthidden"></div>'),
                        $repeater = $(r),
                        $label = $('<label> Candidate may Add/Remove Groups in addition to individual fields marked by you below.</label>'),
                        $input = $('<input type="checkbox" name="repeater_addremove" />'),
                        bAddRemove = false;

                    // Set persisted checkbox stqate if there is one:
                    $.each(jData.RevisionsRequiredFieldNames, function(i,o){
                        if(o.name == 'repeater_addremove'){
                            bAddRemove = o.comment === 'true' ? true : false;
                            return false;
                        }
                    });
                    $input.prop('checked', bAddRemove );

                    $label.prepend($input);
                    $wrap.append($label);
                    $wrap.insertBefore($repeater);
                    $input.on('change', function(){
                        var $in = $(this);

                        $.ajax({
                            url: jData.field_level_revisions_url,
                            type: 'POST',
                            data: JSON.stringify({ name: $in.attr('name'), comment: $in.prop('checked') ? 'true':'false', enabled: true }),
                            headers: { 'Content-Type': 'application/json' },
                            success: function(data, textStatus, xhr) {
                                cvApp.showHeaderMessage('Revision Permission was saved.', cvApp.INFO, false);
                            },
                            error: function(jqXHR, textStatus, errorThrown) {
                                alert('AJAX Error, apologies!');
                                //$('#adminerrormessage').html(textStatus);
                            }
                        });

                    });
                });

            }

        },

        _addFLRevReqdItemEntryButton: function(oIn, jData){
            // console.log('Call to _addFLRevReqdItemEntryButton:', oIn, jData);
            var $that = this,
                $input = $(oIn),
                $jForm = $input.closest('form'),
                $row = $input.closest('.wf-form-right'),
                $button = $('<a href="#" class="btn btn-warning wf-flrr-item-button starthidden"><span class="glyphicon glyphicon-warning-sign"></span></a>'),
                isRowGlobalComment = ($row.hasClass('wf-flrr-global-comment')) ? true : false;

                $button.on('click', function(e){
                    e.preventDefault();
                    e.stopPropagation();

                    // It could be the user is adding a New FLRR on a row without one...if so, we must build some data for the row/control & init it
                    if(typeof $row.data('flrrItem') == 'undefined'){
                        var itemJson = {
                            name: $input.attr('name'),
                            comment: ''
                        }
                        $that._displayFLRevReqdData(itemJson, $jForm);
                    }

                    // Hide any existing Read Mode Note, delete any previous version of this UX:
                    $row.find('.wf-flrr-note').addClass('starthidden');
                    $row.find('.wf-flrr-edit-form, .wf-flrr-saving-msg').remove();

                    // Insert an Edit Mode FLRR UX
                    var $wrap = $('<div class="wf-flrr-edit-form clearfix"></div>'),
                        $chk = $('<input type="checkbox" checked="checked" name="wf-flrr-enabled" class="wf-flrr-enabled"/>'),
                        $lead = $('<span class="wf-flrr-title"><span class="glyphicon glyphicon-warning-sign starthidden"></span> <span class="wf-flrr-label">'+((isRowGlobalComment) ? 'Include General Revisions Notes:': 'Revisions are Required:')+'</span></span>'),
                        $txtArea = $('<textarea placeholder="Optional">' + ((typeof $row.data('flrrComment') != 'undefined') ? $row.data('flrrComment') : '') +'</textarea>'),
                        $save = $('<a href="#" class="btn btn-warning wf-flrr-save-button"><span class="glyphicon glyphicon-floppy-disk"></span></a>'),
                        $cancel = $('<a href="#" class="btn btn-default wf-flrr-cancel-button'+((isRowGlobalComment) ? ' starthidden':'') +'"><span class="glyphicon glyphicon-remove"></span></a>'),
                        $savingMsg = $('<div class="wf-flrr-saving-msg starthidden"><img src="/'+cvApp.skin+'/images/ajax-loader.gif"/> Saving your Revision Required Comment...</div>');

                    $chk.change(function(e){
                        var $box = $(this);
                        if($box.is(':checked')){
                            $txtArea.prop('disabled', false);
                        }
                        else{
                            if(isRowGlobalComment){$txtArea.text('');}
                            $txtArea.prop('disabled', true);
                        }
                    });

                    $save.click(function(e){
                        e.preventDefault();
                        e.stopPropagation();
                        $row.find('.wf-flrr-edit-form, .wf-flrr-saving-msg').toggleClass('starthidden');
                        // BUGBUG: Do AJAX call & then munge results & DOM here...
                        var isEnabled = ($row.find('.wf-flrr-edit-form .wf-flrr-enabled').is(':checked'));
                        rrData = {
                            name: $row.data('flrrName'),
                            comment: isEnabled ? $row.find('.wf-flrr-edit-form textarea').val() : '',
                            enabled: isEnabled ? true : false
                        };
                        cvApp.hideHeaderMessage();
                        $.ajax({
                            url: jData.field_level_revisions_url,
                            type: 'POST',
                            data: JSON.stringify(rrData),
                            headers: { 'Content-Type': 'application/json' },
                            success: function(data, textStatus, xhr) {
                                // Response type 200 is Error if response { errors:[] }...
                                if (typeof data.errors != 'undefined') {
                                    var msg = (typeof data.errors.message != 'undefined') ? data.errors.message : data.errors;
                                    msg = 'Apologies, but something has gone wrong while saving your Revisions Required.  Please Refresh the page, and if the issue persists, contact your site administrator. Error details:<br/><br/>' + msg;
                                    msg = msg + '<br/><br/><a href="#'+window.location.hash+'" onclick="window.location.reload(); return false;">Click here to refresh this page...</a>';
                                    cvApp.showHeaderMessage(msg, cvApp.ERROR);
                                    //$errorEl.text(data.errors.message);
                                    return false;
                                }

                                // Update this row's Data now that server has done so succesfully...
                                //console.log('item data now:', rrData);
                                $row.data('flrrName', rrData.name);
                                $row.data('flrrComment', rrData.comment);
                                $row.data('flrrEnabled', rrData.enabled);
                                $row.data('flrrItem', rrData);

                                cvApp.showHeaderMessage('Revision Requirement was saved.', cvApp.INFO, false);
                                setTimeout(cvApp.hideHeaderMessage, 5000);

                                if(isRowGlobalComment){
                                    $row.find('.wf-flrr-edit-form, .wf-flrr-saving-msg').toggleClass('starthidden');
                                }
                                else{
                                    $row.find('.wf-flrr-saving-msg').remove();
                                    $that._displayFLRevReqdData($row.data('flrrItem'), $jForm);
                                    $row.find('.wf-flrr-item-button').toggleClass('starthidden');
                                }

                                $that._triggerFlrrButtonCheck();

                            },
                            error: function(jqXHR, textStatus, errorThrown) {
                                alert('AJAX Error, apologies!');
                                //$('#adminerrormessage').html(textStatus);
                            }
                        });
                    });
                    $cancel.click(function(e){
                        e.preventDefault();
                        e.stopPropagation();
                        $row.find('.wf-flrr-edit-form').remove();
                        $row.find('.wf-flrr-item-button').toggleClass('starthidden');
                        $row.find('.wf-flrr-note').toggleClass('starthidden');
                        if($row.data('flrrComment') == ''){
                            // $row.find('.wf-flrr-note').addClass('starthidden')
                        }

                    });

                    $lead.prepend($chk);
                    $wrap.append($lead);
                    $wrap.append($cancel);
                    $wrap.append($save);
                    $wrap.append($txtArea);
                    $row.append($wrap);
                    $row.append($savingMsg);
                    $row.css({height: 'auto', 'overflow':'none', 'margin-bottom': '5px'});
                    $row.find('.wf-flrr-item-button').toggleClass('starthidden');
                    $txtArea.focus();

                });

                // The Layout of the Button needs to differ by Control Type, Repeating Controls, etc - so we figure that out & insert some classNames:
                if($input.is('input') && $input.attr('type') == 'text'){
                    if($row.find('.cv-add-field').length > 0){
                        // We have Repeating Text Controls, so indent left?
                        $row.addClass('wf-flrr-repeating-text');
                    }
                }
                else if($input.is('input') && $input.attr('type') == 'radio'){
                    $row.addClass('wf-flrr-btn-border-needed');
                }

                // Remove Previous buttons (Repeating controls)
                $row.find('.wf-flrr-item-button').remove();

                $row.append($button);

        },

        _addSaveCancelFlrrBtnsToRow: function(){

        },

        _displayFLRevReqdData: function(itemJson, $jForm){
            var $this = this,
                $row = $jForm.find('[name="'+itemJson.name+'"]:first').closest('.wf-form-right'),
                $note = $('<div class="wf-flrr-note"><span class="glyphicon glyphicon-warning-sign"></span> <span class="wf-flrr-label">Revision Required'+((itemJson.comment !== '')?':':'')+'</span> '+itemJson.comment+'</div>');


            // console.log('Call to _displayFLRevReqdData: ', itemJson, $jForm, $row);

            // Candidate View has newly disabled inputs, enable the ones with FLRR:
            if(mpsApp._isCandidateView){
                $row.find('input, select, textarea').prop('disabled', false);
            }

            // Remove any existing Note
            $row.find('.wf-flrr-note').remove();

            // Put flrr .name and .note on $row for later Editing...
            $row.data('flrrName', itemJson.name);
            $row.data('flrrComment', itemJson.comment);
            $row.data('flrrEnabled', itemJson.enabled);
            $row.data('flrrItem', itemJson);
            // Insert the UX:
            //console.log('_displayFLRevReqdData pre-insert: ', $note, $row);
            $row.append($note);
            if(typeof itemJson.enabled != 'undefined' && itemJson.enabled == false){
                $note.addClass('starthidden');
            }else{
                $row.css({height: 'auto', 'overflow':'none', 'margin-bottom': '5px'});
            }
        },

        formDestroy: function(){
            var $this = this;
            $this.element.find('.wf-widget-serverside-form').empty();
        },

        renderFormErrors: function(errors){
            var $this = this,
                $form = $this.$form,
                isLDAP = $this.$form.find('.wf-ldap-btn').length > 0;

            // New: sometimes the error object could be a string instead of Array...Just In Case:
            if(!$.isArray(errors)){
                if(isLDAP){
                    var $user = $form.find('input[name=username]'),
                        sUser = $user.val();
                    $form.find('.wf-errors-string-ux').remove();

                    //var $err = $('<div class="form-row wf-errors-string-ux"><div class="col-md-7 col-md-offset-2 alert alert-danger">User '+sUser + ' ' +errors.toLowerCase() +', please try again.</div></div>');
                    //$err.insertAfter($('input[name=username]').parent().parent());

                    $form.find('input').not('[name=username]').not('[name=community]').prop('disabled', true);

                    cvApp._showPopoverErrorOnElement({
                        target: $user,
                        title: '',
                        body: sUser + ' ' +errors.toLowerCase() +'',
                        code: 'has-error',
                        placement: 'right'
                    });
                    $user.on('click change keydown', function(){
                        $user.popover('destroy');
                    });

                    return true;
                }
                else{
                    $form.find('.wf-errors-string-ux').remove();
                    var $err = $('<div class="wf-errors-string-ux alert alert-danger">'+errors+'</div>');
                    $form.prepend($err);
                    $('html,body').scrollTop(95);
                    return true;
                }
            }

            return wfApp._renderFormErrors(errors, $form);
        },

        _fillFormFromServer: function(replacements){
            var $this = this,
                $form = $this.$form,
                $username = $form.find('input[name=username]'),
                $msg = $('<div class="starthidden form-row wf-errors-string-ux"><div class="col-md-7 col-md-offset-2 alert alert-info">A matching username has been found, please review and Submit:</div></div>');

            $('.wf-errors-string-ux').remove();
            $msg.insertAfter($username.closest('.form-row'));

            // Enable the other fields if we have a response to:
            if($form.data('notdisabled') == 'not'){
                $form.find('input, button').prop('disabled', false);
            }

            // BUGBUG: ??? Blank the form except for username field ???
            $form.find('input').not('[name=username]').not('[type=checkbox]').val('');

            // Fill form with server side responses vals
            $.each(replacements, function(iR, replacement){
                $form.find('[name='+replacement.code+']').val(replacement.value);
            });
        },

        // ONLY used by FileUpload at the moment...
        getCommonHeader: function(childStates, sInsert){
            uxDebug('Parent Item Widget trying to render common header back to child...', childStates, sInsert);
            var complete = '<span class="glyphicon glyphicon-ok" title="Complete!"></span>',
                blocked = '<span class="glyphicon glyphicon-ban-circle" title="Blocked!"></span>',
                tbd = '<span class="glyphicon glyphicon-cog" title="TBD"></span>',
                disabled = '(disabled)',
                sTatus = 'status_',
                smartImg = function(){
                    if(childStates.is_blocked){
                        sTatus += 'blocked';
                        return blocked;
                    }
                    else if(childStates.is_complete){
                        sTatus += 'complete';
                        return complete;
                    }
                    else{
                        sTatus += 'tbd';
                        return tbd;
                    }
                },
                sImg = smartImg();

            if(childStates.isFirstActionableItem){
                sImg = '<span class="wf-item-status wf-next-item '+sTatus+'">'+sImg+'<span class="wf-first-actionable-widget glyphicon glyphicon-arrow-left"></span></span>';
            }
            else{
                sImg = '<span class="wf-item-status '+sTatus+'">'+sImg+'</span>';
            }

            var $this = this,
                tplHd = (childStates.isCompleteSingleUpload === true) ? $('#wf-workflow-common-header').html() : $('#wf-workflow-common-header').html(),
                data = {
                    bookmark: wfApp._safeDomGuid(childStates.descr),
                    glyphIcon: '',
                    linkTitle: '',
                    statusImg: sImg,
                    taskTitle: childStates.descr+':',
                    extraTitle: sInsert
                };

            // Logic on States?
            uxDebug('super getCommonHeader', childStates);

            return wfApp.wfTemplate(tplHd, data);
        },

        _triggerFlrrButtonCheck: function(){
            var $this = this;
            if(!mpsApp._isCandidateView){
                if($this.$wfWidget === false){$this.$wfWidget = $('#workflow-content').data('wfWidgets-workFlowPage');}
                $this.$wfWidget._maybeInsertFlrrButton();
            }
        }
    });

});