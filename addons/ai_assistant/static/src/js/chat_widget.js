odoo.define('ai_assistant.chat_widget', function (require) {
    "use strict";

    var rpc = require('web.rpc');

    var ChatWidget = {
        start: function () {
            var $chat = $(`
                <div id="ai_chat_wrapper">
                    
                    <!-- Nút tròn -->
                    <div id="chat_toggle" style="
                        position: fixed;
                        bottom: 20px;
                        right: 20px;
                        width: 60px;
                        height: 60px;
                        background: #007bff;
                        color: white;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        cursor: pointer;
                        z-index: 9999;
                        font-size: 24px;
                    ">
                        💬
                    </div>

                    <!-- Box chat -->
                    <div id="chat_box" style="
                        display: none;
                        position: fixed;
                        bottom: 90px;
                        right: 20px;
                        width: 300px;
                        height: 400px;
                        background: white;
                        border: 1px solid #ccc;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                        z-index: 9999;
                        flex-direction: column;
                    ">
                        <div style="
                            background:#007bff;
                            color:white;
                            padding:10px;
                            border-radius:10px 10px 0 0;
                            display:flex;
                            justify-content: space-between;
                        ">
                            <span>AI Chat</span>
                            <span id="chat_minimize" style="cursor:pointer;">−</span>
                        </div>

                        <div id="chat_messages" style="
                            flex:1;
                            overflow:auto;
                            padding:10px;
                        "></div>

                        <div style="display:flex;border-top:1px solid #ccc;">
                            <input id="chat_input" style="flex:1;border:none;padding:5px;">
                            <button id="chat_send">Gửi</button>
                        </div>
                    </div>

                </div>
            `);

            $('body').append($chat);

            // Mở chat
            $('#chat_toggle').on('click', function () {
                $('#chat_box').toggle();
            });

            // Thu nhỏ
            $('#chat_minimize').on('click', function () {
                $('#chat_box').hide();
            });

            // Gửi tin
            $('#chat_send').on('click', function () {
                var msg = $('#chat_input').val();
                if (!msg) return;

                $('#chat_messages').append(`<div><b>Bạn:</b> ${msg}</div>`);

                rpc.query({
                    route: '/ai/chat',
                    params: {message: msg},
                }).then(function (res) {
                    $('#chat_messages').append(`<div><b>AI:</b> ${res.response}</div>`);
                    $('#chat_messages').scrollTop($('#chat_messages')[0].scrollHeight);
                });

                $('#chat_input').val('');
            });

            // Enter để gửi
            $('#chat_input').on('keypress', function (e) {
                if (e.which === 13) {
                    $('#chat_send').click();
                }
            });
        }
    };

    $(document).ready(function () {
        ChatWidget.start();
    });

    return ChatWidget;
});