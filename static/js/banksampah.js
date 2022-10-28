<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>


$(document).on('submit', '#post-form',function(e){
    $.ajax({
        type:'POST',
        url: '{% url "banksampah:create_post" %}',
        data:{
            alamat:$('#alamat').val(),
            tanggal:$('#tanggal').val(),
            kontak:$('#kontak').val(),
            jenis:$('#jenis').val(),
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        },
        dataType: 'json',
        success:function(json){
            alert("Form Accepted");
            document.getElementById("post-form").reset();
        }
    });
});