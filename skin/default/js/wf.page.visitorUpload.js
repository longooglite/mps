// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

var showBackdrop = function(){
        $('#wf-modal-backdrop').show().removeClass('starthidden');
    },
    hideBackdrop = function(){
        $('#wf-modal-backdrop').hide().addClass('starthidden');
    },
    uploadCallback = function(data){
        if(typeof data.errors !== 'undefined' || typeof data.error !== 'undefined'){
            // Specific Error(s) returned
            hideBackdrop();
            $('#wf-upload-form').hide();
            $('#wf-error-form').show();
            cvApp.showHeaderMessage('Upload Error...', 'danger', true);
            window.setTimeout(cvApp.hideHeaderMessage(),2000);
            console.log('JSON Errors!', data);
            $('#wf-upload-error-text').html('<div class="alert alert-danger">'+((typeof data.errorMsg === 'string') ? 'Error: '+data.errorMsg : 'Error: Unknown Error') +'</div>');
        }
        else if(data.success === true){
            // Success!
            hideBackdrop();
            $('#wf-upload-form').hide();
            $('#wf-thankyou-form').show();
            cvApp.showHeaderMessage('Upload Successful!', 'info', false);
            window.setTimeout(cvApp.hideHeaderMessage(),3000);
            $('#wf-upload-filename').text(data.filename);
            // console.log('Success!!!', data);
        }
        else{
            // General Other Error
            hideBackdrop();
            $('#wf-upload-form').hide();
            $('#wf-error-form').show();
            cvApp.showHeaderMessage('Upload Error...', 'danger', true);
            window.setTimeout(cvApp.hideHeaderMessage(),2000);
            console.log('Unspecified Error!', data);
            $('#wf-upload-error-text').html('<div class="alert alert-danger">An unspecified error has occurred.</div>');
        }
    };

$('body').on('fileselect', '.btn-file :file', function(event, label) {
    var $target = $(event.target),
        $form = $target.closest('form');
    $target.closest('.row').find('input').prop('disabled',false);
    $target.closest('.row').find('.btn').toggleClass('btn-primary btn-default');
    $target.closest('.input-group').find('.cv-import-label').val(label);
    $target.closest('.row').find('input:first').show().focus().click().val('Uploading...').prop('disabled', true);

    // Asynchronous IFrame POST:
    //_uploadWidget = $that;
    $('#wf-modal-backdrop').show().removeClass('starthidden');
    cvApp.showHeaderMessage('Uploading file...', 'info', true);
    $form.submit();
    event.stopPropagation();
});

$('body').on('change', '.btn-file :file', function(e) {
    var input = $(e.target),
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [label]);
    e.stopPropagation();
});