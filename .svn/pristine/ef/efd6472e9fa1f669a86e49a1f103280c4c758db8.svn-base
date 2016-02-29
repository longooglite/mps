// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

// BUGBUG: Add Comments...

// BUGBUG: Invisible Repeating Forms are NOT working.  Deal with Tabled ones hiding all but 1, and with Disclosures item in Candidate View (which starts hidden by default).

$.widget( "wfWidgets.mpsRepeatingForm", {
    options: {},
    _create: function(){
        return true;
    }
});

//
// BUGBUG: In order to use a jQ UI Widget, CV may have to change as well?
//

var mpsApp = mpsApp || {};
mpsApp._initRepeatingForms = function(jOpts, dom){
    var zForms = (typeof dom !== 'undefined') ? dom.find('.Repeating-Form-Wrapper') : $('.Repeating-Form-Wrapper');

    var sOpen = 'Show',
        sClose = 'Hide';

    zForms.each(function(i,v){
        var $wrap = $(v),
            zChunks = $wrap.find('.Repeating-Form'),
            resetNumbers = function(form, iReplace, bClearVals){
                var zControls = form.find('label, input, select, textarea, button'),
                    iOld = Number(form.find('.Repeating-Form-Number').text()),
                    iNew = iReplace,
                    sStrip = form.data('separator') + iOld.toString(),
                    sNew = form.data('separator') + iNew.toString();

                form.find('.Repeating-Form-Number').text(iNew);
                if(bClearVals === true){
                    form.find('input, textarea, select').not('[type="radio"]').not('[type="checkbox"]').val('');
                    form.find('input[type="radio"]').prop('checked', false);
                }

                zControls.each(function(i, el){
                    var $el = $(el), sFor = $el.attr('for') || '', sName = $el.attr('name') || '', sID = $el.attr('id') || '';
                    // label.for, *.name, *.id
                    if(sFor.length > 0){$el.attr('for', sFor.substring(0, sFor.indexOf(sStrip))+sNew );}
                    if(sName.length > 0){$el.attr('name', sName.substring(0, sName.indexOf(sStrip))+sNew );}
                    if(sID.length > 0){$el.attr('id', sName.substring(0, sID.indexOf(sStrip))+sNew );}
                });
                return form;
            },
            // TABLE'd:
            isTabled = ($wrap.hasClass('Tabled-Form-Wrapper') && $('table.Repeating-Form-Table:visible').filter(function(iT, oT){return $($(oT).data('table') == $wrap.data('table'))}).length > 0),
            $table = ($wrap.hasClass('Tabled-Form-Wrapper')) ? $('table.Repeating-Form-Table:visible').filter(function(iT, oT){return $($(oT).data('table') == $wrap.data('table'))}) : false,
            _summarizeFormToTable = (!isTabled) ? function(){return false;} : function($form, $table, j){
                var sHTML = '<tr>',
                    isNotEmpty = false,
                    isFLRR = ($form.find('.wf-flrr-note').length > 0) ? true : false;

                //console.log('isFLRR is:', isFLRR);

                $.each($table.find('tr th').not('.ignore-me'), function(iC, oC){
                    if(typeof $(oC).data('code') == 'undefined'){return false;}
                    var oIn = $form.find('input, select, textarea').filter(function(iT, oT){
                        return $(oT).data('code') == $(oC).data('code');
                    });
                    var sTxt = '';
                    switch(oIn.prop('tagName')){
                        case 'TEXTAREA':
                            sTxt = oIn.val();
                            break;
                        case 'INPUT':
                            switch(oIn.attr('type').toLowerCase()){
                                case 'text':
                                    sTxt = oIn.val();
                                    break;
                                case 'radio':
                                    sTxt = oIn.closest('.wf-form-right').find(':checked').parent().text();
                                    break;
                                case 'checkbox':
                                    sTxt = (oIn.is(':checked')) ? 'checked' : 'Unchecked';
                                    break;
                            }
                            break;
                        case 'SELECT':
                            var zSelds = oIn.find(':selected');
                            zSelds.each(function(iOpt, oOpt){
                                sTxt += $(oOpt).text() + ((iOpt < zSelds.length - 1) ? ', ': '');
                            });
                            if(sTxt == 'Select'){sTxt = '';} // Do not show Default Select value
                            break;
                        default:
                            sTxt = oIn.val();
                            break;
                    }
                    if(sTxt != ''){isNotEmpty = true;}
                    sHTML += '<td class="'+((isFLRR)?'tbl-sum-flrr':'')+'">' + sTxt +'</td>';
                });
                sHTML += '</tr>';
                var $row = $(sHTML),
                    sEd = (($form.data('nth')*1 == zChunks.length-1 && $wrap.find('.Repeating-Form').length < 2) || $form.is(':visible') ) ? sClose : sOpen,
                    $edit = $('<a href="#" style="white-space:nowrap" class="wf-tabled-form-edit" data-form='+$form.data('nth')*1+'>'+sEd+'</a>');

                $edit.on('click', function(e){
                    var $link = $(this);
                    if($link.text() != sClose){
                        $link.addClass('close-me').html(sClose);
                        $link.closest('.Repeating-Form-Table').find('.wf-tabled-form-edit').not('.close-me').html(sOpen);
                        $wrap.find('.Repeating-Form').slideUp();
                        $wrap.find('.Repeating-Form').filter(function(iL, oL){return $(oL).data('nth') == $(e.target).data('form');}).slideDown();
                        $link.closest('.Repeating-Form-Table').find('.wf-tabled-form-edit').removeClass('close-me');
                    }
                    else{
                        $link.html(sOpen);
                        $wrap.find('.Repeating-Form').filter(function(iL, oL){return $(oL).data('nth') == $(e.target).data('form');}).hide();
                    }
                });

                var $cell = $('<td width="1" style="position:relative;">'+(isFLRR ? '<span class="tbl-sum-flrr tbl-row-flrr glyphicon glyphicon-warning-sign" title="Specific revisions are required."></span>' : '')+'</td>');
                $row.prepend($cell.append($edit));
                var $rows = $table.find('tbody tr');
                // console.log($rows.length - 1 , $form.data('nth')*1)
                if($rows.length - 1 < $form.data('nth')*1){
                    // Startup - need NEW row
                    $table.find('tbody').append($row);
                }
                else{
                    // EDIT EXISTING
                    $rows.eq($form.data('nth')*1).replaceWith($row.prepend($cell.append($edit)));
                }
                //console.log('Summarize this:', $form, $table, zCodes, sHTML);
            };

        // Clear out all old buttons...
        $wrap.find('.cv-add-field, .cv-remove-field').remove();

        if(isTabled){
            $wrap.find('.Repeating-Form').hide();
            if($wrap.find('.Repeating-Form').length < 2){$wrap.find('.Repeating-Form:last').show();}
            $table.find('tbody').empty();
        }

        // create Delete Form buttons '-' on all rows but first...
        var iChunks = zChunks.length;
        // console.log('Processing Repeating chunks now...');
        var areGroupActionsDenied = ($('body').hasClass('wf-candidate-view') === false) ? false : ($wrap.closest('form').attr('data-flrr-groupactionsdenied') == 'true') ? true : false;

        $.each(zChunks, function(j,form){
            var $form = $(form),
                sPref = $form.data('prefix'),
                sSep = $form.data('separator'),
                iNum = Number($form.find('.Repeating-Form-Number').text()),
                $plusBtn = areGroupActionsDenied ? false : $('<button title="Add another '+sPref+'" class="btn btn-sm btn-primary cv-add-field cv-add-group-btn"><span class="glyphicon glyphicon-sm glyphicon-plus"></span> Add '+sPref+'...</button>'),
                $minusBtn = areGroupActionsDenied ? false : $('<button title="Delete this '+sPref+'" class="btn btn-sm btn-primary cv-remove-field cv-remove-group-btn"><span class="glyphicon glyphicon-sm glyphicon-minus"></span>'+((isTabled) ? ' Delete' :'')+'</button>');

            if(isTabled){
                $form.attr('data-nth', j);
                // Custom onError callback work...
                $form.on('wfValidateError', function(){
                    // For each NOW VISIBLE form, correct the Table row state...
                    var $form = $(this),
                        $table = $('table.Repeating-Form-Table[data-table="'+$form.closest('.Tabled-Form-Wrapper').data('table')+'"]'),
                        zForms = $form.closest('.Tabled-Form-Wrapper').find('.Repeating-Form:visible');
                    $.each(zForms, function(kF, oF){
                        var $oF = $(oF);
                        if($oF.find('.has-error').length == 0){
                            $oF.hide();
                            $table.find('a[data-form="'+$(oF).data('nth')+'"]').text(sOpen);
                        }
                        else{
                            $table.find('a[data-form="'+$(oF).data('nth')+'"]').text(sClose);
                        }
                    });
                });
            }

            if(iNum > j+1){
                // Reset Number to appropriate next value
                $form = resetNumbers($form, j+1, false);
            }
            if(iChunks > 1 && !areGroupActionsDenied){  // All but First get - button
                // Bind Button...
                var $button = $minusBtn.clone().bind('click', function(e){
                    var $btn = $(this);
                    $btn.closest('.Repeating-Form').remove();
                    cvApp._handleRepeatingFields(jOpts, dom);
                    return false;
                });
                if(isTabled){
                    var $h4 = $form.find('h4:first'),
                        sText = $h4.text(),
                        btnText = $button.text();
                    $button.text(btnText + ' ' + sText).appendTo($form.find('h4'));
                }
                else{$button.prependTo($form.find('h4'));}
            }
            if(j == iChunks-1 && !areGroupActionsDenied){ // Last gets + button after it...
                // Bind Button...
                var $button = $plusBtn.clone().bind('click', function(e){
                    var $btn = $(this),
                        $sec = (isTabled) ? $btn.closest('.Repeating-Form-Wrapper').find('.Repeating-Form:last') : $btn.closest('.Repeating-Form'),
                        iInc = Number($sec.find('.Repeating-Form-Number').text())+1;
                        $clone = $sec.clone();

                    $clone.find('.has-error').removeClass('has-error'); // Remove Error states...
                    $clone.find('.wf-flrr-edit-form, .wf-flrr-note, .wf-flrr-item-button').remove(); // Remove all Field Level Revisions Required DOM (it will get re-created)

                    var $new = resetNumbers($clone, iInc, true);
                    $new.insertAfter($form);

                    // We have to reset the Field Level Revisions Required now...
                    var $widget = $form.closest('.wf-itemWidgetWrapper').data('wfWidgets-serverSideAjaxForm');
                    $widget._processFormForFieldLevelRevisionsRequired();

                    // Newer Candidate FLRR may allow Add/Remove sections, we need to un-disable new sections if so...
                    var isGroupActionsSet = typeof $form.closest('form').attr('data-flrr-groupactionsdenied') == 'string' && $form.closest('form').attr('data-flrr-groupactionsdenied').length > 0;
                    if(isGroupActionsSet && $form.closest('form').attr('data-flrr-groupactionsdenied') === 'false'){
                        $new.find('input, select, textarea').prop('disabled', false);
                    }

                    if(isTabled){
                        $form.hide();
                        setTimeout(function(){
                            $wrap.find('.Repeating-Form .cv-add-group-btn').remove();
                            $new.slideDown();
                            $table.find('tbody tr:last .wf-tabled-form-edit').text('Close');
                        },500);
                    }
                    cvApp._handleRepeatingFields(jOpts, dom);
                    return false;
                });
                $form.append($button);
            }

            // DatePickerize the new DOM in case there are datepickers in it
            mpsApp.mpsDatePickerizeDom($form);

            // Handle nested repeating inputs/selects:
            jOpts.removeEmptyNs = true;

            cvApp._handleRepeatingFields(jOpts, $form);

            var isTableInitd = false;
            if(isTabled){
                _summarizeFormToTable($form, $table, j);
                $form.on('blur change', 'input, select, textarea', function(e){
                    _summarizeFormToTable($form, $table, $(this).closest('.Repeating-Form').data('nth'));
                });

                // Move Add button out of last form as it will not always be visible?
                var $addBtn = $wrap.find('.Repeating-Form > .cv-add-group-btn').eq(0).clone(true);
                $wrap.find('.wf-wrapped-add-btn').remove();
                $wrap.find('.Repeating-Form .cv-add-group-btn').remove();
                var $div = $('<div class="col-xs-offset-2 col-xs-10 wf-wrapped-add-btn" style="margin-bottom:30px; padding-bottom:20px; border-bottom:solid 1px #ccc;"></div>');
                $addBtn.appendTo($div);
                $div.insertAfter(zChunks[zChunks.length-1]);

                // Due to timing of SuperItem vs this widget, we need to make sure we do a render AFTER the superItem has had a chance to insert key state/classes:
                if(isTableInitd === false){
                    window.setTimeout(function(){
                        _summarizeFormToTable($form, $table, j);
                        isTableInitd = true;
                        // We should disable all Add/Delete item buttons if the item itself is disabled to the user:
                        if($form.closest('form').hasClass('wf-item-is-disabled') || $form.closest('form').attr('data-flrr-groupactionsdenied') == 'true'){
                            $form.closest('form').find('.cv-add-group-btn, .cv-remove-group-btn').prop('disabled', true);
                        }
                    }
                ,111);}
            }

            // We should disable all Add/Delete item buttons if the item itself is disabled to the user:
            if($form.closest('form').hasClass('wf-item-is-disabled')){
                $form.closest('form').find('.cv-add-group-btn, .cv-remove-group-btn').prop('disabled', true);
            }
        });

        //
        // Later, after moving the Add button to bottom of form for Usability: If Edit-able, we also make a fake row for Adding another item
        //
        if(!areGroupActionsDenied && false){
            var $table = ($wrap.hasClass('Tabled-Form-Wrapper')) ? $('table.Repeating-Form-Table:visible').filter(function(iT, oT){return $($(oT).data('table') == $wrap.data('table'))}) : false,
                $btn = $wrap.find('.cv-add-group-btn:first').clone(),
                $newRow = $('<tr></tr>');

            console.log('fake row for add:', $wrap, $table);
            if($table !== false){
                $newRow.append($btn);
                $table.find('tbody').append($newRow);
            }

        }

        // DatePickerize the new DOM
        mpsApp.mpsDatePickerizeDom($wrap);
    });
}
