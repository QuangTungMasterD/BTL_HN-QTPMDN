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
                        width: 50px;
                        height: 50px;
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
                        💭
                    </div>

                    <!-- Box chat -->
                    <div id="chat_box" style="
                        display: none;
                        position: fixed;
                        display: flex;
                        bottom: 20px;
                        right: 20px;
                        width: 320px;
                        height: 420px;
                        background: white;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
                        z-index: 9999;
                        flex-direction: column;
                        overflow: hidden;
                    ">
                        <div style="
                            background:#007bff;
                            color:white;
                            padding:10px;
                            display:flex;
                            justify-content: space-between;
                        ">
                            <span>AI Chat</span>
                            <span id="chat_minimize" style="cursor:pointer;">−</span>
                        </div>

                        <!-- Messages -->
                        <div id="chat_messages" style="
                            flex:1;
                            overflow:auto;
                            padding:10px;
                            display:flex;
                            flex-direction:column;
                            // gap:8px;
                            overflow-y: auto;
                        "></div>

                        <!-- Input -->
                        <div style="display:flex;background-color: white;width: 100%; padding: 6px;">
                            <input placeholder="Nhập câu hỏi..." id="chat_input" style="flex:1;border:none;padding:8px 12px;outline:none; border-radius: 20px; border: 2px solid #007bff;">
                            <button id="chat_send" style="border:none;width:40px;height: 40px;border-radius:50%;margin-left: 4px;background:#007bff;color:white;"><svg class="xsrhx6k" height="16px" fill="white" viewBox="0 0 24 24" width="20px"><title>Nhấn Enter để gửi</title><path d="M16.6915026,12.4744748 L3.50612381,13.2599618 C3.19218622,13.2599618 3.03521743,13.4170592 3.03521743,13.5741566 L1.15159189,20.0151496 C0.8376543,20.8006365 0.99,21.89 1.77946707,22.52 C2.41,22.99 3.50612381,23.1 4.13399899,22.8429026 L21.714504,14.0454487 C22.6563168,13.5741566 23.1272231,12.6315722 22.9702544,11.6889879 C22.8132856,11.0605983 22.3423792,10.4322088 21.714504,10.118014 L4.13399899,1.16346272 C3.34915502,0.9 2.40734225,1.00636533 1.77946707,1.4776575 C0.994623095,2.10604706 0.8376543,3.0486314 1.15159189,3.99121575 L3.03521743,10.4322088 C3.03521743,10.5893061 3.34915502,10.7464035 3.50612381,10.7464035 L16.6915026,11.5318905 C16.6915026,11.5318905 17.1624089,11.5318905 17.1624089,12.0031827 C17.1624089,12.4744748 16.6915026,12.4744748 16.6915026,12.4744748 Z" fill="var(--chat-composer-button-color)"></path></svg></button>
                        </div>
                    </div>

                </div>
            `);

            $('body').append($chat);

            // Toggle chat box
            $('#chat_toggle').on('click', function () {
                $('#chat_box').toggle();
            });

            $('#chat_minimize').on('click', function () {
                $('#chat_box').hide();
            });

            // Gửi tin nhắn
            $('#chat_send').on('click', function () {
                var msg = $('#chat_input').val();
                if (!msg) return;

                // Thêm tin nhắn người dùng
                $('#chat_messages').append(`
                    <div style="display:flex; justify-content:flex-end;">
                        <div style="background:#007bff; color:white; padding:8px 12px; border-radius:15px; max-width:70%;margin: 6px 0;">
                            ${msg}
                        </div>
                    </div>
                `);

                // Thêm loading
                var loadingId = 'loading_' + Date.now();
                $('#chat_messages').append(`
                    <div id="${loadingId}" style="display:flex; justify-content:flex-start;">
                        <div style="background:#eee; padding:8px 12px; border-radius:15px;">
                            <div class="typing">
                                <span></span><span></span><span></span>
                            </div>
                        </div>
                    </div>
                `);

                $('#chat_messages').scrollTop($('#chat_messages')[0].scrollHeight);

                rpc.query({
                    route: '/ai/chat',
                    params: {message: msg},
                }, {
                    shadow: true
                }).then(function (res) {
                    $('#' + loadingId).html(`
                        <div style="background:#eee; padding:8px 12px; border-radius:15px; max-width:70%;">
                            ${res.response || "Không có dữ liệu"}
                        </div>
                    `);
                    $('#chat_messages').scrollTop($('#chat_messages')[0].scrollHeight);
                });

                $('#chat_input').val('');
            });

            $('#chat_input').on('keypress', function (e) {
                if (e.which === 13) {
                    $('#chat_send').click();
                }
            });

            // Animation dấu ...
            setInterval(() => {
                $('.dots').each(function () {
                    let text = $(this).text();
                    if (text.length >= 3) {
                        $(this).text('.');
                    } else {
                        $(this).text(text + '.');
                    }
                });
            }, 500);
        }
    };

    $(document).ready(function () {
        ChatWidget.start();
    });

    return ChatWidget;
});